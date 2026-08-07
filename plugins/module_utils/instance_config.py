# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
from ansible.module_utils.basic import env_fallback

# These are all the instance options that the collection supports. They are defined here for all plugin
# types, although the resulting "spec" or how the plugin uses them is defined via methods below.
INSTANCE_OPTIONS = {
    "host": {
        "type": "str",
        "required": True,
        "env_var": "SN_HOST",
    },
    "username": {
        "type": "str",
        "env_var": "SN_USERNAME",
    },
    "password": {
        "type": "str",
        "no_log": True,
        "env_var": "SN_PASSWORD",
    },
    "grant_type": {
        "type": "str",
        "choices": ["password", "refresh_token", "client_credentials"],
        "env_var": "SN_GRANT_TYPE",
    },
    "api_path": {
        "type": "str",
        "default": "api/now",
    },
    "client_id": {
        "type": "str",
        "env_var": "SN_CLIENT_ID",
    },
    "client_secret": {
        "type": "str",
        "no_log": True,
        "env_var": "SN_CLIENT_SECRET",
    },
    "client_certificate_file": {
        "type": "str",
        "no_log": True,
        "env_var": "SN_CLIENT_CERTIFICATE_FILE",
    },
    "client_key_file": {
        "type": "str",
        "no_log": True,
        "env_var": "SN_CLIENT_KEY_FILE",
    },
    "custom_headers": {
        "type": "dict",
    },
    "refresh_token": {
        "type": "str",
        "no_log": True,
        "env_var": "SN_REFRESH_TOKEN",
    },
    "access_token": {
        "type": "str",
        "no_log": True,
        "env_var": "SN_ACCESS_TOKEN",
    },
    "api_key": {
        "type": "str",
        "no_log": True,
        "env_var": "SN_API_KEY",
    },
    "timeout": {
        "type": "float",
        "default": 10,
        "env_var": "SN_TIMEOUT",
    },
    "validate_certs": {
        "type": "bool",
        "default": True,
    },
}


def merge_env_with_param_instance(config_from_params=None, display=None):
    """
    Build a complete instance config by layering parameter values on top of environment variables.

    Values from config_from_params take precedence over environment variables.
    Environment variables that are not set (None) are excluded.
    """
    if config_from_params is None:
        config_from_params = {}

    config_from_env = get_instance_config_from_env(display=display)
    instance = {}
    for k, v in config_from_env.items():
        if v is not None:
            instance[k] = v

    for k, v in config_from_params.items():
        instance[k] = v

    return instance


def get_instance_config_from_env(display=None):
    """
    Read instance config values from environment variables defined in INSTANCE_OPTIONS.

    Handles deprecated SN_SECRET_ID fallback for client_secret. If display is
    provided, a deprecation warning is emitted when SN_SECRET_ID is used.
    """
    config_from_env = {}
    for config_key, attributes in INSTANCE_OPTIONS.items():
        if "env_var" not in attributes:
            continue

        config_from_env[config_key] = os.getenv(attributes["env_var"])

    # Remove this fallback in 3.0.0
    if config_from_env.get("client_secret") is None:
        secret_id = os.getenv("SN_SECRET_ID")
        if secret_id is not None:
            config_from_env["client_secret"] = secret_id
            if display:
                display.deprecated(
                    "Setting environment variable 'SN_SECRET_ID' is being removed "
                    "in favor of 'SN_CLIENT_SECRET'",
                    version="3.0.0",
                    collection_name="servicenow.itsm",
                )

    return config_from_env


def get_instance_module_spec():
    """
    Generate an Ansible module argument spec from INSTANCE_OPTIONS.

    Converts each option's env_var into a fallback=(env_fallback, [...]) entry
    and includes validation constraints (required_together, mutually_exclusive, etc.).
    """
    options = {}
    for config_key, attributes in INSTANCE_OPTIONS.items():
        spec = {k: v for k, v in attributes.items() if k != "env_var"}
        if "env_var" in attributes:
            spec["fallback"] = (env_fallback, [attributes["env_var"]])

        options[config_key] = spec

    return {
        "type": "dict",
        "apply_defaults": True,
        "options": options,
        "required_together": [
            ("client_id", "client_secret"),
            ("username", "password"),
            ("client_certificate_file", "client_key_file"),
        ],
        "required_one_of": [
            (
                "username",
                "refresh_token",
                "access_token",
                "api_key",
                "client_id",
                "client_certificate_file",
            )
        ],
        "mutually_exclusive": [
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
        "required_if": [
            ("grant_type", "password", ("username", "password")),
            ("grant_type", "refresh_token", ("refresh_token",)),
            ("grant_type", "client_connections", ("client_id", "client_secret")),
        ],
    }
