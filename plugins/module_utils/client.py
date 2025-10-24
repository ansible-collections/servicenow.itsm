# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import ssl
import time
import logging

from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from ansible.module_utils.urls import Request, basic_auth_header

from .errors import AuthError, ServiceNowError, UnexpectedAPIResponse

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {"Accept": "application/json"}


class Response:
    def __init__(
        self, status, data, headers=None, json_decoder_hook=None, max_cache_size=100
    ):
        self.status = status
        self.data = data
        # [('h1', 'v1'), ('H2', 'V2')] -> {'h1': 'v1', 'h2': 'V2'}
        self.headers = (
            dict((k.lower(), v) for k, v in dict(headers).items()) if headers else {}
        )

        self._json = None
        self.json_decoder_hook = json_decoder_hook
        self._max_cache_size = max_cache_size
        self._cache_entries = 0

    def clear_cache(self):
        """Clear cached JSON data to free memory"""
        self._json = None
        self._cache_entries = 0

    @property
    def json(self):
        if self._json is None:
            try:
                self._json = json.loads(self.data, object_hook=self.json_decoder_hook)
                self._cache_entries += 1

                # Auto-cleanup if cache gets too large
                if self._cache_entries > self._max_cache_size:
                    logger.debug("JSON cache size exceeded, clearing cache")
                    self.clear_cache()
            except ValueError as exc:
                raise ServiceNowError(
                    f"Received invalid JSON response: {self.data}"
                ) from exc
        return self._json


