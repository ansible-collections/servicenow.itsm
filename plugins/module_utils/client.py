# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.module_utils.six import PY2
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.six.moves.urllib.parse import urlencode, quote
from ansible.module_utils.urls import Request, basic_auth_header

from .errors import ServiceNowError, AuthError, UnexpectedAPIResponse


DEFAULT_HEADERS = dict(Accept="application/json")


class Response:
    def __init__(self, status, data, headers=None):
        self.status = status
        self.data = data
        # [('h1', 'v1'), ('H2', 'V2')] -> {'h1': 'v1', 'h2': 'V2'}
        self.headers = dict((k.lower(), v) for k, v in dict(headers).items()) if headers else {}

        self._json = None

    @property
    def json(self):
        if self._json is None:
            try:
                self._json = json.loads(self.data)
            except ValueError:
                raise ServiceNowError(
                    "Received invalid JSON response: {0}".format(self.data)
                )
        return self._json


class Client:
    def __init__(
        self, host, username=None, password=None, grant_type=None,
        refresh_token=None, client_id=None, client_secret=None, timeout=None
    ):
        if not (host or "").startswith(('https://', 'http://')):
            raise ServiceNowError("Invalid instance host value: '{0}'. "
                                  "Value must start with 'https://' or 'http://'".format(host))

        self.host = host
        self.username = username
        self.password = password
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.timeout = timeout

        self._auth_header = None
        self._client = Request()

    @property
    def auth_header(self):
        if not self._auth_header:
            self._auth_header = self._login()
        return self._auth_header

    def _login(self):
        if self.client_id and self.client_secret:
            return self._login_oauth()
        return self._login_username_password()

    def _login_username_password(self):
        return dict(Authorization=basic_auth_header(self.username, self.password))

    def _login_oauth(self):
        if self.grant_type == 'refresh_token':
            auth_data = urlencode(
                dict(
                    grant_type=self.grant_type,
                    refresh_token=self.refresh_token,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
            )
        # Only other possible value for grant_type is "password"
        else:
            auth_data = urlencode(
                dict(
                    grant_type=self.grant_type,
                    username=self.username,
                    password=self.password,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
            )
        resp = self._request(
            "POST",
            "{0}/oauth_token.do".format(self.host),
            data=auth_data,
            headers=dict(Accept="application/json"),
        )
        if resp.status != 200:
            raise UnexpectedAPIResponse(resp.status, resp.data)

        access_token = resp.json["access_token"]
        return dict(Authorization="Bearer {0}".format(access_token))

    def _request(self, method, path, data=None, headers=None):
        try:
            raw_resp = self._client.open(
                method, path, data=data, headers=headers, timeout=self.timeout
            )
        except HTTPError as e:
            # Wrong username/password, or expired access token
            if e.code == 401:
                raise AuthError(
                    "Failed to authenticate with the instance: {0} {1}".format(
                        e.code, e.reason
                    ),
                )
            # Other HTTP error codes do not necessarily mean errors.
            # This is for the caller to decide.
            return Response(e.code, e.read(), e.headers)
        except URLError as e:
            raise ServiceNowError(e.reason)

        if PY2:
            return Response(raw_resp.getcode(), raw_resp.read(), raw_resp.info())
        return Response(raw_resp.status, raw_resp.read(), raw_resp.headers)

    def request(self, method, path, query=None, data=None, headers=None, bytes=None):
        # Make sure we only have one kind of payload
        if data is not None and bytes is not None:
            raise AssertionError(
                "Cannot have JSON and binary payload in a single request."
            )

        escaped_path = quote(path.rstrip("/"))
        url = "{0}/api/now/{1}".format(self.host, escaped_path)
        if query:
            url = "{0}?{1}".format(url, urlencode(query))
        headers = dict(headers or DEFAULT_HEADERS, **self.auth_header)
        if data is not None:
            data = json.dumps(data, separators=(",", ":"))
            headers["Content-type"] = "application/json"
        elif bytes is not None:
            data = bytes
        return self._request(method, url, data=data, headers=headers)

    def get(self, path, query=None):
        resp = self.request("GET", path, query=query)
        if resp.status in (200, 404):
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)

    def post(self, path, data, query=None):
        resp = self.request("POST", path, data=data, query=query)
        if resp.status == 201:
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)

    def patch(self, path, data, query=None):
        resp = self.request("PATCH", path, data=data, query=query)
        if resp.status == 200:
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)

    def put(self, path, data, query=None):
        resp = self.request("PUT", path, data=data, query=query)
        if resp.status == 200:
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)

    def delete(self, path, query=None):
        resp = self.request("DELETE", path, query=query)
        if resp.status != 204:
            raise UnexpectedAPIResponse(resp.status, resp.data)
