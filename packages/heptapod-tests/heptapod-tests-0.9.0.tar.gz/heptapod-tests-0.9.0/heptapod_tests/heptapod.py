# Copyright 2020-2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import contextlib
import json
from io import BytesIO
import logging
import os
import requests
import selenium.webdriver
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from urllib.parse import urlparse

from . import docker
from .constants import DEFAULT_RUN_DIR
from .namespace import Group
from .user import User

logger = logging.getLogger(__name__)

INITIAL_TIMEOUT = 600  # seconds

BRANCH_PROTECTIONS = dict(none=0,
                          dev_can_push=1,
                          full=2,
                          dev_can_merge=3,
                          )


class Heptapod:
    """Base class and minimum common control of Heptapod server.

    This is used directly in case `--heptapod-remote` is selected.
    """

    fs_access = False
    """True if manipulation of files is possible.

    Implies :attr:`repositories_root` not to be None.
    """

    shell_access = False
    """True if running arbitrary commands as in a shell is possible."""

    repositories_root = None
    """Path to the repositories, from the Heptapod server point of view.

    This is potentially not meaningful on the system that runs the test,
    see :class:`DockerHeptapod` for an example.
    """

    reverse_call_host = None
    """Network address for the system running these tests, seen from Heptapod.
    """

    webdriver_type = 'chrome'
    """Type of webdriver to use."""

    webdriver_remote_url = None
    """URL for a Selenium RemoteWebDriver."""

    wait_after_first_response = 0
    """Time to wait after we've had a first non error HTTP response.
    """

    hg_executable = 'hg'

    chrome_driver_args = ()

    firefox_driver_args = ()

    clever_cloud_sso = False
    """If ``True``, authentications will got through the Clever Cloud SSO.
    """

    default_user_name = 'root'
    """Default user for project, group creation etc."""

    default_group = None
    """Group instance where to create projects in by default."""

    instance_type = 'development'
    """The type of instance, meaning how these tests operate on it.

    It is of course completely possible to treat a development instance
    as if it were for production: that's what happens when developping the
    production server tests, of course.

    Treating a production instance as a development one is also technically
    possible (strongly discouraged of course).
    """

    def __init__(self, url,
                 ssh_user=None,
                 ssh_port=None,
                 ssh_keys_dir=None,
                 run_dir=DEFAULT_RUN_DIR,
                 hg_native=None,
                 clever_cloud_sso=False,
                 reverse_call_host=None,
                 wait_after_first_response=0,
                 webdriver_type=None,
                 webdriver_remote_url=None):
        self.parsed_url = urlparse(url)
        self.url = url
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_keys_dir = ssh_keys_dir
        self.run_dir = run_dir
        self.hg_native = hg_native
        self.hg_without_git = hg_native == 'without-git'
        self.clever_cloud_sso = clever_cloud_sso
        self.users = {}
        if reverse_call_host is not None:
            self.reverse_call_host = reverse_call_host
        self.dead = None
        if webdriver_type is not None:
            self.webdriver_type = webdriver_type
        self.webdriver_remote_url = webdriver_remote_url
        self.wait_after_first_response = wait_after_first_response
        self.settings = {}

    @property
    def heptapod(self):
        return self

    @property
    def ssh_url(self):
        if self.ssh_user is None or self.ssh_port is None:
            raise ValueError("Missing configuration for SSH")
        return 'ssh://{user}@{host}:{port}'.format(
            host=self.host,
            user=self.ssh_user,
            port=self.ssh_port,
        )

    @property
    def host(self):
        return self.parsed_url.netloc.rsplit(':', 1)[0]

    @property
    def api_url(self):
        return '/'.join((self.url, 'api', 'v4'))

    @property
    def root_token_headers(self):
        return {'Private-Token': self.users['root'].token}

    @property
    def basic_user_token_headers(self):
        return {'Private-Token': self.users['test_basic'].token}

    def run_shell(self, command, **kw):
        exit_code, output = self.execute(command, **kw)
        if exit_code != 0:
            raise RuntimeError(
                ('Heptapod command {command} returned a non-zero '
                 'exit code {exit_code}').format(
                     command=command,
                     exit_code=exit_code,
                ))
        return output

    def get_user(self, name):
        """Return a :class:`User` instance, or `None`."""
        return self.users.get(name)

    def new_webdriver(self):
        if self.webdriver_type == 'chrome':
            cls = selenium.webdriver.Chrome
            options = selenium.webdriver.ChromeOptions()
            for arg in self.chrome_driver_args:
                options.add_argument(arg)
            options.add_argument('--headless')
        elif self.webdriver_type == 'firefox':
            cls = selenium.webdriver.Firefox
            options = selenium.webdriver.FirefoxOptions()
            for arg in self.firefox_driver_args:
                options.add_argument(arg)
            options.add_argument('--headless')

        if self.webdriver_remote_url:
            return selenium.webdriver.Remote(
                command_executor=self.webdriver_remote_url,
                options=options
            )
        return cls(options=options)

    def wait_startup(self, first_response_timeout=INITIAL_TIMEOUT,
                     wait_after_first_response=None):
        """Wait for Heptapod to be ready after startup.

        We have to take into account that the server may have just started
        (that's frequent in development and it's annoying for a human to
        wait) or could even be starting from scratch, configuring itself,
        creating the DB schema etc. (typical of CI).
        In that latter case, an amount of extra wait after the first successful
        HTTP response is often needed.
        """
        logger.info("Waiting for Heptapod to answer requests")
        dead_msg = ("Heptapod server did not "
                    "respond in %s seconds" % first_response_timeout)
        start = time.time()
        while time.time() < start + first_response_timeout:
            try:
                resp = requests.get(self.url, allow_redirects=False)
            except IOError:
                resp = None

            if resp is None:
                logger.debug("Couldn't reach Heptapod")
            elif resp.status_code >= 400:
                logger.debug("Heptapod response code %r", resp.status_code)
            else:
                logger.info("Heptapod is up")
                self.dead = False
                if wait_after_first_response:
                    logger.info("Waiting additional %d seconds "
                                "after first successful HTTP call",
                                wait_after_first_response)
                    time.sleep(wait_after_first_response)
                return

            duration = 1
            logger.debug("Retrying in %.1f seconds", duration)
            time.sleep(duration)

        self.dead = True
        raise AssertionError(dead_msg)

    def instance_cache_file(self):
        return self.run_dir / 'instance.cache'

    def load_instance_cache(self):
        path = self.instance_cache_file()

        def invalidate_retry():
            logger.warning("Removing cache file %r and starting afresh.", path)
            os.unlink(path)
            return self.load_instance_cache()

        try:
            with open(path) as cachef:
                cached = json.load(cachef)

        except Exception:
            logger.info("Cache file %r not available or not readable. "
                        "Heptapod instance info will be retrieved "
                        "or initialized", path)
        else:
            instance_type = cached.get('instance_type')
            if instance_type != self.instance_type:
                # None means before the introduction of this invalidation
                # in case anyone wonders (not worth a specific message)
                logger.warning(
                    "Cache file %r is for another instance type (%r) ",
                    path, instance_type)
                return invalidate_retry()

            url = cached.get('url')
            # for now all development instances have the same two
            # fixed test users (root and test_basic). There is already
            # a token invalidation logic.
            if instance_type == 'production' and url != self.url:
                # None means before the introduction of this invalidation
                # in case anyone wonders (not worth a specific message)
                logger.warning(
                    "Cache file %r is for another instance (%r) ",
                    path, url)
                return invalidate_retry()

            for name, info in cached['users'].items():
                if 'id' not in info:
                    logger.warning("Cache file %r is from an earlier version "
                                   "of heptapod-tests. ", path)
                    return invalidate_retry()
                self.users[name] = User(heptapod=self,
                                        name=name,
                                        id=info['id'],
                                        token=info['token'])

    def update_instance_cache(self):
        users = {user.name: dict(token=user.token, id=user.id)
                 for user in self.users.values()}
        with open(self.instance_cache_file(), 'w') as cachef:
            json.dump(dict(url=self.url,
                           instance_type=self.instance_type,
                           users=users), cachef)

    def prepare(self, root_password):
        """Make all preparations for the Heptapod instance to be testable.

        This currently amounts to

        - defining the root password
        - activating and retrieving a root API token
        - creating a persistent `test_basic` user
        - activating and retrieving an API token for `test_basic`
        - keeping a logged in webdriver for each persistent user
        """
        assert not self.dead, "Heptapod server marked dead by previous test."

        if self.dead is None:
            self.wait_startup(
                wait_after_first_response=self.wait_after_first_response)
        self.load_instance_cache()

        logger.info("Preparing root user.")
        start = time.time()
        root = self.users.get('root')
        if root is None:
            root = User.init_root(self, root_password)
        else:
            root.password = root_password
        root.ensure_private_token()

        logger.info("Preparing application settings.")
        wait_settings = self.set_application_settings(
            # necessary if we want to listen to web hooks from these tests
            # in GitLab v12.2.0, this is deprecated for ...from_web_hooks...
            allow_local_requests_from_web_hooks_and_services="true",
            # needed in GitLab ≥14.8
            api_cache_expiration_factor=0.0,
            # Depending on Heptapod version, native or non-native Mercurial
            # VCS type may not be allowed by default.
            vcs_types='hg,git,hg_git',
        )

        feature_flags = dict(
            api_caching_branches=False,
        )
        feature_flags['hg_without_git'] = self.hg_without_git
        wait_flags = self.set_feature_flags(feature_flags)

        ttw = max(wait_settings, wait_flags)
        if ttw:
            logger.warning("Application settings or Feature flags updated. "
                           "Waiting %d seconds for the change "
                           "to be visible by all server processes", ttw)
            time.sleep(ttw)

        logger.info("Preparing basic user.")
        User.ensure(self, 'test_basic',
                    fullname='Bäsîc Test',
                    password='test_basic')

        if self.ssh_keys_dir is not None:
            logger.info("Uploading users SSH keys.")
            self.load_ssh_keys()
            self.upload_ssh_pub_keys()
            subprocess.call((
                'ssh-keygen',
                '-R', '[{host}]:{port}'.format(
                    host=self.host, port=self.ssh_port)))
        self.update_instance_cache()
        logger.info("All preparations done in %.2f seconds. "
                    "Proceeding with tests.", time.time() - start)

    def set_application_settings(self, **settings):
        """Change GitLab application settings and update :attr:`settings`.

        :returns: the type to wait in seconds for cache expiration
        """
        settings_url = self.api_url + '/application/settings'
        existing = requests.get(settings_url,
                                headers=self.root_token_headers).json()
        # The format for update is different from the read format.
        # For instance, `vcs_types` is read as a list, but has to be set
        # as a comma-separated string. Therefore the simplest is not to
        # update only if needed, rather to update inconditionally and
        # check after the fact if anything was changed
        resp = requests.put(
            settings_url,
            headers=self.root_token_headers,
            data=settings,
        )
        assert resp.status_code == 200
        new_settings = resp.json()
        if existing == new_settings:
            logger.info("Application settings were already set as required.")
            return 0

        self.settings = new_settings
        # TODO the cache expiration is configurable as
        # Gitlab.config.gitlab['application_settings_cache_seconds']
        # (see app/models/concerns/cacheable_attributes.rb)
        logger.info("Application settings changed")
        return 60

    def sync_application_settings(self):
        """Update :attr:`settings` for current values"""
        resp = requests.get(
            self.api_url + '/application/settings',
            headers=self.root_token_headers,
        )
        assert resp.status_code == 200
        self.settings = resp.json()

    def set_feature_flags(self, flags):
        """Make sure that GitLab feature flags are as specified

        This controls instance-wide value of the feature flags. Any value
        subsequently set for a specific actor (Project, User etc) will
        be ignored.

        :param flags: `dict` mapping flag names to the wished boolean value.
        :returns: time to wait for cache expiration, in seconds

        Uses the dedicated API:
         https://docs.gitlab.com/ce/api/features.html#set-or-create-a-feature
        """
        if self.check_feature_flags(flags):
            logger.info("Feature flags %r already set as required",
                        flags)
            return 0

        headers = self.root_token_headers
        for flag, value in flags.items():
            resp = requests.post('/'.join((self.api_url,
                                           'features',
                                           flag)),
                                 headers=headers,
                                 # True doesn't seem to do anything, so
                                 # let's go the percentage way.
                                 data=dict(value=100 if value else 0)
                                 )
            assert resp.status_code < 400

        # Feature flags have several level of caching, with L1 being
        # a process-level RAM cache (memoization) with no invalidation
        # but expiration set to 1 minute (see lib/feature.rb in the Rails app
        # source).
        # We have no other choice than waiting:
        return 60

    @property
    def feature_flags_defaults(self):
        defaults = getattr(self, '_feature_flags_defaults', None)
        if defaults is None:
            resp = requests.get(self.api_url + '/features/definitions',
                                headers=self.root_token_headers)
            assert resp.status_code == 200
            self._feature_flags_defaults = defaults = {
                f['name']: f['default_enabled'] for f in resp.json()
            }

        return defaults

    def feature_flags_values(self):
        """Return boolean values of all defined feature flags.

        Like all feature flags treatment in this class, it does not
        understand partially activated flags (percentage etc.).

        The main API point for feature flags only lists the persisted
        values, i.e. does not take into account those that have never been
        mutated since they were defined (first installation or update that
        includes them), so we have to merge them with defaults.
        """
        flags = self.feature_flags_defaults.copy()
        resp = requests.get(self.api_url + '/features',
                            headers=self.root_token_headers)
        assert resp.status_code == 200
        for item in resp.json():
            logger.debug("Persisted feature flag response item: %r", item)
            flags[item['definition']['name']] = item['state'] == 'on'

        return flags

    def check_feature_flags(self, expected_flags):
        current_flags = self.feature_flags_values()
        for name, expected in expected_flags.items():
            current = current_flags.get(name)
            if current is None:
                raise RuntimeError("Feature flag %r is not defined in this "
                                   "Heptapod instance" % name)
            if current is not expected:
                logger.info("Value of feature flag %r is %s, differing from "
                            "the expected %s", name, current, expected)
                return False

        return True

    def api_request(self, method, user=None, subpath='', **kwargs):
        """Perform a simple API HTTP request

        `method` is the HTTP method to use, same as in `requests.request`.

        The full URL is made of the API URL of the instance, together with
        the given subpath (example 'snippets/42').

        Appropriate authentication headers are added on the fly.

        :param user: the :class:`User` to run the request as. If not specified,
                     the request is sent as the root user.

        All other kwargs are passed to `requests.request()`
        """
        headers = kwargs.pop('headers', {})
        token = self.owner_token if user is None else user.token
        headers['Private-Token'] = token
        return requests.request(method,
                                '/'.join((self.api_url, subpath)),
                                headers=headers,
                                **kwargs)

    def api_get(self, **kwargs):
        return self.api_request('GET', **kwargs)

    def api_post(self, **kwargs):
        return self.api_request('POST', **kwargs)

    def api_put(self, **kwargs):
        return self.api_request('PUT', **kwargs)

    def api_delete(self, **kwargs):
        return self.api_request('DELETE', **kwargs)

    def load_ssh_keys(self, key_name_mapping=None):
        """Load client-side information to use SSH keys

        Also makes sure the keys are actually usable (perms)

        :param key_name_mapping: allow to control the variable part of the
           key file name instead of simply using the user name.
        """
        if key_name_mapping is None:
            key_name_mapping = {}

        ssh_dir = self.ssh_keys_dir
        for name, user in self.users.items():
            base_fname = 'id_rsa_heptapod_' + key_name_mapping.get(name, name)
            priv = ssh_dir / base_fname
            pub = ssh_dir / (base_fname + '.pub')

            # VCSes tend not to preserve non-executable perm bits
            priv.chmod(0o600)
            user.ssh = dict(priv=str(priv), pub=pub.read_text())

    def upload_ssh_pub_keys(self):
        """Upload SSH public keys for all users to Heptapod."""
        for user in self.users.values():
            user.ensure_ssh_pub_key(user.ssh['pub'])

    def close_webdrivers(self):
        for user in self.users.values():
            user.close_webdrivers()

    def close(self):
        if self.dead is not False:
            return
        self.close_webdrivers()

    def execute(self, command, **kw):
        raise NotImplementedError('execute')

    def force_remove_route(self, route_path, source_type='Project'):
        logger.error("Attempt to force-remove route %r, not implemented "
                     "for %r", route_path, self.__class__)
        raise NotImplementedError('force_remove_route')

    def gitlab_ctl(self, command, services=None):
        """Apply service management command.

        'command' would typically be 'start', 'stop', etc.

        :param services: an iterable of service names (who can themselves
                         be different depending on the concrete subclass).
                         If supplied, the command will apply only to those
                         services.
        """
        raise NotImplementedError('gitlab_ctl')

    def rake(self, *args):
        """Call GitLab Rake"""
        raise NotImplementedError('rake')

    def psql(self, statement):
        """Calls psql on the instance database.

        This is *not* an access through the client library, we cannot separate
        arguments as is usually mandatory in regular applications to prevent
        SQL injections.
        """
        raise NotImplementedError('psql')

    def remove_all_backups(self):
        """Remove all existing backups with no impediment for new backups.
        """
        raise NotImplementedError('remove_all_backups')

    def backup_create(self, clean_previous=True):
        """Create a new backup

        :param bool clean_previous: if true, any previously existing backups
            are removed. This is handy so that the restore rake task knows
            which one to restore without any need to tell it.
        """
        if clean_previous:
            self.remove_all_backups()
        start = time.time()
        logger.info("Starting backup task")
        self.rake('gitlab:backup:create')
        elapsed = time.time() - start
        logger.info("Backup task finished in %d seconds (%.1f minutes)",
                    elapsed, elapsed / 60)

    @contextlib.contextmanager
    def backup_restore(self):
        """Context manager for backups restoration.

        This is a context manager as a way to provide resuming of the
        tests session on errors, in a convenient way for the caller.
        That means ensuring as much as possible that the server is running,
        maybe wait again for it, reinitialize passwords and tokens…
        """
        try:
            self.gitlab_ctl('stop', services=self.RAILS_SERVICES)
            start = time.time()
            logger.info("Starting backup restoration")
            self.rake('gitlab:backup:restore', 'force=yes')
            elapsed = time.time() - start
            logger.info("Backup restoration finished in %d seconds "
                        "(%.1f minutes). Now restarting Rails.",
                        elapsed, elapsed / 60)
            self.gitlab_ctl('start', services=self.RAILS_SERVICES)

            self.wait_startup()
            yield

        except Exception:
            logger.error("Backup restoration failed")
            # these are idempotent
            self.gitlab_ctl('start', services=self.RAILS_SERVICES)

            # Worst case scenario, we lost all our data. We need to
            # reprepare the server for subsequent tests
            self.prepare(self.users['root'].password)
            raise

    def set_vcs_types_settings(self, vcs_types):
        self.set_application_settings(vcs_types=','.join(vcs_types))

    def apply_hashed_storage_setting(self, hashed_storage):
        # TODO it would be tempting not to restart if the setting is already
        # at the wished value, but this currently cannot take into account
        # rollbacked values that aren't followed by a restart. This will
        # be more complicated and take more time than we can afford right now
        # to really make work.
        self.set_application_settings(hashed_storage_enabled=hashed_storage)

        # let's be sure that redis is restarted when the Rails services
        # start
        self.gitlab_ctl('stop', self.RAILS_SERVICES)
        self.gitlab_ctl('stop', ['redis'])
        # we restart everything in case a service would depend on Redis
        # and would fail to reconnect automatically

        # closing all webdrivers, because restart of Redis will kill sessions
        self.close_webdrivers()
        self.gitlab_ctl('restart')
        self.wait_startup()

        # recheck that the setting is applied
        self.sync_application_settings()
        assert self.settings['hashed_storage_enabled'] is hashed_storage


