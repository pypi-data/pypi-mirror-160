# Copyrightqhg 2019-2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import enum


class Access(enum.IntEnum):
    """Union of all possible values for Projects and Groups."""
    NO_ACCESS = 0
    MINIMAL = 5  # Introduced in GitLab 13.5
    GUEST = 10
    REPORTER = 20
    DEVELOPER = 30
    HG_PUBLISHER = 33  # Introduced in Heptapod 0.26
    MAINTAINER = 40
    OWNER = 50


class ProjectAccess(enum.IntEnum):
    """Subset of Access suitable to set on a Project.

    - `OWNER` is only settable on Groups.
    - `NO_ACCESS` is probably not settable on Projects
    - `MINIMAL` is to be determined
    """
    GUEST = Access.GUEST
    REPORTER = Access.REPORTER
    DEVELOPER = Access.DEVELOPER
    HG_PUBLISHER = Access.HG_PUBLISHER
    MAINTAINER = Access.MAINTAINER


class GroupAccess(enum.IntEnum):
    """Subset of Access suitable to set on a Group"""
    GUEST = Access.GUEST
    REPORTER = Access.REPORTER
    DEVELOPER = Access.DEVELOPER
    MAINTAINER = Access.MAINTAINER
    OWNER = Access.OWNER
