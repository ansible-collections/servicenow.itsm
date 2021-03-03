#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: change_request_info

author:
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)
short_description: List ServiceNow change requests
description:
  - Retrieve information about ServiceNow change requests.
  - For more information, refer to the ServiceNow change management documentation at
    U(https://docs.servicenow.com/bundle/paris-it-service-management/page/product/change-management/concept/c_ITILChangeManagement.html).
version_added: 1.0.0
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id.info
  - servicenow.itsm.number.info
seealso:
  - module: servicenow.itsm.change_request
"""

EXAMPLES = r"""
- name: Retrieve all change requests
  servicenow.itsm.change_request_info:
  register: result

- name: Retrieve a specific change request by its sys_id
  servicenow.itsm.change_request_info:
    sys_id: 471bfbc7a9fe198101e77a3e10e5d47f
  register: result

- name: Retrieve change requests by number
  servicenow.itsm.change_request_info:
    number: PRB0007601
  register: result
"""

RETURN = r"""
records:
  description:
    - A list of change request records.
  returned: success
  type: list
  sample:
    - "active": "false"
      "activity_due": ""
      "additional_assignee_list": ""
      "approval": "approved"
      "approval_history": ""
      "approval_set": ""
      "assigned_to": ""
      "assignment_group": "d625dccec0a8016700a222a0f7900d06"
      "backout_plan": ""
      "business_duration": ""
      "business_service": ""
      "cab_date": ""
      "cab_delegate": ""
      "cab_recommendation": ""
      "cab_required": "false"
      "calendar_duration": ""
      "category": "Other"
      "change_plan": ""
      "close_code": "successful"
      "close_notes": "Completed successfully"
      "closed_at": "2015-07-06 18:18:53"
      "closed_by": "6816f79cc0a8016401c5a33be04be441"
      "cmdb_ci": ""
      "comments": ""
      "comments_and_work_notes": ""
      "company": ""
      "conflict_last_run": ""
      "conflict_status": "Not Run"
      "contact_type": "phone"
      "contract": ""
      "correlation_display": ""
      "correlation_id": ""
      "delivery_plan": ""
      "delivery_task": ""
      "description": "Decommission a server"
      "due_date": ""
      "end_date": ""
      "escalation": "0"
      "expected_start": ""
      "follow_up": ""
      "group_list": ""
      "impact": "3"
      "implementation_plan": "Implementation plan"
      "justification": ""
      "knowledge": "false"
      "location": ""
      "made_sla": "true"
      "number": "CHG0000023"
      "on_hold": "false"
      "on_hold_reason": ""
      "on_hold_task": ""
      "opened_at": "2015-07-06 18:17:21"
      "opened_by": "6816f79cc0a8016401c5a33be04be441"
      "order": ""
      "outside_maintenance_schedule": "false"
      "parent": ""
      "phase": "requested"
      "phase_state": "open"
      "priority": "4"
      "production_system": "false"
      "reason": ""
      "reassignment_count": "2"
      "requested_by": "6816f79cc0a8016401c5a33be04be441"
      "requested_by_date": ""
      "review_comments": ""
      "review_date": ""
      "review_status": ""
      "risk": "3"
      "risk_impact_analysis": ""
      "route_reason": ""
      "scope": "3"
      "service_offering": ""
      "short_description": "Decommission server"
      "sla_due": ""
      "start_date": ""
      "state": "3"
      "std_change_producer_version": "deb8544047810200e90d87e8dee490af"
      "sys_class_name": "change_request"
      "sys_created_by": "admin"
      "sys_created_on": "2015-07-06 18:17:22"
      "sys_domain": "global"
      "sys_domain_path": "/"
      "sys_id": "70ad699e47410200e90d87e8dee4907d"
      "sys_mod_count": "8"
      "sys_tags": ""
      "sys_updated_by": "admin"
      "sys_updated_on": "2015-07-06 18:18:53"
      "task_effective_number": "CHG0000023"
      "test_plan": "Test plan"
      "time_worked": ""
      "type": "standard"
      "unauthorized": "false"
      "universal_request": ""
      "upon_approval": "proceed"
      "upon_reject": "cancel"
      "urgency": "3"
      "user_input": ""
      "watch_list": ""
      "work_end": "2015-07-06 18:18:34"
      "work_notes": ""
      "work_notes_list": ""
      "work_start": "2015-07-06 18:17:41"
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, errors, utils, table
from ..module_utils.change_request import PAYLOAD_FIELDS_MAPPING


def run(module, table_client):
    query = utils.filter_dict(module.params, "sys_id", "number")
    mapper = utils.PayloadMapper(PAYLOAD_FIELDS_MAPPING)

    return [
        mapper.to_ansible(record)
        for record in table_client.list_records("change_request", query)
    ]


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("instance", "sys_id", "number"),
        ),
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