class ProductionHeptapod(Heptapod):
    """An Heptapod server for which we don't have the root password.

    This allows tests to be naturally sandboxed, typically in the groups
    and personal namespaces of a couple of users.
    """

    instance_type = 'production'

    def __init__(self, group_owner_credentials, default_group_id,
                 **kw):
        super(ProductionHeptapod, self).__init__(**kw)
        self.load_instance_cache()
        self.group_owner = self.init_user(group_owner_credentials)
        self.default_user_name = self.group_owner.name
        self.default_group_id = default_group_id

    def init_user(self, cli_credentials):
        """Instantiate a viable `User` from pytest options credentials."""
        user_id, name, email, pwd = cli_credentials.split(':', 3)
        user_id = int(user_id)
        user = self.users.get(name)
        if user is None:
            user = self.users[name] = User(heptapod=self,
                                           id=user_id,
                                           email=email,
                                           name=name,
                                           password=pwd)
        else:
            # id and password could have changed since last execution
            user.id = user_id
            user.password = pwd
            # email is not cached but can actually be necessary
            # (identifier for SSO login)
            user.email = email

        return user

    def prepare(self, root_password):
        """Prepare the group owner.

        root password is just ignored in this subclass.
        """
        start = time.time()
        assert not self.dead, "Heptapod server marked dead by previous test."

        if self.dead is None:
            self.wait_startup(
                wait_after_first_response=self.wait_after_first_response)

        logger.info("Preparing Group owner: %r", self.group_owner)
        self.group_owner.ensure_private_token()

        self.update_instance_cache()
        logger.info("All preparations done in %.2f seconds. "
                    "Proceeding with tests.", time.time() - start)

        self.load_ssh_keys(key_name_mapping={
            self.group_owner.name: 'group_owner',
        })
        self.upload_ssh_pub_keys()
        self.init_default_group()

    def init_default_group(self):
        gid = self.default_group_id
        if gid is None:
            groups = self.group_owner.api_owned_groups()
            min_depth = None
            for group in groups:
                depth = group['full_path'].count('/')
                if min_depth is None or depth < min_depth:
                    min_depth = depth
                    gid = group['id']

        if gid is None:
            raise RuntimeError(
                "Could not find a group owned by %r" % self.group_owner)
        self.default_group = Group.api_retrieve(
            self, gid, owner_name=self.group_owner.name)

    def remove_ssh_keys(self):
        for user in (self.group_owner, ):
            user.delete_ssh_keys()

    def close(self):
        super(ProductionHeptapod, self).close()
        self.remove_ssh_keys()


