# Copyright 2018 Paul Morelle <madprog@htkc.org>
# Copyright 2019-2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from .selenium import (
    wait_could_click_element,
    wait_element_visible,
    webdriver_wait_get,
)


logger = logging.getLogger(__name__)


def initialize_root(driver, heptapod, password):
    # Create initial password
    elem = driver.find_element(By.NAME, 'user[password]')
    elem.send_keys(password)
    elem = driver.find_element(By.NAME, 'user[password_confirmation]')
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)

    sign_in_page_login(driver, heptapod, 'root', password=password)


def finalize_password(driver, heptapod, user, password, current_password=None):
    """Enter the final password, if already on the "Set up new password" page.
    """
    if current_password is None:
        current_password = password

    elem = driver.find_element(By.NAME, 'user[password]')
    elem.send_keys(current_password)
    elem = driver.find_element(By.NAME, 'user[new_password]')
    elem.send_keys(password)
    elem = driver.find_element(By.NAME, 'user[password_confirmation]')
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)


def sign_in_page_login(driver, heptapod, user_name, password=None):
    """Perform login as user, with webdriver already on the signin page.

    If password is not specified, it is read from the heptapod object.
    If it is, it'll be stored in the heptapod object
    """
    user = heptapod.users[user_name]
    if password is None:
        password = user.password
    else:
        user.password = password
    if heptapod.clever_cloud_sso:
        user.vcs_token_only = True
        return sign_in_page_clever_cloud_login(driver, user)

    elem = driver.find_element(By.NAME, 'user[login]')
    elem.send_keys(user_name)
    elem = driver.find_element(By.NAME, 'user[password]')
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)

    # Wait for login to be complete
    wait_element_visible(driver,
                         By.XPATH,
                         '//li[@data-qa-selector="user_menu"]')


def sign_in_page_clever_cloud_login(driver, user):
    wait_could_click_element(
        driver,
        lambda d: d.find_element(By.ID, 'oauth-login-saml'))
    assert 'clever-cloud.com' in driver.current_url

    elem = driver.find_element(By.ID, 'login-email')
    elem.send_keys(user.email)
    elem = driver.find_element(By.ID, 'login-pwd')
    elem.send_keys(user.password)
    elem.send_keys(Keys.RETURN)

    assert driver.current_url.startswith(user.heptapod.url)


def page_is_password_setup(driver):
    """Return if the current page is the password setup page.

    This happens for instance after first login with a password considered
    to be temporary
    """
    # plural form to get an empty list instead of an exception
    return bool(driver.find_elements(By.NAME, 'user[password_confirmation]'))


def login_as_root(driver, heptapod, password):
    start = time.time()
    webdriver_wait_get(heptapod, driver, relative_uri='/users/sign_in')
    assert 'GitLab' in driver.title
    html = driver.find_element(By.TAG_NAME, 'html').get_attribute('innerHTML')

    if 'Please create a password for your new account.' in html:
        initialize_root(driver, heptapod, password)
    else:
        sign_in_page_login(driver, heptapod, 'root', password)
        if page_is_password_setup(driver):
            finalize_password(driver, heptapod, 'root', password)
            sign_in_page_login(driver, heptapod, 'root', password)
        logger.info("Made signed-in webdriver for user %r in %.2f seconds",
                    'root', time.time() - start)
