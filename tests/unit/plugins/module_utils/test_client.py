# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError

from ansible_collections.servicenow.itsm.plugins.module_utils import client, errors

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestResponseInit:
    @pytest.mark.parametrize(
        "raw_headers,expected_headers",
        [
            (None, {}),
            ([], {}),
            ([("a", "aVal"), ("b", "bVal")], {"a": "aVal", "b": "bVal"}),
        ],
    )
    def test_headers(self, raw_headers, expected_headers):
        resp = client.Response(200, "{}", headers=raw_headers)
        assert resp.headers == expected_headers

    def test_valid_json(self):
        resp = client.Response(
            200,
            '{"a": ["b", "c"], "d": 1}',
            headers=[("Content-type", "applcation/json")],
        )

        assert resp.status == 200
        assert resp.headers == {"Content-type": "applcation/json"}
        assert resp.data == '{"a": ["b", "c"], "d": 1}'
        assert resp.json == {"a": ["b", "c"], "d": 1}

    def test_invalid_json(self):
        resp = client.Response(404, "Not Found")

        assert resp.status == 404
        assert resp.headers == {}
        assert resp.data == "Not Found"
        with pytest.raises(errors.ServiceNowError, match="invalid JSON"):
            resp.json

    def test_json_is_cached(self, mocker):
        json_mock = mocker.patch.object(client, "json")
        resp = client.Response(
            200,
            '{"a": ["b", "c"], "d": 1}',
            headers=[("Content-type", "applcation/json")],
        )
        resp.json
        resp.json

        assert json_mock.loads.call_count == 1


class TestClientAuthHeader:
    def test_basic_auth(self):
        c = client.Client("instance.com", "user", "pass")
        assert c.auth_header == {"Authorization": b"Basic dXNlcjpwYXNz"}

    def test_oauth(self, mocker):
        resp_mock = mocker.MagicMock(status=200)
        resp_mock.read.return_value = '{"access_token": "token"}'
        request_mock = mocker.patch.object(client, "Request").return_value
        request_mock.open.return_value = resp_mock

        c = client.Client(
            "instance.com", "user", "pass", client_id="id", client_secret="secret"
        )

        assert c.auth_header == {"Authorization": "Bearer token"}

    def test_oauth_failure(self, mocker):
        request_mock = mocker.patch.object(client, "Request").return_value
        request_mock.open.side_effect = HTTPError("", 403, "Forbidden", {}, None)

        c = client.Client(
            "instance.com", "user", "pass", client_id="id", client_secret="secret"
        )
        with pytest.raises(errors.UnexpectedAPIResponse, match="Forbidden"):
            c.auth_header

    def test_header_is_cached(self, mocker):
        raw_resp_mock = mocker.MagicMock(status=200)
        raw_resp_mock.read.return_value = '{"access_token": "token"}'
        request_mock = mocker.patch.object(client, "Request").return_value
        request_mock.open.return_value = raw_resp_mock

        c = client.Client(
            "instance.com", "user", "pass", client_id="id", client_secret="secret"
        )
        c.auth_header
        c.auth_header

        assert request_mock.open.call_count == 1


