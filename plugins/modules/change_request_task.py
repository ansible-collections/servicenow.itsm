#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: change_request_task

author:
  - Matej Pevec (@mysteriouswolf)
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)

short_description: Manage ServiceNow change request tasks

description:
  - Create, delete or update a ServiceNow change request tasks.
  - For more information, refer to the ServiceNow change management documentation at
    U(https://docs.servicenow.com/bundle/paris-it-service-management/page/product/change-management/concept/c_ITILChangeManagement.html).
version_added: 1.0.0
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id
  - servicenow.itsm.number

seealso:
  - module: servicenow.itsm.change_request_task_info

options:
  configuration_item:
    description:
      - The configuration item (CI) or service that the change task applies to.
    type: str
  type:
    description:
      - The type of change task.
      - Default workflow generates tasks in I(type) C(review)
    choices: [ planning, implementation, testing, review ]
    type: str
  state:
    description:
      - The state of the change request task.
    choices: [ pending, open, in_progress, closed, canceled ]
    type: str
  assigned_to:
    description:
      - The user that the change task is assigned to.
    type: str
  assignment_group:
    description:
      - The group that the change task is assigned to.
    type: str
  short_description:
    description:
      - A summary of the task.
    type: str
  description:
    description:
      - A detailed description of the task.
    type: str
  on_hold:
    description:
      - A change task can be put on hold when I(state)
        is not in the C(pending), C(canceled), or C(closed).
      - Provide an On hold reason if a change task is placed on hold.
    type: bool
  hold_reason:
    description:
      - Reason why change task is on hold.
      - Required if change task's I(on_hold) value will be C(true).
    type: str
  planned_start_date:
    description:
      - The date you plan to begin working on the task.
    type: datetime
  planned_end_date:
    description:
      - The date the change task is planned to be completed.
      - If the task I(type) is C(implementation), the I(planned_start_date) and I(planned_end_date) values 
      must fall within the planned start and end dates specified in the I(change_request).
    type: datetime
  
"""

# TODO Check whether datetime type exists
# TODO Check for more potentially useful fields

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
"""

# TODO Add actual examples
