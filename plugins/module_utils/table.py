# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from . import errors


def _path(table, *subpaths):
    return "/".join(("table", table) + subpaths)


def _query(original=None):
    # Flatten the response (skip embedded links to resources)
    return dict(original or {}, sysparm_exclude_reference_link="true")


class TableClient:
    def __init__(self, client):
        self.client = client

    def list_records(self, table, query=None):
        return self.client.get(_path(table), query=_query(query)).json["result"]

    def get_record(self, table, query, must_exist=False):
        records = self.list_records(table, query)

        if len(records) > 1:
            raise errors.ServiceNowError(
                "{0} {1} records match the {2} query.".format(
                    len(records), table, query
                )
            )

        if must_exist and not records:
            raise errors.ServiceNowError(
                "No {0} records match the {1} query.".format(table, query)
            )

        return records[0] if records else None

    def create_record(self, table, payload, check_mode):
        if check_mode:
            # Approximate the result using the payload.
            return payload

        return self.client.post(_path(table), payload, query=_query()).json["result"]

    def update_record(self, table, record, payload, check_mode):
        if check_mode:
            # Approximate the result by manually patching the existing state.
            return dict(record, **payload)

        return self.client.patch(
            _path(table, record["sys_id"]), payload, query=_query()
        ).json["result"]

    def delete_record(self, table, record, check_mode):
        if not check_mode:
            self.client.delete(_path(table, record["sys_id"]))