class TestClientRequest:
    def test_request_without_data_success(self, mocker):
        c = client.Client("instance.com", "user", "pass")
        mock_response = client.Response(
            200, '{"returned": "data"}', headers=[("Content-type", "application/json")]
        )
        request_mock = mocker.patch.object(c, "_request")
        request_mock.return_value = mock_response

        resp = c.request("GET", "some/path")

        request_mock.assert_called_once_with(
            "GET",
            "instance.com/api/now/some/path",
            data=None,
            headers=dict(Accept="application/json", **c.auth_header),
        )
        assert resp == mock_response

    def test_request_with_data_success(self, mocker):
        c = client.Client("instance.com", "user", "pass")
        mock_response = client.Response(
            200, '{"returned": "data"}', headers=[("Content-type", "application/json")]
        )
        request_mock = mocker.patch.object(c, "_request")
        request_mock.return_value = mock_response

        resp = c.request("PUT", "some/path", {"some": "data"})

        request_mock.assert_called_once_with(
            "PUT",
            "instance.com/api/now/some/path",
            data='{"some":"data"}',
            headers={
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": c.auth_header["Authorization"],
            },
        )
        assert resp == mock_response

    def test_auth_error(self, mocker):
        request_mock = mocker.patch.object(client, "Request").return_value
        request_mock.open.side_effect = HTTPError("", 401, "Unauthorized", {}, None)

        c = client.Client("instance.com", "user", "pass")
        with pytest.raises(errors.AuthError):
            c.request("GET", "some/path")

    def test_http_error(self, mocker):
        request_mock = mocker.patch.object(client, "Request").return_value
        request_mock.open.side_effect = HTTPError("", 404, "Not Found", {}, None)

        c = client.Client("instance.com", "user", "pass")
        resp = c.request("GET", "some/path")

        assert resp.status == 404
        assert resp.data == "Not Found"
        assert resp.headers == {}

    def test_url_error(self, mocker):
        request_mock = mocker.patch.object(client, "Request").return_value
        request_mock.open.side_effect = URLError("some error")

        c = client.Client("instance.com", "user", "pass")

        with pytest.raises(errors.ServiceNowError, match="some error"):
            c.request("GET", "some/path")

    def test_path_escaping(self, mocker):
        request_mock = mocker.patch.object(client, "Request").return_value
        raw_request = mocker.MagicMock(status=200)
        raw_request.read.return_value = "{}"

        c = client.Client("instance.com", "user", "pass")
        c.request("GET", "some path")

        request_mock.open.assert_called_once()
        path_arg = request_mock.open.call_args.args[1]
        assert path_arg == "instance.com/api/now/some%20path"


class TestClientGet:
    def test_ok(self, mocker):
        c = client.Client("instance.com", "user", "pass")
        mock_response = client.Response(200, '{"incident": 1}', None)
        request_mock = mocker.patch.object(c, "request")
        request_mock.return_value = mock_response

        resp = c.get("table/incident/1")

        assert resp == mock_response
        assert resp.json == {"incident": 1}

    def test_ok_missing(self, mocker):
        c = client.Client("instance.com", "user", "pass")
        mock_response = client.Response(404, "Not Found", None)
        request_mock = mocker.patch.object(c, "request")
        request_mock.return_value = mock_response

        resp = c.get("table/incident/1")

        assert resp == mock_response

    def test_error(self, mocker):
        c = client.Client("instance.com", "user", "pass")
        request_mock = mocker.patch.object(c, "request")
        request_mock.return_value = client.Response(403, "forbidden")

        with pytest.raises(errors.UnexpectedAPIResponse, match="forbidden"):
            c.get("table/incident/1")


class TestClientPost:
    def test_ok(self, mocker):
        c = client.Client("instance.com", "user", "pass")
        mock_response = client.Response(201, '{"incident": 1}')
        request_mock = mocker.patch.object(c, "request")
        request_mock.return_value = mock_response

        resp = c.post("table/incident", {"some": "data"})

        assert resp == mock_response
        assert resp.json == {"incident": 1}

    def test_error(self, mocker):
        c = client.Client("instance.com", "user", "pass")
        request_mock = mocker.patch.object(c, "request")
        request_mock.return_value = client.Response(400, "bad request")

        with pytest.raises(errors.UnexpectedAPIResponse, match="bad request"):
            c.post("table/incident", {"some": "data"})


class TestClientPut:
    def test_ok(self, mocker):
        c = client.Client("instance.com", "user", "pass")
        mock_response = client.Response(200, '{"incident": 1}')
        request_mock = mocker.patch.object(c, "request")
        request_mock.return_value = mock_response

        resp = c.put("table/incident/1", {"some": "data"})

        assert resp == mock_response
        assert resp.json == {"incident": 1}

    def test_error(self, mocker):
        c = client.Client("instance.com", "user", "pass")
        request_mock = mocker.patch.object(c, "request")
        request_mock.return_value = client.Response(400, "bad request")

        with pytest.raises(errors.UnexpectedAPIResponse, match="bad request"):
            c.put("table/incident/1", {"some": "data"})


class TestClientDelete:
    def test_ok(self, mocker):
        c = client.Client("instance.com", "user", "pass")
        request_mock = mocker.patch.object(c, "request")
        request_mock.return_value = client.Response(204, {})

        c.delete("table/resource/1")

    def test_error(self, mocker):
        c = client.Client("instance.com", "user", "pass")
        request_mock = mocker.patch.object(c, "request")
        request_mock.return_value = client.Response(404, "not found")

        with pytest.raises(errors.UnexpectedAPIResponse, match="not found"):
            c.delete("table/resource/1")
