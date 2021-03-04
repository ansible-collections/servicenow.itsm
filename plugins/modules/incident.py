#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: incident

author:
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)

short_description: Manage ServiceNow incidents

description:
  - Create, delete or update a ServiceNow incident.
  - For more information, refer to the ServiceNow incident management documentation at
    U(https://docs.servicenow.com/bundle/paris-it-service-management/page/product/incident-management/concept/c_IncidentManagement.html).

extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id
  - servicenow.itsm.number

options:
  state:
    description:
      - State of incident.
      - If I(state) value is C(on_hold), I(on_hold_reason) parameter must be filled in.
    choices: [ new, in_progress, on_hold, resolved, closed, canceled, absent ]
    type: str
  hold_reason:
    description:
      - Reason why incident is on hold.
      - Required if I(state) value is C(on_hold).
    choices: [ awaiting_caller, awaiting_change, awaiting_problem, awaiting_vendor ]
    type: str
  caller:
    description:
      - A person who reported or is affected by this incident.
      - Expected value for I(caller) is user id (usually in the form of
        C(first_name.last_name)).
      - Required if the incident does not exist yet.
    type: str
  short_description:
    description:
      - Short description of the incident.
      - Required if the incident does not exist yet.
    type: str
  description:
    description:
      - Long description of the incident with some more details.
    type: str
  impact:
    description:
      - The measure of the business criticality of the affected service.
    choices: [ low, medium, high ]
    type: str
  urgency:
    description:
      - The extent to which resolution of an incident can bear delay.
    choices: [ low, medium, high ]
    type: str
  close_code:
    description:
      - Provide information on how the incident was resolved.
    choices: [ Solved (Work Around), Solved (Permanently),
               Solved Remotely (Work Around), Solved Remotely (Permanently),
               Not Solved (Not Reproducible), Not Solved (Too Costly),
               Closed/Resolved by Caller ]
    type: str
  close_notes:
    description:
      - Resolution notes added by the user who closed the incident.
    type: str
  other:
    description:
      - Optional remaining parameters.
      - For more information on optional parameters, refer to the ServiceNow
        create incident documentation at
        U(https://docs.servicenow.com/bundle/paris-it-service-management/page/product/incident-management/task/create-an-incident.html).
    type: dict
"""

EXAMPLES = r"""
- name: Create incident
  servicenow.itsm.incident:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass

    state: new
    caller: some.user
    short_description: User is not receiving email
    description: User has been unable to receive email for the past 15 minutes
    impact: low
    urgency: low

    other:
      expected_start: 2021-02-12

- name: Change state of the incident
  servicenow.itsm.incident:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass

    state: in_progress
    number: INC0000001

- name: Close incident
  servicenow.itsm.incident:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass

    state: closed
    number: INC0000001
    close_code: "Solved (Permanently)"
    close_notes: "Closed"

- name: Delete incident
  servicenow.itsm.incident:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass

    state: absent
    number: INC0000001
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, errors, table, utils, validation
from ..module_utils.incident import PAYLOAD_FIELDS_MAPPING

DIRECT_PAYLOAD_FIELDS = (
    "state",
    "hold_reason",
    "short_description",
    "description",
    "impact",
    "urgency",
    "close_code",
    "close_notes",
)


def ensure_absent(module, table_client):
    mapper = utils.PayloadMapper(PAYLOAD_FIELDS_MAPPING)
    query = utils.filter_dict(module.params, "sys_id", "number")
    incident = table_client.get_record("incident", query)

    if incident:
        table_client.delete_record("incident", incident, module.check_mode)
        return True, None, dict(before=mapper.to_ansible(incident), after=None)

    return False, None, dict(before=None, after=None)


def build_payload(module, table_client):
    payload = (module.params["other"] or {}).copy()
    payload.update(utils.filter_dict(module.params, *DIRECT_PAYLOAD_FIELDS))

    if module.params["caller"]:
        user = table.find_user(table_client, module.params["caller"])
        payload["caller_id"] = user["sys_id"]

    return payload


def validate_params(params, incident=None):
    missing = []
    if params["state"] in ("resolved", "closed"):
        missing.extend(
            validation.missing_from_params_and_remote(
                ("close_code", "close_notes"), params, incident
            )
        )

    if missing:
        raise errors.ServiceNowError(
            "Missing required parameters {0}".format(", ".join(missing))
        )


def ensure_present(module, table_client):
    mapper = utils.PayloadMapper(PAYLOAD_FIELDS_MAPPING)
    query = utils.filter_dict(module.params, "sys_id", "number")
    payload = build_payload(module, table_client)

    if not query:
        # User did not specify existing incident, so we need to create a new one.
        validate_params(module.params)
        new = mapper.to_ansible(
            table_client.create_record(
                "incident", mapper.to_snow(payload), module.check_mode
            )
        )
        return True, new, dict(before=None, after=new)

    old = mapper.to_ansible(table_client.get_record("incident", query, must_exist=True))
    if utils.is_superset(old, payload):
        # No change in parameters we are interested in - nothing to do.
        return False, old, dict(before=old, after=old)

    validate_params(module.params, old)
    new = mapper.to_ansible(
        table_client.update_record(
            "incident", mapper.to_snow(old), mapper.to_snow(payload), module.check_mode
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
                "in_progress",
                "on_hold",
                "resolved",
                "closed",
                "canceled",
                "absent",
            ],
        ),
        hold_reason=dict(
            type="str",
            choices=[
                "awaiting_caller",
                "awaiting_change",
                "awaiting_problem",
                "awaiting_vendor",
            ],
        ),
        caller=dict(
            type="str",
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
        close_code=dict(
            type="str",
            choices=[
                "Solved (Work Around)",
                "Solved (Permanently)",
                "Solved Remotely (Work Around)",
                "Solved Remotely (Permanently)",
                "Not Solved (Not Reproducible)",
                "Not Solved (Too Costly)",
                "Closed/Resolved by Caller",
            ],
        ),
        close_notes=dict(
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
            ("state", "on_hold", ("hold_reason",)),
        ],
        # If there is no sys id or number create a new ticket
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
