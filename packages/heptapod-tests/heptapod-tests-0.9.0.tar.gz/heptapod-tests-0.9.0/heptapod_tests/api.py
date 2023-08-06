# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import requests


def api_request(method, obj, user, subpath='', **kwargs):
    """Perform a simple API HTTP request as the given user on given obj.


    :param method: the HTTP method to use, same as in `requests.request`.
    :param obj: the GitLab/Heptapod object, e.g. a `Project` instance.
       It must implement have an `api_url` attribute or property.
    :param user: a class:`User` instance.

    The full URL is made of the API URL of the object, together with
    the given subpath (example 'merge_requests/1').

    Appropriate authentication headers are added on the fly.

    All kwargs are passed to `requests.request()`
    """
    headers = kwargs.pop('headers', {})
    headers['Private-Token'] = user.token
    return requests.request(method,
                            '/'.join((obj.api_url, subpath)),
                            headers=headers,
                            **kwargs)


class GitLabEntity:
    """Abstract base class for various API entities (Project, Group…).

    Expected attributes or properties:

    - ``api_url``
    - ``owner_user``
    """

    def api_request(self, method, user=None, **kwargs):
        """Perform an API request as the given user.

        :param User user: if ``None``, defaults to the project owner

        Other params are passed down to :func:`api_request`.

        This method will eventually replace the older :meth:`api_request`,
        or be replaced by defaulting logic directly in the :func:`api_request`
        function.
        """
        if user is None:
            user = self.owner_user
        return api_request(method, self, user, **kwargs)

    # compat alias for subclass also having an `api_request` method
    user_api_request = api_request

    def api_get(self, **kwargs):
        """Perform a simple HTTP API GET, by default as the owner.

        :param kwargs: as in :meth:`user_api_request`
        """
        return self.user_api_request('GET', **kwargs)

    def api_put(self, **kwargs):
        """Perform a simple HTTP API PUT, by default as the owner.

        :param kwargs: as in :meth:`user_api_request`
        """
        return self.user_api_request('PUT', **kwargs)

    def api_post(self, **kwargs):
        """Perform a simple HTTP API POST, by default as the owner.

        :param kwargs: as in :meth:`user_api_request`
        """
        return self.user_api_request('POST', **kwargs)

    def api_delete(self, **kwargs):
        """Perform a simple HTTP API DELETE, by default as the owner.

        :param kwargs: as in :meth:`user_api_request`
        """
        return self.user_api_request('DELETE', **kwargs)
