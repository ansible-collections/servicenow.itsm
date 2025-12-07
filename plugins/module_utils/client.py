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

from .errors import (
    AuthError,
    ServiceNowError,
    UnexpectedAPIResponse,
    ApiCommunicationError,
)

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = dict(Accept="application/json")


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
        self._access_count = 0  # Track total accesses for cleanup

    def clear_cache(self):
        """Clear cached JSON data to free memory"""
        self._json = None
        self._cache_entries = 0
        self._access_count = 0

    @property
    def json(self):
        if self._json is None:
            try:
                self._json = json.loads(self.data, object_hook=self.json_decoder_hook)
                self._cache_entries += 1
                self._access_count += 1

                # Auto-cleanup if cache gets too large
                if self._cache_entries > self._max_cache_size:
                    logger.debug("JSON cache size exceeded, clearing cache")
                    self.clear_cache()
            except ValueError as exc:
                raise ServiceNowError(
                    "Received invalid JSON response: {0}".format(self.data)
                ) from exc
        else:
            self._access_count += 1

        return self._json

    def cleanup_if_unused(self, max_access_count=10):
        """Clean up cache if it hasn't been accessed recently"""
        if self._access_count > max_access_count and self._json is not None:
            logger.debug("Clearing unused response cache")
            self.clear_cache()


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
                "Invalid instance host value: '{0}'. "
                "Value must start with 'https://' or 'http://'".format(host)
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
        # self.timeout = timeout
        self.timeout = 300
        self.validate_certs = validate_certs
        self.json_decoder_hook = json_decoder_hook
        self.connection_timeout = connection_timeout
        self.max_retries = max_retries

        self._auth_header = None
        self._client = Request()
        self._connection_created = time.time()
        self._request_count = 0
        self._response_cache = []  # Track response objects for cleanup
        self._max_response_cache = 50  # Maximum cached responses

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
            # Clear all cached responses
            for response in self._response_cache:
                if hasattr(response, "clear_cache"):
                    response.clear_cache()
            self._response_cache.clear()

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

        # Clear response cache during connection refresh
        for response in self._response_cache:
            if hasattr(response, "clear_cache"):
                response.clear_cache()
        self._response_cache.clear()

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

    def cleanup_unused_responses(self):
        """Clean up unused response objects to free memory"""
        cleaned_count = 0
        for response in self._response_cache[:]:
            if hasattr(response, "cleanup_if_unused"):
                response.cleanup_if_unused()
                if response._json is None:  # Cache was cleared
                    self._response_cache.remove(response)
                    cleaned_count += 1

        if cleaned_count > 0:
            logger.debug("Cleaned up %d unused response objects", cleaned_count)

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
        return dict(Authorization=basic_auth_header(self.username, self.password))

    def _login_token(self, token, is_api_key=False):
        if is_api_key:
            return {"x-sn-apikey": token}
        else:
            return {"Authorization": "Bearer {0}".format(token)}

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
            "{0}/oauth_token.do".format(self.host),
            data=auth_data,
            headers=dict(Accept="application/json"),
        )
        if resp.status != 200:
            raise UnexpectedAPIResponse(resp.status, resp.data)

        access_token = resp.json["access_token"]
        return self._login_token(access_token, is_api_key=False)

    def _request(self, method, path, data=None, headers=None):
        # Check if connection should be refreshed
        if self._should_refresh_connection():
            self._refresh_connection()

        request_kwargs = {
            "data": data,
            "headers": headers,
            "timeout": self.timeout,
            "validate_certs": self.validate_certs,
            "client_cert": self.client_certificate_file,
            "client_key": self.client_key_file,
        }
        request_error_handler = ClientRequestErrorHandler(method, path, request_kwargs)
        for attempt in range(self.max_retries + 1):
            try:
                raw_resp = self._client.open(method, path, **request_kwargs)
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
            except Exception as e:
                # An exception occurred, and we need to parse it to add additional context
                # for the user. Some errors may be retryable, in which case the loop will be
                # if the retry limit has not been reached.
                request_error_handler.handle_request_error(
                    exception=e, retry_is_allowed=(attempt < self.max_retries)
                )
            else:
                # No exceptions occurred, so the request was successful
                # and the loop can be exited
                break

        # Increment request count for connection management
        self._request_count += 1

        # Create response and track it for cleanup
        response = Response(
            raw_resp.status, raw_resp.read(), raw_resp.headers, self.json_decoder_hook
        )

        # Add to response cache and cleanup if needed
        self._response_cache.append(response)
        if len(self._response_cache) > self._max_response_cache:
            # Remove oldest responses and clear their cache
            old_response = self._response_cache.pop(0)
            if hasattr(old_response, "clear_cache"):
                old_response.clear_cache()

        return response

    def request(self, method, path, query=None, data=None, headers=None, bytes=None):
        # Make sure we only have one kind of payload
        if data is not None and bytes is not None:
            raise AssertionError(
                "Cannot have JSON and binary payload in a single request."
            )

        escaped_path = quote(path.strip("/"))
        if escaped_path:
            escaped_path = "/" + escaped_path
        url = "{0}{1}".format(self.host, escaped_path)
        if query:
            url = "{0}?{1}".format(url, urlencode(query))
        headers = dict(headers or DEFAULT_HEADERS, **self.auth_header)
        if self.custom_headers:
            headers = dict(headers, **self.custom_headers)
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


