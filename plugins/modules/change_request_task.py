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
  change_request_id:
    description:
      - I(sys_id) of the change request this task belongs to.
      - Mutually exclusive with I(change_request_number).
    type: str
  change_request_number:
    description:
      - I(number) of the change request this task belongs to.
      - Mutually exclusive with I(change_request_id).
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
    choices: [ pending, open, in_progress, closed, canceled, absent ]
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
  close_code:
    description:
      - Provide information on how the change task was resolved.
      - The change task must have this parameter set prior to
        transitioning to the C(closed) state.
    choices: [ successful, successful_issues, unsuccessful ]
    type: str
  close_notes:
    description:
      - Resolution notes added by the user who closed the change task.
      - The change task must have this parameter set prior to
        transitioning to the C(closed) state.
    type: str
"""

EXAMPLES = """
- name: Create a change task
  servicenow.itsm.change_request_task:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass

    configuration_item: Rogue Squadron Launcher
    change_request_number: CHG0000001
    type: planning
    state: open
    assigned_to: fred.luddy
    assignment_group: robot.embedded
    short_description: Implement collision avoidance
    description: "Implement collision avoidance based on the newly installed TOF sensor arrays."
    on_hold: true
    hold_reason: "Waiting for a report from the hardware team"
    planned_start_date: 2021-07-15 08:00:00
    planned_end_date: 2021-07-21 16:00:00
  
- name: Change state of the change task
  servicenow.itsm.change_request_task:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass

    state: in_progress
    on_hold: false
    number: CTASK0000001

- name: Close a change task
  servicenow.itsm.change_request_task:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass

    state: closed
    close_code: "successful"
    close_notes: "Closed"
    number: CTASK0000001

- name: Delete a change task
  servicenow.itsm.change_request_task:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass

    state: absent
    number: CTASK0000001
"""