#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["stableinterface"],
    "supported_by": "certified",
}

DOCUMENTATION = """
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
seealso:
  - module: servicenow.itsm.incident
"""

EXAMPLES = """
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
"""

RETURN = """
records:
  description:
    - A list of incident records, as returned by the ServiceNow API.
  returned: success
  type: list
  sample: [
    {
      "active":"false",
      "activity_due":"",
      "additional_assignee_list":"",
      "approval":"",
      "approval_history":"",
      "approval_set":"",
      "assigned_to":{
        "link":"https://my.service-now.com//api/now/table/sys_user/46b87022a9fe198101a78787e40d7547",
        "value":"46b87022a9fe198101a78787e40d7547"
      },
      "assignment_group":{
        "link":"https://my.service-now.com//api/now/table/sys_user_group/d625dccec0a8016700a222a0f7900d06",
        "value":"d625dccec0a8016700a222a0f7900d06"
      },
      "business_duration":"1970-01-22 21:46:21",
      "business_service":"",
      "business_stc":"1892781",
      "calendar_duration":"1970-04-02 20:46:21",
      "calendar_stc":"7937181",
      "caller_id":{
        "link":"https://my.service-now.com//api/now/table/sys_user/5137153cc611227c000bbd1bd8cd2005",
        "value":"5137153cc611227c000bbd1bd8cd2005"
      },
      "category":"network",
      "caused_by":"",
      "child_incidents":"",
      "close_code":"Closed/Resolved by Caller",
      "close_notes":"Closed before close notes were made mandatory\n\t\t",
      "closed_at":"2020-06-25 23:10:06",
      "closed_by":{
        "link":"https://my.service-now.com//api/now/table/sys_user/9ee1b13dc6112271007f9d0efdb69cd0",
        "value":"9ee1b13dc6112271007f9d0efdb69cd0"
      },
      "cmdb_ci":{
        "link":"https://my.service-now.com//api/now/table/cmdb_ci/b0c4030ac0a800090152e7a4564ca36c",
        "value":"b0c4030ac0a800090152e7a4564ca36c"
      },
      "comments":"",
      "comments_and_work_notes":"",
      "company":"",
      "contact_type":"",
      "contract":"",
      "correlation_display":"",
      "correlation_id":"",
      "delivery_plan":"",
      "delivery_task":"",
      "description":"User can't access email on mail.company.com.\n\t\t",
      "due_date":"",
      "escalation":"0",
      "expected_start":"",
      "follow_up":"",
      "group_list":"",
      "hold_reason":"",
      "impact":"1",
      "incident_state":"7",
      "knowledge":"false",
      "location":{
        "link":"https://my.service-now.com//api/now/table/cmn_location/1083361cc611227501b682158cabf646",
        "value":"1083361cc611227501b682158cabf646"
      },
      "made_sla":"false",
      "notify":"1",
      "number":"INC0000001",
      "opened_at":"2020-06-24 23:09:51",
      "opened_by":{
        "link":"https://my.service-now.com//api/now/table/sys_user/681ccaf9c0a8016400b98a06818d57c7",
        "value":"681ccaf9c0a8016400b98a06818d57c7"
      },
      "order":"",
      "parent":"",
      "parent_incident":"",
      "priority":"1",
      "problem_id":{
        "link":"https://my.service-now.com//api/now/table/problem/9d3a266ac6112287004e37fb2ceb0133",
        "value":"9d3a266ac6112287004e37fb2ceb0133"
      },
      "reassignment_count":"1",
      "reopen_count":"",
      "reopened_by":"",
      "reopened_time":"",
      "resolved_at":"2020-09-24 19:56:12",
      "resolved_by":{
        "link":"https://my.service-now.com//api/now/table/sys_user/6816f79cc0a8016401c5a33be04be441",
        "value":"6816f79cc0a8016401c5a33be04be441"
      },
      "rfc":"",
      "route_reason":"",
      "service_offering":"",
      "severity":"1",
      "short_description":"Can't read email",
      "sla_due":"",
      "state":"7",
      "subcategory":"",
      "sys_class_name":"incident",
      "sys_created_by":"pat",
      "sys_created_on":"2019-01-24 18:24:13",
      "sys_domain":{
        "link":"https://my.service-now.com//api/now/table/sys_user_group/global",
        "value":"global"
      },
      "sys_domain_path":"/",
      "sys_id":"9c573169c611228700193229fff72400",
      "sys_mod_count":"21",
      "sys_tags":"",
      "sys_updated_by":"admin",
      "sys_updated_on":"2020-09-24 20:16:07",
      "task_effective_number":"INC0000001",
      "time_worked":"",
      "universal_request":"",
      "upon_approval":"",
      "upon_reject":"",
      "urgency":"1",
      "user_input":"",
      "watch_list":"",
      "work_end":"",
      "work_notes":"",
      "work_notes_list":"",
      "work_start":""
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, errors, utils


def run(module, snow_client):
    query = utils.filter_dict(module.params, "sys_id", "number")

    resp = snow_client.get("table/incident", query=query)
    incidents = resp.json["result"]

    return incidents


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("instance", "sys_id", "number"),
        ),
    )

    try:
        snow_client = client.Client(**module.params["instance"])
        records = run(module, snow_client)
        module.exit_json(changed=False, records=records)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
