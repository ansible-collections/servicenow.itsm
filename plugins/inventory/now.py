# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os

from ansible.errors import AnsibleParserError
from ansible.inventory.group import to_safe_group_name as orig_safe
from ansible.plugins.inventory import (
    BaseInventoryPlugin,
    Constructable,
    to_safe_group_name,
)

from ..module_utils.client import Client
from ..module_utils.errors import ServiceNowError
from ..module_utils.query import parse_query, serialize_query
from ..module_utils.table import TableClient


DOCUMENTATION = r"""
name: servicenow.itsm.now
plugin_type: inventory
author:
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)
short_description: Inventory source for ServiceNow table records.
description:
  - Builds inventory from ServiceNow table records.
  - Requires a configuration file ending in C(now.yml) or C(now.yaml).
  - The plugin sets host variables denoted by I(columns).
version_added: 1.0.0
extends_documentation_fragment:
  - ansible.builtin.constructed
  - servicenow.itsm.query
notes:
  - Query feature and constructed groups were added in version 1.2.0.
options:
  plugin:
    description:
      - The name of the ServiceNow Inventory Plugin.
      - This should always be C(servicenow.itsm.now).
    required: true
    type: str
    choices: [ servicenow.itsm.now ]
  instance:
    description:
      - ServiceNow instance information.
    type: dict
    default: {}
    suboptions:
      host:
        description:
          - The ServiceNow host name.
        env:
          - name: SN_HOST
        required: true
        type: str
      username:
        description:
          - Username used for authentication.
        env:
          - name: SN_USERNAME
        required: true
        type: str
      password:
        description:
          - Password used for authentication.
        env:
          - name: SN_PASSWORD
        required: true
        type: str
      client_id:
        description:
          - ID of the client application used for OAuth authentication.
          - If provided, it requires I(client_secret).
        env:
          - name: SN_CLIENT_ID
        type: str
      client_secret:
        description:
          - Secret associated with I(client_id). Used for OAuth authentication.
          - If provided, it requires I(client_id).
        env:
          - name: SN_CLIENT_SECRET
        type: str
      timeout:
        description:
          - Timeout in seconds for the connection with the ServiceNow instance.
        env:
          - name: SN_TIMEOUT
        type: float
  table:
    description: The ServiceNow table to use as the inventory source.
    type: str
    default: cmdb_ci_server
  columns:
    description:
      - List of I(table) columns to be included as hostvars.
    type: list
    default: [name, host_name, fqdn, ip_address]
  ansible_host_source:
    description:
      - Host variable to use as I(ansible_host) when generating inventory hosts.
    type: str
    default: ip_address
    deprecated:
      why: Constructed features made this obsolete
      version: 2.0.0
      collection_name: servicenow.itsm
      alternatives: Use the 'compose' parameter to set the 'ansible_host' variable
  inventory_hostname_source:
    type: str
    description:
      - The column to use for inventory hostnames.
    default: name
  named_groups:
    description:
      - Group hosts in the provided groups, according to the specified criteria.
      - Only the specified groups will be created.
      - Mutually exclusive with I(group_by).
    type: dict
    default: {}
    deprecated:
      why: Constructed features made this obsolete
      version: 2.0.0
      collection_name: servicenow.itsm
      alternatives: Use the 'groups' parameter instead
    suboptions:
      <group_name>:
        type: dict
        description:
          - The group to create.
        default: {}
        suboptions:
          <column>:
            type: dict
            description: Criteria for including a host in this group.
            default: {}
            suboptions:
              includes:
                description:
                  - Add a host to the group only if <column> matches any of
                    the values specified in this list.
                  - For reference fields, you need to provide C(sys_id).
                  - Mutually exclusive with I(excludes).
                type: list
                default: None
              excludes:
                description:
                  - Add a host to the group if <column> matches any value
                    except the ones specified in this list.
                  - For reference fields, you need to provide C(sys_id).
                  - Mutually exclusive with I(includes).
                type: list
                default: None
  group_by:
    description:
      - Group hosts automatically, according to the values of the specified columns.
      - You can include or exclude records from being added to the inventory
        by limiting the column values with I(include) or I(exclude).
      - Mutually exclusive with I(named_groups).
    type: dict
    default: {}
    deprecated:
      why: Constructed features made this obsolete
      version: 2.0.0
      collection_name: servicenow.itsm
      alternatives: Use the 'query' and 'keyed_groups' parameters instead
    suboptions:
      <column>:
        type: dict
        description: Column to use when grouping inventory hosts into groups.
        default: {}
        suboptions:
          includes:
            description:
              - Create Ansible inventory groups only for records with <column>
                matching any of the values specified in this list.
              - For reference fields, you need to provide C(sys_id).
              - Mutually exclusive with I(excludes).
            type: list
            default: None
          excludes:
            description:
              - Create Ansible inventory groups only for records with <column>
                matching any value except the ones specified in this list.
              - For reference fields, you need to provide C(sys_id).
              - Mutually exclusive with I(includes).
            type: list
            default: None
"""

