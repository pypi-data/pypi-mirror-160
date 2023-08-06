# Copyrightqhg 2019-2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import re
import time
from pytest import register_assert_rewrite

# Ask pytest to rewrite assertions in non-test modules
register_assert_rewrite("tests.utils.project", "tests.utils.session")


def unique_name(name):
    return '%s_%s' % (name, str(time.time()).replace('.', '_'))


def assert_message(message, expectations):
    """assert that a message matches expectations

    :param expectattions: any iterable whose elements can be either `bytes`,
       `str` or a compiled regexp.
       In the two former cases a simple `in` operator is used. In the latter
       case, the :meth:`search` is used.
       For caller convenience, a single value can also be used.

    Note: if expected is an empty string, the assertion is a no-op.
    """
    if isinstance(expectations, (str, bytes, re.Pattern)):
        expectations = (expectations, )

    for exp in expectations:
        if isinstance(exp, re.Pattern):
            if exp.search(message) is None:
                return False
        elif exp not in message:
            return False
    return True
