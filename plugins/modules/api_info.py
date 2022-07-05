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
short_description: List ServiceNow REST Table API results
description:
  - Retrieve information about ServiceNow REST Table API results from arbitrary table
  - For more information, refer to the ServiceNow REST TAble API documentation at
    U(https://docs.servicenow.com/bundle/paris-application-development/page/integrate/inbound-rest/concept/c_TableAPI.html#c_TableAPIO
version_added: 1.4.0
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id.info
  - servicenow.itsm.resource
  - servicenow.itsm.query
  - servicenow.itsm.display_value
  - servicenow.itsm.exclude_reference_link
  - servicenow.itsm.query_category
  - servicenow.itsm.query_no_domain
  - servicenow.itsm.no_count
seealso:
  - module: servicenow.itsm.api

options:
  sys_id:
    description:
      - Unique ID of the record
      - If sys_id is specified, the output is going to be either empty list (if a record in table,
        specified in resource does not exist) or a list with single element (since sys_id is unique identifier)
    type: str
    required: true
  resource:
    description:
      - The name of the table that we want to obtain records from
    type: str
    required: true
  query:
    description:
      - Query for obtaining records with certain properties.
      - Will be ignored if sys_id is specified (since query is intended for obtaining multiple records
        with certiain properties, and sys_id is uniquely defined property)
      - Query is dictionary, with table's column names as keys and additional dictionaries as values
        Inner dictionaries have keys as possible filter operators (starts_with, contains, is, ...) and list
        of values that this operator can match as values. Elements in the same list will get mapped with
        'OR' operator and elements in different list will get mapped with 'AND' operator. Example of query may 
        be seen under examples (the one with query specified).
      - "Example: query = dict(number=dict(starts_with=['A1', 'A2'], ends_with=['B1', 'B2']), state=dict(is=[7]))) 
        will get mapped to URL query as
        numberSTARTSWITHA1^ORnumberSTARTSWITHA2^numberENDSWITHB1^ORnumberENDSWITHB2^state=7 (it would be same
        had you inputed this string directly in REST API."
      - "List of all possible operators may be found at 
        U(https://docs.servicenow.com/en-US/bundle/sandiego-platform-user-interface/page/use/common-ui-elements/reference/r_OpAvailableFiltersQueries.html).
        under column operator label with spaces replaced with underline (for example: 'is same' is written in the
        link above --> write 'is_same' when filtering through playbook. Same others, e.g.: 'is not' --> 'is_not')"
      - "If your operator is one of the following: 'is_empty', 'is_not_empty', 'is_anything', 'is_empty_string',
        nothing has to be specified in list of possible values as they're boolean operators that don't need any 
        value on the right side of the operator. For example, if you want to use 'is_empty_string' as query for
        column 'short_desciption', you'd say: query = dict(short_description=dict(is_empty_string=None)).
        Anything else than None would fit the needs be okay. See example of this under the examples (the one with
        query specified)"
    type: dict
  display_value:
    description:
      - Return field display values (true), actual values (false), or both (all) (default: false)
    type: bool
  exclude_reference_link:
    description:
      - "true to exclude Table API links for reference fields (default: false)"
    type: bool
  columns:
    description:
      - List of fields/columns to return in the response
    type: list
  query_category:
    description:
      - Name of the query category to use for queries
    type: str
  query_no_domain:
    description:
      - "true to access data across domains if authorized (default: false)"
    type: bool
  no_count:
    description:
      - "Do not execute a select count(*) on table (default: false)"
    type: bool
"""

EXAMPLES = """ 
- name: Retrieve all records from table incidents
  servicenow.itsm.api_info:
    resource: incident
  register: result

- name: Retrieve a record with specified sys_id from the resource incidents
  servicenow.itsm.api_info:
    resource: incident
    sys_id: 471bfbc7a9fe198101e77a3e10e5d47f
  register: result

- name: Retrieve all incidents with properties specified in query
  servicenow.itsm.api_info:
    resource: incident
    query:
      number:
        starts_with:
          - 'INC'
          - 'ABC'
        state:
          is:
            - 7
          between:
            - 5@9
        short_description:
          is_empty_string: # No need to list any values for operator is_empty_string
  register: result

- name: Retrieve all incidents with properties specified in query with additional filter parameters
  servicenow.itsm.api_info:
    resource: incident
    query:
      number:
        starts_with:
          - 'INC'
          - 'ABC'
      state:
        is:
          - 7
        between:
          - 5@9
    display_value: true
    exclude_reference_link: true
    columns:
      - state
      - number
      - sys_id
    query_no_domain: true
    no_count: false
"""

RETURN = r"""
records:
  description:
    - A list of records from the specified table.
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

from ..module_utils import arguments, client, errors, table, utils
from ..module_utils.api import (
    transform_query_to_servicenow_query, POSSIBLE_FILTER_PARAMETERS, table_name, FIELD_COLUMNS_NAME, FIELD_QUERY_NAME,
    ACTION_POST, ACTION_PATCH, ACTION_DELETE, FIELD_SYS_ID
)


def run(module, table_client):
    if FIELD_COLUMNS_NAME in module.params:
        module.params[FIELD_COLUMNS_NAME] = ",".join([field.lower() for field in module.params[FIELD_COLUMNS_NAME]])
    if FIELD_QUERY_NAME in module.params:
        module.params[FIELD_QUERY_NAME] = utils.sysparm_query_from_conditions(module.params[FIELD_QUERY_NAME])
    if module.params[FIELD_SYS_ID] is not None:
        # If sys_id is specified, we're only going to retrieve a single record
        servicenow_query = dict(sys_id=module.params[FIELD_SYS_ID])
    else:
        # Otherwise, retrieve records that fit the values specified in query
        query = utils.filter_dict(module.params, *POSSIBLE_FILTER_PARAMETERS)
        servicenow_query = transform_query_to_servicenow_query(query)
    raise errors.ServiceNowError(servicenow_query)
    # raise errors.ServiceNowError(servicenow_query)
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
            type="dict",
            default=dict()
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
            type="bool",
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
            type="bool",
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