EXAMPLES = r"""
# A trivial example that creates a host from every record of the
# ServiceNow cmdb_ci_server table. The ip_address column is used for
# for ansible host, and server name for inventory hostname.
# No groups will be created - all the resulting hosts are ungrouped.
plugin: servicenow.itsm.now

# `ansible-inventory -i inventory.now.yaml --graph` output:
# @all:
#  |--@ungrouped:
#  |  |--DatabaseServer1
#  |  |--DatabaseServer2
#  |  |--INSIGHT-NY-03
#  |  |--MailServerUS
#  |  |--VMWARE-SD-04


# Group hosts automatically, according to values of the manufacturer column.
plugin: servicenow.itsm.now
keyed_groups:
  - key: manufacturer
    separator: ""

# `ansible-inventory -i inventory.now.yaml --graph` output:
# @all:
#  |--@Dell Inc.:
#  |  |--DatabaseServer1
#  |  |--DatabaseServer2
#  |  |--INSIGHT-NY-03
#  |--@Lenovo:
#  |  |--FileServerFloor1
#  |  |--FileServerFloor2
#  |--@ungrouped:

# Group hosts automatically, according to values of the os column. Filtering ensures
# that we only see selected operating systems.
plugin: servicenow.itsm.now
query:
  - os: = Linux Red Hat
  - os: = Windows XP
keyed_groups:
  - key: os
    prefix: os

# `ansible-inventory -i inventory.now.yaml --graph` output:
#  |--@os_Linux_Red_Hat:
#  |  |--DatabaseServer1
#  |  |--DatabaseServer2
#  |--@os_Windows_XP:
#  |  |--FileServerFloor1
#  |  |--FileServerFloor2
#  |  |--INSIGHT-NY-03
#  |--@ungrouped:

# Group hosts into named according to the specified criteria. Here, we created a group
# of non-Windows production servers.
plugin: servicenow.itsm.now
groups:
  non_windows_prod_servers: >-
    classification == "Production" and
    os not in ("Windows XP", "Windows 2000", "Windows 2000 Server")

# `ansible-inventory -i inventory.now.yaml --graph` output:
# @all:
#  |--@non_windows_prod_servers:
#  |  |--DatabaseServer2
#  |  |--PS LinuxApp01
#  |  |--PS LinuxApp02
#  |  |--lnux100
#  |  |--lnux101

# Add composed variables to hosts. In the following example, we created a cost variable
# that contains an amount and a currency, and set the ansible_host variable to the fqdn
# listed in the record.
plugin: servicenow.itsm.now
inventory_hostname_source: asset_tag
columns:
  - name
  - classification
  - cpu_type
compose:
    cost: cost ~ " " ~ cost_cc
    ansible_host: fqdn

# `ansible-inventory -i inventory.now.yaml --graph --vars` output:
# @all:
#  |--@ungrouped:
#  |  |--P1000019
#  |  |  |--{ansible_host = my.server.com}
#  |  |  |--{classification = Production}
#  |  |  |--{cost = 100 USD}
#  |  |  |--{cpu_type = Intel}
#  |  |  |--{name = SAP-SD-02}


# NOTE: All examples from here on are deprecated and should not be used when writing new
# inventory sources.

# Group hosts automatically, according to values of manufacturer and os columns.
# Include only records with the specified operating systems.
# Groups will most likely overlap.
plugin: servicenow.itsm.now
group_by:
  manufacturer:
  os:
    includes:
      - Linux Red Hat
      - Windows XP

# `ansible-inventory -i inventory.now.yaml --graph` output:
# @all:
#  |--@Dell_Inc_:
#  |  |--DatabaseServer1
#  |  |--DatabaseServer2
#  |  |--INSIGHT-NY-03
#  |--@Lenovo:
#  |  |--FileServerFloor1
#  |  |--FileServerFloor2
#  |--@Linux_Red_Hat:
#  |  |--DatabaseServer1
#  |  |--DatabaseServer2
#  |--@Windows_XP:
#  |  |--FileServerFloor1
#  |  |--FileServerFloor2
#  |  |--INSIGHT-NY-03
#  |--@ungrouped:


# Group hosts into named groups, according to the specified criteria.
# Below example creates a single group containing hosts that match
# all the criteria.
named_groups:
  non_windows_prod_servers:
    classification:
      includes: [ Production ]
    os:
      excludes:
        - Windows XP
        - Windows 2000
        - Windows 2000 Server
        - Windows 2003 Standard

# `ansible-inventory -i inventory.now.yaml --graph` output:
# @all:
#  |--@non_windows_prod_servers:
#  |  |--DatabaseServer2
#  |  |--PS LinuxApp01
#  |  |--PS LinuxApp02
#  |  |--lnux100
#  |  |--lnux101
#  |--@ungrouped:
"""


