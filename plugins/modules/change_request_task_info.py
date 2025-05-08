#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: change_request_task_info

author:
  - Matej Pevec (@mysteriouswolf)
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)
short_description: List ServiceNow change request tasks
description:
  - Retrieve information about ServiceNow change request tasks.
  - For more information, refer to the ServiceNow change management documentation at
    U(https://docs.servicenow.com/bundle/tokyo-it-service-management/page/product/change-management/concept/c_ITILChangeManagement.html).
version_added: 1.3.0
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id.info
  - servicenow.itsm.number.info
  - servicenow.itsm.query
  - servicenow.itsm.change_request_task_mapping
  - servicenow.itsm.sysparm_display_value
seealso:
  - module: servicenow.itsm.change_request_task
"""

EXAMPLES = r"""
- name: Retrieve all change request tasks
  servicenow.itsm.change_request_task_info:
  register: result

- name: Retrieve a specific change request task by its sys_id
  servicenow.itsm.change_request_task_info:
    sys_id: 471bfbc7a9fe198101e77a3e10e5d47f
  register: result

- name: Retrieve change request tasks by number
  servicenow.itsm.change_request_task_info:
    number: CTASK0000001
  register: result

- name: Retrieve change request tasks that contain SAP in their short description by using field query
  servicenow.itsm.change_request_task_info:
    query:
      - short_description: LIKE SAP
  register: result

- name: Retrieve change request tasks that contain SAP in their short description by using field sysparm-query
  servicenow.itsm.change_request_task_info:
    sysparm_query: short_descriptionLIKESAP
  register: result

- name: Retrieve new change requests assigned to abel.tuter or bertie.luby
  servicenow.itsm.change_request_task_info:
    query:
      - state: = new
        assigned_to: = abel.tuter
      - state: = new
        assigned_to: = bertie.luby
"""

RETURN = r"""
records:
  description:
    - A list of change task records.
  returned: success
  type: list
  sample:
    - "active": "true"
      "activity_due": ""
      "additional_assignee_list": ""
      "approval": "not requested"
      "approval_history": ""
      "approval_set": ""
      "assigned_to": "f298d2d2c611227b0106c6be7f154bc8"
      "assignment_group": ""
      "business_duration": ""
      "business_service": ""
      "calendar_duration": ""
      "change_request": "a9e9c33dc61122760072455df62663d2"
      "change_task_type": ""
      "close_code": ""
      "close_notes": ""
      "closed_at": ""
      "closed_by": ""
      "cmdb_ci": ""
      "comments": ""
      "comments_and_work_notes": ""
      "company": ""
      "contact_type": "phone"
      "contract": ""
      "correlation_display": ""
      "correlation_id": ""
      "created_from": ""
      "delivery_plan": ""
      "delivery_task": ""
      "description": "Preliminary System Testing"
      "due_date": "2020-09-05 22:22:39"
      "escalation": "0"
      "expected_start": ""
      "follow_up": ""
      "group_list": ""
      "impact": "3"
      "knowledge": "false"
      "location": ""
      "made_sla": "false"
      "number": "CTASK0010005"
      "on_hold": false
      "on_hold_reason": ""
      "opened_at": "2020-08-30 22:22:48"
      "opened_by": "6816f79cc0a8016401c5a33be04be441"
      "order": ""
      "parent": ""
      "planned_end_date": ""
      "planned_start_date": ""
      "priority": "3"
      "reassignment_count": ""
      "route_reason": ""
      "service_offering": ""
      "short_description": "Preliminary System Testing"
      "sla_due": ""
      "state": "open"
      "sys_class_name": "change_task"
      "sys_created_by": "admin"
      "sys_created_on": "2020-08-30 22:22:48"
      "sys_domain": "global"
      "sys_domain_path": "/"
      "sys_id": "a9f2e5bdc61122760052c1250f7ac503"
      "sys_mod_count": "0"
      "sys_tags": ""
      "sys_updated_by": "admin"
      "sys_updated_on": "2020-08-30 22:22:48"
      "task_effective_number": "CTASK0010005"
      "time_worked": ""
      "universal_request": ""
      "upon_approval": ""
      "upon_reject": ""
      "urgency": "3"
      "user_input": ""
      "watch_list": ""
      "work_end": ""
      "work_notes": ""
      "work_notes_list": ""
      "work_start": ""
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, errors, query, table, utils
from ..module_utils.change_request_task import PAYLOAD_FIELDS_MAPPING
from ..module_utils.utils import get_mapper




class ReMapper():
    def __init__(self, table_client):
        self.table_client = table_client
        self.query_args = dict()

    def type(self, val):
        self.query_args["change_task_type"] = (val[0], val[1])

    def hold_reason(self, val):
        self.query_args["on_hold_reason"] = (val[0], val[1])

    def configuration_item_id(self, val):
        self.query_args["cmdb_ci"] = (val[0], val[1])

    def configuration_item(self, val):
        configuration_item = table.find_configuration_item(self.table_client, val[1])
        self.query_args["cmdb_ci"] = (val[0], configuration_item["sys_id"])

    def change_request_id(self, val):
        self.query_args["change_request"] = (val[0], val[1])

    def change_request_number(self, val):
        change_request = table.find_change_request(self.table_client, val[1])
        self.query_args["change_request"] = (val[0], change_request["sys_id"])

    def assigned_to(self, val):
        user = table.find_user(self.table_client, val[1])
        self.query_args["assigned_to"] = (val[0], user["sys_id"])

    def assignment_group(self, val):
        assignment_group = table.find_assignment_group(self.table_client, val[1])
        self.query_args["assignment_group"] = (val[0], assignment_group["sys_id"])

    def default(self, key, val):
        self.query_args[key] = val


def remap_params(query, table_client):
    query_load = []
    for item in query:
        remapper = ReMapper(table_client)
        for k, v in item.items():
            try:
                getattr(remapper, k)(v)
            except AttributeError:
                remapper.default(k, v)
        query_load.append(remapper.query_args)

    return query_load


def sysparms_query(module, table_client, mapper):
    parsed, err = query.parse_query(module.params["query"])
    if err:
        raise errors.ServiceNowError(err)

    remap_query = remap_params(parsed, table_client)

    return query.serialize_query(query.map_query_values(remap_query, mapper))


def run(module, table_client):
    mapper = get_mapper(
        module,
        "change_request_task_mapping",
        PAYLOAD_FIELDS_MAPPING,
        sysparm_display_value=module.params["sysparm_display_value"],
    )

    if module.params["query"]:
        query = {
            "sysparm_query": sysparms_query(module, table_client, mapper),
            "sysparm_display_value": module.params["sysparm_display_value"],
        }
    elif module.params["sysparm_query"]:
        query = {"sysparm_query": module.params["sysparm_query"]}
    else:
        query = utils.filter_dict(
            module.params, "sys_id", "number", "sysparm_display_value"
        )

    return [
        mapper.to_ansible(record)
        for record in table_client.list_records("change_task", query)
    ]


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec(
                "instance",
                "sys_id",
                "number",
                "query",
                "change_request_task_mapping",
                "sysparm_query",
                "sysparm_display_value",
            ),
        ),
        mutually_exclusive=[
            ("sys_id", "query"),
            ("number", "query"),
            ("sysparm_query", "query"),
            ("sys_id", "sysparm_query"),
            ("number", "sysparm_query"),
        ],
    )

    try:
        snow_client = client.Client(**module.params["instance"])
        table_client = table.TableClient(snow_client)
        records = run(module, table_client)
        module.exit_json(changed=False, records=records)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
