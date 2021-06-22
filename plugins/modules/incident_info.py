#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: incident_info

author:
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)
short_description: List ServiceNow incidents
description:
  - Retrieve information about ServiceNow incidents.
  - For more information, refer to the ServiceNow incident management documentation at
    U(https://docs.servicenow.com/bundle/paris-it-service-management/page/product/incident-management/concept/c_IncidentManagement.html).
version_added: 1.0.0
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id.info
  - servicenow.itsm.number.info
  - servicenow.itsm.query
seealso:
  - module: servicenow.itsm.incident
"""

EXAMPLES = r"""
- name: Retrieve all incidents
  servicenow.itsm.incident_info:
  register: result

- name: Retrieve a specific incident by its sys_id
  servicenow.itsm.incident_info:
    sys_id: 471bfbc7a9fe198101e77a3e10e5d47f
  register: result

- name: Retrieve incidents by number
  servicenow.itsm.incident_info:
    number: INC0000039
  register: result

- name: Retrieve all incidents that contain SAP in its short description
  servicenow.itsm.incident_info:
    query:
      - short_description: LIKE SAP
  register: result

- name: Retrieve new incidents reported by abel.tuter or bertie.luby
  servicenow.itsm.incident_info:
    query:
      - state: = new
        caller: = abel.tuter
      - state: = new
        caller: = bertie.luby
"""

RETURN = r"""
records:
  description:
    - A list of incident records.
  returned: success
  type: list
  sample:
    - active: "false"
      activity_due: ""
      additional_assignee_list: ""
      approval: not requested
      approval_history: ""
      approval_set: ""
      assigned_to: 5137153cc611227c000bbd1bd8cd2007
      assignment_group: 8a4dde73c6112278017a6a4baf547aa7
      business_duration: "1970-01-20 05:38:50"
      business_service: ""
      business_stc: "1661930"
      calendar_duration: "1970-03-21 20:38:50"
      calendar_stc: "6899930"
      caller_id: 681ccaf9c0a8016400b98a06818d57c7
      category: inquiry
      caused_by: ""
      child_incidents: ""
      close_code: Solved (Work Around)
      close_notes: Gave workaround
      closed_at: "2020-07-07 23:18:40"
      closed_by: 9ee1b13dc6112271007f9d0efdb69cd0
      cmdb_ci: ""
      comments: ""
      comments_and_work_notes: ""
      company: 31bea3d53790200044e0bfc8bcbe5dec
      contact_type: phone
      contract: ""
      correlation_display: ""
      correlation_id: ""
      delivery_plan: ""
      delivery_task: ""
      description: Noticing today that any time I send an email with an attachment, it
        takes at least 20 seconds to send.
      due_date: ""
      escalation: "0"
      expected_start: ""
      follow_up: ""
      group_list: ""
      hold_reason: ""
      impact: "1"
      incident_state: "7"
      knowledge: "false"
      location: ""
      made_sla: "false"
      notify: "1"
      number: INC0000013
      opened_at: "2020-07-06 23:15:58"
      opened_by: 9ee1b13dc6112271007f9d0efdb69cd0
      order: ""
      parent: ""
      parent_incident: ""
      priority: "1"
      problem_id: ""
      reassignment_count: "2"
      reopen_count: ""
      reopened_by: ""
      reopened_time: ""
      resolved_at: "2020-09-24 19:54:48"
      resolved_by: 6816f79cc0a8016401c5a33be04be441
      rfc: ""
      route_reason: ""
      service_offering: ""
      severity: "3"
      short_description: EMAIL is slow when an attachment is involved
      sla_due: ""
      state: "7"
      subcategory: ""
      sys_class_name: incident
      sys_created_by: don.goodliffe
      sys_created_on: "2020-07-07 23:18:07"
      sys_domain: global
      sys_domain_path: /
      sys_id: 46cebb88a9fe198101aee93734f9768b
      sys_mod_count: "5"
      sys_tags: ""
      sys_updated_by: VALUE_SPECIFIED_IN_NO_LOG_PARAMETER
      sys_updated_on: "2020-09-24 19:54:48"
      task_effective_number: INC0000013
      time_worked: ""
      universal_request: ""
      upon_approval: ""
      upon_reject: ""
      urgency: "1"
      user_input: ""
      watch_list: ""
      work_end: ""
      work_notes: ""
      work_notes_list: ""
      work_start: ""
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, errors, query, table, utils
from ..module_utils.incident import PAYLOAD_FIELDS_MAPPING


def remap_caller(query, table_client):
    query_load = []

    for item in query:
        q = dict()
        for k, v in item.items():
            if k == "caller":
                user = table.find_user(table_client, v[1])
                q["caller_id"] = (v[0], user["sys_id"])
            else:
                q[k] = v
        query_load.append(q)

    return query_load


def sysparms_query(module, table_client, mapper):
    parsed, err = query.parse_query(module.params["query"])
    if err:
        raise errors.ServiceNowError(err)

    remap_query = remap_caller(parsed, table_client)

    return query.serialize_query(query.map_query_values(remap_query, mapper))


def run(module, table_client):
    mapper = utils.PayloadMapper(PAYLOAD_FIELDS_MAPPING, module.warn)

    if module.params["query"]:
        query = {"sysparm_query": sysparms_query(module, table_client, mapper)}
    else:
        query = utils.filter_dict(module.params, "sys_id", "number")

    return [
        mapper.to_ansible(record)
        for record in table_client.list_records("incident", query)
    ]


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("instance", "sys_id", "number", "query"),
        ),
        mutually_exclusive=[("sys_id", "query"), ("number", "query")],
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
