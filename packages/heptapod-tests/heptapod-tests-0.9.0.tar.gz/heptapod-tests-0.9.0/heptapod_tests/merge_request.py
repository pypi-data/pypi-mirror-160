# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import attr
from urllib.parse import (
    urlencode,
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .api import api_request
from .selenium import (
    wait_could_click_element,
    webdriver_wait,
)
from .wait import (
    wait_assert,
)


@attr.s
class MergeRequest:
    project = attr.ib()
    iid = attr.ib()

    @property
    def api_url(self):
        return '%s/merge_requests/%d' % (self.project.api_url, self.iid)

    @property
    def url(self):
        return '%s/-/merge_requests/%d' % (self.project.url, self.iid)

    @classmethod
    def api_create(cls, source_project, source_branch,
                   target_branch='branch/default',
                   target_project=None,
                   user=None,
                   title="Created through API"):
        data = dict(id=source_project.id,
                    source_branch=source_branch,
                    target_branch=target_branch,
                    title=title)
        if target_project is None:
            target_project = source_project
        else:
            data['target_project_id'] = target_project.id
        if user is None:
            user = source_project.owner_user
        resp = api_request('post', source_project, user,
                           subpath='merge_requests',
                           data=data)

        assert resp.status_code in (200, 201)
        return cls(target_project, resp.json()['iid'])

    @classmethod
    def webdriver_create(cls, source_project, source_branch,
                         target_branch='branch/default',
                         target_project=None,
                         user=None):
        """Create a merge request through the Web UI and return it.
        """
        if user is None:
            user = source_project.owner_user
        if target_project is None:
            target_project = source_project

        driver = user.webdriver
        compare_qs = {
            'merge_request[source_project_id]': source_project.id,
            'merge_request[source_branch]': source_branch,
            'merge_request[target_project_id]': target_project.id,
            'merge_request[target_branch]': target_branch,
        }
        driver.get('{url}/merge_requests/new?{qs}'.format(
            url=source_project.url,
            qs=urlencode(compare_qs),
        ))
        assert 'new merge request' in driver.title.lower()
        assert source_project.name in driver.title

        wait_could_click_element(driver, lambda d: d.find_element(
            By.XPATH,
            '//input[@type="submit" '
            'and @value="Create merge request"]')
        )

        split_url = driver.current_url.rsplit('/', 2)
        assert split_url[-2] == 'merge_requests'
        # same as with API creations: the MR belongs to target Project
        return cls(target_project, int(split_url[-1]))

    def api_get(self, user=None, assert_existence=True, check=True, **params):
        if user is None:
            user = self.project.owner_user
        resp = api_request('get', self, user, params=params)
        if resp.status_code == 404 and not assert_existence:
            return None

        if not check:
            return resp

        assert resp.status_code < 400
        return resp.json()

    def wait_assert(self, condition,
                    with_rebase_progress=False,
                    with_diverged_count=False,
                    msg=None,
                    **kw):
        if msg is None:
            msg = (
                "The given condition on Merge Request %s was still not "
                "fulfilled after retrying for {timeout} seconds") % self
        mr_opts = dict(include_diverged_commits_count=with_diverged_count,
                       include_rebase_in_progress=with_rebase_progress)
        return wait_assert(
            lambda: self.api_get(assert_existence=False, **mr_opts),
            condition,
            msg=msg, **kw)

    def api_put(self, data, user=None, check=True, subpath=''):
        if user is None:
            user = self.project.owner_user

        resp = api_request('put', self, user, subpath=subpath, data=data)
        if not check:
            return resp

        assert resp.status_code < 400
        return resp.json()

    def api_edit(self, user=None, check=True, **data):
        return self.api_put(data, user=user, check=check)

    def api_rebase(self, user=None, **kw):
        """Trigger rebase and wait_assert for completion.

        :param kwargs: passed down to :meth:`wait_assert`
        """
        resp = self.api_put(None, user=user, subpath='rebase', check=False)
        assert resp.status_code == 202  # Means "accepted", this is async
        mr_info = self.wait_assert(lambda info: not info['rebase_in_progress'],
                                   with_rebase_progress=True)
        assert mr_info['merge_error'] is None

    def api_accept(self,
                   user=None,
                   wait_mergeability=True,
                   timeout_factor=1,
                   check_merged=True,
                   **opts):
        if wait_mergeability:
            self.wait_assert(
                lambda info: info.get('merge_status') == 'can_be_merged',
                timeout_factor=timeout_factor,
                msg="Mergeability wrong or still unknown after "
                "{timeout} seconds")

        resp = self.api_put(dict(merge_request_iid=self.iid,
                                 id=self.project.id,
                                 **opts),
                            subpath='merge',
                            user=user,
                            check=False)

        if not check_merged:
            return resp

        assert resp.status_code == 200
        info = resp.json()
        assert info['state'] == 'merged'
        return info

    def wait_assert_merged(self,
                           expected_source_branch=None,
                           expected_source_branch_category=None,
                           check_source_branch_removal=True,
                           **wait_kw):
        """Checks that after a while, state is `merged` plus options

        :param expected_source_branch: if passed, will check that once merged
            the source branch is the given one. Not taken from MR info
            before waiting, for it could have been damaged by a bug (e.g. in
            `PostReceiveWorker`.
        :param expected_source_branch_category: similar to
            ``expected_source_branch`` but only checks for correct category,
            where category is translated to prefix and slash (e.g., ``topic/``)
        :param check_source_branch_removal: if `True`, check that the
            source branch does not exist any more server-side.
        """
        info = self.wait_assert(lambda info: info.get('state') == 'merged',
                                msg="Merge not detected in {timeout} seconds",
                                **wait_kw)

        project = self.project

        # Web UI for the merge request is not broken
        webdriver = project.owner_webdriver
        webdriver.get(self.url)
        assert '(500)' not in webdriver.title

        source_branch = info['source_branch']
        if expected_source_branch is not None:
            assert source_branch == expected_source_branch

        if expected_source_branch_category:
            assert source_branch.startswith(
                expected_source_branch_category + '/')

        if check_source_branch_removal:
            project.wait_assert_api_branches(
                lambda branches: source_branch not in branches)

    def webdriver_get_commit_links(self):
        """Retrieve the commit links from the 'commits' panel of the MR."""
        webdriver = self.project.owner_webdriver
        # this is the 'commits' pane, loading is dynamic, hence the wait
        webdriver.get(self.url + '/commits')
        webdriver_wait(webdriver).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'a.commit-row-message')))

        return webdriver.find_elements(By.CSS_SELECTOR, 'li.commit')

    def assert_user_cannot_merge(self, user):
        # let's decrease chances of false negatives by testing that user has
        # access to the MR (projects tend to be private by default).
        # We could do better by, e.g., adding a comment but that requires only
        # the Reporter role.
        resp = api_request('GET', self, user)
        assert resp.status_code == 200

        resp = self.api_accept(user=user, check_merged=False)
        assert resp.status_code >= 400

    def assert_commit_link(self, expected_text, expected_sha):
        """Assert that a commit link with expected text and sha is present.
        """
        for li in self.webdriver_get_commit_links():
            if expected_text in li.text:
                # finer assertions about commit hash widget
                copy_label = li.find_element(
                    By.XPATH,
                    # div with class 'label', in a div having a button child
                    './/div[button]/div[contains(@class, "label")]')
                copy_button = li.find_element(
                    By.XPATH,
                    './/button[@title="Copy commit SHA"]')
                assert copy_button.get_attribute(
                    'data-clipboard-text') == expected_sha
                assert expected_sha.startswith(copy_label.text)
                return
        else:
            raise AssertionError(
                "Could not find a commit row with text %r" % expected_text)
