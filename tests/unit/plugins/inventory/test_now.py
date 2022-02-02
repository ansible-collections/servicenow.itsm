# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible.errors import AnsibleParserError, AnsibleError
from ansible.inventory.data import InventoryData
from ansible.module_utils.common.text.converters import to_text
from ansible.template import Templar

from ansible_collections.servicenow.itsm.plugins.inventory import now

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


@pytest.fixture
def inventory_plugin():
    plugin = now.InventoryModule()
    plugin.inventory = InventoryData()
    plugin.templar = Templar(loader=None)
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

    def test_no_query_with_fields(self, table_client):
        now.fetch_records(table_client, "table_name", None, fields=["a", "b", "c"])

        table_client.list_records.assert_called_once_with(
            "table_name", dict(sysparm_display_value=True, sysparm_fields="a,b,c")
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


class TestInventoryModuleFillEnhancedAutoGroups:
    def test_construction(self, inventory_plugin):
        record = dict(
            sys_id="1",
            ip_address="1.1.1.1",
            fqdn="a1",
            relationship_groups=set(
                (
                    "NY-01-01_Rack_contains",
                    "Storage Area Network 002_Sends_data_to",
                    "Blackberry_Depends_on",
                    "Retail Adding Points_Depends_on",
                )
            ),
        )

        host = inventory_plugin.add_host(record, "ip_address", "fqdn")
        inventory_plugin.fill_enhanced_auto_groups(record, host)

        assert set(inventory_plugin.inventory.groups) == set(
            (
                "all",
                "ungrouped",
                "NY_01_01_Rack_contains",
                "Storage_Area_Network_002_Sends_data_to",
                "Blackberry_Depends_on",
                "Retail_Adding_Points_Depends_on",
            )
        )

        assert set(inventory_plugin.inventory.hosts) == set(("a1",))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set(
            (
                "NY_01_01_Rack_contains",
                "Storage_Area_Network_002_Sends_data_to",
                "Blackberry_Depends_on",
                "Retail_Adding_Points_Depends_on",
            )
        )

        assert a1.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="1.1.1.1"
        )

    def test_construction_empty(self, inventory_plugin):
        record = dict(
            sys_id="1", ip_address="1.1.1.1", fqdn="a1", relationship_groups=set()
        )

        host = inventory_plugin.add_host(record, "ip_address", "fqdn")
        inventory_plugin.fill_enhanced_auto_groups(record, host)

        assert set(inventory_plugin.inventory.groups) == set(("all", "ungrouped"))

        assert set(inventory_plugin.inventory.hosts) == set(("a1",))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set()

        assert a1.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="1.1.1.1"
        )


