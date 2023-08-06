# Copyright 2019-2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import attr
import logging
import requests
import time
import threading

from gitlab import Gitlab  # python-gitlab
from selenium.webdriver.common.by import By


from .namespace import UserNameSpace
from .selenium import (
    webdriver_wait_get,
)
from .session import (
    login_as_root,
    sign_in_page_login,
)

logger = logging.getLogger(__name__)


def default_password(username):
    return username + '.' * (8 - len(username))


@attr.s
class User(object):
    name = attr.ib()
    id = attr.ib()
    heptapod = attr.ib(repr=False)
    email = attr.ib(default=None, repr=False)
    password = attr.ib(default=None, repr=False)
    token = attr.ib(default=None, repr=False)

    vcs_token_only = attr.ib(default=False, repr=False)
    """Are VCS HTTP operations to be made only with the access token?

    If two-factor authentication is activated, or if the user can only log
    through SSO, only private tokens can enable VCS HTTP push and pull.
    """

    thread_locals = attr.ib(factory=threading.local, repr=False)
    webdrivers_all_threads = attr.ib(factory=list, repr=False)
    _python_gitlab_client = attr.ib(default=None, repr=False)

    @classmethod
    def create(cls, heptapod, name,
               password=None,
               email=None,
               fullname=None, **kw):
        if password is None:
            # requirements on password length are also enforced in the API
            password = default_password(name)
        if fullname is None:
            fullname = name
        if email is None:
            email = name + '@heptapod.example.net',

        resp = requests.post(
            '/'.join((heptapod.api_url, 'users')),
            data=dict(name=fullname,
                      username=name,
                      password=password,
                      reset_password=False,
                      email=email,
                      skip_confirmation=True,
                      **kw
                      ),
            headers=heptapod.root_token_headers,
        )
        assert resp.status_code < 300, "User %r creation failed" % name
        user = cls(name=name, heptapod=heptapod, password=password,
                   email=email,
                   id=resp.json()['id'])
        user.store_in_heptapod()
        return user

    @classmethod
    def init_root(cls, heptapod, password):
        """Singled out because we have to use hardcoded values for root."""
        user = cls(id=1, heptapod=heptapod, name='root', password=password)
        user.store_in_heptapod()
        return user

    @classmethod
    def ensure(cls, heptapod, name, password=None, fullname=None):
        """Retrieve user or create it.

        :returns: `User` instance
        """
        if password is None:
            password = default_password(password)

        user = heptapod.users.get(name)
        if user is None:
            user = cls.search(heptapod, name)
            if user is None:
                user = cls.create(heptapod, name,
                                  password=password, fullname=fullname)
            user.store_in_heptapod()

        user.password = password
        user.ensure_private_token()
        return user

    @classmethod
    def search(cls, heptapod, name):
        """Lookup user in API and returns instance.

        The returned User instance doesn't know its password. Either it
        has an expected value, or it won't be suitable for webdriver
        authentication (API auth is usually done with access tokens).
        """
        resp = requests.get(
            '/'.join((heptapod.api_url, 'users')),
            params=dict(username=name),
            headers=heptapod.root_token_headers,
        )
        found = resp.json()
        if resp.status_code == 404 or not found:
            return

        assert len(found) == 1
        details = found[0]
        return cls(name=name,
                   id=details['id'],
                   email=details['email'],
                   heptapod=heptapod)

    def store_in_heptapod(self):
        self.heptapod.users[self.name] = self

    @property
    def personal_namespace(self):
        """Return a UserNameSpace instance for self."""
        return UserNameSpace(user_name=self.name, heptapod=self.heptapod)

    @property
    def webdriver(self):
        """Selenium webdriver, authentified as self.
        """
        driver = getattr(self.thread_locals, 'webdriver', None)
        if driver is not None:
            return driver

        thread_name = threading.current_thread().name

        logger.info(
            "Initializing a signed-in webdriver for user %r in thread %r",
            self.name, thread_name)

        # guaranteeing driver to be available for teardown as soon as created
        driver = self.thread_locals.webdriver = self.heptapod.new_webdriver()

        heptapod = self.heptapod
        if self.name == 'root':
            login_as_root(driver, heptapod, self.password)
        else:
            start = time.time()
            webdriver_wait_get(heptapod, driver, relative_uri='/users/sign_in')
            sign_in_page_login(driver, heptapod, self.name,
                               password=self.password)
            logger.info("Signed in user %s in %.2f seconds",
                        self.name, time.time() - start)
        # thank you, GIL
        self.webdrivers_all_threads.append((thread_name, driver))

        return driver

    def close_webdrivers(self):
        """Close current web driver for all threads."""
        for thread_name, driver in self.webdrivers_all_threads:
            logger.info("Closing webdriver of user %r for thread %r",
                        self.name, thread_name)
            driver.close()

        self.webdriver_all_threads = []
        self.thread_locals.webdriver = None

    def root_api_request(self, method, subpath=None, **data):
        """Perform a request on user API as root"""
        hepta = self.heptapod
        segments = [hepta.api_url, 'users', str(self.id)]
        if subpath is not None:
            segments.append(subpath)

        return requests.request(method, '/'.join(segments),
                                headers=hepta.root_token_headers,
                                data=data)

    def root_api_post(self, subpath=None, **data):
        return self.root_api_request('POST', subpath=subpath, **data)

    def delete(self, hard=True):
        self.close_webdrivers()
        hepta = self.heptapod

        unregistered = hepta.users.pop(self.name, None)
        if unregistered is not self:
            logger.warning("While unregistering user %r from Heptapod "
                           "instance, found %r registered in its place "
                           "instead", self.name, unregistered)

        resp = requests.delete(
            '/'.join((hepta.api_url, 'users', str(self.id))),
            data=dict(id=self.id, hard_delete=hard),
            headers=hepta.root_token_headers,
        )

        assert resp.status_code == 204, "Failed to delete %r" % self

    def edit(self, **data):
        resp = self.root_api_request('PUT', **data)
        assert resp.status_code == 200, "Failed to edit %r" % self

    def block(self):
        resp = self.root_api_post(subpath='block')
        assert resp.status_code == 201, "Failed to block %r" % self

    def unblock(self):
        resp = self.root_api_post(subpath='unblock')
        assert resp.status_code == 201, "Failed to unblock %r" % self

    def deactivate(self):
        resp = self.root_api_post(subpath='deactivate')
        assert resp.status_code == 201, "Failed to deactivate %r" % self

    def activate(self):
        resp = self.root_api_post(subpath='activate')
        assert resp.status_code == 201, "Failed to activate %r" % self

    def ensure_ssh_pub_key(self, pubkey, title='heptapod-tests'):
        """Upload the SSH public key if needed.

        Does not require any special privilege if a token for the user
        is already known
        """
        hepta = self.heptapod
        if self.token:
            keys_api_url = '/'.join((
                hepta.api_url, 'user', 'keys'))
            headers = self.token_headers()
        else:
            keys_api_url = '/'.join((
                hepta.api_url, 'users', str(self.id), 'keys'))
            headers = hepta.root_token_headers

        ls_resp = requests.get(keys_api_url, headers=headers)
        assert ls_resp.status_code == 200

        # check existence based on title. This is quite lame (we should
        # check fingerprint), but that's good enough for these first tests.
        for key_info in ls_resp.json():
            if key_info['title'] == title:
                return

        create_resp = requests.post(keys_api_url,
                                    data=dict(id=self.id,
                                              title=title,
                                              key=pubkey),
                                    headers=headers,
                                    )
        assert create_resp.status_code == 201
        assert create_resp.json()['title'] == title

    def delete_ssh_keys(self):
        """Delete all SSH keys of current user.

        Does not require any special privilege.
        """
        hepta = self.heptapod

        if self.token:
            keys_api_url = '/'.join((
                hepta.api_url, 'user', 'keys'))
            headers = self.token_headers()
        else:
            keys_api_url = '/'.join((
                hepta.api_url, 'users', str(self.id), 'keys'))
            headers = hepta.root_token_headers

        ls_resp = requests.get(keys_api_url, headers=headers)
        assert ls_resp.status_code == 200
        # check existence based on title. This is quite lame (we should
        # check fingerprint), but that's good enough for these first tests.
        for key_info in ls_resp.json():
            resp = requests.delete('%s/%d' % (keys_api_url, key_info['id']),
                                   headers=headers)
            assert resp.status_code == 204

    @property
    def ssh_command(self):
        """Return a SSH command to perform operations as the given user.
        """
        # IdentitiesOnly makes sure no other SSH key than the one
        # specified with -i are going to be used. Otherwise, current user
        # SSH keys could be attempted before the correct one, leading
        # to either too much auth failures, or use of the wrong key if
        # one happens to be also known by Heptapod
        return ' '.join(('ssh',
                         '-o', 'IdentitiesOnly=yes',
                         '-o', 'NoHostAuthenticationForLocalhost=yes ',
                         '-o', 'StrictHostKeyChecking=no',
                         '-i', self.ssh['priv']))

    def token_headers(self):
        """Return a *new* headers dict suitable for authenticated API acces.
        """
        return {'Private-Token': self.token}

    @property
    def basic_auth_url(self):
        url = self.heptapod.parsed_url
        return "{scheme}://{auth}@{netloc}".format(
            scheme=url.scheme,
            netloc=url.netloc,
            auth=':'.join((self.name, self.password)),
        )

    def api_get(self):
        """Perform GET on users API for self, using :attr:`token`.

        :return: response or `None` if :attr:`token` is None
        """
        token = self.token
        if token is None:
            return None

        return requests.get(self.heptapod.api_url + '/users/%d' % self.id,
                            headers=self.token_headers())

    def api_owned_groups(self):
        """List the groups owned by this user.

        TODO it lists actually the first page, which is expected to
        be good enough for the foreseeable future.
        """
        resp = requests.get(self.heptapod.api_url + '/groups',
                            params=dict(owned=True),
                            headers=self.token_headers(),
                            )
        assert resp.status_code < 400
        return resp.json()

    def ensure_private_token(self):
        """Generate a private token for already logged in user if needed.

        The generation involves obtaining a signed-in webdriver for the user.
        It is therefore costly.
        """
        resp = self.api_get()
        if resp is not None and resp.status_code == 200:
            logger.info("%r: reusing existing access token.", self)
            return

        heptapod = self.heptapod
        start = time.time()
        webdriver = self.webdriver
        webdriver.get(heptapod.url + '/-/profile/personal_access_tokens')
        name_elt = webdriver.find_element(
            By.XPATH,
            '//input[@name="personal_access_token[name]"]')
        name_elt.send_keys("heptapod-tests")

        for scope in webdriver.find_elements(
                By.XPATH,
                '//input[@type="checkbox"]'):
            # forcing click via JavaScript because on GitLab 14.10,
            # selenium complains with the "click intercepted" exception
            # and there is nothing obvious why (after inspections, screenshots,
            # etc).
            webdriver.execute_script("arguments[0].click();", scope)
        submit = webdriver.find_element(By.XPATH, '//input[@type="submit"]')
        submit.click()

        elem = webdriver.find_element(By.ID, 'created-personal-access-token')
        token = elem.get_attribute('value')
        self.token = token

        logger.info("%r: access token generated in %.2f seconds",
                    self, time.time() - start)

    @property
    def python_gitlab_client(self):
        """Return the API client from the python-gitlab library

        See https://python-gitlab.readthedocs.io
        """
        cl = self._python_gitlab_client
        if cl is None:
            cl = self._python_gitlab_client = Gitlab(self.heptapod.url,
                                                     private_token=self.token)
        return cl

    def __enter__(self):
        return self

    def __exit__(self, *exc_args):
        self.delete()
        return False
