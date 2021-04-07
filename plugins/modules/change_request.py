#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: change_request

author:
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)

short_description: Manage ServiceNow change requests

description:
  - Create, delete or update a ServiceNow change request.
  - For more information, refer to the ServiceNow change management documentation at
    U(https://docs.servicenow.com/bundle/paris-it-service-management/page/product/change-management/concept/c_ITILChangeManagement.html).
version_added: 1.0.0
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id
  - servicenow.itsm.number

seealso:
  - module: servicenow.itsm.change_request_info

options:
  state:
    description:
      - The state of the change request.
      - If I(state) value is C(assess) or C(authorize) or C(scheduled) or
        C(implement) or C(review) or C(closed),
        I(assignment_group) parameter must be filled in.
      - For more information on state model and transition,
        refere to the ServiceNow documentation at
        U(https://docs.servicenow.com/bundle/paris-it-service-management/page/product/change-management/concept/c_ChangeStateModel.html)
    choices: [ new, assess, authorize, scheduled,
               implement, review, closed, canceled, absent ]
    type: str
  type:
    description:
      - Specify what type of change is required.
    choices: [ standard, normal, emergency ]
    type: str
  template:
    description:
      - Predefined template name for standard change request.
      - For more information on templates refer to ServiceNow documentation at
        U(https://docs.servicenow.com/bundle/quebec-it-service-management/page/product/change-management/concept/c_StandardChangeCatalogPlugin.html)
        or find template names on <your_service_id>.service-now.com/nav_to.do?uri=%2Fstd_change_producer_version_list.do%3F
    type: str
  requested_by:
    description:
      - User who requested the change.
    type: str
  assignment_group:
    description:
      - The group that the change request is assigned to.
      - Required if I(state) value is C(assess) or C(authorize) or
        C(scheduled) or C(implement) or C(review) or C(closed).
    type: str
  category:
    description:
      - The category of the change request.
    choices: [ hardware, software, service, system_software, aplication_software,
               network, telecom, documentation, other ]
    type: str
  priority:
    description:
      - Priority is based on impact and urgency, and it identifies how quickly
        the service desk should address the task.
    choices: [ critical, high, moderate, low ]
    type: str
  risk:
    description:
      - The risk level for the change.
    choices: [ high, moderate, low ]
    type: str
  impact:
    description:
      - Impact is a measure of the effect of an incident, problem,
        or change on business processes.
    choices: [ high, medium, low ]
    type: str
  urgency:
    description:
      - The extent to which resolution of an change request can bear delay.
    choices: [ low, medium, high ]
    type: str
  short_description:
    description:
      - A summary of the change request.
    type: str
  description:
    description:
      - A detailed description of the change request.
    type: str
  close_code:
    description:
      - Provide information on how the change request was resolved.
      - The change request must have this parameter set prior to
        transitioning to the C(closed) state.
    choices: [ successful, successful_issues, unsuccessful ]
    type: str
  close_notes:
    description:
      - Resolution notes added by the user who closed the change request.
      - The change request must have this parameter set prior to
        transitioning to the C(closed) state.
    type: str
  on_hold:
    description:
      - A change request can be put on hold when I(state)
        is not in the C(new), C(canceled), or C(closed).
    type: bool
  hold_reason:
    description:
      - Reason why change request is on hold.
      - Required if change request's I(on_hold) value will be C(true).
    type: str
  other:
    description:
      - Optional remaining parameters.
      - For more information on optional parameters, refer to the ServiceNow
        change request documentation at
        U(https://docs.servicenow.com/bundle/paris-it-service-management/page/product/change-management/task/t_CreateAChange.html).
    type: dict
"""

EXAMPLES = """
- name: Create change request
  servicenow.itsm.change_request:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass

    type: standard
    state: new
    requested_by: some.user
    short_description: Install new Cisco
    description: Please install new Cat. 6500 in Data center 01
    priority: moderate
    risk: low
    impact: low

    other:
      expected_start: 2021-02-12

- name: Change state of the change request
  servicenow.itsm.change_request:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass

    state: assess
    assignment_group: some.group
    number: CHG0000001

- name: Close change_request
  servicenow.itsm.change_request:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass

    state: closed
    close_code: "successful"
    close_notes: "Closed"
    assignment_group: some.group
    number: CHG0000001

- name: Delete change_request
  servicenow.itsm.change_request:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass

    state: absent
    number: CHG0000001
"""


from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, table, errors, utils, validation
from ..module_utils.change_request import PAYLOAD_FIELDS_MAPPING


DIRECT_PAYLOAD_FIELDS = (
    "state",
    "type",
    "requested_by",
    "assignment_group",
    "category",
    "priority",
    "risk",
    "impact",
    "short_description",
    "description",
    "close_code",
    "close_notes",
    "on_hold",
    "hold_reason",
)


def ensure_absent(module, table_client):
    mapper = utils.PayloadMapper(PAYLOAD_FIELDS_MAPPING, module.warn)
    query = utils.filter_dict(module.params, "sys_id", "number")
    change = table_client.get_record("change_request", query)

    if change:
        table_client.delete_record("change_request", change, module.check_mode)
        return True, None, dict(before=mapper.to_ansible(change), after=None)

    return False, None, dict(before=None, after=None)


def validate_params(params, change_request=None):
    missing = []
    if params["state"] == "closed":
        missing.extend(
            validation.missing_from_params_and_remote(
                ("close_code", "close_notes"), params, change_request
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
        # User did not specify existing change request, so we need to create a new one.
        validate_params(module.params)
        new = mapper.to_ansible(
            table_client.create_record(
                "change_request", mapper.to_snow(payload), module.check_mode
            )
        )
        return True, new, dict(before=None, after=new)

    old = mapper.to_ansible(
        table_client.get_record("change_request", query, must_exist=True)
    )
    if utils.is_superset(old, payload):
        # No change in parameters we are interested in - nothing to do.
        return False, old, dict(before=old, after=old)

    validate_params(module.params, old)
    new = mapper.to_ansible(
        table_client.update_record(
            "change_request",
            mapper.to_snow(old),
            mapper.to_snow(payload),
            module.check_mode,
        )
    )
    return True, new, dict(before=old, after=new)


def build_payload(module, table_client):
    payload = (module.params["other"] or {}).copy()
    payload.update(utils.filter_dict(module.params, *DIRECT_PAYLOAD_FIELDS))

    # The change model is set to the same value as the change type
    # as the standard change request requires the model to be set.
    # For that reason change model is set for every type of change request.
    if module.params["type"]:
        payload["chg_model"] = payload["type"]

    if module.params["hold_reason"]:
        payload["on_hold_reason"] = module.params["hold_reason"]

    if module.params["requested_by"]:
        user = table.find_user(table_client, module.params["requested_by"])
        payload["requested_by"] = user["sys_id"]

    if module.params["assignment_group"]:
        assignment_group = table.find_assignment_group(
            table_client, module.params["assignment_group"]
        )
        payload["assignment_group"] = assignment_group["sys_id"]

    if module.params["template"]:
        standard_change_template = table.find_standard_change_template(
            table_client, module.params["template"]
        )
        payload["std_change_producer_version"] = standard_change_template["sys_id"]

    return payload


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
                "authorize",
                "scheduled",
                "implement",
                "review",
                "closed",
                "canceled",
                "absent",
            ],
        ),
        type=dict(
            type="str",
            choices=[
                "standard",
                "normal",
                "emergency",
            ],
        ),
        template=dict(
            type="str",
        ),
        requested_by=dict(
            type="str",
        ),
        assignment_group=dict(
            type="str",
        ),
        category=dict(
            type="str",
            choices=[
                "hardware",
                "software",
                "service",
                "system_software",
                "aplication_software",
                "network",
                "telecom",
                "documentation",
                "other",
            ],
        ),
        priority=dict(
            type="str",
            choices=[
                "critical",
                "high",
                "moderate",
                "low",
            ],
        ),
        risk=dict(
            type="str",
            choices=[
                "high",
                "moderate",
                "low",
            ],
        ),
        impact=dict(
            type="str",
            choices=[
                "high",
                "medium",
                "low",
            ],
        ),
        urgency=dict(
            type="str",
            choices=["high", "medium", "low"],
        ),
        short_description=dict(
            type="str",
        ),
        description=dict(
            type="str",
        ),
        close_code=dict(
            type="str",
            choices=[
                "successful",
                "successful_issues",
                "unsuccessful",
            ],
        ),
        close_notes=dict(
            type="str",
        ),
        on_hold=dict(
            type="bool",
        ),
        hold_reason=dict(
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
            ("state", "authorize", ("assignment_group",)),
            ("state", "scheduled", ("assignment_group",)),
            ("state", "assess", ("assignment_group",)),
            ("state", "on_hold", ("hold_reason",)),
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
