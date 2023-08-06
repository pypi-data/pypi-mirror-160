# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import attr


@attr.s
class ProjectMirror:
    id = attr.ib()
    project = attr.ib()

    @classmethod
    def api_create(cls, project, **data):
        resp = project.api_post(subpath='remote_mirrors',
                                data=data)

        assert resp.status_code < 300
        return cls(project=project, id=resp.json()['id'])

    @classmethod
    def api_list(cls, project, user=None, check=True):
        """Return a list of dicts, not of ProjectMirror instances.

        The reason is that ProjectMirror currently does not keep more
        state than that's needed for identification.
        """
        resp = project.api_get(subpath='remote_mirrors', user=user)
        if not check:
            return resp
        assert resp.status_code < 300
        return resp.json()

    @property
    def api_subpath(self):
        return 'remote_mirrors/%d' % self.id

    def api_update(self, check=True, **data):
        resp = self.project.api_put(subpath=self.api_subpath, **data)

        if not check:
            return resp

        assert resp.status_code < 300
        return resp.json()

    def api_get(self):
        # no direct method for that, have to resort to the list
        for info in self.api_list(self.project):
            if info['id'] == self.id:
                return info
        raise LookupError(self)

    def api_trigger(self, check=True):
        resp = self.project.api_put(
            subpath=self.api_subpath + '/trigger')
        if not check:
            return resp

        assert resp.status_code < 300
        return resp.json()
