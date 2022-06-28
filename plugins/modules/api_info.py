#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: api_info

author:
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)
  - Matej Pevec (@mysteriouswolf)

short_description: ServiceNow REST API "client" module

description:
    - 

"""

EXAMPLES = """ """

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, attachment, client, errors, query, table, utils
from ..module_utils.change_request import PAYLOAD_FIELDS_MAPPING
from ..module_utils.utils import get_mapper
from ..module_utils.api import transform_query_to_servicenow_query


def run(module, table_client):
    module.params["fields"] = ",".join([field.lower() for field in module.params["fields"]])
    query = utils.filter_dict(
        module.params,
        "query", "display_value", "exclude_reference_link", "fields",
        "query_category", "query_no_domain", "no_count"
    )

    servicenow_query = transform_query_to_servicenow_query(query)
    return table_client.list_records(module.params["resource"], servicenow_query)


def main():
    # TODO:
    #   - Rename and implement query conditions
    #   - Rename: fields --> columns
    #   - Look at now.py's line 253
    arg_spec = dict(
        arguments.get_spec(
            "instance", "sys_id"
        ),
        resource=dict(  # resource - table name
            type="str",
            required=True
        ),
        query=dict(
            type="str",
            default=None
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
        ),  # True to exclude Table API links for reference fields (default: false)
        fields=dict(
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
