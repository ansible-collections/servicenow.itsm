# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  mapping:
    version_added: "1.3.0"
    description:
      - Optional parameters where user can override Choice Lists values for objects.
      - Currently, only values inside incident object mapping can be overridden.
    type: dict
    suboptions:
      incident:
        description:
          - User mappings for Incident object.
          - Where mapping is not set, the default will be used.
        type: dict
        suboptions:
          hold_reason:
            description:
              - Reason why incident is on hold.
              - Required if I(state) value is C(on_hold).
            type: dict
          impact:
            description:
              - The measure of the business criticality of the affected service.
            type: dict
          state:
            description:
              - State of the incident.
              - If I(state) value is C(on_hold), I(on_hold_reason) parameter must be filled in.
              - Special value that can not be overridden is C(absent), which would remove an incident from ServiceNow.
            type: dict
          urgency:
            description:
              - The extent to which resolution of an incident can bear delay.
            type: dict
      change_request:
        description:
          - User mappings for Change request object.
          - Where mapping is not set, the default will be used.
        type: dict
        suboptions:
          priority:
            description:
              - Priority is based on impact and urgency, and it identifies how quickly the service desk should address the task.
            type: dict
          risk:
            description:
              - The risk level for the change.
            type: dict
          impact:
            description:
              - Impact is a measure of the effect of an incident, problem,
                or change on business processes.
            type: dict
          urgency:
            description:
              - The extent to which resolution of an change request can bear delay.
            type: dict
          state:
            description:
              - The state of the change request.
              - If I(state) value is C(assess) or C(authorize) or C(scheduled) or
                C(implement) or C(review) or C(closed),
                I(assignment_group) parameter must be filled in. In case that any field is renamed,
                that check is not performed there.
              - For more information on state model and transition,
                refer to the ServiceNow documentation at
                U(https://docs.servicenow.com/bundle/paris-it-service-management/page/product/change-management/concept/c_ChangeStateModel.html)
              - Special value that can not be overridden is C(absent), which would remove a change request from ServiceNow.
            type: dict
"""
