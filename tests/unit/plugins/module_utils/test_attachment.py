# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.module_utils import errors, attachment
from ansible_collections.servicenow.itsm.plugins.module_utils.client import Response

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestAttachmentCreateRecords:
    def test_normal_mode(self, client):
        client.request_binary.return_value = Response(
            201, '{"result": {"a": 3, "b": "sys_id"}}'
        )
        a = attachment.AttachmentClient(client)

        payload = {
            "table_name": "change_request",
            "table_sys_id": "368a41361b61301029dcece4604bcba0",
        }
        file_dict = [
            {
                "path": "targets/attachment/res/sample_file.txt",
                "name": None,
                "type": None,
            }
        ]

        print(os.getcwd())
        os.chdir("tests/integration/")
        print(os.getcwd())
        record = a.upload_records(payload, file_dict, False)

        assert True  # TODO, temporary value
