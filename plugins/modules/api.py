#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r""" """

EXAMPLES = """ """

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, attachment, client, errors, query, table, utils
from ..module_utils.change_request import PAYLOAD_FIELDS_MAPPING
from ..module_utils.utils import get_mapper


def update_resource(module, table_client, payload):
    # TODO: Implement updating the resource here
    changed, record, diff = True, None, dict(before={}, after={})
    return changed, record, diff


def create_resource(module, table_client, payload):
    new = table_client.create_record(table=module.params["resource"], payload=None, check_mode=None)
    return True, new, dict(before=None, after=new)


def delete_resource(module, table_client):
    record = table_client.get_record(module.params["resource"], module.params["data"])
    table_client.delete_record(module.params["resource"], record, module.check_mode)
    return True, None, dict(before=record, after=None)


def run(module, table_client):
    # TODO:
    #   - Build payload. Temporarily None
    #   - Define field DIRECT_PAYLOAD_FIELDS. Look at files incident.py and problem.py as an example
    #   - Look at: Module utils --> query --> parse query
    payload = None
    if module.params["action"] == "update":  # PATCH method
        return update_resource(module, table_client, payload)
    elif module.params["action"] == "create":  # POST method
        return create_resource(module, table_client, payload)
    return delete_resource(module, table_client)  # DELETE method


def main():
    arg_spec = dict(
        arguments.get_spec(
            "instance", "sys_id"
        ),
        resource=dict(
            type="str",
            required=True
        ),
        action=dict(
            type="str",
            required=True,
            choices=[
                "create",
                "update",
                "delete"
            ]
        ),
        data=dict(
            type="dict",
        )
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=arg_spec
    )

    try:
        snow_client = client.Client(**module.params["instance"])
        table_client = table.TableClient(snow_client)
        changed, record, diff = run(module, table_client)
        module.exit_json(changed=changed, record=record, diff=diff)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
