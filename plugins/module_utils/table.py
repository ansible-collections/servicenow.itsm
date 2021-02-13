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


def _flatten(data):
    result = {}
    for k, v in data.items():
        if isinstance(v, dict) and "link" in v:
            result[k] = v["value"]
        else:
            result[k] = v
    return result


def list_records(client, table, query=None):
    return [_flatten(r) for r in client.get(_path(table), query=query).json["result"]]


def get_record(client, table, query, must_exist=False):
    records = list_records(client, table, query)

    if len(records) > 1:
        raise errors.ServiceNowError(
            "{0} {1} records match the {2} query.".format(len(records), table, query)
        )

    if must_exist and not records:
        raise errors.ServiceNowError(
            "No {0} records match the {1} query.".format(table, query)
        )

    return records[0] if records else None


def create_record(client, table, payload, check_mode):
    if check_mode:
        # Approximate the result using the payload.
        return payload
    return _flatten(client.post(_path(table), payload).json["result"])


def update_record(client, table, record, payload, check_mode):
    if check_mode:
        # Approximate the result by manually patching the existing state.
        return dict(record, **payload)
    return _flatten(
        client.patch(_path(table, record["sys_id"]), payload).json["result"]
    )


def delete_record(client, table, record, check_mode):
    if not check_mode:
        client.delete(_path(table, record["sys_id"]))