def _includes_query(column, includes):
    """ column, [v1, v2] -> 'column=v1^ORcolumn=v2' """
    return "^OR".join("{0}={1}".format(column, i) for i in includes)


def _excludes_query(column, excludes):
    """ column, [v1, v2] -> 'column!=v1^column!=v2' """
    return "^".join("{0}!={1}".format(column, i) for i in excludes)


def sysparm_query_from_conditions(conditions):
    """
    From a dictionary that holds conditions for the specified fields
    dict(
       a=dict(includes=["a1", "a2"]),
       b=dict(excludes=["b1", "b2"]),
    )
    creates the value directly usable for the sysparm_query ServiceNow API
    query parameter: "a=a1^ORa=a2^b!=b1^b!=b2"
    """
    param_queries = []
    for column, val in conditions.items():
        if val:
            includes = val.get("includes")
            if includes:
                param_queries.append(_includes_query(column, includes))
            excludes = val.get("excludes")
            if excludes:
                param_queries.append(_excludes_query(column, excludes))
    if param_queries:
        return "^".join(param_queries)
    return None


def construct_sysparm_query(query):
    parsed, err = parse_query(query)
    if err:
        raise AnsibleParserError(err)
    return serialize_query(parsed)


def fetch_records(table_client, table, query):
    snow_query = dict(
        # Make references and choice fields human-readable
        sysparm_display_value=True,
    )
    if query:
        snow_query["sysparm_query"] = construct_sysparm_query(query)

    return table_client.list_records(table, snow_query)


