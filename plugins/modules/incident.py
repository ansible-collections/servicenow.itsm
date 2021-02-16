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

options:
  state:
    description:
      - State of incident.
      - If I(state) value is C(on_hold), I(on_hold_reason) parameter must be filled in.
    choices: [ new, in_progress, on_hold, resolved, closed, canceled, absent ]
    type: str
  on_hold_reason:
    description:
      - Reason why incident is on hold.
      - Required if I(state) value is C(on_hold).
    choices: [ awaiting_caller, awaiting_change, awaiting_problem, awaiting_vendor ]
    type: str
  caller_id:
    description:
      - A person who reported or is affected by this incident.
      - Expected value for I(caller_id) is user id.
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
      host: instance_id.service-now.com
      username: user
      password: pass

    state: new
    caller_id: some.user
    short_description: User is not receiving email
    description: User has been unable to receive email for the past 15 minutes
    impact: low
    urgency: low

    other:
      expected_start: 2021-02-12

- name: Change state of the incident
  servicenow.itsm.incident:
    instance:
      host: instance_id.service-now.com
      username: user
      password: pass

    state: in_progress
    number: INC0000001

- name: Close incident
  servicenow.itsm.incident:
    instance:
      host: instance_id.service-now.com
      username: user
      password: pass

    state: closed
    number: INC0000001

- name: Delete incident
  servicenow.itsm.incident:
    instance:
      host: instance_id.service-now.com
      username: user
      password: pass

    state: absent
    number: INC0000001
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments


def main():
    module_args = dict(
        arguments.get_spec("instance"),
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
        on_hold_reason=dict(
            type="str",
            choices=[
                "awaiting_caller",
                "awaiting_change",
                "awaiting_problem",
                "awaiting_vendor",
            ],
        ),
        caller_id=dict(
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
        other=dict(
            type="dict",
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    module.exit_json(changed=False, object=None)


if __name__ == "__main__":
    main()
