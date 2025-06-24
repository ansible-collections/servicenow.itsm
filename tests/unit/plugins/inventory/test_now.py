# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.inventory.data import InventoryData
from ansible.module_utils.common.text.converters import to_text
from ansible.template import Templar
from ansible_collections.servicenow.itsm.plugins.inventory import now
from ansible_collections.servicenow.itsm.plugins.module_utils.relations import REL_FIELDS, REL_TABLE, REL_QUERY


try:
    # post 2.19 is strict about jinja template safety. This means test inputs
    # for params (like groups) that could contain jinja templates need
    # to be trusted using the method below
    from ansible.template import trust_as_template as _trust_as_template

    HAS_DATATAGGING = True
except ImportError:
    # pre 2.19
    HAS_DATATAGGING = False

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


def trust_jinja_input(input):
    if HAS_DATATAGGING:
        return _trust_as_template(input)
    return input


@pytest.fixture
def inventory_plugin():
    plugin = now.InventoryModule()
    plugin.inventory = InventoryData()
    plugin.templar = Templar(loader=None)
    return plugin


class TestContructSysparmQuery:
    def test_valid_query(self):
        assert "column=value" == now.construct_sysparm_query(
            [dict(column="= value")], False
        )

    def test_invalid_query(self):
        with pytest.raises(AnsibleParserError, match="INVALID"):
            now.construct_sysparm_query([dict(column="INVALID operator")], False)

    def test_valid_encoded_query(self):
        assert "column=value^ORfield=something" == now.construct_sysparm_query(
            "column=value^ORfield=something", True
        )


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


class TestInventoryModuleVerifyFile:
    @pytest.mark.parametrize(
        "name,valid",
        [("sample.now.yaml", True), ("sample.now.yml", True), ("invalid.yaml", False)],
    )
    def test_file_name(self, inventory_plugin, tmp_path, name, valid):
        config = tmp_path / name
        config.write_text(to_text("plugin: servicenow.itsm.now"))

        assert inventory_plugin.verify_file(to_text(config)) is valid