class Client:
    def __init__(
        self,
        host,
        username=None,
        password=None,
        grant_type=None,
        refresh_token=None,
        access_token=None,
        api_key=None,
        client_id=None,
        client_secret=None,
        client_certificate_file=None,
        client_key_file=None,
        custom_headers=None,
        api_path="api/now",
        timeout=None,
        validate_certs=None,
        json_decoder_hook=None,
        connection_timeout=300,  # 5 minutes
        max_retries=3,
    ):
        if not (host or "").startswith(("https://", "http://")):
            raise ServiceNowError(
                f"Invalid instance host value: '{host}'. "
                "Value must start with 'https://' or 'http://'"
            )

        self.host = host
        self.username = username
        self.password = password
        # Since version: 2.3.0: make up for removed default from arg specs to preserve backward compatibility.
        self.grant_type = "password" if grant_type is None else grant_type
        self.client_id = client_id
        self.client_certificate_file = client_certificate_file
        self.client_key_file = client_key_file
        self.client_secret = client_secret
        self.custom_headers = custom_headers
        self.api_path = tuple(api_path.strip("/").split("/"))
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.api_key = api_key
        self.timeout = timeout
        self.validate_certs = validate_certs
        self.json_decoder_hook = json_decoder_hook
        self.connection_timeout = connection_timeout
        self.max_retries = max_retries

        self._auth_header = None
        self._client = Request()
        self._connection_created = time.time()
        self._request_count = 0

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup resources"""
        self.close()

    def __del__(self):
        """Cleanup connections when client is destroyed"""
        try:
            self.close()
        except Exception:
            pass  # Ignore errors during cleanup

    def close(self):
        """Explicitly close connections and cleanup resources"""
        try:
            if hasattr(self._client, "close"):
                self._client.close()
            self._auth_header = None
            self._client = None
            logger.debug("Client connections closed")
        except Exception as e:
            logger.warning("Error during client cleanup: %s", e)

    def _refresh_connection(self):
        """Refresh the underlying connection"""
        try:
            if hasattr(self._client, "close"):
                self._client.close()
        except Exception:
            pass
        self._client = Request()
        self._connection_created = time.time()
        self._request_count = 0
        logger.debug("Connection refreshed")

    def _should_refresh_connection(self):
        """Check if connection should be refreshed"""
        return (
            time.time() - self._connection_created > self.connection_timeout
            or self._request_count > 1000
        )

    @property
    def auth_header(self):
        if not self._auth_header:
            self._auth_header = self._login()
        return self._auth_header

    def _login(self):
        if self.client_id and self.client_secret:
            return self._login_oauth()
        elif self.api_key:
            return self._login_token(self.api_key, is_api_key=True)
        elif self.access_token:
            return self._login_token(self.access_token, is_api_key=False)
        return self._login_username_password()

    def _login_username_password(self):
        return {"Authorization": basic_auth_header(self.username, self.password)}

    def _login_token(self, token, is_api_key=False):
        if is_api_key:
            return {"x-sn-apikey": token}
        else:
            return {"Authorization": f"Bearer {token}"}

    def _login_oauth_generate_auth_data(self):
        """
        Creates a dictionary of auth data to be used in OAUTH requests, depending on the
        grant type. See SNOW docs for more details:
        https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB1647747
        """
        if self.grant_type == "refresh_token":
            return urlencode(
                dict(
                    grant_type=self.grant_type,
                    refresh_token=self.refresh_token,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
            )
        elif self.grant_type == "client_credentials":
            return urlencode(
                dict(
                    grant_type=self.grant_type,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
            )
        # Default value for grant_type is "password"
        else:
            return urlencode(
                dict(
                    grant_type=self.grant_type,
                    username=self.username,
                    password=self.password,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
            )

    def _login_oauth(self):
        auth_data = self._login_oauth_generate_auth_data()
        resp = self._request(
            "POST",
            f"{self.host}/oauth_token.do",
            data=auth_data,
            headers={"Accept": "application/json"},
        )
        if resp.status != 200:
            raise UnexpectedAPIResponse(resp.status, resp.data)

        access_token = resp.json["access_token"]
        return self._login_token(access_token, is_api_key=False)

    def _request(self, method, path, data=None, headers=None):
        """Make a request with retry logic and connection management"""
        if self._should_refresh_connection():
            self._refresh_connection()

        for attempt in range(self.max_retries):
            try:
                return self._make_single_request(method, path, data, headers)
            except HTTPError as e:
                return self._handle_http_error(e)
            except (URLError, ConnectionError, TimeoutError) as e:
                if not self._handle_connection_error(e, attempt):
                    break
            except ssl.SSLError as e:
                self._handle_ssl_error(e)
            except Exception as e:
                if not self._handle_generic_error(e, attempt):
                    break

    def _make_single_request(self, method, path, data, headers):
        """Make a single HTTP request and return response"""
        raw_resp = self._client.open(
            method,
            path,
            data=data,
            headers=headers,
            timeout=self.timeout,
            validate_certs=self.validate_certs,
            client_cert=self.client_certificate_file,
            client_key=self.client_key_file,
        )

        # Increment request count
        self._request_count += 1

        # Read response data
        response_data = raw_resp.read()

        return Response(
            raw_resp.status,
            response_data,
            raw_resp.headers,
            self.json_decoder_hook,
        )

    def _handle_http_error(self, error):
        """Handle HTTP errors"""
        if error.code == 401:
            raise AuthError(
                f"Failed to authenticate with the instance: {error.code} {error.reason}",
            )
        # Other HTTP error codes do not necessarily mean errors.
        # This is for the caller to decide.
        return Response(error.code, error.read(), error.headers)

    def _handle_connection_error(self, error, attempt):
        """Handle connection errors with retry logic"""
        if attempt == self.max_retries - 1:
            raise ServiceNowError(
                f"Connection failed after {self.max_retries} attempts: {error.reason}"
            )
        logger.warning(
            "Connection error, retrying... (%s/%s): %s",
            attempt + 1,
            self.max_retries,
            error,
        )
        time.sleep(2**attempt)  # Exponential backoff
        self._refresh_connection()
        return True

    def _handle_ssl_error(self, error):  # pylint: disable=unused-argument
        """Handle SSL errors"""
        if self.client_certificate_file:
            raise ServiceNowError(
                "Failed to communicate with instance due to SSL error, likely related to the client certificate or key. "
                "Ensure the files are accessible on the Ansible host and in the correct format (see module documentation)."
            )
        raise error

    def _handle_generic_error(self, error, attempt):
        """Handle generic errors with retry logic"""
        if attempt == self.max_retries - 1:
            raise error
        logger.warning(
            "Unexpected error, retrying... (%s/%s): %s",
            attempt + 1,
            self.max_retries,
            error,
        )
        time.sleep(2**attempt)
        self._refresh_connection()
        return True

    def _request_streaming(
        self, method, path, data=None, headers=None, chunk_size=8192
    ):
        """Stream large responses instead of loading into memory"""
        if self._should_refresh_connection():
            self._refresh_connection()

        for attempt in range(self.max_retries):
            try:
                return self._make_streaming_request(
                    method, path, data, headers, chunk_size
                )
            except (URLError, ConnectionError, TimeoutError) as e:
                if not self._handle_connection_error(e, attempt):
                    break
            except Exception as e:
                if not self._handle_generic_error(e, attempt):
                    break

    def _make_streaming_request(self, method, path, data, headers, chunk_size):
        """Make a streaming HTTP request and return response"""
        raw_resp = self._client.open(
            method,
            path,
            data=data,
            headers=headers,
            timeout=self.timeout,
            validate_certs=self.validate_certs,
            client_cert=self.client_certificate_file,
            client_key=self.client_key_file,
        )

        # Increment request count
        self._request_count += 1

        # Stream response data
        response_data = b""
        for chunk in iter(lambda: raw_resp.read(chunk_size), b""):
            response_data += chunk

        return Response(
            raw_resp.status,
            response_data,
            raw_resp.headers,
            self.json_decoder_hook,
        )

    def request(
        self,
        method,
        path,
        query=None,
        data=None,
        headers=None,
        bytes=None,  # pylint: disable=redefined-builtin
        stream=False,
    ):
        # Make sure we only have one kind of payload
        if data is not None and bytes is not None:
            raise AssertionError(
                "Cannot have JSON and binary payload in a single request."
            )

        escaped_path = quote(path.strip("/"))
        if escaped_path:
            escaped_path = "/" + escaped_path
        url = f"{self.host}{escaped_path}"
        if query:
            url = f"{url}?{urlencode(query)}"
        headers = dict(headers or DEFAULT_HEADERS, **self.auth_header)
        if self.custom_headers:
            headers = dict(headers, **self.custom_headers)
        if data is not None:
            data = json.dumps(data, separators=(",", ":"))
            headers["Content-type"] = "application/json"
        elif bytes is not None:
            data = bytes

        # Use streaming for large requests if requested
        if stream:
            return self._request_streaming(method, url, data=data, headers=headers)
        else:
            return self._request(method, url, data=data, headers=headers)

    def get(self, path, query=None):
        resp = self.request("GET", path, query=query)
        if resp.status in (200, 404):
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)

    def post(self, path, data, query=None):
        resp = self.request("POST", path, data=data, query=query)
        if resp.status in (200, 201):
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
        if resp.status in (200, 204):
            return resp
        raise UnexpectedAPIResponse(resp.status, resp.data)
