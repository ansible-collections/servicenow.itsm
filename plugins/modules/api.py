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

from ..module_utils import arguments, client, errors, table
from ..module_utils.api import table_name


def update_resource(module, table_client):
    record_old = table_client.get_record(table_name(module), module.params["data"])
    if record_old is None:
        return False, None, dict(before=None, after=None)
    record_new = table_client.update_record(
        table_name(module), record_old, module.params["update_data"], module.check_mode)
    return True, record_new, dict(before=record_old, after=record_new)


def create_resource(module, table_client):
    # At the moment, creating a resource is not idempotent (meaning: If a record with such data as specified in
    # module.params["data"] already exists, such resource will get created once again).
    new = table_client.create_record(table=table_name(module), payload=module.params["data"], check_mode=None)
    return True, new, dict(before=None, after=new)


def delete_resource(module, table_client):
    record = table_client.get_record(table_name(module), module.params["data"])
    if record is None:
        return False, None, dict(before=None, after=None)
    table_client.delete_record(table_name(module), record, module.check_mode)
    return True, None, dict(before=record, after=None)


def run(module, table_client):
    if module.params["action"] == "patch":  # PATCH method
        return update_resource(module, table_client)
    elif module.params["action"] == "post":  # POST method
        return create_resource(module, table_client)
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
                "post",
                "patch",
                "delete"
            ]
        ),
        data=dict(
            type="dict",
        ),
        update_data=dict(
            type="dict"
        ),
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
