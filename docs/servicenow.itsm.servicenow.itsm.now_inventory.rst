.. _servicenow.itsm.servicenow.itsm.now_inventory:


***********************************
servicenow.itsm.servicenow.itsm.now
***********************************

**Inventory source for ServiceNow table records.**



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
                        <div>Mutually exclusive with <em>groups</em>.</div>
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
    </table>
    <br/>




Examples
--------

.. code-block:: yaml+jinja

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




Status
------


Authors
~~~~~~~

- Manca Bizjak (@mancabizjak)
- Miha Dolinar (@mdolin)
- Tadej Borovsak (@tadeboro)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
