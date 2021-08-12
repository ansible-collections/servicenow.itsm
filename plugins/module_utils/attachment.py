# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import hashlib
import mimetypes
import os

from . import errors


def _path(*subpaths):
    return "/".join(filter(None, ("attachment",) + subpaths))


class AttachmentClient:
    def __init__(self, client, batch_size=10000):
        # 10000 records is default batch size for ServiceNow Attachment REST API, so we also use it
        # as a default.
        self.client = client
        self.batch_size = batch_size

    def list_records(self, query=None):
        base_query = (query or {})
        base_query["sysparm_limit"] = self.batch_size

        offset = 0
        total = 1  # Dummy value that ensures loop executes at least once
        result = []

        while offset < total:
            response = self.client.get(
                _path(), query=dict(base_query, sysparm_offset=offset)
            )

            result.extend(response.json["result"])
            total = int(response.headers["X-Total-Count"])
            offset += self.batch_size

        return result

    def get_record(self, query, must_exist=False):
        records = self.list_records(query)

        if len(records) > 1:
            raise errors.ServiceNowError(
                "{0} attachments match the {1} query.".format(len(records), query)
            )

        if must_exist and not records:
            raise errors.ServiceNowError(
                "No attachments match the {0} query.".format(query)
            )

        return records[0] if records else None

    def create_record(self, metadata, data, check_mode, mime_type):
        if check_mode:
            # Approximate the result using the payload and data.
            return metadata
        return self.client.request_binary(
            "POST", _path("file"), mime_type, bin_data=data, query=(metadata or {})
        ).json["result"]

    def upload_record(self, payload, file_dict, check_mode=False):
        # "payload" is a dict with defined "table_name", "table_sys_id". This is defined by the module directly.
        #
        # "file_dict" is a dict with a mandatory key "path" and optional "name", "type" and "encryption_context".
        # These properties can be read directly from the yaml attachment list and can be set by the user.
        new_payload = payload.copy()
        new_payload["file_name"] = get_file_name(file_dict)
        file_type = get_file_type(file_dict)

        if (
            "encryption_context" in file_dict
            and file_dict["encryption_context"] is not None
        ):
            new_payload["encryption_context"] = file_dict["encryption_context"]

        data = None
        if not check_mode:
            with open(file_dict["path"], "rb") as file_obj:
                data = file_obj.read()
        return self.create_record(new_payload, data, check_mode, file_type)

    def upload_records(self, payload, file_dict_list, check_mode):
        return [
            self.upload_record(payload, file_dict, check_mode)
            for file_dict in (file_dict_list or [])
        ]

    def delete_record(self, record, check_mode, silent=False):
        if not check_mode:
            if record is None and silent:
                return {"changed": False, "msg": "Skipped. Record doesn't exist."}
            else:
                try:
                    self.client.delete(_path(record["sys_id"]))
                    return {"changed": True}
                except errors.UnexpectedAPIResponse:
                    return {"changed": False}

    def delete_attached_records(self, payload, check_mode, silent=False):
        return [
            self.delete_record(record, check_mode, silent)
            for record in self.list_records(payload)
        ]

    def is_changed(self, payload, file_dict):
        rec = self.get_record(build_query(payload, file_dict))
        if rec is not None:
            return file_hash(file_dict["path"]) != rec["hash"]
        return True

    def are_changed(self, payload, file_dict_list):
        if file_dict_list is not None:
            return [
                self.is_changed(payload, file_dict)
                for file_dict in (file_dict_list or [])
            ]
        return []

    def update_record(self, payload, file_dict, check_mode=False):
        if self.is_changed(payload, file_dict):
            self.delete_record(
                self.get_record(build_query(payload, file_dict)), check_mode, True
            )
            return dict(
                {
                    "changed": True,
                    "msg": "Changes detected, hash doesn't match remote. Remote updated.",
                },
                **self.upload_record(payload, file_dict, check_mode)
            )
        else:
            return dict(
                {"changed": False, "msg": "Skipped. Hash matches remote."},
                **self.get_record(build_query(payload, file_dict))
            )

    def update_records(self, payload, file_dict_list, check_mode=False):
        return [
            self.update_record(payload, file_dict, check_mode)
            for file_dict in (file_dict_list or [])
        ]


def get_file_name(file_dict):
    if "name" in file_dict and file_dict["name"] is not None:
        return file_dict["name"]
    return os.path.splitext(os.path.basename(file_dict["path"]))[0]


def get_file_type(file_dict):
    if "type" in file_dict and file_dict["type"] is not None:
        return file_dict["type"]
    return mimetypes.guess_type(file_dict["path"])[0]


def build_query(payload, file_dict):
    return dict(
        file_name=get_file_name(file_dict),
        content_type=get_file_type(file_dict),
        **payload
    )


def file_hash(file):
    with open(file, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()
