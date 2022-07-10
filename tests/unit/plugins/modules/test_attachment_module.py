# -*- coding: utf-8 -*-
# # Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.modules import attachment

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
        )
        success, result = run_main(attachment, params)

        assert success is True

    def test_fail(self, run_main):
        success, result = run_main(attachment)

        assert success is False
        #   assert "instance" in result["msg"]  ## REPLACE!


# class TestRun:
#     def test_run(self, create_module, table_client, attachment_client):
#         module = create_module(
#             params=dict(
#                 instance=dict(
#                     host="https://my.host.name", username="user", password="pass"
#                 ),
#                 sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
#                 sys_class_name="cmdb_ci",
#                 query=None,
#             )
#         )
#         table_client.list_records.return_value = [
#             dict(p=1, sys_id=1234),
#             dict(q=2, sys_id=4321),
#             dict(r=3, sys_id=1212),
#         ]
#         attachment_client.list_records.side_effect = [
#             [
#                 {
#                     "content_type": "text/plain",
#                     "file_name": "sample_file",
#                     "table_name": "change_request",
#                     "table_sys_id": 1234,
#                     "sys_id": 4444,
#                 },
#             ],
#             [],
#             [],
#         ]

#         records = configuration_item_info.run(module, table_client, attachment_client)

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






# def test_get_attachment_404(self):
#         # "msg": "Record doesn't exist or ACL restricts the record retrieval" 
#         pass

#     def test_get_attachment_unexpected_response(self):
#         # "msg": "Unexpected response..." 
#         pass

#     def test_get_attachment_wrong_auth(self):
#         # "msg": "Failed to authenticate with the instance: 401 Unauthorized" (from client.py _request())
#         pass

#     def test_get_attachment_wrong_host(self):
#         # "msg": "[Errno -2] Name or service not known" (from client.py _request())
#         pass
