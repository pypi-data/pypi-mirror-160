# Copyright 2020-2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
from contextlib import contextmanager
import time

from .namespace import Group
from .project import Project
from .utils import unique_name


@contextmanager
def project_fixture(heptapod, name_prefix, owner=None, group=None, **opts):
    # TODO provide importable from heptapod_tests
    if owner is None:
        owner = heptapod.default_user_name
    if group is None:
        group = heptapod.default_group
    name = '%s_%s' % (name_prefix, str(time.time()).replace('.', '_'))
    with Project.api_create(heptapod, owner, name,
                            group=group, **opts) as proj:
        yield proj


@contextmanager
def group_fixture(heptapod, path_prefix, creator_name='root', parent=None):
    with Group.api_create(heptapod, unique_name(path_prefix),
                          user_name=creator_name,
                          parent=parent) as group:
        yield group
