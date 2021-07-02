#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: change_request_task_info

author:
  - Matej Pevec (@mysteriouswolf)
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)
  
short_description: List ServiceNow change request tasks
description:
  - Retrieve information about ServiceNow change request tasks.
  - For more information, refer to the ServiceNow change management documentation at
    U(https://docs.servicenow.com/bundle/paris-it-service-management/page/product/change-management/concept/c_ITILChangeManagement.html).
version_added: 1.0.0
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id.info
  - servicenow.itsm.number.info
  - servicenow.itsm.query
seealso:
  - module: servicenow.itsm.change_request_task
"""

EXAMPLES = r"""
- name: Retrieve all change request tasks
  servicenow.itsm.change_request_task_info:
  register: result

- name: Retrieve a specific change request task by its sys_id
  servicenow.itsm.change_request_task_info:
    sys_id: 471bfbc7a9fe198101e77a3e10e5d47f
  register: result

- name: Retrieve change request tasks by number
  servicenow.itsm.change_request_task_info:
    number: TASK0000001
  register: result

- name: Retrieve change request tasks that contain SAP in their short description
  servicenow.itsm.change_request_task_info:
    query:
      - short_description: LIKE SAP
  register: result

- name: Retrieve new change requests assigned to abel.tuter or bertie.luby
  servicenow.itsm.change_request_task_info:
    query:
      - state: = new
        assigned_to: = abel.tuter
      - state: = new
        assigned_to: = bertie.luby
"""

RETURN = r"""
records:
  description:
    - A list of change request records.
  returned: success
  type: list
  sample:
    - TBD
"""