class TestInventoryModuleAddHost:
    def test_valid(self, inventory_plugin):
        host = inventory_plugin.add_host(
            dict(name_source="dummy_host", sys_id="123"),
            "name_source",
        )

        assert host == "dummy_host"
        hostvars = inventory_plugin.inventory.get_host("dummy_host").vars
        assert hostvars is not None

    def test_valid_empty_name(self, inventory_plugin):
        host = inventory_plugin.add_host(
            dict(name_source="", sys_id="123"),
            "name_source",
        )

        assert host is None
        assert inventory_plugin.inventory.get_host("dummy_host") is None

    def test_invalid_name(self, inventory_plugin):
        with pytest.raises(AnsibleParserError, match="invalid_name"):
            inventory_plugin.add_host(
                dict(name_source="dummy_host", sys_id="123"),
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


class TestInstance:
    @pytest.mark.parametrize(
        "instance_conf,instance_env,expected",
        [
            (dict(), dict(), dict()),
            (dict(a="a"), dict(), dict()),
            (dict(), dict(a="a"), dict(a="a")),
            (dict(a="a", b="b"), dict(a="c"), dict(a="a")),
            (dict(a="a"), dict(a="c", b="b"), dict(a="a", b="b")),
        ],
    )
    def test_merge_instance_config(
        self, inventory_plugin, instance_conf, instance_env, expected
    ):
        merged_conf = inventory_plugin._merge_instance_config(
            instance_conf, instance_env
        )

        assert merged_conf == expected

    def test_get_instance_from_env(self, inventory_plugin, mocker):
        def getenv(key):
            return dict(
                SN_HOST="host",
                SN_USERNAME="username",
                SN_PASSWORD="password",
                SN_CLIENT_ID="client_id",
                SN_CLIENT_SECRET="client_secret",
                SN_REFRESH_TOKEN="refresh_token",
                SN_GRANT_TYPE="grant_type",
                SN_TIMEOUT="100",
            ).get(key)

        mocker.patch("os.getenv", new=getenv)

        config = inventory_plugin._get_instance_from_env()
        assert config == dict(
            host="host",
            username="username",
            password="password",
            client_id="client_id",
            client_secret="client_secret",
            refresh_token="refresh_token",
            grant_type="grant_type",
            timeout=100,
        )

    def test_get_instance(self, inventory_plugin, mocker):
        def get_option(*args):
            return dict(a="a", password="b", host="host")

        mocker.patch("os.getenv", new=lambda x: x)
        mocker.patch.object(inventory_plugin, "get_option", new=get_option)

        instance = inventory_plugin._get_instance()

        assert instance == dict(
            host="host",
            username="SN_USERNAME",
            password="b",
            client_id="SN_CLIENT_ID",
            client_secret="SN_CLIENT_SECRET",
            refresh_token="SN_REFRESH_TOKEN",
            grant_type="SN_GRANT_TYPE",
            timeout=120,
        )

    def test_get_timeout_default_value(self, inventory_plugin, mocker):
        def getenv(key):
            return dict(
                SN_HOST="host",
                SN_USERNAME="username",
                SN_PASSWORD="password",
                SN_CLIENT_ID="client_id",
                SN_CLIENT_SECRET="client_secret",
                SN_REFRESH_TOKEN="refresh_token",
                SN_GRANT_TYPE="grant_type",
                SN_TIMEOUT="wrong_timeout",
            ).get(key)

        mocker.patch("os.getenv", new=getenv)

        config = inventory_plugin._get_instance_from_env()
        assert config == dict(
            host="host",
            username="username",
            password="password",
            client_id="client_id",
            client_secret="client_secret",
            refresh_token="refresh_token",
            grant_type="grant_type",
            timeout=120,
        )

    def test_get_timeout_missing_env_value(self, inventory_plugin, mocker):
        def getenv(key):
            return dict(
                SN_HOST="host",
                SN_USERNAME="username",
                SN_PASSWORD="password",
                SN_CLIENT_ID="client_id",
                SN_CLIENT_SECRET="client_secret",
                SN_REFRESH_TOKEN="refresh_token",
                SN_GRANT_TYPE="grant_type",
            ).get(key)

        mocker.patch("os.getenv", new=getenv)

        config = inventory_plugin._get_instance_from_env()
        assert config == dict(
            host="host",
            username="username",
            password="password",
            client_id="client_id",
            client_secret="client_secret",
            refresh_token="refresh_token",
            grant_type="grant_type",
            timeout=120,
        )

    def test_get_timeout(self, inventory_plugin, mocker):
        def getenv(key):
            return dict(
                SN_HOST="host",
                SN_USERNAME="username",
                SN_PASSWORD="password",
                SN_CLIENT_ID="client_id",
                SN_CLIENT_SECRET="client_secret",
                SN_REFRESH_TOKEN="refresh_token",
                SN_GRANT_TYPE="grant_type",
                SN_TIMEOUT="50",
            ).get(key)

        mocker.patch("os.getenv", new=getenv)

        config = inventory_plugin._get_instance_from_env()
        assert config == dict(
            host="host",
            username="username",
            password="password",
            client_id="client_id",
            client_secret="client_secret",
            refresh_token="refresh_token",
            grant_type="grant_type",
            timeout=50,
        )


class TestInventoryModuleFillEnhancedAutoGroups:
    def test_construction(self, inventory_plugin):
        record = dict(
            sys_id="1",
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

        host = inventory_plugin.add_host(record, "fqdn")
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

        assert a1.vars == dict(inventory_file=None, inventory_dir=None)

    def test_construction_empty(self, inventory_plugin):
        record = dict(sys_id="1", fqdn="a1", relationship_groups=set())

        host = inventory_plugin.add_host(record, "fqdn")
        inventory_plugin.fill_enhanced_auto_groups(record, host)

        assert set(inventory_plugin.inventory.groups) == set(("all", "ungrouped"))

        assert set(inventory_plugin.inventory.hosts) == set(("a1",))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set()

        assert a1.vars == dict(inventory_file=None, inventory_dir=None)


class TestInventoryModuleFillConstructed:
    def test_construction_empty(self, inventory_plugin):
        records = []
        columns = []
        name_source = "fqdn"
        compose = {}
        groups = {}
        keyed_groups = []
        strict = False
        enhanced = False
        aggregation = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
            aggregation,
        )

        assert set(inventory_plugin.inventory.groups) == set(("all", "ungrouped"))
        assert set(inventory_plugin.inventory.hosts) == set()

    def test_construction_host(self, inventory_plugin):
        records = [
            dict(
                sys_id="1",
                fqdn="a1",
            ),
            dict(
                sys_id="2",
                fqdn="a2",
            ),
        ]

        columns = []
        name_source = "fqdn"
        compose = {}
        groups = {}
        keyed_groups = []
        strict = False
        enhanced = False
        aggregation = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
            aggregation,
        )

        assert set(inventory_plugin.inventory.groups) == set(("all", "ungrouped"))
        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set()

        assert a1.vars == dict(inventory_file=None, inventory_dir=None)

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set()

        assert a2.vars == dict(inventory_file=None, inventory_dir=None)

    def test_construction_hostvars(self, inventory_plugin):
        records = [
            dict(sys_id="1", fqdn="a1", cost="82", cost_cc="EUR"),
            dict(sys_id="2", fqdn="a2", cost="94", cost_cc="USD"),
        ]

        columns = ["cost", "cost_cc"]
        name_source = "fqdn"
        compose = {}
        groups = {}
        keyed_groups = []
        strict = False
        enhanced = False
        aggregation = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
            aggregation,
        )

        assert set(inventory_plugin.inventory.groups) == set(("all", "ungrouped"))
        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set()

        assert a1.vars == dict(
            inventory_file=None,
            inventory_dir=None,
            cost="82",
            cost_cc="EUR",
        )

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set()

        assert a2.vars == dict(
            inventory_file=None,
            inventory_dir=None,
            cost="94",
            cost_cc="USD",
        )

    def test_construction_composite_vars(self, inventory_plugin):
        records = [
            dict(
                sys_id="1",
                fqdn="a1",
                cost="82",
                cost_cc="EUR",
                sys_updated_on="2021-09-17 02:13:25",
            ),
            dict(
                sys_id="2",
                fqdn="a2",
                cost="94",
                cost_cc="USD",
                sys_updated_on="2021-08-30 01:47:03",
            ),
        ]

        columns = []
        name_source = "fqdn"
        compose = dict(
            cost_res='"%s %s" % (cost, cost_cc)',
            amortized_cost="(cost | int // 2) | string",
            sys_updated_on_date="sys_updated_on | slice(2) | first | join",
            sys_updated_on_time="sys_updated_on | slice(2) | list | last | join | trim",
            silently_failed="non_existing + 3",
        )
        groups = {}
        keyed_groups = []
        strict = False
        enhanced = False
        aggregation = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
            aggregation,
        )

        assert set(inventory_plugin.inventory.groups) == set(("all", "ungrouped"))
        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set()

        assert a1.vars == dict(
            inventory_file=None,
            inventory_dir=None,
            cost_res=("82 EUR"),
            amortized_cost=("41"),
            sys_updated_on_date=("2021-09-17"),
            sys_updated_on_time=("02:13:25"),
        )

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set()

        assert a2.vars == dict(
            inventory_file=None,
            inventory_dir=None,
            cost_res=("94 USD"),
            amortized_cost=("47"),
            sys_updated_on_date=("2021-08-30"),
            sys_updated_on_time=("01:47:03"),
        )

    def test_construction_composite_vars_strict(self, inventory_plugin):
        records = [
            dict(sys_id="1", fqdn="a1"),
            dict(sys_id="2", fqdn="a2"),
        ]

        columns = []
        name_source = "fqdn"
        compose = dict(failed=trust_jinja_input("non_existing + 3"))
        groups = {}
        keyed_groups = []
        strict = True
        enhanced = False
        aggregation = False

        with pytest.raises(AnsibleError, match="non_existing"):
            inventory_plugin.fill_constructed(
                records,
                columns,
                name_source,
                compose,
                groups,
                keyed_groups,
                strict,
                enhanced,
                aggregation,
            )

    def test_construction_composite_vars_ansible_host(self, inventory_plugin):
        records = [
            dict(
                sys_id="1",
                fqdn="a1",
            ),
            dict(
                sys_id="2",
                fqdn="a2",
            ),
        ]

        columns = []
        name_source = "fqdn"
        compose = dict(ansible_host='fqdn + "_" + sys_id')
        groups = {}
        keyed_groups = []
        strict = False
        enhanced = False
        aggregation = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
            aggregation,
        )

        assert set(inventory_plugin.inventory.groups) == set(("all", "ungrouped"))
        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set()

        assert a1.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="a1_1"
        )

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set()

        assert a2.vars == dict(
            inventory_file=None, inventory_dir=None, ansible_host="a2_2"
        )

    def test_construction_composed_groups(self, inventory_plugin):
        records = [
            dict(sys_id="1", ip_address="1.1.1.1", fqdn="a1"),
            dict(sys_id="2", ip_address="1.1.1.2", fqdn="a2"),
        ]

        columns = []
        name_source = "fqdn"
        compose = {}
        groups = dict(
            ip1=trust_jinja_input('ip_address == "1.1.1.1"'),
            ip2=trust_jinja_input('ip_address != "1.1.1.1"'),
            cost=trust_jinja_input("cost_usd < 90"),  # ignored due to strict = False
        )
        keyed_groups = []
        strict = False
        enhanced = False
        aggregation = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
            aggregation,
        )

        assert set(inventory_plugin.inventory.groups) == set(
            ("all", "ungrouped", "ip1", "ip2")
        )

        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set(("ip1",))

        assert a1.vars == dict(inventory_file=None, inventory_dir=None)

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set(("ip2",))

        assert a2.vars == dict(inventory_file=None, inventory_dir=None)

    def test_construction_composed_groups_strict(self, inventory_plugin):
        records = [
            dict(sys_id="1", ip_address="1.1.1.1", fqdn="a1"),
            dict(sys_id="2", ip_address="1.1.1.2", fqdn="a2"),
        ]

        columns = []
        name_source = "fqdn"
        compose = {}
        groups = dict(
            ip1=trust_jinja_input('ip_address == "1.1.1.1"'),
            ip2=trust_jinja_input('ip_address != "1.1.1.1"'),
            cost=trust_jinja_input("cost_usd < 90"),
        )
        keyed_groups = []
        strict = True
        enhanced = False
        aggregation = False

        with pytest.raises(AnsibleError, match="cost_usd"):
            inventory_plugin.fill_constructed(
                records,
                columns,
                name_source,
                compose,
                groups,
                keyed_groups,
                strict,
                enhanced,
                aggregation,
            )

    def test_construction_keyed_groups(self, inventory_plugin):
        records = [
            dict(sys_id="1", fqdn="a1", cost_cc="EUR"),
            dict(sys_id="2", fqdn="a2", cost_cc="USD"),
        ]

        columns = []
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
        aggregation = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
            aggregation,
        )

        assert set(inventory_plugin.inventory.groups) == set(
            ("all", "ungrouped", "cc_EUR", "cc_USD")
        )

        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)

        assert set(a1_groups) == set(("cc_EUR",))

        assert a1.vars == dict(inventory_file=None, inventory_dir=None)

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set(("cc_USD",))

        assert a2.vars == dict(inventory_file=None, inventory_dir=None)

    def test_construction_keyed_groups_with_parent(self, inventory_plugin):
        records = [
            dict(sys_id="1", ip_address="1.1.1.1", fqdn="a1", cost_cc="EUR"),
            dict(sys_id="2", ip_address="1.1.1.2", fqdn="a2", cost_cc="USD"),
        ]

        columns = []
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
        aggregation = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
            aggregation,
        )

        assert set(inventory_plugin.inventory.groups) == set(
            ("all", "ungrouped", "cc_EUR", "cc_USD", "ip_address")
        )

        assert set(inventory_plugin.inventory.hosts) == set(("a1", "a2"))

        a1 = inventory_plugin.inventory.get_host("a1")
        a1_groups = (group.name for group in a1.groups)
        assert set(a1_groups) == set(("cc_EUR", "ip_address"))

        assert a1.vars == dict(inventory_file=None, inventory_dir=None)

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set(("cc_USD", "ip_address"))

        assert a2.vars == dict(inventory_file=None, inventory_dir=None)

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
        name_source = "fqdn"
        compose = {}
        groups = {}
        keyed_groups = []
        strict = False
        enhanced = True
        aggregation = False

        inventory_plugin.fill_constructed(
            records,
            columns,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
            aggregation,
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

        assert a1.vars == dict(inventory_file=None, inventory_dir=None)

        a2 = inventory_plugin.inventory.get_host("a2")
        a2_groups = (group.name for group in a2.groups)
        assert set(a2_groups) == set(
            ("Storage_Area_Network_002_Sends_data_to", "OWA_SD_01_Runs_on")
        )

        assert a2.vars == dict(inventory_file=None, inventory_dir=None)

    def test_aggragation(self, inventory_plugin):
        records = [
            {"sys_id": "1", "app": "tomcat1", "app.env": "dev", "fqdn": "a1"},
            {"sys_id": "2", "app": "tomcat2", "app.env": "prod", "fqdn": "a1"},
            {"sys_id": "3", "app": "tomcat3", "app.env": "staging", "fqdn": "a1"},
            {"sys_i": "4", "app": "tomcat4", "app.env": "dev", "fqdn": "a2"},
        ]

        columns = [
            "app",
            "app.env",
            "fqdn",
        ]
        name_source = "fqdn"
        compose = {}
        groups = {}
        keyed_groups = []
        strict = False
        enhanced = False
        aggregation = True

        inventory_plugin.fill_constructed(
            records,
            columns,
            name_source,
            compose,
            groups,
            keyed_groups,
            strict,
            enhanced,
            aggregation,
        )

        a1 = inventory_plugin.inventory.get_host("a1")
        assert isinstance(a1.vars["app"], list)
        for val in a1.vars["app"]:
            assert "env" in val.keys()
            assert "app" in val.keys()
            assert val["env"] in ["prod", "dev", "staging"]
            assert val["app"] in ["tomcat1", "tomcat2", "tomcat3"]


class TestConstructCacheSuffix:
    def test_from_query(self, inventory_plugin, mocker):
        from base64 import b64encode

        real_suffix = b64encode("opt1_a_opt2_b".encode()).decode()

        def get_option(*args):
            return [dict(opt1="a"), dict(opt2="b")]

        mocker.patch.object(inventory_plugin, "get_option", new=get_option)

        suffix = inventory_plugin._construct_cache_suffix()

        assert suffix == real_suffix

    def test_from_query_2(self, inventory_plugin, mocker):
        from base64 import b64encode

        real_suffix = b64encode("opt1_a".encode()).decode()

        def get_option(*args):
            return [dict(opt1="a")]

        mocker.patch.object(inventory_plugin, "get_option", new=get_option)

        suffix = inventory_plugin._construct_cache_suffix()

        assert suffix == real_suffix

    def test_from_sysparm_query(self, inventory_plugin, mocker):
        from base64 import b64encode

        real_suffix = b64encode("a".encode()).decode()

        def get_option(*args):
            if args[0] == "sysparm_query":
                return "a"
            return []

        mocker.patch.object(inventory_plugin, "get_option", new=get_option)

        suffix = inventory_plugin._construct_cache_suffix()

        assert suffix == real_suffix

    def test_from_sysparm_query_2(self, inventory_plugin, mocker):
        def get_option(*args):
            return None

        mocker.patch.object(inventory_plugin, "get_option", new=get_option)

        suffix = inventory_plugin._construct_cache_suffix()

        assert suffix == ""


class TestInventoryModuleEnhancedQueryFeatures:
    def setup_get_option_side_effect(self, **options):
        def get_option(option_name):
            if option_name == "enhanced":
                return options.get("enhanced", True)
            return options.get(option_name, None)
        return get_option

    def setup_mocks(self, mocker):
        self.mock_fetch_records = mocker.patch('ansible_collections.servicenow.itsm.plugins.inventory.now.fetch_records')
        self.mock_fetch_records.return_value = []

        self.mock_enhance_records_with_rel_groups = mocker.patch('ansible_collections.servicenow.itsm.plugins.inventory.now.enhance_records_with_rel_groups')

        self.mock_table_client = mocker.Mock()
        self.mock_records = []

    def assert_fetch_records_called_with(self, query, expected_fields, is_encoded_query):
        self.mock_fetch_records.assert_called_once_with(
            self.mock_table_client,
            REL_TABLE,
            query=query,
            fields=expected_fields,
            is_encoded_query=is_encoded_query
        )

    def test_populate_enhanced_records_with_enhanced_query(self, inventory_plugin, mocker):
        """Test __populate_enhanced_records_from_remote with enhanced_query option"""
        mocker.patch.object(inventory_plugin, "get_option", side_effect=self.setup_get_option_side_effect(
            enhanced_query=[{"type.name": "Contains:Contained By"}],
            enhanced_additional_columns=["extra_col1", "extra_col2"],
        ))
        self.setup_mocks(mocker)

        # Test the method
        inventory_plugin._InventoryModule__populate_enhanced_records_from_remote(self.mock_table_client, self.mock_records)
        expected_fields = REL_FIELDS.union({"extra_col1", "extra_col2"})

        self.assert_fetch_records_called_with(
            query=[{"type.name": "Contains:Contained By"}],
            expected_fields=expected_fields,
            is_encoded_query=False,
        )

        # Verify enhance_records_with_rel_groups was called
        self.mock_enhance_records_with_rel_groups.assert_called_once_with(self.mock_records, [])

    def test_populate_enhanced_records_with_enhanced_sysparm_query(self, inventory_plugin, mocker):
        """Test __populate_enhanced_records_from_remote with enhanced_sysparm_query option"""

        mocker.patch.object(inventory_plugin, "get_option", side_effect=self.setup_get_option_side_effect(
            enhanced_sysparm_query="type.nameSTARTSWITHContains",
            enhanced_additional_columns=[],
        ))
        self.setup_mocks(mocker)

        # Call the method
        inventory_plugin._InventoryModule__populate_enhanced_records_from_remote(self.mock_table_client, self.mock_records)

        # Verify fetch_records was called with correct parameters
        self.assert_fetch_records_called_with(
            query="type.nameSTARTSWITHContains",
            expected_fields=REL_FIELDS,
            is_encoded_query=True,
        )

        # Verify enhance_records_with_rel_groups was called
        self.mock_enhance_records_with_rel_groups.assert_called_once_with(self.mock_records, [])

    def test_populate_enhanced_records_with_default_query(self, inventory_plugin, mocker):
        """Test __populate_enhanced_records_from_remote with no custom query (default REL_QUERY)"""
        mocker.patch.object(inventory_plugin, "get_option", side_effect=self.setup_get_option_side_effect(
            enhanced_additional_columns=["custom_col"],
        ))
        self.setup_mocks(mocker)

        # Call the method
        inventory_plugin._InventoryModule__populate_enhanced_records_from_remote(self.mock_table_client, self.mock_records)

        # Verify fetch_records was called with correct parameters
        expected_fields = REL_FIELDS.union({"custom_col"})

        self.assert_fetch_records_called_with(
            query=REL_QUERY,
            expected_fields=expected_fields,
            is_encoded_query=False,
        )

    def test_populate_enhanced_records_mutual_exclusivity_error(self, inventory_plugin, mocker):
        """Test that enhanced_query and enhanced_sysparm_query are mutually exclusive"""
        mocker.patch.object(inventory_plugin, "get_option", side_effect=self.setup_get_option_side_effect(
            enhanced_query=[{"type.name": "STARTSWITH Contains"}],
            enhanced_sysparm_query="type.nameSTARTSWITHContains",
            enhanced_additional_columns=[],
        ))
        self.setup_mocks(mocker)
        # Verify that AnsibleParserError is raised
        with pytest.raises(AnsibleParserError, match="Invalid configuration: 'enhanced_query' and 'enhanced_sysparm_query' are mutually exclusive"):
            inventory_plugin._InventoryModule__populate_enhanced_records_from_remote(self.mock_table_client, self.mock_records)

    def test_get_query_columns_with_enhanced(self, inventory_plugin, mocker):
        """Test __get_query_columns includes REL_FIELDS when enhanced is enabled"""
        mocker.patch.object(inventory_plugin, "get_option", side_effect=self.setup_get_option_side_effect(
            query_limit_columns=True,
            query_additional_columns=["extra_col"],
        ))

        columns = ["name", "ip_address"]
        result = inventory_plugin._InventoryModule__get_query_columns(columns)

        expected_columns = set(["name", "ip_address", "extra_col"]).union(REL_FIELDS)

        assert set(result) == expected_columns

    def test_get_query_columns_no_limit(self, inventory_plugin, mocker):
        """Test __get_query_columns returns None when query_limit_columns is False"""
        mocker.patch.object(inventory_plugin, "get_option", side_effect=self.setup_get_option_side_effect(
            query_limit_columns=False,
        ))

        columns = ["name", "ip_address"]
        result = inventory_plugin._InventoryModule__get_query_columns(columns)

        assert result is None
