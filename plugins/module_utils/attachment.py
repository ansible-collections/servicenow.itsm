# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import collections
import mimetypes
import os

from . import errors


def _path(*subpaths):
    return "/".join(("attachment",) + subpaths)


class AttachmentClient:
    def __init__(self, client, batch_size=10000):
        # 10000 records is default batch size for ServiceNow Attachment REST API, so we also use it
        # as a default.
        self.client = client
        self.batch_size = batch_size

    def list_records(self, query=None):
        base_query = dict(query or {}, sysparm_limit=self.batch_size)

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

    def create_record(self, query, data, check_mode, mime_type):
        if check_mode:
            return query
        return self.client.request(
            "POST",
            _path("file"),
            query=(query or {}),
            headers={"Accept": "application/json", "Content-type": mime_type},
            bytes=data,
        ).json["result"]

    def upload_record(self, table, table_sys_id, metadata, check_mode=False):
        # Table and table_sys_id parameters uniquely identify the record we will attach a file to.
        query = dict(
            table_name=table,
            table_sys_id=table_sys_id,
            file_name=metadata["name"],
            content_type=metadata["type"],
            hash=metadata["hash"],
        )
        try:
            with open(metadata["path"], "rb") as file_obj:
                data = file_obj.read()
        except (IOError, OSError):
            raise errors.ServiceNowError("Cannot open {0}".format(metadata["path"]))
        return self.create_record(query, data, check_mode, query["content_type"])

    def upload_records(self, table, table_sys_id, metadata_dict, check_mode):
        return [
            self.upload_record(
                table, table_sys_id, dict(metadata, name=name), check_mode
            )
            for name, metadata in metadata_dict.items()
        ]

    def delete_record(self, record, check_mode):
        if not check_mode:
            self.client.delete(_path(record["sys_id"]))

    def delete_attached_records(self, table, table_sys_id, check_mode):
        for record in self.list_records(
            dict(table_name=table, table_sys_id=table_sys_id)
        ):
            self.delete_record(record, check_mode)

    def update_records(
        self, table, table_sys_id, metadata_dict, records, check_mode=False
    ):
        mapped_records = dict((r["file_name"], r) for r in records)

        for name, metadata in metadata_dict.items():
            record = mapped_records.get(name, None)
            if (record or {}).get("hash") != metadata["hash"]:
                if record is not None:
                    self.delete_record(record, check_mode)
                mapped_records[name] = self.upload_record(
                    table, table_sys_id, dict(metadata, name=name), check_mode
                )

        return list(mapped_records.values())


def transform_metadata_list(metadata_list, hashing_method):
    metadata_dict = dict()
    dups = collections.defaultdict(list)

    for metadata in metadata_list or []:
        name = get_file_name(metadata)
        dups[name].append(metadata["path"])
        metadata_dict[name] = {
            "path": metadata["path"],
            "type": get_file_type(metadata),
            "hash": hashing_method(metadata["path"]),
        }

    dup_sets = ["({0})".format(", ".join(v)) for v in dups.values() if len(v) > 1]
    if dup_sets:
        raise errors.ServiceNowError(
            "Found the following duplicates: {0}".format(" ".join(dup_sets))
        )
    return metadata_dict


def get_file_name(metadata):
    if "name" in metadata and metadata["name"] is not None:
        return metadata["name"]
    return os.path.splitext(os.path.basename(metadata["path"]))[0]


def get_file_type(metadata):
    if "type" in metadata and metadata["type"] is not None:
        return metadata["type"]
    return mimetypes.guess_type(metadata["path"])[0]


def build_query(table, table_sys_id, metadata):
    return dict(
        file_name=get_file_name(metadata),
        content_type=get_file_type(metadata),
        table_name=table,
        table_sys_id=table_sys_id,
    )


def are_changed(records, metadata_dict):
    mapped_records = dict((r["file_name"], r) for r in records)
    return [
        metadata["hash"] != mapped_records.get(name, {}).get("hash")
        for name, metadata in metadata_dict.items()
    ]
