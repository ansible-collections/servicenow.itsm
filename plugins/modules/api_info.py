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

from ..module_utils import arguments, client, errors, table, utils
from ..module_utils.api import (
    transform_query_to_servicenow_query, POSSIBLE_FILTER_PARAMETERS, table_name, FIELD_COLUMNS_NAME, FIELD_QUERY_NAME
)


def run(module, table_client):
    if FIELD_COLUMNS_NAME in module.params:
        module.params[FIELD_COLUMNS_NAME] = ",".join([field.lower() for field in module.params[FIELD_COLUMNS_NAME]])
    if FIELD_QUERY_NAME in module.params:
        module.params[FIELD_QUERY_NAME] = utils.sysparm_query_from_conditions(module.params[FIELD_QUERY_NAME])
    query = utils.filter_dict(module.params, *POSSIBLE_FILTER_PARAMETERS)
    servicenow_query = transform_query_to_servicenow_query(query)
    return table_client.list_records(table_name(module), servicenow_query)


def main():
    arg_spec = dict(
        arguments.get_spec(
            "instance", "sys_id"
        ),
        resource=dict(  # resource - table name
            type="str",
            required=True
        ),
        query=dict(
            type="dict"
        ),  # An encoded query string used to filter the results
        display_value=dict(
            type="str",
            choices=[
                "true",
                "false",
                "both"
            ]
        ),  # Return field display values (true), actual values (false), or both (all) (default: false)
        exclude_reference_link=dict(
            type="bool"
        ),  # True to exclude Table API links for reference columns (default: false)
        columns=dict(
            type="list",
            default=[]
        ),  # A comma-separated list of fields to return in the response
        query_category=dict(
            type="str"
        ),  # Name of the query category (read replica category) to use for queries
        query_no_domain=dict(
            type="bool"
        ),  # True to access data across domains if authorized (default: false)
        no_count=dict(
            type="bool"
        ),  # Do not execute a select count(*) on table (default: false)
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=arg_spec
    )

    try:
        snow_client = client.Client(**module.params["instance"])
        table_client = table.TableClient(snow_client)
        records = run(module, table_client)
        module.exit_json(changed=False, record=records)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
