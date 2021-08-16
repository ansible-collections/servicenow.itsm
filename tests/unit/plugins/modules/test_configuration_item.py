# -*- coding: utf-8 -*-
# # Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys
import pytest


from ansible_collections.servicenow.itsm.plugins.modules import configuration_item
from ansible_collections.servicenow.itsm.plugins.module_utils import errors


pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestEnsureAbsent:
    def test_delete_configuration_item(
        self, create_module, table_client, attachment_client
    ):
        module = create_module(
            params=dict(
                instance=dict(host="https://my.host.name", username="user", password="pass"),
                state="absent",
                number=None,
                sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                sys_class_name="cmdb_ci",
            )
        )
        table_client.get_record.return_value = dict(
            sys_class_name="cmdb_ci", sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3"
        )

        result = configuration_item.ensure_absent(
            module, table_client, attachment_client
        )

        table_client.delete_record.assert_called_once()
        assert result == (
            True,
            None,
            dict(
                before=dict(
                    sys_class_name="cmdb_ci", sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3"
                ),
                after=None,
            ),
        )

    def test_delete_configuration_item_none_cmdb_ci(
        self, create_module, table_client, attachment_client
    ):
        module = create_module(
            params=dict(
                instance=dict(host="https://my.host.name", username="user", password="pass"),
                state="absent",
                number=None,
                sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                sys_class_name="cmdb_ci_computer",
            )
        )
        table_client.get_record.return_value = dict(
            sys_class_name="cmdb_ci_computer", sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3"
        )

        result = configuration_item.ensure_absent(
            module, table_client, attachment_client
        )

        table_client.delete_record.assert_called_once()
        assert result == (
            True,
            None,
            dict(
                before=dict(
                    sys_class_name="cmdb_ci_computer",
                    sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                ),
                after=None,
            ),
        )

    def test_delete_configuration_item_not_present(
        self, create_module, table_client, attachment_client
    ):
        module = create_module(
            params=dict(
                instance=dict(host="https://my.host.name", username="user", password="pass"),
                state="absent",
                number=None,
                sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                sys_class_name="cmdb_ci",
            ),
        )
        table_client.get_record.return_value = None

        result = configuration_item.ensure_absent(
            module, table_client, attachment_client
        )

        table_client.delete_record.assert_not_called()
        assert result == (False, None, dict(before=None, after=None))


class TestBuildPayload:
    def test_build_payload(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="https://my.host.name", username="user", password="pass"),
                state="present",
                sys_id=None,
                name=None,
                short_description="Test configuration item",
                sys_class_name="cmdb_ci",
                assigned_to="some.user",
                asset_tag="P1000613",
                install_status=None,
                operational_status=None,
                serial_number="ECE-164-E10834-NO",
                ip_address=None,
                mac_address=None,
                category="Hardware",
                environment="production",
                other=None,
            ),
        )
        table_client.get_record.return_value = {
            "sys_id": "681ccaf9c0a8016400b98a06818d57c7"
        }

        result = configuration_item.build_payload(module, table_client)

        assert "state" not in result
        assert result["short_description"] == "Test configuration item"
        assert result["sys_class_name"] == "cmdb_ci"
        assert result["assigned_to"] == "681ccaf9c0a8016400b98a06818d57c7"
        assert result["asset_tag"] == "P1000613"
        assert result["serial_number"] == "ECE-164-E10834-NO"
        assert result["category"] == "Hardware"
        assert result["environment"] == "production"

    def test_build_payload_with_other_option(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="https://my.host.name", username="user", password="pass"),
                state="present",
                sys_id=None,
                name=None,
                short_description="Test configuration item",
                sys_class_name="cmdb_ci",
                assigned_to=None,
                asset_tag="P1000613",
                install_status=None,
                operational_status=None,
                serial_number="ECE-164-E10834-NO",
                ip_address=None,
                mac_address=None,
                category="Hardware",
                environment="production",
                other=dict(subcategory="Computer"),
            ),
        )

        result = configuration_item.build_payload(module, table_client)

        assert "state" not in result
        assert result["short_description"] == "Test configuration item"
        assert result["sys_class_name"] == "cmdb_ci"
        assert "assigned_to" not in result
        assert result["asset_tag"] == "P1000613"
        assert result["serial_number"] == "ECE-164-E10834-NO"
        assert result["category"] == "Hardware"
        assert result["environment"] == "production"
        assert result["subcategory"] == "Computer"