class OmnibusHeptapod(Heptapod):

    fs_access = True

    shell_access = True

    repositories_root = '/var/opt/gitlab/git-data/repositories'

    backups_dir = '/var/opt/gitlab/backups'

    RAILS_SERVICES = ('puma', 'sidekiq')

    gitlab_ctl_command = ('sudo', 'gitlab-ctl')

    reverse_call_host = '127.0.0.1'

    ssh_url = 'ssh://git@localhost'

    # TODO read from conf for logical dependency loosening.
    # Not an immediate priority, since we're not concerned about Python 2
    # any more (see heptapod#353)
    hg_executable = '/opt/gitlab/embedded/bin/hg'

    chrome_driver_args = ('--no-sandbox', )

    def execute(self, command, user='git'):
        if user != 'git':
            raise NotImplementedError(
                "On Omnibus Heptapod, only 'git' user is allowed")

        logger.debug("OmnibusHeptapod: executing command %r", command)
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = [o.decode() for o in process.communicate()]
        retcode = process.poll()

        if out:
            sys.stdout.write(out)
        if err:
            sys.stderr.write(err)
        return retcode, out

    def put_archive(self, dest, path, owner='git'):
        # this assumes owner has write access to parent directory,
        # but that should be enough, and avoids some processing as root
        self.run_shell(['tar', '-xf', path, '-C', dest], user=owner)

    def put_archive_bin(self, dest, fobj):
        with tempfile.NamedTemporaryFile() as tempf:
            tempf.write(fobj.read())
            self.put_archive(dest, tempf.name)

    def put_file_lines(self, path, lines, uid=998, gid=998):
        with open(path, 'w') as fobj:
            fobj.writelines(lines)
        os.chown(path, uid, gid)

    def path_exists(self, path):
        return os.path.exists(path)

    def get_file_lines(self, path):
        with open(path) as fobj:
            return fobj.readlines()

    def remove_all_backups(self):
        # using find in order not to rely on shell expansion for *.tar
        self.run_shell(('find', '/var/opt/gitlab/backups',
                        '-name', '*.tar',
                        '-delete'))

    def rake(self, *args):
        cmd = ['gitlab-rake']
        cmd.extend(args)
        code, out = self.execute(cmd, user='git')
        return out.encode()  # Consistency with HDK (returns bytes)

    def gitlab_ctl(self, command, services=None):
        base_cmd = self.gitlab_ctl_command + (command, )
        if services is None:
            self.run_shell(base_cmd)
        else:
            for service in services:
                self.run_shell(base_cmd + (service, ))

    def psql(self, statement):
        # db name is hardcoded.
        # This is good enough for now, but we could
        # read it from config if needed.
        return self.run_shell(('gitlab-psql', 'gitlabhq_production',
                               '-c', statement))