class InventoryModule(BaseInventoryPlugin, Constructable):

    NAME = "servicenow.itsm.now"

    # Constructable methods use the _sanitize_group_name class method to filter out
    # invalid characters from group names. By default, characters that are not valid in
    # python variables, are always replaced by underscores. We are overriding this with
    # a function that respects the TRANSFORM_INVALID_GROUP_CHARS configuration option
    # and allows users to control the behavior.
    _sanitize_group_name = staticmethod(orig_safe)

    def verify_file(self, path):
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(("now.yaml", "now.yml")):
                return True
            self.display.vvv(
                'Skipping due to inventory source not ending in "now.yaml" nor "now.yml"'
            )
        return False

    def _verify_includes_and_excludes(self, conditions):
        if conditions and all(i in conditions for i in ["includes", "excludes"]):
            raise AnsibleParserError(
                "Invalid configuration: 'includes' and 'excludes' are mutually exclusive."
            )

    def validate_grouping_conditions(self, named_groups, group_by):
        for group, column in named_groups.items():
            for conditions in column.values():
                self._verify_includes_and_excludes(conditions)
        for column, conditions in group_by.items():
            self._verify_includes_and_excludes(conditions)

    def query(self, conditions, host_source, name_source, columns):
        fields = set(columns).union(("sys_id", host_source, name_source), conditions)
        query = dict(
            # Request only the table columns we're interested in
            sysparm_fields=",".join(fields),
            # Make references and choice fields human-readable
            sysparm_display_value=True,
        )
        sysparm_query = sysparm_query_from_conditions(conditions)
        if sysparm_query:
            query["sysparm_query"] = sysparm_query

        return query

    def add_host(self, record, host_source, name_source):
        if host_source not in record:
            msg = "Ansible host source column '{0}' is not present in the record."
            raise AnsibleParserError(msg.format(host_source))

        if name_source not in record:
            msg = "Inventory hostname source column '{0}' is not present in the record."
            raise AnsibleParserError(msg.format(name_source))

        inventory_hostname = record[name_source]
        if inventory_hostname:
            host = self.inventory.add_host(inventory_hostname)
            if record[host_source]:
                self.inventory.set_variable(host, "ansible_host", record[host_source])
            else:
                self.display.warning(
                    "The ansible_host variable for host {0} is empty.".format(host)
                )

            return host

        self.display.warning(
            "Skipping host {0} due to empty {1}".format(record["sys_id"], name_source)
        )
        return None

    def set_hostvars(self, host, record, columns):
        missing = set(columns).difference(record)
        if missing:
            raise AnsibleParserError(
                "Invalid column names: {0}.".format(", ".join(missing))
            )

        for k in columns:
            self.inventory.set_variable(host, k, record[k])

    def fill_auto_groups(
        self, table_client, table, host_source, name_source, columns, group_by
    ):
        records = table_client.list_records(
            table, query=self.query(group_by, host_source, name_source, columns)
        )

        for record in records:
            host = self.add_host(record, host_source, name_source)
            if host:
                for category in group_by.keys():
                    group_name = to_safe_group_name(record[category])
                    # Only truthy names are allowed
                    # Column values can be set to "None", and we don't want those
                    if group_name:
                        self.inventory.add_group(group_name)
                        self.inventory.add_host(host, group=group_name)
                    else:
                        msg = (
                            "Encountered invalid group name '{1}' for host {0}. "
                            "Group will not be created."
                        ).format(group_name, host)
                        self.display.warning(msg)

                self.set_hostvars(host, record, columns)

    def fill_desired_groups(
        self, table_client, table, host_source, name_source, columns, named_groups
    ):
        for group_name, group_conditions in named_groups.items():
            self.inventory.add_group(group_name)

            records = table_client.list_records(
                table,
                query=self.query(group_conditions, host_source, name_source, columns),
            )
            for r in records:
                host = self.add_host(r, host_source, name_source)
                self.inventory.add_host(host, group=group_name)
                self.set_hostvars(host, r, columns)

    def fill_constructed(
        self,
        records,
        columns,
        host_source,
        name_source,
        compose,
        groups,
        keyed_groups,
        strict,
    ):
        for record in records:
            host = self.add_host(record, host_source, name_source)
            if host:
                self.set_hostvars(host, record, columns)
                self._set_composite_vars(compose, record, host, strict)
                self._add_host_to_composed_groups(groups, record, host, strict)
                self._add_host_to_keyed_groups(keyed_groups, record, host, strict)

    def _merge_instance_config(self, instance_config, instance_env):
        # Pulls the values from the environment, and if necessary, overrides
        # with configuration provided in the inventory source.
        instance = instance_env.copy()
        given_keys = instance_config.keys()
        to_override = set(instance.keys()).intersection(given_keys)
        for option in to_override:
            instance[option] = instance_config[option]
        return instance

    def _get_instance_from_env(self):
        return dict(
            host=os.getenv("SN_HOST"),
            username=os.getenv("SN_USERNAME"),
            password=os.getenv("SN_PASSWORD"),
            client_id=os.getenv("SN_CLIENT_ID"),
            client_secret=os.getenv("SN_SECRET_ID"),
            timeout=os.getenv("SN_TIMEOUT"),
        )

    def _get_instance(self):
        instance_config = self.get_option("instance")
        instance_env = self._get_instance_from_env()
        return self._merge_instance_config(instance_config, instance_env)

    # The next function is a temporary workaround for
    # https://github.com/ansible/ansible/issues/73051. In an ideal world, Ansible would
    # print the deprecation messages in its own. But until that bug is fixed, we need to
    # manually print the warning if we want our users to see the deprecation message
    # during the runtime.
    def _warn_about_deprecations(self):
        for opt in ("ansible_host_source", "named_groups", "group_by"):
            if self.get_option(opt):
                self.display.warning(
                    "'{0}' option is deprecated since version 1.2.0 and will be "
                    "removed in 2.0.0.".format(opt)
                )

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)

        self._read_config_data(path)

        self._warn_about_deprecations()

        named_groups = self.get_option("named_groups")
        group_by = self.get_option("group_by")
        if named_groups and group_by:
            raise AnsibleParserError(
                "Invalid configuration: 'named_groups' and 'group_by' are mutually "
                "exclusive."
            )

        self.validate_grouping_conditions(named_groups, group_by)

        try:
            client = Client(**self._get_instance())
        except ServiceNowError as e:
            raise AnsibleParserError(e)
        table_client = TableClient(client)

        table = self.get_option("table")
        host_source = self.get_option("ansible_host_source")
        name_source = self.get_option("inventory_hostname_source")
        columns = self.get_option("columns")

        if named_groups:
            # Creates exactly the specified groups (which might be empty).
            # Leaves nothing ungrouped.
            self.fill_desired_groups(
                table_client, table, host_source, name_source, columns, named_groups
            )
            return

        if group_by:
            self.fill_auto_groups(
                table_client, table, host_source, name_source, columns, group_by
            )
            return

        # TODO: Insert caching here once we remove deprecated functionality
        records = fetch_records(
            table_client, self.get_option("table"), self.get_option("query")
        )
        self.fill_constructed(
            records,
            self.get_option("columns"),
            self.get_option("ansible_host_source"),
            self.get_option("inventory_hostname_source"),
            self.get_option("compose"),
            self.get_option("groups"),
            self.get_option("keyed_groups"),
            self.get_option("strict"),
        )
