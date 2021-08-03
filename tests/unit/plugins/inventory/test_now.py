# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible.errors import AnsibleParserError
from ansible.inventory.data import InventoryData
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.servicenow.itsm.plugins.inventory import now

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


@pytest.fixture
def inventory_plugin():
    plugin = now.InventoryModule()
    plugin.inventory = InventoryData()
    return plugin


class TestContructSysparmQuery:
    def test_valid_query(self):
        assert "column=value" == now.construct_sysparm_query([dict(column="= value")])

    def test_invalid_query(self):
        with pytest.raises(AnsibleParserError, match="INVALID"):
            now.construct_sysparm_query([dict(column="INVALID operator")])


class TestFetchRecords:
    def test_no_query(self, table_client):
        now.fetch_records(table_client, "table_name", None)

        table_client.list_records.assert_called_once_with(
            "table_name", dict(sysparm_display_value=True)
        )

    def test_query(self, table_client):
        now.fetch_records(table_client, "table_name", [dict(my="!= value")])

        table_client.list_records.assert_called_once_with(
            "table_name", dict(sysparm_display_value=True, sysparm_query="my!=value")
        )


class TestSysparmQueryFromConditions:
    def test_empty_conditions(self):
        assert now.sysparm_query_from_conditions({}) is None

    @pytest.mark.parametrize(
        "conditions,expected",
        [
            (dict(a=dict(includes=["b"])), "a=b"),
            (dict(a=dict(includes=["b", "c"])), "a=b^ORa=c"),
            (dict(a=dict(excludes=["b"])), "a!=b"),
            (dict(a=dict(excludes=["b", "c"])), "a!=b^a!=c"),
        ],
    )
    def test_conditions_single_field(self, conditions, expected):
        assert expected == now.sysparm_query_from_conditions(conditions)

    def test_conditions_multiple_fields(self):
        conditions = dict(
            a=dict(includes=["a1", "a2"]),
            b=dict(excludes=["b1", "b2"]),
        )
        sysparm_query = now.sysparm_query_from_conditions(conditions)

        # We do not care about the order, we just want to make sure
        # that there is "and" between conditions for both fields.
        assert sysparm_query in ("a=a1^ORa=a2^b!=b1^b!=b2", "b!=b1^b!=b2^a=a1^ORa=a2")


class TestInventoryModuleVerifyFile:
    @pytest.mark.parametrize(
        "name,valid",
        [("sample.now.yaml", True), ("sample.now.yml", True), ("invalid.yaml", False)],
    )
    def test_file_name(self, inventory_plugin, tmp_path, name, valid):
        config = tmp_path / name
        config.write_text(to_text("plugin: servicenow.itsm.now"))

        assert inventory_plugin.verify_file(to_text(config)) is valid


class TestInventoryModuleValidateGroupingConditions:
    def test_valid_named_groups(self, inventory_plugin):
        inventory_plugin.validate_grouping_conditions(
            dict(
                group1=dict(
                    col1=dict(includes=[1, 2, 3]),
                    col2=dict(excludes=[4, 5, 6]),
                ),
                group2=dict(
                    col3=dict(excludes=["a", "b"]),
                    col4=dict(includes=["c", "d"]),
                ),
            ),
            dict(),
        )

    def test_invalid_named_groups(self, inventory_plugin):
        with pytest.raises(AnsibleParserError, match="mutually exclusive"):
            inventory_plugin.validate_grouping_conditions(
                dict(
                    group=dict(
                        col=dict(includes=[1], excludes=[2]),
                    ),
                ),
                dict(),
            )

    def test_valid_group_by(self, inventory_plugin):
        inventory_plugin.validate_grouping_conditions(
            dict(),
            dict(
                col1=dict(includes=[1, 2, 3]),
                col2=dict(excludes=[4, 5, 6]),
            ),
        )

    def test_invalid_group_by(self, inventory_plugin):
        with pytest.raises(AnsibleParserError, match="mutually exclusive"):
            inventory_plugin.validate_grouping_conditions(
                dict(),
                dict(
                    col=dict(includes=[4, 5], excludes=["test"]),
                ),
            )


