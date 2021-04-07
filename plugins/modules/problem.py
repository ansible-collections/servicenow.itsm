#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: problem

author:
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)

short_description: Manage ServiceNow problems

description:
  - Create, delete or update a ServiceNow problem.
  - For more information, refer to the ServiceNow problem management documentation at
    U(https://docs.servicenow.com/bundle/paris-it-service-management/page/product/problem-management/concept/c_ProblemManagement.html).
version_added: 1.0.0
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id
  - servicenow.itsm.number

seealso:
  - module: servicenow.itsm.problem_info

options:
  state:
    description:
      - State of the problem.
      - If a problem does not yet exist, all states except for C(new)
        require setting of I(assigned_to) parameter.
    choices: [ new, assess, root_cause_analysis, fix_in_progress, resolved, closed, absent ]
    type: str
  short_description:
    description:
      - Short description of the problem that the problem-solving team should address.
      - Required if the problem does not exist yet.
    type: str
  description:
    description:
      - Detailed description of the problem.
    type: str
  impact:
    description:
      - Effect that the problem has on business.
    choices: [ low, medium, high ]
    type: str
  urgency:
    description:
      - The extent to which the problem resolution can bear delay.
    choices: [ low, medium, high ]
    type: str
  assigned_to:
    description:
      - A person who will assess this problem.
      - Expected value for I(assigned_to) is user id (usually in the form of
        C(first_name.last_name)).
      - This field is required when creating new problems for all problem
        I(state)s except C(new).
    type: str
  resolution_code:
    description:
      - The reason for problem resolution.
    choices: [ fix_applied, risk_accepted, duplicate, canceled ]
    type: str
  cause_notes:
    description:
      - Provide information on what caused the problem.
      - Required if I(state) is C(in_progress).
      - Required if I(state) is C(resolved) or C(closed) and I(resolution_code)
        is C(fix_applied) or C(risk_accepted).
    type: str
  close_notes:
    description:
      - The reason for closing the problem.
      - Required if I(state) is C(resolved) or C(closed) and I(resolution_code)
        is C(risk_accepted) or C(canceled).
    type: str
  fix_notes:
    description:
      - Notes on how the problem was fixed.
      - Required if I(state) is C(in_progress).
      - Required if I(state) is C(resolved) or C(closed) and I(resolution_code)
        is C(fix_applied).
    type: str
  duplicate_of:
    description:
      - Number of the problem of which this problem is a duplicate of.
      - Required if I(state) is C(resolved) or C(closed) and I(resolution_code)
        is C(duplicate).
    type: str
  other:
    description:
      - Optional remaining parameters.
      - For more information on optional parameters, refer to the ServiceNow
        documentation on creating problems at
        U(https://docs.servicenow.com/bundle/paris-it-service-management/page/product/problem-management/task/create-a-problem-v2.html).
    type: dict
"""

EXAMPLES = r"""
- name: Create a problem
  servicenow.itsm.problem:
    state: new
    short_description: Issue with the network printer
    description: Since this morning, all printer jobs are stuck.
    impact: medium
    urgency: low
    other:
      user_input: notes

- name: Assign a problem to a user for assessment
  servicenow.itsm.problem:
    number: PRB0000010
    state: assess
    assigned_to: problem.manager

- name: Mark a problem for root cause analysis
  servicenow.itsm.problem:
    number: PRB0000010
    state: root_cause_analysis

- name: Work on fixing a problem
  servicenow.itsm.problem:
    number: PRB0000010
    state: fix_in_progress
    cause_notes: I identified the issue.
    fix_notes: Fix here.


- name: Close a problem as fixed
  servicenow.itsm.problem:
    number: PRB0000010
    state: closed
    resolution_code: fix_applied
    cause_notes: I found that this doesn't work.
    fix_notes: I solved it like this.

- name: Close a problem as duplicate
  servicenow.itsm.problem:
    number: PRB0000010
    state: closed
    resolution_code: duplicate
    duplicate_of: PRB0000001

- name: Cancel a problem
  servicenow.itsm.problem:
    number: PRB0000010
    state: closed
    resolution_code: canceled
    close_notes: The problem seems to have resolved itself.

- name: Delete a problem
  servicenow.itsm.problem:
    number: PRB0000010
    state: absent
"""

RETURN = r"""
record:
  description:
    - The problem record.
  returned: success
  type: dict
  sample:
    "active": "true"
    "activity_due": ""
    "additional_assignee_list": ""
    "approval": "not requested"
    "approval_history": ""
    "approval_set": ""
    "assigned_to": "73ab3f173b331300ad3cc9bb34efc4df"
    "assignment_group": ""
    "business_duration": ""
    "business_service": ""
    "calendar_duration": ""
    "category": "software"
    "cause_notes": ""
    "close_notes": ""
    "closed_at": ""
    "closed_by": ""
    "cmdb_ci": "27d32778c0a8000b00db970eeaa60f16"
    "comments": ""
    "comments_and_work_notes": ""
    "company": ""
    "confirmed_at": ""
    "confirmed_by": ""
    "contact_type": ""
    "contract": ""
    "correlation_display": ""
    "correlation_id": ""
    "delivery_plan": ""
    "delivery_task": ""
    "description": "Unable to send or receive emails."
    "due_date": ""
    "duplicate_of": ""
    "escalation": "0"
    "expected_start": ""
    "first_reported_by_task": ""
    "fix_communicated_at": ""
    "fix_communicated_by": ""
    "fix_notes": ""
    "follow_up": ""
    "group_list": ""
    "impact": "low"
    "knowledge": "false"
    "known_error": "false"
    "location": ""
    "made_sla": "true"
    "major_problem": "false"
    "number": "PRB0007601"
    "opened_at": "2018-08-30 08:08:39"
    "opened_by": "6816f79cc0a8016401c5a33be04be441"
    "order": ""
    "parent": ""
    "priority": "5"
    "problem_state": "new"
    "reassignment_count": "0"
    "related_incidents": "0"
    "reopen_count": "0"
    "reopened_at": ""
    "reopened_by": ""
    "resolution_code": ""
    "resolved_at": ""
    "resolved_by": ""
    "review_outcome": ""
    "rfc": ""
    "route_reason": ""
    "service_offering": ""
    "short_description": "Unable to send or receive emails."
    "sla_due": ""
    "state": "new"
    "subcategory": "email"
    "sys_class_name": "problem"
    "sys_created_by": "admin"
    "sys_created_on": "2018-08-30 08:09:05"
    "sys_domain": "global"
    "sys_domain_path": "/"
    "sys_id": "62304320731823002728660c4cf6a7e8"
    "sys_mod_count": "1"
    "sys_tags": ""
    "sys_updated_by": "admin"
    "sys_updated_on": "2018-12-12 07:16:57"
    "task_effective_number": "PRB0007601"
    "time_worked": ""
    "universal_request": ""
    "upon_approval": "proceed"
    "upon_reject": "cancel"
    "urgency": "low"
    "user_input": ""
    "watch_list": ""
    "work_end": ""
    "work_notes": ""
    "work_notes_list": ""
    "work_start": ""
    "workaround": ""
    "workaround_applied": "false"
    "workaround_communicated_at": ""
    "workaround_communicated_by": ""
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, errors, table, utils, validation
from ..module_utils.problem import PAYLOAD_FIELDS_MAPPING

DIRECT_PAYLOAD_FIELDS = (
    "state",
    "short_description",
    "description",
    "impact",
    "urgency",
    "resolution_code",
    "fix_notes",
    "cause_notes",
    "close_notes",
)


def ensure_absent(module, table_client):
    mapper = utils.PayloadMapper(PAYLOAD_FIELDS_MAPPING, module.warn)
    query = utils.filter_dict(module.params, "sys_id", "number")
    problem = table_client.get_record("problem", query)

    if problem:
        table_client.delete_record("problem", problem, module.check_mode)
        return True, None, dict(before=mapper.to_ansible(problem), after=None)

    return False, None, dict(before=None, after=None)


def build_payload(module, table_client):
    payload = (module.params["other"] or {}).copy()
    payload.update(utils.filter_dict(module.params, *DIRECT_PAYLOAD_FIELDS))

    if module.params["state"]:
        # If we set 'state' field directly when modifying an existing record,
        # ServiceNow API sometimes ignores the desired state.
        # This happens for state transitions other than new -> assessment.
        # Using 'problem_state' instead of 'state' resovles the issue.
        payload["problem_state"] = module.params["state"]
    if module.params["assigned_to"]:
        user = table.find_user(table_client, module.params["assigned_to"])
        payload["assigned_to"] = user["sys_id"]
    if module.params["duplicate_of"]:
        problem = table_client.get_record(
            "problem",
            query=dict(number=module.params["duplicate_of"]),
            must_exist=True,
        )
        payload["duplicate_of"] = problem["sys_id"]

    return payload


def validate_params(params, problem=None):
    # Validation is compliant with the data policies described at
    # https://docs.servicenow.com/bundle/madrid-release-notes/page/release-notes/it-service-management/problem-management-rn.html
    # If we do not enforce this, the user gets 403 on invalid input.
    state = params["state"]
    missing = []
    if state in ("new", "assessment", "analysis", "in_progress", "resolved", "closed"):
        missing.extend(
            validation.missing_from_params_and_remote(
                ["short_description"], params, problem
            )
        )
    if state in ("assessment", "analysis", "in_progress", "resolved", "closed"):
        missing.extend(
            validation.missing_from_params_and_remote(["assigned_to"], params, problem)
        )
    if state in ("resolved", "closed"):
        missing.extend(
            validation.missing_from_params_and_remote(
                ["resolution_code"], params, problem
            )
        )
    if state == "in_progress":
        missing.extend(
            validation.missing_from_params_and_remote(
                ["cause_notes", "fix_notes"], params, problem
            )
        )
    resolution_params = dict(
        fix_applied=["cause_notes", "fix_notes"],
        risk_accepted=["cause_notes", "close_notes"],
        canceled=["close_notes"],
        duplicate=["duplicate_of"],
    )
    if params["resolution_code"]:
        missing.extend(
            validation.missing_from_params_and_remote(
                resolution_params[params["resolution_code"]], params, problem
            )
        )

    if missing:
        raise errors.ServiceNowError(
            "Missing required parameters {0}".format(", ".join(missing))
        )


def ensure_present(module, table_client):
    mapper = utils.PayloadMapper(PAYLOAD_FIELDS_MAPPING, module.warn)
    query = utils.filter_dict(module.params, "sys_id", "number")
    payload = build_payload(module, table_client)

    if not query:
        # User did not specify existing problem, so we need to create a new one.
        validate_params(module.params)
        new = mapper.to_ansible(
            table_client.create_record(
                "problem", mapper.to_snow(payload), module.check_mode
            )
        )
        return True, new, dict(before=None, after=new)

    old = mapper.to_ansible(table_client.get_record("problem", query, must_exist=True))
    if utils.is_superset(old, payload):
        # No change in parameters we are interested in - nothing to do.
        return False, old, dict(before=old, after=old)

    validate_params(module.params, old)
    new = mapper.to_ansible(
        table_client.update_record(
            "problem", mapper.to_snow(old), mapper.to_snow(payload), module.check_mode
        )
    )
    return True, new, dict(before=old, after=new)


def run(module, table_client):
    if module.params["state"] == "absent":
        return ensure_absent(module, table_client)
    return ensure_present(module, table_client)


def main():
    module_args = dict(
        arguments.get_spec("instance", "sys_id", "number"),
        state=dict(
            type="str",
            choices=[
                "new",
                "assess",
                "root_cause_analysis",
                "fix_in_progress",
                "resolved",
                "closed",
                "absent",
            ],
        ),
        short_description=dict(
            type="str",
        ),
        description=dict(
            type="str",
        ),
        impact=dict(
            type="str",
            choices=[
                "low",
                "medium",
                "high",
            ],
        ),
        urgency=dict(
            type="str",
            choices=[
                "low",
                "medium",
                "high",
            ],
        ),
        assigned_to=dict(
            type="str",
        ),
        resolution_code=dict(
            type="str",
            choices=[
                "fix_applied",
                "risk_accepted",
                "duplicate",
                "canceled",
            ],
        ),
        cause_notes=dict(
            type="str",
        ),
        close_notes=dict(
            type="str",
        ),
        fix_notes=dict(
            type="str",
        ),
        duplicate_of=dict(
            type="str",
        ),
        other=dict(
            type="dict",
        ),
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
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