class DockerHeptapod(OmnibusHeptapod):

    gitlab_ctl_command = ('gitlab-ctl', )

    git_executable = 'git'

    chrome_driver_args = ()

    def __init__(self, docker_container, **kw):
        super(DockerHeptapod, self).__init__(**kw)
        self.docker_container = docker_container
        if self.reverse_call_host is None:
            self.reverse_call_host = docker.host_address(docker_container)

    def execute(self, command, user='root'):
        return docker.heptapod_exec(self.docker_container, command, user=user)

    def run_shell(self, command, **kw):
        return docker.heptapod_run_shell(self.docker_container, command, **kw)

    @property
    def ssh_url(self):
        return super(OmnibusHeptapod, self).ssh_url

    def put_archive(self, dest, path, owner='git'):
        res = docker.heptapod_put_archive(self.docker_container, dest, path)
        self.run_shell(['chown', '-R', 'git:root', dest])
        return res

    def put_archive_bin(self, dest, fobj):
        return docker.heptapod_put_archive_bin(
            self.docker_container, dest, fobj)

    def get_archive(self, path, tarf):
        return docker.heptapod_get_archive(self.docker_container, path, tarf)

    def path_exists(self, path):
        code, out = self.execute(['stat', path])
        return code == 0

    def put_file_lines(self, path, lines, uid=998, gid=998):
        dirpath, filename = path.rsplit('/', 1)
        tar_buf = BytesIO()
        tarf = tarfile.open(mode='w:', fileobj=tar_buf)

        tinfo = tarfile.TarInfo(name='hgrc')
        contents_buf = BytesIO()
        contents_buf.writelines(l.encode() for l in lines)
        tinfo.size = contents_buf.tell()
        tinfo.uid, tinfo.gid = uid, gid
        contents_buf.seek(0)
        tarf.addfile(tinfo, fileobj=contents_buf)

        tar_buf.seek(0)
        self.put_archive_bin(dirpath, tar_buf)

    def get_file_lines(self, path):
        dirname, filename = path.rsplit('/', 1)
        buf = BytesIO()
        self.get_archive(path, buf)
        buf.seek(0)
        tarf = tarfile.open(mode='r:', fileobj=buf)
        return [l.decode() for l in tarf.extractfile(filename).readlines()]

    def force_remove_route(self, route_path, source_type='Project'):
        """Delete a route from the database.

        Sometimes GitLab fails to clean Project routes after failed tests.
        """
        logger.warn("Cleaning up leftover route at %r", route_path)
        self.psql("DELETE FROM routes "
                  "WHERE source_type='%s' "
                  "  AND path='%s'" % (source_type, route_path))


