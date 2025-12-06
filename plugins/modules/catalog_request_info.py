#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: catalog_request_info
author:
  - ServiceNow ITSM Collection Contributors (@ansible-collections)
short_description: List ServiceNow catalog requests
description:
  - Retrieve information about ServiceNow catalog requests (sc_request).
  - For more information, refer to the ServiceNow service catalog documentation at
    U(https://docs.servicenow.com/bundle/utah-servicenow-platform/page/product/service-catalog/concept/c_ServiceCatalogProcess.html).
version_added: 2.11.0
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id.info
  - servicenow.itsm.number.info
  - servicenow.itsm.query
  - servicenow.itsm.sysparm_display_value
seealso:
  - module: servicenow.itsm.catalog_request
  - module: servicenow.itsm.catalog_request_task_info
"""

EXAMPLES = r"""
- name: Retrieve all catalog requests
  servicenow.itsm.catalog_request_info:
  register: result

- name: Retrieve a specific catalog request by its sys_id
  servicenow.itsm.catalog_request_info:
    sys_id: 471bfbc7a9fe198101e77a3e10e5d47f
  register: result

- name: Retrieve catalog requests by number
  servicenow.itsm.catalog_request_info:
    number: REQ0007601
  register: result

- name: Retrieve catalog requests that contain laptop in short description
  servicenow.itsm.catalog_request_info:
    query:
      - short_description: LIKE laptop
  register: result

- name: Retrieve catalog requests by request state
  servicenow.itsm.catalog_request_info:
    query:
      - request_state: = submitted
  register: result

- name: Retrieve catalog requests requested by specific user
  servicenow.itsm.catalog_request_info:
    query:
      - requested_by: = abel.tuter
  register: result

- name: Retrieve catalog requests for specific user
  servicenow.itsm.catalog_request_info:
    query:
      - requested_for: = john.doe
  register: result

- name: Retrieve catalog requests using sysparm_query
  servicenow.itsm.catalog_request_info:
    sysparm_query: short_descriptionLIKElaptop^request_state=submitted
  register: result
"""

RETURN = r"""
records:
  description:
    - A list of catalog request records.
  returned: success
  type: list
  sample:
    - "active": "true"
      "approval": "not_requested"
      "assigned_to": ""
      "assignment_group": ""
      "attachments": []
      "business_service": ""
      "comments": ""
      "delivery_plan": ""
      "delivery_task": ""
      "description": "User needs a new laptop for remote work"
      "due_date": ""
      "impact": "3"
      "number": "REQ0000123"
      "opened_at": "2024-01-15 10:30:00"
      "opened_by": "jane.smith"
      "priority": "2"
      "request_state": "submitted"
      "requested_by": "jane.smith"
      "requested_for": "john.doe"
      "short_description": "Request for new laptop"
      "stage": "request_approved"
      "sys_created_by": "jane.smith"
      "sys_created_on": "2024-01-15 10:30:00"
      "sys_id": "b25d93a37b1200001c9c9b5b8a9619a8"
      "sys_updated_by": "jane.smith"
      "sys_updated_on": "2024-01-15 10:30:00"
      "urgency": "2"
      "work_notes": ""
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, errors, table, query
from ..module_utils.utils import get_mapper


def sysparms_query(query_param, table_client, mapper):
    parsed, err = query.parse_query(query_param)
    if err:
        raise errors.ServiceNowError(err)

    remap_query = remap_params(parsed, table_client)

    return query.serialize_query(query.map_query_values(remap_query, mapper))


def remap_params(query, table_client):
    query_load = []

    for item in query:
        q = dict()
        for k, v in item.items():
            if k == "requested_by":
                user = table.find_user(table_client, v[1])
                q["requested_by"] = (v[0], user["sys_id"])

            elif k == "requested_for":
                user = table.find_user(table_client, v[1])
                q["requested_for"] = (v[0], user["sys_id"])

            elif k == "assignment_group":
                assignment_group = table.find_assignment_group(table_client, v[1])
                q["assignment_group"] = (v[0], assignment_group["sys_id"])

            else:
                q[k] = v

        query_load.append(q)

    return query_load


def run(module, table_client):

    query = {}
    if module.params.get("sysparm_query"):
        query = {"sysparm_query": module.params["sysparm_query"]}
    elif module.params.get("query"):
        mapper = get_mapper(module, "catalog_request_mapping", dict())
        query = {
            "sysparm_query": sysparms_query(
                module.params.get("query"), table_client, mapper
            )
        }
    else:
        if module.params.get("sys_id"):
            query["sys_id"] = module.params["sys_id"]
        if module.params.get("number"):
            query["number"] = module.params["number"]

    if module.params.get("sysparm_display_value"):
        query["sysparm_display_value"] = module.params["sysparm_display_value"]

    return table_client.list_records("sc_request", query)


def main():
    module_args = dict(
        arguments.get_spec(
            "instance",
            "sys_id",
            "number",
            "query",
            "sysparm_query",
            "sysparm_display_value",
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[
            ("sysparm_query", "query", "sys_id"),
            ("sysparm_query", "query", "number"),
        ],
    )

    try:
        snow_client = client.Client(**module.params["instance"])
        table_client = table.TableClient(snow_client)
        records = run(module, table_client)
        module.exit_json(changed=False, records=records)
    except errors.ServiceNowError as e:
        module.fail_json(**e.to_module_fail_json_output())



if __name__ == "__main__":
    main()
