# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Red Hat
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.module_utils import instance_config

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


# Every SN_* environment variable that get_instance_config_from_env reads, so a
# test can start from a clean slate regardless of the runner's environment.
_ALL_SN_ENV_VARS = [
    attrs["env_var"]
    for attrs in instance_config.INSTANCE_OPTIONS.values()
    if "env_var" in attrs
] + ["SN_SECRET_ID"]


@pytest.fixture
def clean_sn_env(monkeypatch):
    for var in _ALL_SN_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    return monkeypatch


class TestGetInstanceConfigFromEnv:
    def test_timeout_from_env_is_coerced_to_float(self, clean_sn_env):
        # Regression test: SN_TIMEOUT arrives from the environment as a string.
        # It must be coerced to its declared type (float) so it does not reach
        # the HTTP client as a string and raise
        # "'str' object cannot be interpreted as an integer".
        clean_sn_env.setenv("SN_TIMEOUT", "120")

        config = instance_config.get_instance_config_from_env()

        assert isinstance(config["timeout"], float)
        assert config["timeout"] == 120.0

    def test_str_option_from_env_stays_str(self, clean_sn_env):
        clean_sn_env.setenv("SN_HOST", "https://example.service-now.com")

        config = instance_config.get_instance_config_from_env()

        assert config["host"] == "https://example.service-now.com"
        assert isinstance(config["host"], str)

    def test_unset_env_var_is_none(self, clean_sn_env):
        config = instance_config.get_instance_config_from_env()

        assert config["timeout"] is None
        assert config["host"] is None

    def test_invalid_timeout_raises(self, clean_sn_env):
        clean_sn_env.setenv("SN_TIMEOUT", "not-a-number")

        with pytest.raises(ValueError):
            instance_config.get_instance_config_from_env()


class TestMergeEnvWithParamInstance:
    def test_env_timeout_is_float_after_merge(self, clean_sn_env):
        clean_sn_env.setenv("SN_TIMEOUT", "45")

        instance = instance_config.merge_env_with_param_instance()

        assert isinstance(instance["timeout"], float)
        assert instance["timeout"] == 45.0

    def test_params_override_env(self, clean_sn_env):
        clean_sn_env.setenv("SN_HOST", "https://from-env.service-now.com")
        clean_sn_env.setenv("SN_TIMEOUT", "45")

        instance = instance_config.merge_env_with_param_instance(
            {"host": "https://from-params.service-now.com", "timeout": 10.0}
        )

        assert instance["host"] == "https://from-params.service-now.com"
        assert instance["timeout"] == 10.0

    def test_unset_env_var_excluded_from_merge(self, clean_sn_env):
        instance = instance_config.merge_env_with_param_instance()

        # Values that are not set in the environment are excluded entirely so the
        # Client falls back to its own defaults.
        assert "timeout" not in instance
        assert "host" not in instance
