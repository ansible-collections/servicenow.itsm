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
from ..module_utils.api import table_name, get_query_by_sys_id, ACTION_POST, ACTION_PATCH, ACTION_DELETE, FIELD_SYS_ID


def update_resource(module, table_client):
    query = get_query_by_sys_id(module)
    # raise errors.ServiceNowError(module.params[FIELD_SYS_ID])
    record_old = table_client.get_record(table_name(module), query)
    if record_old is None:
        return False, None, dict(before=None, after=None)
    record_new = table_client.update_record(
        table_name(module), record_old, module.params["data"], module.check_mode)
    return True, record_new, dict(before=record_old, after=record_new)


def create_resource(module, table_client):
    # At the moment, creating a resource is not idempotent (meaning: If a record with such data as specified in
    # module.params["data"] already exists, such resource will get created once again).
    new = table_client.create_record(
        table=table_name(module), payload=module.params["data"], check_mode=module.check_mode)
    return True, new, dict(before=None, after=new)


def delete_resource(module, table_client):
    query = get_query_by_sys_id(module)
    record = table_client.get_record(table_name(module), query)
    if record is None:
        return False, None, dict(before=None, after=None)
    table_client.delete_record(table_name(module), record, module.check_mode)
    return True, None, dict(before=record, after=None)


def run(module, table_client):
    action = module.params['action']
    if (action == ACTION_PATCH or action == ACTION_DELETE) and module.params[FIELD_SYS_ID] is None:
        raise errors.ServiceNowError('For actions patch and delete sys_id needs to be specified.')
    if action == ACTION_PATCH:  # PATCH method
        return update_resource(module, table_client)
    elif action == ACTION_POST:  # POST method
        return create_resource(module, table_client)
    return delete_resource(module, table_client)  # DELETE method


def main():
    arg_spec = dict(
        arguments.get_spec(
            "instance",
            "sys_id"  # necessary for deleting and patching a resource, not relevant if creating a resource
        ),
        resource=dict(
            type="str",
            required=True
        ),
        action=dict(
            type="str",
            required=True,
            choices=[
                ACTION_POST,  # create
                ACTION_PATCH,  # update
                ACTION_DELETE  # delete
            ]
        ),
        data=dict(
            type="dict",
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
