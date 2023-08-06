# Copyright 2019-2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os
import time

logger = logging.getLogger(__name__)

BASE_TIMEOUT = int(os.environ.get('HEPTAPOD_TESTS_BASE_TIMEOUT', '10').strip())


def log_base_timeout():
    logger.info("Base timeout is set to %r seconds", BASE_TIMEOUT)


def wait_assert(get_info, condition,
                before_retry=None,
                timeout_factor=1,
                retry_wait_factor=0.02,
                msg="Condition not fulfilled after {timeout} seconds"):
    """Assert some condition to become True after some tries.

    Many things are asynchronous in GitLab and moreso with time.

    :param get_info: callable with no arguments
    :param condition: callable that will passed the result of `get_info`
                      as its unique arguments
    :param before_retry: callable that will be invoked on retries only, with
      the result of `get_info`. It can be used to log the retry, or to
      recreate the proper conditions to call `get_info` again (if there were
      side effects).
    :param timeout_factor: how many times :const:`BASE_TIMEOUT` to wait until
       the condition is fulfilled.
    :param retry_wait_factor: time to wait between retries, expressed in
       multiples of the computed timeout.
    :param msg: format string used when raising AssertionError
    :returns: the latest list returned by `get_info`, guaranteed to fulfill
              `condition`
    :raises: AssertionError with the formatted given `msg`.
    """
    fulfilled = False
    timeout = timeout_factor * BASE_TIMEOUT
    retry_wait = timeout * retry_wait_factor
    start = time.time()
    while not fulfilled and time.time() - start < timeout:
        info = get_info()
        fulfilled = condition(info)
        if not fulfilled:
            if before_retry is not None:
                before_retry(info)
            time.sleep(retry_wait)

    if not fulfilled:
        raise AssertionError(msg.format(timeout=timeout))
    return info