class TestInventoryModuleAddHost:
    def test_valid(self, inventory_plugin):
        host = inventory_plugin.add_host(
            dict(host_source="1.2.3.4", name_source="dummy_host", sys_id="123"),
            "host_source",
            "name_source",
        )

        assert host == "dummy_host"
        hostvars = inventory_plugin.inventory.get_host("dummy_host").vars
        assert hostvars["ansible_host"] == "1.2.3.4"

    def test_valid_empty_host(self, inventory_plugin):
        host = inventory_plugin.add_host(
            dict(host_source="", name_source="dummy_host", sys_id="123"),
            "host_source",
            "name_source",
        )

        assert host == "dummy_host"
        hostvars = inventory_plugin.inventory.get_host("dummy_host").vars
        assert "ansible_host" not in hostvars

    def test_valid_empty_name(self, inventory_plugin):
        host = inventory_plugin.add_host(
            dict(host_source="1.2.3.4", name_source="", sys_id="123"),
            "host_source",
            "name_source",
        )

        assert host is None
        assert inventory_plugin.inventory.get_host("dummy_host") is None

    def test_invalid_host(self, inventory_plugin):
        with pytest.raises(AnsibleParserError, match="invalid_host"):
            inventory_plugin.add_host(
                dict(host_source="1.2.3.4", name_source="dummy_host", sys_id="123"),
                "invalid_host",
                "name_source",
            )

    def test_invalid_name(self, inventory_plugin):
        with pytest.raises(AnsibleParserError, match="invalid_name"):
            inventory_plugin.add_host(
                dict(host_source="1.2.3.4", name_source="dummy_host", sys_id="123"),
                "host_source",
                "invalid_name",
            )


class TestInventoryModuleSetHostvars:
    def test_valid(self, inventory_plugin):
        inventory_plugin.inventory.add_host("dummy_host")

        inventory_plugin.set_hostvars(
            "dummy_host",
            dict(sys_id="123", platform="demo", unused="column"),
            ("sys_id", "platform"),
        )

        hostvars = inventory_plugin.inventory.get_host("dummy_host").vars
        assert hostvars["sys_id"] == "123"
        assert hostvars["platform"] == "demo"
        assert "unused" not in hostvars

    def test_invalid_column(self, inventory_plugin):
        with pytest.raises(AnsibleParserError, match="bad_column"):
            inventory_plugin.set_hostvars(
                "dummy_host",
                dict(sys_id="123", platform="demo", unused="column"),
                ("sys_id", "platform", "bad_column"),
            )


class TestInventoryModuleQuery:
    def test_construction(self, inventory_plugin):
        result = inventory_plugin.query(
            dict(cname=dict(includes="b")), "host", "name", ("col1", "col2")
        )

        assert set(result["sysparm_fields"].split(",")) == set(
            ("col1", "col2", "host", "name", "sys_id", "cname")
        )
        assert result["sysparm_display_value"] is True
        assert result["sysparm_query"] == "cname=b"


class TestInventoryModuleFillDesiredGroups:
    def test_inventory_construction(self, inventory_plugin, table_client):
        table_client.list_records.return_value = [
            dict(sys_id="1", host="1.1.1.1", name="a1", material="wood"),
            dict(sys_id="2", host="1.1.1.2", name="a2", material="metal"),
        ]

        inventory_plugin.fill_desired_groups(
            table_client,
            "cmdb_ci_abacuses",
            "host",
            "name",
            ("material", "sys_id"),
            dict(g1=dict(material={})),
        )

        a1 = inventory_plugin.inventory.get_host("a1")
        assert a1.vars["sys_id"] == "1"
        assert a1.vars["material"] == "wood"
        assert a1.vars["ansible_host"] == "1.1.1.1"

        a2 = inventory_plugin.inventory.get_host("a2")
        assert a2.vars["sys_id"] == "2"
        assert a2.vars["material"] == "metal"
        assert a2.vars["ansible_host"] == "1.1.1.2"

        groups = inventory_plugin.inventory.get_groups_dict()
        assert set(groups["g1"]) == set(("a1", "a2"))


class TestInventoryModuleFillAutoGroups:
    def test_inventory_construction(self, inventory_plugin, table_client):
        table_client.list_records.return_value = [
            dict(sys_id="3", host_source="1.1.1.3", name_source="a3", material="b-a-d"),
            dict(sys_id="4", host_source="1.1.1.4", name_source="a4", material="glass"),
            dict(sys_id="5", host_source="1.1.1.5", name_source="a5", material=""),
        ]

        inventory_plugin.fill_auto_groups(
            table_client,
            "cmdb_ci_abacuses",
            "host_source",
            "name_source",
            ("material", "sys_id"),
            dict(material={}),
        )

        a3 = inventory_plugin.inventory.get_host("a3")
        assert a3.vars["sys_id"] == "3"
        assert a3.vars["material"] == "b-a-d"
        assert a3.vars["ansible_host"] == "1.1.1.3"

        a4 = inventory_plugin.inventory.get_host("a4")
        assert a4.vars["sys_id"] == "4"
        assert a4.vars["material"] == "glass"
        assert a4.vars["ansible_host"] == "1.1.1.4"

        a5 = inventory_plugin.inventory.get_host("a5")
        assert a5.vars["sys_id"] == "5"
        assert a5.vars["material"] == ""
        assert a5.vars["ansible_host"] == "1.1.1.5"

        groups = inventory_plugin.inventory.get_groups_dict()
        assert set(groups["b_a_d"]) == set(("a3",))
        assert set(groups["glass"]) == set(("a4",))