class SourceHeptapod(Heptapod):
    """An Heptapod server installed from source on the same system.

    Same system means without using any container technology (Docker or
    otherwise) that would insulate the tests from the server.
    """

    fs_access = True

    shell_access = True

    reverse_call_host = '127.0.0.1'

    @property
    def ssh_url(self):
        return 'ssh://{host}:{port}'.format(
            host=self.host,
            port=self.ssh_port,
        )

    def __init__(self, repositories_root, **kw):
        super(SourceHeptapod, self).__init__(**kw)
        self.repositories_root = repositories_root

    def execute(self, command, user='git'):
        if user != 'git':
            raise NotImplementedError(
                "On source Heptapod, only same user as for Rails and HgServe "
                "is allowed")
        logger.debug("SourceHeptapod: executing command %r", command)
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = [o.decode() for o in process.communicate()]
        retcode = process.poll()

        if out:
            sys.stdout.write(out)
        if err:
            sys.stderr.write(err)
        return retcode, out

    def put_archive(self, dest, path, owner='git'):
        if owner != 'git':
            raise NotImplementedError(
                "On source Heptapod, only same owner as for Rails and HgServe "
                "is allowed")
        subprocess.check_call(['tar', 'xf', path], cwd=dest)

    def get_file_lines(self, path):
        with open(path, 'r') as fobj:
            return fobj.readlines()

    def put_file_lines(self, path, lines):
        with open(path, 'w') as fobj:
            fobj.writelines(lines)

    def path_exists(self, path):
        return os.path.exists(path)


