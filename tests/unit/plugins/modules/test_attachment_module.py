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
    def test_minimal_set_of_params(self, run_main):
        params = dict(
            instance=dict(
                host="https://my.host.name", username="user", password="pass"
            ),
        )
        success, result = run_main(attachment, params)

        assert success is True

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

        assert success is False  # THIS DOESNT PASS, success is True - WHY?
        #   assert "instance" in result["msg"]  ## REPLACE!


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
            {"x-attachment-metadata": "{  \"size_bytes\" : \"106879\"}"},
        )

        mocker.patch("ansible_collections.servicenow.itsm.plugins.modules.attachment.secure_hash_s").return_value = 17
        mocker.patch("ansible_collections.servicenow.itsm.plugins.modules.attachment.secure_hash").return_value = 17
        mocker.patch("ansible_collections.servicenow.itsm.plugins.modules.attachment.time.time").return_value = 0
        # we don't need this anymore, but still, how can I patch json.loads?
        #mocker.patch("ansible_collections.servicenow.itsm.plugins.modules.attachment.json.loads").return_value = 1000

        records = attachment.run(module, attachment_client)

        assert records == {
            "elapsed": "0.0",
            "checksum_src": 17,
            "checksum_dest": 17,
            "size": "106879",
            "status_code": 200,
            "msg": "OK",
        }

#         table_client.list_records.assert_called_once_with(
#             "cmdb_ci", dict(sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3")
#         )
#         attachment_client.list_records.assert_any_call(
#             {"table_name": "cmdb_ci", "table_sys_id": 1234}
#         )
#         attachment_client.list_records.assert_any_call(
#             {"table_name": "cmdb_ci", "table_sys_id": 4321}
#         )
#         attachment_client.list_records.assert_any_call(
#             {"table_name": "cmdb_ci", "table_sys_id": 1212}
#         )
#         assert attachment_client.list_records.call_count == 3
#         assert records == [
#             dict(
#                 p=1,
#                 sys_id=1234,
#                 attachments=[
#                     {
#                         "content_type": "text/plain",
#                         "file_name": "sample_file",
#                         "table_name": "change_request",
#                         "table_sys_id": 1234,
#                         "sys_id": 4444,
#                     },
#                 ],
#             ),
#             dict(q=2, sys_id=4321, attachments=[]),
#             dict(r=3, sys_id=1212, attachments=[]),
#         ]

    def test_run_404(self, create_module, attachment_client):
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
            {"error": {"detail": "Record doesn't exist or ACL restricts the record retrieval"}},
            {"headers": "headers"},
        )

        with pytest.raises(errors.ServiceNowError) as exc:
            attachment.run(module, attachment_client)
        # need to patch response.json["error"]["detail"]
        assert str(exc.value).find("Status code: 404, Details: Record doesn't exist") != -1



#     def test_get_attachment_unexpected_response(self):
#         # "msg": "Unexpected response..." 
#         pass

#     def test_get_attachment_wrong_auth(self):
#         # "msg": "Failed to authenticate with the instance: 401 Unauthorized" (from client.py _request())
#         pass

#     def test_get_attachment_wrong_host(self):
#         # "msg": "[Errno -2] Name or service not known" (from client.py _request())
#         pass
