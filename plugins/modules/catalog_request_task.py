#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: catalog_request_task
author:
  - ServiceNow ITSM Collection Contributors (@ansible-collections)
short_description: Manage ServiceNow catalog request tasks
description:
  - Create, delete or update a ServiceNow catalog request task (sc_task).
  - For more information, refer to the ServiceNow service catalog documentation at
    U(https://docs.servicenow.com/bundle/utah-servicenow-platform/page/product/service-catalog/concept/c_ServiceCatalogProcess.html).
version_added: 2.11.0
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id
  - servicenow.itsm.number
  - servicenow.itsm.attachments
  - servicenow.itsm.catalog_request_task_mapping
seealso:
  - module: servicenow.itsm.catalog_request_task_info
  - module: servicenow.itsm.catalog_request
  - module: servicenow.itsm.service_catalog
options:
  state:
    description:
      - The state of the catalog request task.
      - If I(state) value is C(present), the record is created or updated.
      - If I(state) value is C(absent), the record is deleted.
      - Default choices are C(present) and C(absent).
    type: str
    choices: [ present, absent ]
    default: present
  task_state:
    description:
      - The current state of the catalog request task.
      - Default choices are C(pending), C(open), C(work_in_progress), C(closed_complete), C(closed_incomplete), C(closed_skipped).
    type: str
    choices: [ pending, open, work_in_progress, closed_complete, closed_incomplete, closed_skipped ]
  request:
    description:
      - The catalog request (sc_request) this task belongs to.
      - Can be specified as sys_id or number of the catalog request.
    type: str
  requested_for:
    description:
      - User who the catalog item is being requested for.
      - Expected value is user login name (user_name field).
    type: str
  requested_by:
    description:
      - User who requested the catalog item.
      - Expected value is user login name (user_name field).
    type: str
  assignment_group:
    description:
      - The name of the group that the catalog request task is assigned to.
    type: str
  assigned_to:
    description:
      - User assigned to handle this catalog request task.
      - Expected value is user login name (user_name field).
    type: str
  priority:
    description:
      - Priority of the catalog request task.
      - Default choices are C(1), C(2), C(3), C(4), C(5).
      - Priority 1 is the highest, 5 is the lowest priority.
    type: str
    choices: [ "1", "2", "3", "4", "5" ]
  urgency:
    description:
      - Urgency of the catalog request task.
      - Default choices are C(1), C(2), C(3).
      - Urgency 1 is the highest, 3 is the lowest urgency.
    type: str
    choices: [ "1", "2", "3" ]
  impact:
    description:
      - Impact of the catalog request task.
      - Default choices are C(1), C(2), C(3).
      - Impact 1 is the highest, 3 is the lowest impact.
    type: str
    choices: [ "1", "2", "3" ]
  short_description:
    description:
      - Brief summary of the catalog request task.
    type: str
  description:
    description:
      - Detailed description of the catalog request task.
    type: str
  comments:
    description:
      - Additional comments for the catalog request task.
    type: str
  work_notes:
    description:
      - Work notes for the catalog request task (internal notes).
      - This field is not idempotent. Any value set here will be added to the existing work notes
        on the task.
      - This field is always empty in the record returned by the module.
    type: str
  due_date:
    description:
      - Expected due date for the catalog request task.
      - Expected format is YYYY-MM-DD.
    type: str
  close_notes:
    description:
      - Notes added when closing the catalog request task.
    type: str
  order:
    description:
      - Order/sequence number for task execution.
    type: int
  approval:
    description:
      - Approval status of the catalog request task.
      - Default choices are C(requested), C(approved), C(rejected), C(not requested).
    type: str
    choices: [ requested, approved, rejected, not requested ]
  delivery_plan:
    description:
      - Delivery plan for the catalog request task.
    type: str
  delivery_task:
    description:
      - Delivery task reference for the catalog request task.
    type: str
  other:
    description:
      - Optional remaining parameters.
      - For more information on optional parameters, refer to the ServiceNow
        catalog request task documentation.
    type: dict
"""

EXAMPLES = r"""
- name: Create a catalog request task
  servicenow.itsm.catalog_request_task:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass
    state: present
    request: REQ0000123
    short_description: Configure new laptop
    description: Install required software and configure user settings
    assignment_group: IT Support
    priority: "2"
    urgency: "2"
    impact: "3"
- name: Update catalog request task
  servicenow.itsm.catalog_request_task:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass
    state: present
    number: SCTASK0000456
    task_state: work_in_progress
    assigned_to: john.doe
    work_notes: Started configuration process
- name: Close catalog request task
  servicenow.itsm.catalog_request_task:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass
    state: present
    number: SCTASK0000456
    task_state: closed_complete
    close_notes: Configuration completed successfully
- name: Delete catalog request task
  servicenow.itsm.catalog_request_task:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass
    state: absent
    number: SCTASK0000456
- name: Create catalog request task with other parameters
  servicenow.itsm.catalog_request_task:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass
    state: present
    request: REQ0000123
    short_description: Custom task
    order: 10
    other:
      special_instructions: Handle with care
      vendor: Dell
"""

RETURN = r"""
record:
  description: The catalog request task record.
  returned: success
  type: dict
  sample:
    active: true
    approval: not requested
    assigned_to: "john.doe"
    assignment_group: "IT Support"
    close_notes: ""
    comments: ""
    delivery_plan: ""
    delivery_task: ""
    description: "Install required software and configure user settings"
    due_date: ""
    impact: "3"
    number: "SCTASK0000456"
    opened_at: "2024-01-15 10:30:00"
    opened_by: "jane.smith"
    order: 10
    priority: "2"
    request: "REQ0000123"
    requested_by: "jane.smith"
    requested_for: "john.doe"
    short_description: "Configure new laptop"
    state: "present"
    sys_created_by: "jane.smith"
    sys_created_on: "2024-01-15 10:30:00"
    sys_id: "c36d93a37b1200001c9c9b5b8a9619a9"
    sys_updated_by: "jane.smith"
    sys_updated_on: "2024-01-15 10:30:00"
    task_state: "open"
    urgency: "2"
    work_notes: ""
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, errors, table, utils
from ..module_utils.utils import get_mapper
from ..module_utils.catalog_request_task import PAYLOAD_FIELDS_MAPPING

DIRECT_PAYLOAD_FIELDS = (
    "requested_for",
    "requested_by",
    "assignment_group",
    "assigned_to",
    "priority",
    "urgency",
    "impact",
    "short_description",
    "description",
    "comments",
    "work_notes",
    "due_date",
    "close_notes",
    "order",
    "approval",
    "delivery_plan",
    "delivery_task",
)


def ensure_absent(module, table_client):
    mapper = get_mapper(module, "catalog_request_task_mapping", PAYLOAD_FIELDS_MAPPING)
    query = utils.filter_dict(module.params, "sys_id", "number")
    catalog_request_task = table_client.get_record("sc_task", query, must_exist=False)

    if catalog_request_task:
        table_client.delete_record(
            "sc_task", catalog_request_task, check_mode=module.check_mode
        )
        return (
            True,
            mapper.to_ansible(catalog_request_task),
            dict(before=mapper.to_ansible(catalog_request_task), after=None),
        )

    return False, None, dict(before=None, after=None)


def ensure_present(module, table_client):
    mapper = get_mapper(module, "catalog_request_task_mapping", PAYLOAD_FIELDS_MAPPING)
    query = utils.filter_dict(module.params, "sys_id", "number")
    payload = build_payload(module, table_client)

    if not query:
        # Create new record
        new = mapper.to_ansible(
            table_client.create_record(
                "sc_task", mapper.to_snow(payload), module.check_mode
            )
        )
        return True, new, dict(before=None, after=new)

    old = mapper.to_ansible(table_client.get_record("sc_task", query, must_exist=True))
    if utils.is_superset(old, payload):
        return False, old, dict(before=old, after=old)

    # Update existing record
    new = mapper.to_ansible(
        table_client.update_record(
            "sc_task",
            mapper.to_snow(old),
            mapper.to_snow(payload),
            module.check_mode,
        )
    )
    return True, new, dict(before=old, after=new)


def _lookup_request_sys_id(request_value, table_client):
    # Check if it's a sys_id (32-character hex string) or number
    if len(request_value) == 32 and all(
        c in "0123456789abcdef" for c in request_value.lower()
    ):
        # It's a sys_id
        return table_client.get_record(
            "sc_request", {"sys_id": request_value}, must_exist=True
        )
    else:
        # It's a number
        return table_client.get_record(
            "sc_request", {"number": request_value}, must_exist=True
        )


def build_payload(module, table_client):
    payload = (module.params.get("other") or {}).copy()
    payload.update(utils.filter_dict(module.params, *DIRECT_PAYLOAD_FIELDS))
    if module.params.get("task_state"):
        payload["state"] = module.params["task_state"]

    # Handle catalog request lookup
    if module.params.get("request"):
        catalog_request = _lookup_request_sys_id(module.params["request"], table_client)
        payload["request"] = catalog_request["sys_id"]

    # Handle user lookups
    if module.params.get("requested_for"):
        payload["requested_for"] = table_client.get_record(
            "sys_user", {"user_name": module.params["requested_for"]}, must_exist=True
        )["sys_id"]

    if module.params.get("requested_by"):
        payload["requested_by"] = table_client.get_record(
            "sys_user", {"user_name": module.params["requested_by"]}, must_exist=True
        )["sys_id"]

    if module.params.get("assigned_to"):
        payload["assigned_to"] = table_client.get_record(
            "sys_user", {"user_name": module.params["assigned_to"]}, must_exist=True
        )["sys_id"]

    # Handle group lookup
    if module.params.get("assignment_group"):
        payload["assignment_group"] = table_client.get_record(
            "sys_user_group",
            {"name": module.params["assignment_group"]},
            must_exist=True,
        )["sys_id"]

    return payload


def run(module, table_client):
    if module.params["state"] == "absent":
        return ensure_absent(module, table_client)
    return ensure_present(module, table_client)


def main():
    module_args = dict(
        arguments.get_spec(
            "instance",
            "sys_id",
            "number",
            "attachments",
            "catalog_request_task_mapping",
        ),
        state=dict(
            type="str",
            choices=["present", "absent"],
            default="present",
        ),
        task_state=dict(
            type="str",
            choices=[
                "pending",
                "open",
                "work_in_progress",
                "closed_complete",
                "closed_incomplete",
                "closed_skipped",
            ],
        ),
        request=dict(type="str"),
        requested_for=dict(type="str"),
        requested_by=dict(type="str"),
        assignment_group=dict(type="str"),
        assigned_to=dict(type="str"),
        priority=dict(
            type="str",
            choices=["1", "2", "3", "4", "5"],
        ),
        urgency=dict(
            type="str",
            choices=["1", "2", "3"],
        ),
        impact=dict(
            type="str",
            choices=["1", "2", "3"],
        ),
        short_description=dict(type="str"),
        description=dict(type="str"),
        comments=dict(type="str"),
        work_notes=dict(type="str"),
        due_date=dict(type="str"),
        close_notes=dict(type="str"),
        order=dict(type="int"),
        approval=dict(
            type="str",
            choices=["requested", "approved", "rejected", "not requested"],
        ),
        delivery_plan=dict(type="str"),
        delivery_task=dict(type="str"),
        other=dict(type="dict"),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("sys_id", "number"), True),
        ],
    )

    try:
        snow_client = client.Client(**module.params["instance"])
        table_client = table.TableClient(snow_client)
        changed, record, diff = run(module, table_client)
        module.exit_json(changed=changed, record=record, diff=diff)
    except errors.ServiceNowError as e:
        module.fail_json(**e.to_module_fail_json_output())


if __name__ == "__main__":
    main()
