# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import mimetypes
import os

from . import errors


def _path(*subpaths):
    return "/".join(filter(None, ("attachment",) + subpaths))


def _query(original=None):
    # Flatten the response (skip embedded links to resources)
    return dict(original or {}, sysparm_exclude_reference_link="true")


class AttachmentClient:
    def __init__(self, client, batch_size=10000):
        # 10000 records is default batch size for ServiceNow Attachment REST API, so we also use it
        # as a default.
        self.client = client
        self.batch_size = batch_size

    def list_records(self, query=None, sys_id=None, file=True):
        base_query = _query(query)
        base_query["sysparm_limit"] = self.batch_size

        offset = 0
        total = 1  # Dummy value that ensures loop executes at least once
        result = []

        while offset < total:
            response = self.client.get(
                _path(sys_id, "file" if file else None),
                query=dict(base_query, sysparm_offset=offset),
            )

            result.extend(response.json["result"])
            total = int(response.headers["X-Total-Count"])
            offset += self.batch_size

        return result

    def get_record(self, query, sys_id=None, file=True, must_exist=False):
        records = self.list_records(query, sys_id, file)

        if len(records) > 1:
            raise errors.ServiceNowError(
                "{0} attachments match the {1} query.".format(len(records), query)
            )

        if must_exist and not records:
            raise errors.ServiceNowError(
                "No attachments match the {0} query.".format(query)
            )

        return records[0] if records else None

    def create_record(self, payload, data, check_mode, mime_type=None):
        if check_mode:
            # Approximate the result using the payload and data. TODO
            return dict(payload, data=data)
        return self.client.request_binary(
            "POST", _path("file"), data, _query(payload), mime_type
        ).json["result"]

    def upload_record(self, payload, file_dict, check_mode):
        # "payload" is a dict with defined "table_name", "table_sys_id". This is defined by the module directly.
        #
        # "file_dict" is a dict with a mandatory key "path" and optional "name", "type" and "encryption_context".
        # These properties can be read directly from the yaml attachment list and can be set by the user.
        if "name" in file_dict:
            payload["file_name"] = file_dict["name"]
        else:
            payload["file_name"] = os.path.splitext(
                os.path.basename(file_dict["path"])
            )[0]

        if "type" in file_dict:
            file_type = file_dict["type"]
        else:
            file_type = mimetypes.guess_type(payload.file_name)

        if "encryption_context" in file_dict:
            payload["encryption_context"] = file_dict["encryption_context"]

        data = open(file_dict["path"], "rb")
        self.create_record(payload, data, check_mode, file_type)

    def delete_record(self, record, check_mode):
        if not check_mode:
            self.client.delete(_path(record["sys_id"]))
