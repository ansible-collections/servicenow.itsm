# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import env_fallback
from .instance_config import get_instance_module_spec

INCIDENT_MAPPING_SPEC = dict(
    type="dict",
    required=False,
    options=dict(
        state=dict(type="dict"),
        hold_reason=dict(type="dict"),
        impact=dict(type="dict"),
        urgency=dict(type="dict"),
        close_code=dict(type="dict"),
    ),
)

CHANGE_REQUEST_MAPPING_SPEC = dict(
    type="dict",
    required=False,
    options=dict(
        priority=dict(type="dict"),
        risk=dict(type="dict"),
        impact=dict(type="dict"),
        urgency=dict(type="dict"),
        state=dict(type="dict"),
        category=dict(type="dict"),
    ),
)


CHANGE_REQUEST_TASK_MAPPING_SPEC = dict(
    type="dict",
    required=False,
    options=dict(
        state=dict(type="dict"),
    ),
)


CONFIGURATION_ITEM_MAPPING_SPEC = dict(
    type="dict",
    required=False,
    options=dict(
        environment=dict(type="dict"),
        install_status=dict(type="dict"),
        operational_status=dict(type="dict"),
    ),
)

PROBLEM_MAPPING_SPEC = dict(
    type="dict",
    required=False,
    options=dict(
        impact=dict(type="dict"),
        urgency=dict(type="dict"),
        problem_state=dict(type="dict"),
        state=dict(type="dict"),
    ),
)

PROBLEM_TASK_MAPPING_SPEC = dict(
    type="dict",
    required=False,
    options=dict(
        state=dict(type="dict"),
        priority=dict(type="dict"),
    ),
)

CATALOG_REQUEST_MAPPING_SPEC = dict(
    type="dict",
    required=False,
    options=dict(
        priority=dict(type="dict"),
        urgency=dict(type="dict"),
        impact=dict(type="dict"),
        state=dict(type="dict"),
        approval=dict(type="dict"),
    ),
)

CATALOG_REQUEST_TASK_MAPPING_SPEC = dict(
    type="dict",
    required=False,
    options=dict(
        priority=dict(type="dict"),
        urgency=dict(type="dict"),
        impact=dict(type="dict"),
        state=dict(type="dict"),
        approval=dict(type="dict"),
    ),
)

SHARED_SPECS = dict(
    instance=get_instance_module_spec(),
    sys_id=dict(type="str"),
    number=dict(type="str"),
    query=dict(type="list", elements="dict"),
    sysparm_query=dict(
        type="str",
        fallback=(env_fallback, ["SN_SYSPARM_QUERY"]),
    ),
    attachments=dict(
        type="list",
        elements="dict",
        options=dict(
            path=dict(
                type="str",
                required=True,
            ),
            name=dict(
                type="str",
            ),
            type=dict(
                type="str",
            ),
        ),
    ),
    sysparm_display_value=dict(
        type="str",
        choices=[
            "true",
            "false",
            "all",
        ],
        default="false",
    ),
    incident_mapping=INCIDENT_MAPPING_SPEC,
    change_request_mapping=CHANGE_REQUEST_MAPPING_SPEC,
    change_request_task_mapping=CHANGE_REQUEST_TASK_MAPPING_SPEC,
    configuration_item_mapping=CONFIGURATION_ITEM_MAPPING_SPEC,
    problem_mapping=PROBLEM_MAPPING_SPEC,
    problem_task_mapping=PROBLEM_TASK_MAPPING_SPEC,
    catalog_request_mapping=CATALOG_REQUEST_MAPPING_SPEC,
    catalog_request_task_mapping=CATALOG_REQUEST_TASK_MAPPING_SPEC,
)


def get_spec(*param_names):
    return dict((p, SHARED_SPECS[p]) for p in param_names)