class TestEnsurePresent:
    def test_ensure_present_create_new(
        self, create_module, table_client, attachment_client
    ):
        module = create_module(
            params=dict(
                instance=dict(host="https://my.host.name", username="user", password="pass"),
                state="present",
                sys_id=None,
                name="test.name",
                short_description="Test configuration item",
                sys_class_name="cmdb_ci",
                assigned_to=None,
                asset_tag=None,
                install_status=None,
                operational_status=None,
                serial_number=None,
                ip_address=None,
                mac_address=None,
                category=None,
                environment=None,
                production=None,
                other=None,
                attachments=None,
            ),
        )
        table_client.create_record.return_value = dict(
            name="test.name",
            short_description="Test configuration item",
            sys_class_name="cmdb_ci",
            sys_id="1234",
        )
        attachment_client.upload_records.return_value = []

        result = configuration_item.ensure_present(
            module, table_client, attachment_client
        )

        table_client.create_record.assert_called_once()
        assert result == (
            True,
            dict(
                name="test.name",
                short_description="Test configuration item",
                sys_class_name="cmdb_ci",
                sys_id="1234",
                attachments=[],
            ),
            dict(
                before=None,
                after=dict(
                    name="test.name",
                    short_description="Test configuration item",
                    sys_class_name="cmdb_ci",
                    sys_id="1234",
                    attachments=[],
                ),
            ),
        )

    def test_ensure_present_create_new_error(
        self, create_module, table_client, attachment_client
    ):
        module = create_module(
            params=dict(
                instance=dict(host="https://my.host.name", username="user", password="pass"),
                state="present",
                sys_id=None,
                name=None,
                short_description="Test configuration item",
                sys_class_name="cmdb_ci",
                assigned_to=None,
                asset_tag="P1000613",
                install_status=None,
                operational_status=None,
                serial_number="ECE-164-E10834-NO",
                ip_address=None,
                mac_address=None,
                category="Hardware",
                environment=None,
                production=None,
                other=None,
                attachments=None,
            ),
        )

        with pytest.raises(
            errors.ServiceNowError, match="Missing required parameter: name"
        ):
            configuration_item.ensure_present(module, table_client, attachment_client)

    def test_ensure_present_nothing_to_do(
        self, create_module, table_client, attachment_client
    ):
        module = create_module(
            params=dict(
                instance=dict(host="https://my.host.name", username="user", password="pass"),
                state="present",
                sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                name="test.name",
                short_description="Test configuration item",
                sys_class_name="cmdb_ci_computer",
                assigned_to=None,
                asset_tag=None,
                install_status=None,
                operational_status=None,
                serial_number=None,
                ip_address=None,
                mac_address=None,
                category=None,
                environment=None,
                other=None,
                attachments=None,
            ),
        )
        table_client.get_record.return_value = dict(
            sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
            name="test.name",
            short_description="Test configuration item",
            sys_class_name="cmdb_ci_computer",
        )
        attachment_client.update_records.return_value = []
        attachment_client.list_records.return_value = []

        result = configuration_item.ensure_present(
            module, table_client, attachment_client
        )

        table_client.get_record.assert_called()
        assert result == (
            False,
            dict(
                sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                name="test.name",
                short_description="Test configuration item",
                sys_class_name="cmdb_ci_computer",
                attachments=[],
            ),
            dict(
                before=dict(
                    sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                    name="test.name",
                    short_description="Test configuration item",
                    sys_class_name="cmdb_ci_computer",
                    attachments=[],
                ),
                after=dict(
                    sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                    name="test.name",
                    short_description="Test configuration item",
                    sys_class_name="cmdb_ci_computer",
                    attachments=[],
                ),
            ),
        )

    def test_ensure_present_update(
        self, mocker, create_module, table_client, attachment_client
    ):
        module = create_module(
            params=dict(
                instance=dict(host="https://my.host.name", username="user", password="pass"),
                state="present",
                sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                name=None,
                short_description=None,
                sys_class_name="cmdb_ci",
                assigned_to=None,
                asset_tag=None,
                install_status="installed",
                operational_status="ready",
                serial_number=None,
                ip_address=None,
                mac_address=None,
                category=None,
                environment=None,
                other=None,
                attachments=None,
            ),
        )
        payload_mocker = mocker.patch.object(configuration_item, "build_payload")
        payload_mocker.return_value = dict(
            sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
            sys_class_name="cmdb_ci",
            install_status="installed",
            operational_status="ready",
        )
        table_client.get_record.return_value = dict(
            sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
            sys_class_name="cmdb_ci",
            install_status="",
            operational_status="",
        )
        table_client.update_record.return_value = dict(
            sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
            sys_class_name="cmdb_ci",
            install_status="1",
            operational_status="5",
        )
        attachment_client.update_records.return_value = []
        attachment_client.list_records.return_value = []

        result = configuration_item.ensure_present(
            module, table_client, attachment_client
        )

        table_client.update_record.assert_called_once()
        assert result == (
            True,
            dict(
                sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                sys_class_name="cmdb_ci",
                install_status="installed",
                operational_status="ready",
                attachments=[],
            ),
            dict(
                before=dict(
                    sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                    sys_class_name="cmdb_ci",
                    install_status="",
                    operational_status="",
                    attachments=[],
                ),
                after=dict(
                    sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                    sys_class_name="cmdb_ci",
                    install_status="installed",
                    operational_status="ready",
                    attachments=[],
                ),
            ),
        )
