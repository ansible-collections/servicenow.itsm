# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import env_fallback


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
                choices=[
                    "password",
                    "refresh_token"
                ],
                default="password",
                fallback=(env_fallback, ["SN_GRANT_TYPE"]),
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
            refresh_token=dict(
                type="str",
                no_log=True,
                fallback=(env_fallback, ["SN_REFRESH_TOKEN"]),
            ),
            timeout=dict(
                type="float",
                fallback=(env_fallback, ["SN_TIMEOUT"]),
            ),
        ),
        required_together=[
            ("client_id", "client_secret"),
            ("username", "password")
        ],
        required_one_of=[
            ("username", "refresh_token")
        ],
        mutually_exclusive=[
            ("username", "refresh_token")
        ],
        required_if=[
            ("grant_type", "password", ("username", "password")),
            ("grant_type", "refresh_token", ("refresh_token",))
        ]
    ),
    sys_id=dict(type="str"),
    number=dict(type="str"),
    query=dict(type="list", elements="dict"),
)


def get_spec(*param_names):
    return dict((p, SHARED_SPECS[p]) for p in param_names)
