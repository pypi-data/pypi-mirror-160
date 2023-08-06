# Copyright 2019-2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import attr
import requests

from .access_levels import GroupAccess


class NameSpace:

    @property
    def url(self):
        return '/'.join((self.heptapod.url, self.full_path))


@attr.s
class UserNameSpace(NameSpace):
    user_name = attr.ib()
    heptapod = attr.ib()

    @property
    def full_path(self):
        return self.user_name

    def __eq__(self, other):
        return other.__class__ == self.__class__ and self.user == other.user


@attr.s
class Group(NameSpace):

    id = attr.ib()
    path = attr.ib()
    full_path = attr.ib()
    heptapod = attr.ib()
    owner_name = attr.ib(default=None)

    api_uri = '/api/v4/groups'

    @classmethod
    def api_create(cls, heptapod, group_path, user_name='root', parent=None):
        data = dict(name=group_path,
                    path=group_path)
        if parent is not None:
            data['parent_id'] = parent.id

        headers = {'Private-Token': heptapod.users[user_name].token}
        resp = requests.post(heptapod.url + cls.api_uri,
                             headers=headers,
                             data=data)
        assert resp.status_code == 201
        res = resp.json()
        return cls.api_retrieve(heptapod, group_id=res['id'])

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    def api_retrieve(cls, heptapod, group_id, owner_name=None):
        """Return a checked Group object for the given id.

        :owner_name: if specified, registered as :attr:`owner_name` on the
           returned object, and used for all API calls, including the check
           performed by this method.
        """
        grp = Group(heptapod=heptapod,
                    id=group_id,
                    full_path=None,
                    owner_name=owner_name,
                    path=None)
        resp = grp.api_get()
        assert resp.status_code == 200
        info = resp.json()
        grp.path = info['path']
        grp.full_path = info['full_path']
        return grp

    def private_token(self):
        """Return a token strong enough for all operations.

        Namely, using a token for an owner, if there's a known one or
        an Administrator token
        """
        user_name = self.owner_name if self.owner_name is not None else 'root'
        return {'Private-Token': self.heptapod.users[user_name].token}

    def api_get(self, subpath=''):
        return requests.get('/'.join((self.api_url, subpath)),
                            headers=self.private_token())

    def api_post(self, subpath='', **params):
        return requests.post('/'.join((self.api_url, subpath)),
                             headers=self.private_token(),
                             data=params)

    def api_put(self, subpath='', **params):
        return requests.put('/'.join((self.api_url, subpath)),
                            headers=self.private_token(),
                            data=params)

    @classmethod
    def api_search(cls, heptapod, group_name, user_name='root'):
        headers = {'Private-Token': heptapod.users[user_name].token}
        resp = requests.get(heptapod.url + cls.api_uri,
                            headers=headers,
                            params=dict(search=group_name))
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        group = data[0]
        return cls.api_retrieve(heptapod, group_id=group['id'])

    @property
    def api_url(self):
        return self.heptapod.url + self.api_uri + '/%d' % self.id

    def api_delete(self):
        resp = requests.delete(self.api_url, headers=self.private_token())
        assert resp.status_code in (202, 204)

    def grant_member_access(self, user, level):
        """Grant given user the given access level.

        It doesn't matter whether the user is already a member or not: this
        method abstracts over it.

        This method is idempotent.

        TODO factorize with Project (as surely is done in the Rails app)
        """
        assert level in GroupAccess

        user_id = user.id
        resp = self.api_get(subpath='members/%d' % user_id)
        if resp.status_code == 404:
            subpath = 'members'
            meth = self.api_post
        else:
            subpath = 'members/%d' % user_id
            meth = self.api_put

        resp = meth(subpath=subpath,
                    user_id=user_id,
                    access_level=int(level))
        assert resp.status_code < 400

    def custom_attribute_api_url(self, key):
        return '/'.join((self.api_url, 'custom_attributes', key))

    def api_set_custom_attribute(self, key, value, user=None):
        if user is None:
            user = self.heptapod.get_user('root')

        resp = requests.put(self.custom_attribute_api_url(key),
                            headers={'Private-Token': user.token},
                            data=dict(value=value))

        assert resp.status_code == 200
        return resp.json()

    def api_get_custom_attribute(self, key, check=True, user=None):
        if user is None:
            user = self.heptapod.get_user('root')

        resp = requests.get(self.custom_attribute_api_url(key),
                            headers={'Private-Token': user.token})

        if not check:
            return resp

        assert resp.status_code < 400
        return resp.json()['value']

    def fs_path(self):
        return '/'.join((self.heptapod.repositories_root, self.full_path))

    def put_hgrc(self, lines):
        """Replace group's server-side HGRC with given lines.

        The lines have to include LF, same as with `writelines()`.
        """
        fs_path = self.fs_path()
        self.heptapod.run_shell(('mkdir', '-p', fs_path), user='git')
        self.heptapod.put_file_lines(fs_path + '/hgrc', lines)

    def __enter__(self):
        return self

    def __exit__(self, *exc_args):
        self.api_delete()
        return False
