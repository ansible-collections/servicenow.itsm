# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import env_fallback

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
    instance=dict(
        type="dict",
        apply_defaults=True,
        options=dict(
            host=dict(
                type="str",
                required=True,
                fallback=(env_fallback, ["SN_HOST"]),
            ),
            username=dict(
                type="str",
                fallback=(env_fallback, ["SN_USERNAME"]),
            ),
            password=dict(
                type="str",
                no_log=True,
                fallback=(env_fallback, ["SN_PASSWORD"]),
            ),
            grant_type=dict(
                type="str",
                choices=["password", "refresh_token", "client_credentials"],
                fallback=(env_fallback, ["SN_GRANT_TYPE"]),
            ),
            api_path=dict(
                type="str",
                default="api/now",
            ),
            client_id=dict(
                type="str",
                fallback=(env_fallback, ["SN_CLIENT_ID"]),
            ),
            client_secret=dict(
                type="str",
                no_log=True,
                fallback=(env_fallback, ["SN_CLIENT_SECRET"]),
            ),
            client_certificate_file=dict(
                type="str",
                no_log=True,
                fallback=(env_fallback, ["SN_CLIENT_CERTIFICATE_FILE"]),
            ),
            client_key_file=dict(
                type="str",
                no_log=True,
                fallback=(env_fallback, ["SN_CLIENT_KEY_FILE"]),
            ),
            custom_headers=dict(type="dict"),
            refresh_token=dict(
                type="str",
                no_log=True,
                fallback=(env_fallback, ["SN_REFRESH_TOKEN"]),
            ),
            access_token=dict(
                type="str",
                no_log=True,
                fallback=(env_fallback, ["SN_ACCESS_TOKEN"]),
            ),
            api_key=dict(
                type="str",
                no_log=True,
                fallback=(env_fallback, ["SN_API_KEY"]),
            ),
            timeout=dict(
                type="float",
                default=10,
                fallback=(env_fallback, ["SN_TIMEOUT"]),
            ),
            validate_certs=dict(
                type="bool",
                default=True,
            ),
        ),
        required_together=[
            ("client_id", "client_secret"),
            ("username", "password"),
            ("client_certificate_file", "client_key_file"),
        ],
        required_one_of=[
            (
                "username",
                "refresh_token",
                "access_token",
                "api_key",
                "client_id",
                "client_certificate_file",
            )
        ],
        mutually_exclusive=[
            (
                "username",
                "refresh_token",
                "access_token",
                "api_key",
                "client_certificate_file",
            ),
            ("client_id", "access_token", "client_certificate_file"),
            ("grant_type", "access_token", "client_certificate_file"),
        ],
        required_if=[
            ("grant_type", "password", ("username", "password")),
            ("grant_type", "refresh_token", ("refresh_token",)),
            ("grant_type", "client_connections", ("client_id", "client_secret")),
        ],
    ),
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