class ClientRequestErrorHandler:
    """
    Handles exceptions that occur during HTTP requests to the ServiceNow instance.

    This class centralizes error handling logic for network and SSL-related errors,
    providing consistent error messages and determining whether errors are retryable.
    It is used by the Client class's retry mechanism to handle transient network
    issues such as SSL handshake timeouts.

    Args:
        method (str): The HTTP method used for the request (e.g., 'GET', 'POST').
        path (str): The URL path that was requested.
        request_kwargs (dict): Dictionary containing request parameters such as
            timeout, validate_certs, client_cert, etc. Used for error context.
    """

    def __init__(self, method, path, request_kwargs):
        self.method = method
        self.path = path
        self.request_kwargs = request_kwargs

    def handle_request_error(self, exception, retry_is_allowed=False):
        """
        Route exception to the appropriate handler based on exception type.

        This method categorizes exceptions and delegates to specific functions.
        For retryable errors (like SSL handshake timeouts), if retry_is_allowed
        is True, the method returns None to allow the caller's loop to continue.
        Otherwise, it raises an appropriate exception.

        Args:
            exception (Exception): The exception that occurred during the request.
            retry_is_allowed (bool): Whether retries are still allowed. If True
                and the error is retryable (e.g., TLS handshake timeout), the
                method returns None instead of raising, allowing the retry loop
                to continue. Defaults to False.

        Raises:
            ServiceNowError or subclass thereof: For non-retryable errors.

        Returns:
            None: When retry_is_allowed is True and the error is retryable
                (specifically TLS handshake timeouts). This signals the caller
                to retry the request.
        """
        if isinstance(exception, URLError):
            self._handle_request_urlerror(exception, retry_is_allowed)

        elif isinstance(exception, ssl.SSLError):
            self._handle_ssl_error(exception)

        else:
            self._raise_generic_communication_error(exception)

    def _raise_generic_communication_error(self, exception):
        """
        Raise a generic ApiCommunicationError for unexpected exceptions.
        """
        raise ApiCommunicationError(
            exception=exception,
            message="Unexpected error communicating with ServiceNow instance: %s"
            % exception,
            method=self.method,
            path=self.path,
            **self.request_kwargs,
        )

    def _handle_request_urlerror(self, exception, retry_is_allowed=False):
        """
        Handle URLError exceptions, including timeouts and handshake failures.

        This method handles various URL-related errors:
          - General request timeouts: Always raises an error with timeout info.
          - TLS handshake timeouts: Returns None if retry_is_allowed is True,
            otherwise raises an error. This allows the retry mechanism to handle
            intermittent SSL handshake issues.
          - Other URLErrors: Raises a generic communication error.

        Args:
            exception (URLError): The URLError that occurred.
            retry_is_allowed (bool): Whether retries are still allowed. If True
                and the error is a TLS handshake timeout, returns None to allow
                retry. Defaults to False.

        Raises:
            ApiCommunicationError: For non-retryable errors or when retries are
                exhausted. Includes timeout settings for timeout errors.

        Returns:
            None: When retry_is_allowed is True and the error is a TLS handshake
                timeout. This allows the retry loop to continue.
        """
        try:
            reason = str(exception.reason)
        except AttributeError:
            reason = None

        if reason == "timed out":
            raise ApiCommunicationError(
                exception=exception,
                message="The request to the ServiceNow instance timed out.",
                method=self.method,
                path=self.path,
                timeout_setting=self.request_kwargs.get("timeout", "unknown"),
            )

        if reason and reason.endswith("The handshake operation timed out"):
            if retry_is_allowed:
                return

            raise ApiCommunicationError(
                exception=exception,
                message="Failed to communicate with instance. The TLS handshake operation timed out.",
                method=self.method,
                path=self.path,
            )

        self._raise_generic_communication_error(exception)

    def _handle_ssl_error(self, exception):
        """
        Handle SSL/TLS related errors.

        This method provides specific error messages for SSL errors, particularly
        when client certificates are involved. SSL handshake timeouts are
        typically handled by _handle_request_urlerror when they manifest as
        URLErrors, but direct ssl.SSLError exceptions are handled here.

        Args:
            exception (ssl.SSLError): The SSL error that occurred.

        Raises:
            ServiceNowError: When client certificates are configured, with a
                message suggesting certificate/key file issues.
            ApiCommunicationError: For other SSL errors, with generic error
                information.
        """
        if self.request_kwargs.get("client_cert"):
            raise ServiceNowError(
                "Failed to communicate with instance due to SSL error, likely related to the client certificate or key. "
                "Ensure the files are accessible on the Ansible host and in the correct format (see module documentation)."
            )

        self._raise_generic_communication_error(exception)
