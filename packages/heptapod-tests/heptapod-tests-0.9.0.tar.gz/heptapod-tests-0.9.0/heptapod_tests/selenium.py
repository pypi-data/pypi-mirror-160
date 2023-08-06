# Copyright 2019-2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Shared Selenium utils."""

import logging
import time
from selenium.common.exceptions import (
    ElementNotVisibleException,
    ElementNotInteractableException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from heptapod_tests.wait import (
    BASE_TIMEOUT,
    wait_assert,
)

logger = logging.getLogger(__name__)


def page_means_not_ready(driver):
    """Detect a few symptoms of Heptapod not fully ready"""
    if '502' in driver.title:
        return True
    if 'Gitlab::Webpack::Manifest::ManifestLoadError' in driver.title:
        return True
    return False


def raw_page_content(driver):
    """Extract the content of a page meant for GitLab raw downloads.

    The webdriver rewraps it into a HTML ``pre`` element.
    """
    try:
        return driver.find_element(By.TAG_NAME, 'pre').text
    except NoSuchElementException:
        raise AssertionError("Page is empty or not a GitLab raw page")


def webdriver_wait_get(heptapod, driver,
                       relative_uri='', timeout=300, retry_delay=1):
    """Get the given URL when it's ready.

    At this stage, we already got the 302 on the site base URL, it's not
    clear why we can still get 502s, maybe just because that's harder
    that the simple redirection. Anyway, that justifies a shorter timeout
    by default than the initial one.
    """
    url = heptapod.url + relative_uri
    start = time.time()
    dead_msg = ("Heptapod server did not give a successful response"
                "in %s seconds" % timeout)
    while True:
        if time.time() > start + timeout:
            heptapod.dead = True  # will abort subsequent tests
        driver.get(url)
        if not page_means_not_ready(driver):
            break
        logger.debug("Title of page at %r is %r, retrying in %.1f seconds",
                     url, driver.title, retry_delay)
        time.sleep(retry_delay)
    assert not heptapod.dead, dead_msg


def could_click_element(selector):
    def try_click_element(driver):
        try:
            elem = selector(driver)
            elem.click()
            return True
        except (ElementNotVisibleException,
                NoSuchElementException,
                ElementNotInteractableException):
            return False
        except Exception:
            import traceback
            traceback.print_exc()
            return False
    return try_click_element


def webdriver_wait(driver, timeout_factor=1):
    return WebDriverWait(driver, BASE_TIMEOUT * timeout_factor)


def wait_could_click_element(driver, selector, **wait_kw):
    webdriver_wait(driver, **wait_kw).until(could_click_element(selector))


def wait_element_visible(driver, loc_by, loc_expr, **wait_kw):
    return webdriver_wait(driver, **wait_kw).until(
        ec.visibility_of_element_located((loc_by, loc_expr))
    )


def wait_assert_in_page_source(driver, s):
    """Wait until the given string is in page source.

    Avoid doubts with eager evaluation of `driver.page_source` (would not
    happen in a lambda, but still).
    """
    wait_assert(lambda: driver.page_source,
                lambda source: s in source)


def assert_webdriver_not_error(webdriver):
    """assert that the current page is not GitLab's error page rendering.

    We don't have a reliable way to detect an error
    The page title would be just 500 in production and the error class name in
    # development mode.
    """
    title = webdriver.title
    assert "Error" not in title
    assert not any(("(%d)" % code) in title
                   for code in (500, 502, 504, 403, 404))
