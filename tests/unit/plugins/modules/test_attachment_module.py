# -*- coding: utf-8 -*-
# # Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.modules import attachment
from ansible_collections.servicenow.itsm.plugins.module_utils import errors
from ansible_collections.servicenow.itsm.plugins.module_utils.client import Response
from ansible.module_utils._text import to_bytes, to_text

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestMain:
    # minimal_set_of_params == test_all_params
    def test_all_params(self, run_main):
        params = dict(
            instance=dict(
                host="https://my.host.name", username="user", password="pass"
            ),
            sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
            dest="tmp",
        )
        success, result = run_main(attachment, params)

        assert success is True

    def test_fail(self, run_main):
        success, result = run_main(attachment)

        assert success is False
        assert "missing required arguments" in result["msg"]

    def test_missing_dest(self, run_main):
        params = dict(
            instance=dict(
                host="https://my.host.name", username="user", password="pass"
            ),
            sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
        )
        success, result = run_main(attachment, params)

        assert success is False
        assert "missing required arguments: dest" in result["msg"]

    def test_missing_sys_id(self, run_main):
        params = dict(
            instance=dict(
                host="https://my.host.name", username="user", password="pass"
            ),
            dest="tmp",
        )
        success, result = run_main(attachment, params)

        assert success is False
        assert "missing required arguments: sys_id" in result["msg"]


class TestRun:
    def test_run(self, create_module, attachment_client, mocker):
        module = create_module(
            params=dict(
                instance=dict(
                    host="https://my.host.name", username="user", password="pass"
                ),
                sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                dest="tmp",
            )
        )
        attachment_client.get_attachment.return_value = Response(
            200,
            to_bytes("binary_data"),
            {"x-attachment-metadata": '{  "size_bytes" : "1000"}'},
        )

        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.modules.attachment.secure_hash_s"
        ).return_value = "6e642bb8dd5c2e027bf21dd923337cbb4214f827"
        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.modules.attachment.secure_hash"
        ).return_value = "6e642bb8dd5c2e027bf21dd923337cbb4214f828"
        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.modules.attachment.time.time"
        ).return_value = 0
        # mocker.patch(
        #     "ansible_collections.servicenow.itsm.plugins.modules.attachment.json.loads"
        # ).return_value = {"size_bytes": "1000"}

        records = attachment.run(module, attachment_client)

        assert records == {
            "elapsed": 0.0,
            "checksum_src": "6e642bb8dd5c2e027bf21dd923337cbb4214f827",
            "checksum_dest": "6e642bb8dd5c2e027bf21dd923337cbb4214f828",
            "size": 1000,
            "status_code": 200,
            "msg": "OK",
        }
        attachment_client.get_attachment.assert_called_once_with(
            "01a9ec0d3790200044e0bfc8bcbe5dc3"
        )
        attachment_client.save_attachment.assert_called_once_with(
            to_bytes("binary_data"), "tmp"
        )

    def test_run_404(self, create_module, attachment_client, mocker):
        module = create_module(
            params=dict(
                instance=dict(
                    host="https://my.host.name", username="user", password="pass"
                ),
                sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                dest="tmp",
            )
        )
        attachment_client.get_attachment.return_value = Response(
            404,
            to_bytes(
                '{"error":{"message":"No Record found","detail":"Record doesnt exist"},"status":"failure"}'
            ),
            {"headers": "headers"},
        )
        # mocker.patch(
        #     "ansible_collections.servicenow.itsm.plugins.modules.attachment.json.loads"
        # ).return_value = {"error": {"detail": "Record doesnt exist"}}
        # could also patch response.json["error"]["detail"], but how can I do that?

        with pytest.raises(errors.ServiceNowError) as exc:
            attachment.run(module, attachment_client)

        assert "Status code: 404, Details: Record doesnt exist" in str(exc.value)