class TestInventoryModuleFillConstructed:
    def test_construction_empty(self, inventory_plugin):
        records = []
        columns = []
        host_source = "ip_address"
        name_source = "fqdn"
        compose = {}
        groups = {}
        keyed_groups = []
        strict = False
        enhanced = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            host_source,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
        )

        assert set(inventory_plugin.inventory.groups) == set(("all", "ungrouped"))
        assert set(inventory_plugin.inventory.hosts) == set()

    def test_construction_host(self, inventory_plugin):
        records = [
            dict(
                sys_id="1",
                ip_address="1.1.1.1",
                fqdn="a1",
            ),
            dict(
                sys_id="2",
                ip_address="1.1.1.2",
                fqdn="a2",
            ),
        ]

        columns = []
        host_source = "ip_address"
        name_source = "fqdn"
        compose = {}
        groups = {}
        keyed_groups = []
        strict = False
        enhanced = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            host_source,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
        )

        assert set(inventory_plugin.inventory.groups) == set(("all", "ungrouped"))
        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set()

        assert a1.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="1.1.1.1"
        )

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set()

        assert a2.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="1.1.1.2"
        )

    def test_construction_hostvars(self, inventory_plugin):
        records = [
            dict(sys_id="1", ip_address="1.1.1.1", fqdn="a1", cost="82", cost_cc="EUR"),
            dict(sys_id="2", ip_address="1.1.1.2", fqdn="a2", cost="94", cost_cc="USD"),
        ]

        columns = ["cost", "cost_cc"]
        host_source = "ip_address"
        name_source = "fqdn"
        compose = {}
        groups = {}
        keyed_groups = []
        strict = False
        enhanced = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            host_source,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
        )

        assert set(inventory_plugin.inventory.groups) == set(("all", "ungrouped"))
        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set()

        assert a1.vars == dict(
            inventory_file=None,
            inventory_dir=None,
            ansible_host="1.1.1.1",
            cost="82",
            cost_cc="EUR",
        )

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set()

        assert a2.vars == dict(
            inventory_file=None,
            inventory_dir=None,
            ansible_host="1.1.1.2",
            cost="94",
            cost_cc="USD",
        )

    def test_construction_composite_vars(self, inventory_plugin):
        records = [
            dict(
                sys_id="1",
                ip_address="1.1.1.1",
                fqdn="a1",
                cost="82",
                cost_cc="EUR",
                sys_updated_on="2021-09-17 02:13:25",
            ),
            dict(
                sys_id="2",
                ip_address="1.1.1.2",
                fqdn="a2",
                cost="94",
                cost_cc="USD",
                sys_updated_on="2021-08-30 01:47:03",
            ),
        ]

        columns = []
        host_source = "ip_address"
        name_source = "fqdn"
        compose = dict(
            cost_res='"%s %s" % (cost, cost_cc)',
            amortized_cost="cost | int // 2",
            sys_updated_on_date="sys_updated_on | slice(2) | first | join",
            sys_updated_on_time="sys_updated_on | slice(2) | last | join | trim",
            silently_failed="non_existing + 3",
        )
        groups = {}
        keyed_groups = []
        strict = False
        enhanced = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            host_source,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
        )

        assert set(inventory_plugin.inventory.groups) == set(("all", "ungrouped"))
        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set()

        assert a1.vars == dict(
            inventory_file=None,
            inventory_dir=None,
            ansible_host="1.1.1.1",
            cost_res="82 EUR",
            amortized_cost="41",
            sys_updated_on_date="2021-09-17",
            sys_updated_on_time="02:13:25",
        )

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set()

        assert a2.vars == dict(
            inventory_file=None,
            inventory_dir=None,
            ansible_host="1.1.1.2",
            cost_res="94 USD",
            amortized_cost="47",
            sys_updated_on_date="2021-08-30",
            sys_updated_on_time="01:47:03",
        )

    def test_construction_composite_vars_strict(self, inventory_plugin):
        records = [
            dict(sys_id="1", ip_address="1.1.1.1", fqdn="a1"),
            dict(sys_id="2", ip_address="1.1.1.2", fqdn="a2"),
        ]

        columns = []
        host_source = "ip_address"
        name_source = "fqdn"
        compose = dict(silently_failed="non_existing + 3")
        groups = {}
        keyed_groups = []
        strict = True
        enhanced = False

        with pytest.raises(AnsibleError, match="non_existing"):
            inventory_plugin.fill_constructed(
                records,
                columns,
                host_source,
                name_source,
                compose,
                groups,
                keyed_groups,
                strict,
                enhanced,
            )

    def test_construction_composed_groups(self, inventory_plugin):
        records = [
            dict(sys_id="1", ip_address="1.1.1.1", fqdn="a1"),
            dict(sys_id="2", ip_address="1.1.1.2", fqdn="a2"),
        ]

        columns = []
        host_source = "ip_address"
        name_source = "fqdn"
        compose = {}
        groups = dict(
            ip1='ip_address == "1.1.1.1"',
            ip2='ip_address != "1.1.1.1"',
            cost="cost_usd < 90",  # ignored due to strict = False
        )
        keyed_groups = []
        strict = False
        enhanced = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            host_source,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
        )

        assert set(inventory_plugin.inventory.groups) == set(
            ("all", "ungrouped", "ip1", "ip2")
        )

        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set(("ip1",))

        assert a1.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="1.1.1.1"
        )

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set(("ip2",))

        assert a2.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="1.1.1.2"
        )

    def test_construction_composed_groups_strict(self, inventory_plugin):
        records = [
            dict(sys_id="1", ip_address="1.1.1.1", fqdn="a1"),
            dict(sys_id="2", ip_address="1.1.1.2", fqdn="a2"),
        ]

        columns = []
        host_source = "ip_address"
        name_source = "fqdn"
        compose = {}
        groups = dict(
            ip1='ip_address == "1.1.1.1"',
            ip2='ip_address != "1.1.1.1"',
            cost="cost_usd < 90",
        )
        keyed_groups = []
        strict = True
        enhanced = False

        with pytest.raises(AnsibleError, match="cost_usd"):
            inventory_plugin.fill_constructed(
                records,
                columns,
                host_source,
                name_source,
                compose,
                groups,
                keyed_groups,
                strict,
                enhanced,
            )

    def test_construction_keyed_groups(self, inventory_plugin):
        records = [
            dict(sys_id="1", ip_address="1.1.1.1", fqdn="a1", cost_cc="EUR"),
            dict(sys_id="2", ip_address="1.1.1.2", fqdn="a2", cost_cc="USD"),
        ]

        columns = []
        host_source = "ip_address"
        name_source = "fqdn"
        compose = {}
        groups = {}
        keyed_groups = [
            dict(
                key="cost_cc",
                default_value="EUR",
                prefix="cc",
            )
        ]
        strict = False
        enhanced = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            host_source,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
        )

        assert set(inventory_plugin.inventory.groups) == set(
            ("all", "ungrouped", "cc_EUR", "cc_USD")
        )

        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set(("cc_EUR",))

        assert a1.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="1.1.1.1"
        )

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set(("cc_USD",))

        assert a2.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="1.1.1.2"
        )

    def test_construction_keyed_groups_with_parent(self, inventory_plugin):
        records = [
            dict(sys_id="1", ip_address="1.1.1.1", fqdn="a1", cost_cc="EUR"),
            dict(sys_id="2", ip_address="1.1.1.2", fqdn="a2", cost_cc="USD"),
        ]

        columns = []
        host_source = "ip_address"
        name_source = "fqdn"
        compose = {}
        groups = {}
        keyed_groups = [
            dict(
                key="cost_cc",
                default_value="EUR",
                prefix="cc",
                parent_group="ip_address",
            )
        ]
        strict = False
        enhanced = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            host_source,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
        )

        assert set(inventory_plugin.inventory.groups) == set(
            ("all", "ungrouped", "cc_EUR", "cc_USD", "ip_address")
        )

        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set(("cc_EUR", "ip_address"))

        assert a1.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="1.1.1.1"
        )

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set(("cc_USD", "ip_address"))

        assert a2.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="1.1.1.2"
        )

    def test_construction_enhanced(self, inventory_plugin):
        records = [
            dict(
                sys_id="1",
                ip_address="1.1.1.1",
                fqdn="a1",
                relationship_groups=set(("NY-01-01_Rack_contains",)),
            ),
            dict(
                sys_id="2",
                ip_address="1.1.1.2",
                fqdn="a2",
                relationship_groups=set(
                    ("Storage Area Network 002_Sends_data_to", "OWA-SD-01_Runs_on")
                ),
            ),
        ]

        columns = []
        host_source = "ip_address"
        name_source = "fqdn"
        compose = {}
        groups = {}
        keyed_groups = []
        strict = False
        enhanced = True

        inventory_plugin.fill_constructed(
            records,
            columns,
            host_source,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
        )

        assert set(inventory_plugin.inventory.groups) == set(
            (
                "all",
                "ungrouped",
                "NY_01_01_Rack_contains",
                "Storage_Area_Network_002_Sends_data_to",
                "OWA_SD_01_Runs_on",
            )
        )

        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set(("NY_01_01_Rack_contains",))

        assert a1.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="1.1.1.1"
        )

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set(
            ("Storage_Area_Network_002_Sends_data_to", "OWA_SD_01_Runs_on")
        )

        assert a2.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="1.1.1.2"
        )
