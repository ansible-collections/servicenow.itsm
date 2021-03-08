# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os

from ansible.errors import AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin, to_safe_group_name

from ..module_utils.client import Client
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
  inventory_hostname_source:
    type: str
    description:
      - The column to use for inventory hostnames.
    default: name
  groups:
    description:
      - Group hosts in the provided groups, according to the specified criteria.
      - Only the specified groups will be created.
      - Mutually exclusive with I(group_by).
    type: dict
    default: {}
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
      - Mutually exclusive with I(groups).
    type: dict
    default: {}
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
groups:
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


# Configure inventory host names and host vars.
plugin: servicenow.itsm.now
columns:
  - name
  - classification
  - cpu_type
ansible_host_source: fqdn
inventory_hostname_source: asset_tag

# `ansible-inventory -i inventory.now.yaml --graph --vars` output:
# @all:
#  |--@ungrouped:
#  |  |--P1000019
#  |  |  |--{ansible_host = my.server.com}
#  |  |  |--{classification = Production}
#  |  |  |--{cpu_type = Intel}
#  |  |  |--{name = SAP-SD-02}
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


class InventoryModule(BaseInventoryPlugin):

    NAME = "servicenow.itsm.now"

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

    def validate_grouping_conditions(self, groups, group_by):
        for group, column in groups.items():
            for conditions in column.values():
                self._verify_includes_and_excludes(conditions)
        for column, conditions in group_by.items():
            self._verify_includes_and_excludes(conditions)

    def _query(self, conditions):
        columns = self.get_option("columns")
        ansible_host_source = self.get_option("ansible_host_source")
        inventory_hostname_source = self.get_option("inventory_hostname_source")

        requested_fields = set(
            columns
            + ["sys_id", ansible_host_source, inventory_hostname_source]
            + list(conditions.keys())
        )
        query = dict(
            # Request only the table columns we're interested in
            sysparm_fields=",".join(requested_fields),
            # Make references and choice fields human-readable
            sysparm_display_value=True,
        )
        sysparm_query = sysparm_query_from_conditions(conditions)
        if sysparm_query:
            query["sysparm_query"] = sysparm_query

        return query

    def add_host(self, record):
        ansible_host_source = self.get_option("ansible_host_source")
        inventory_hostname_source = self.get_option("inventory_hostname_source")

        if inventory_hostname_source not in record:
            # The user specified an invalid column
            raise AnsibleParserError(
                "Inventory hostname source column '{0}'"
                " is not present in table {1}.".format(
                    inventory_hostname_source, self.get_option("table")
                )
            )

        inventory_hostname = record[inventory_hostname_source]
        if inventory_hostname:
            host = self.inventory.add_host(inventory_hostname)
            if ansible_host_source in record and record[ansible_host_source]:
                self.inventory.set_variable(
                    host, "ansible_host", record[ansible_host_source]
                )
            else:
                self.display.warning(
                    "The ansible_host variable for host {0} is empty.".format(host)
                )

            return host

        self.display.warning(
            "Skipping host {0} due to empty {1}".format(
                record["sys_id"], inventory_hostname_source
            )
        )
        return None

    def set_hostvars(self, host, record):
        for k, v in record.items():
            if k in self.get_option("columns"):
                # Set all the columns that user desired as hostvars.
                self.inventory.set_variable(host, k, v)

    def fill_auto_groups(self, table_client, table, group_by):
        records = table_client.list_records(table, query=self._query(group_by))

        for record in records:
            host = self.add_host(record)
            if host:
                for category in group_by.keys():
                    group_name = to_safe_group_name(record[category])
                    # Only truthy names are allowed
                    # Column values can be set to "None", and we don't want those
                    if group_name:
                        self.inventory.add_group(group_name)
                        self.inventory.add_host(host, group=group_name)
                    else:
                        self.display.warning(
                            "Encountered invalid group name '{1}' for host {0}. Group will not be created.".format(
                                group_name, host
                            )
                        )

                self.set_hostvars(host, record)

    def fill_desired_groups(self, table_client, table, groups):
        for group_name, group_conditions in groups.items():
            self.inventory.add_group(group_name)

            records = table_client.list_records(
                table, query=self._query(group_conditions)
            )
            for r in records:
                host = self.add_host(r)
                self.inventory.add_host(host, group=group_name)
                self.set_hostvars(host, r)

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

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)

        self._read_config_data(path)

        groups = self.get_option("groups")
        group_by = self.get_option("group_by")
        if groups and group_by:
            raise AnsibleParserError(
                "Invalid configuration: 'groups' and 'group_by' are mutually exclusive."
            )

        self.validate_grouping_conditions(groups, group_by)

        client = Client(**self._get_instance())
        table_client = TableClient(client)

        table = self.get_option("table")
        if groups:
            # Creates exactly the specified groups (which might be empty).
            # Leaves nothing ungrouped.
            self.fill_desired_groups(table_client, table, groups)
        else:
            self.fill_auto_groups(table_client, table, group_by)