class GdkHeptapod(SourceHeptapod):
    """An Heptapod server running with the GDK.
    """

    fs_access = True

    shell_access = True

    reverse_call_host = '127.0.0.1'

    RAILS_SERVICES = ('rails-web', 'rails-background-jobs')

    def __init__(self, gdk_root, **kw):
        self.gdk_root = gdk_root
        self.rails_root = os.path.join(gdk_root, 'gitlab')
        super(GdkHeptapod, self).__init__(
            repositories_root=os.path.join(gdk_root, 'repositories'),
            **kw)

    @property
    def backups_dir(self):
        return os.path.join(self.rails_root, 'tmp', 'backups')

    def remove_all_backups(self):
        if os.path.exists(self.backups_dir):
            shutil.rmtree(self.backups_dir)
        # as of GitLab 12.10, parent dir is always present
        os.mkdir(self.backups_dir)

    def rake(self, *args):
        cmd = ['bundle', 'exec', 'rake']
        cmd.extend(args)
        logger.debug("GdkHeptapod: calling %r", cmd)
        return subprocess.check_output(cmd, cwd=self.rails_root)

    def gitlab_ctl(self, command, services=None):
        base_cmd = ('gdk', command)

        def do_command(*opt_args):
            cmd = base_cmd + opt_args
            logger.debug("GdkHeptapod: calling %r", cmd)
            subprocess.check_call(cmd, cwd=self.rails_root)

        if services is None:
            do_command()
        else:
            for service in services:
                do_command(service)

    def psql(self, statement):
        # Assuming Unix socket, and db name is hardcoded.
        # This is good enough for now, but we could
        # read connection parameters from gdk.yml if needed.
        return self.run_shell(('psql',
                               '-h', os.path.join(self.gdk_root, 'postgresql'),
                               '-c', statement,
                               'gitlabhq_development',
                               ))
