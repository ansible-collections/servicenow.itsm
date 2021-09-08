.. _servicenow.itsm.servicenow.itsm.now_inventory:


***********************************
servicenow.itsm.servicenow.itsm.now
***********************************

**Inventory source for ServiceNow table records.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Builds inventory from ServiceNow table records.
- Requires a configuration file ending in ``now.yml`` or ``now.yaml``.
- The plugin sets host variables denoted by *columns*.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="4">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ansible_host_source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"ip_address"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Host variable to use as <em>ansible_host</em> when generating inventory hosts.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>columns</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">["name", "host_name", "fqdn", "ip_address"]</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>List of <em>table</em> columns to be included as hostvars.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>compose</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Create vars from jinja2 expressions.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>group_by</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Group hosts automatically, according to the values of the specified columns.</div>
                        <div>You can include or exclude records from being added to the inventory by limiting the column values with <em>include</em> or <em>exclude</em>.</div>
                        <div>Mutually exclusive with <em>named_groups</em>.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b><column></b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Column to use when grouping inventory hosts into groups.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>excludes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"None"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Create Ansible inventory groups only for records with &lt;column&gt; matching any value except the ones specified in this list.</div>
                        <div>For reference fields, you need to provide <code>sys_id</code>.</div>
                        <div>Mutually exclusive with <em>includes</em>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>includes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"None"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Create Ansible inventory groups only for records with &lt;column&gt; matching any of the values specified in this list.</div>
                        <div>For reference fields, you need to provide <code>sys_id</code>.</div>
                        <div>Mutually exclusive with <em>excludes</em>.</div>
                </td>
            </tr>


            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>groups</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Add hosts to group based on Jinja2 conditionals.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>instance</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>ServiceNow instance information.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>client_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:SN_CLIENT_ID</div>
                    </td>
                <td>
                        <div>ID of the client application used for OAuth authentication.</div>
                        <div>If provided, it requires <em>client_secret</em>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>client_secret</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:SN_CLIENT_SECRET</div>
                    </td>
                <td>
                        <div>Secret associated with <em>client_id</em>. Used for OAuth authentication.</div>
                        <div>If provided, it requires <em>client_id</em>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:SN_HOST</div>
                    </td>
                <td>
                        <div>The ServiceNow host name.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:SN_PASSWORD</div>
                    </td>
                <td>
                        <div>Password used for authentication.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">float</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:SN_TIMEOUT</div>
                    </td>
                <td>
                        <div>Timeout in seconds for the connection with the ServiceNow instance.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>username</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:SN_USERNAME</div>
                    </td>
                <td>
                        <div>Username used for authentication.</div>
                </td>
            </tr>

            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>inventory_hostname_source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"name"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The column to use for inventory hostnames.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>keyed_groups</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">[]</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Add hosts to group based on the values of a variable.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>leading_separator</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.11</div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"yes"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Use in conjunction with keyed_groups.</div>
                        <div>By default, a keyed group that does not have a prefix or a separator provided will have a name that starts with an underscore.</div>
                        <div>This is because the default prefix is &quot;&quot; and the default separator is &quot;_&quot;.</div>
                        <div>Set this option to False to omit the leading underscore (or other separator) if no prefix is given.</div>
                        <div>If the group name is derived from a mapping the separator is still used to concatenate the items.</div>
                        <div>To not use a separator in the group name at all, set the separator for the keyed group to an empty string instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>named_groups</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Group hosts in the provided groups, according to the specified criteria.</div>
                        <div>Only the specified groups will be created.</div>
                        <div>Mutually exclusive with <em>group_by</em>.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b><group_name></b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The group to create.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b><column></b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Criteria for including a host in this group.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>excludes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"None"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Add a host to the group if &lt;column&gt; matches any value except the ones specified in this list.</div>
                        <div>For reference fields, you need to provide <code>sys_id</code>.</div>
                        <div>Mutually exclusive with <em>includes</em>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>includes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"None"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Add a host to the group only if &lt;column&gt; matches any of the values specified in this list.</div>
                        <div>For reference fields, you need to provide <code>sys_id</code>.</div>
                        <div>Mutually exclusive with <em>excludes</em>.</div>
                </td>
            </tr>



            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>plugin</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>servicenow.itsm.now</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The name of the ServiceNow Inventory Plugin.</div>
                        <div>This should always be <code>servicenow.itsm.now</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>query</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Provides a set of operators for use with filters, condition builders, and encoded queries.</div>
                        <div>The data type of a field determines what operators are available for it. Refer to the ServiceNow Available Filters Queries documentation at <a href='https://docs.servicenow.com/bundle/quebec-platform-user-interface/page/use/common-ui-elements/reference/r_OpAvailableFiltersQueries.html'>https://docs.servicenow.com/bundle/quebec-platform-user-interface/page/use/common-ui-elements/reference/r_OpAvailableFiltersQueries.html</a>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>strict</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                    <td>
                    </td>
                <td>
                        <div>If <code>yes</code> make invalid entries a fatal error, otherwise skip and continue.</div>
                        <div>Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>table</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"cmdb_ci_server"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The ServiceNow table to use as the inventory source.</div>
                </td>
            </tr>
            <tr>
                <td colspan="4">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>use_extra_vars</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.11</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                    <td>
                            <div> ini entries:
                                    <p>[inventory_plugins]<br>use_extra_vars = no</p>
                            </div>
                                <div>env:ANSIBLE_INVENTORY_USE_EXTRA_VARS</div>
                    </td>
                <td>
                        <div>Merge extra vars into the available variables for composition (highest precedence).</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Query feature and constructed groups were added in version 1.2.0.



Examples
--------

.. code-block:: yaml

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




Status
------


Authors
~~~~~~~

- Manca Bizjak (@mancabizjak)
- Miha Dolinar (@mdolin)
- Tadej Borovsak (@tadeboro)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
