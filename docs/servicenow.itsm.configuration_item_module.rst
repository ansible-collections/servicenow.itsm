.. _servicenow.itsm.configuration_item_module:


**********************************
servicenow.itsm.configuration_item
**********************************

**Manage ServiceNow configuration items**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Create, delete or update a ServiceNow configuration item.
- For more information, refer to the ServiceNow configuration management documentation at https://docs.servicenow.com/bundle/paris-servicenow-platform/page/product/configuration-management/reference/cmdb-table-property-descriptions.html.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>asset_tag</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Asset tag of the asset logically related to this configuration item.</div>
                        <div>Read more about the relationship between configuration items and assets at <a href='https://docs.servicenow.com/bundle/paris-it-asset-management/page/product/asset-management/concept/c_ManagingAssets.html'>https://docs.servicenow.com/bundle/paris-it-asset-management/page/product/asset-management/concept/c_ManagingAssets.html</a>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>assigned_to</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A person to whom this configuration item is assigned to.</div>
                        <div>Expected value for <em>assigned_to</em> is user id (usually in the form of <code>first_name.last_name</code>).</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>attachments</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.2.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>ServiceNow attachments.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the file to be uploaded without the file extension.</div>
                        <div>If not specified, the module will use <em>path</em>&#x27;s base name.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Path to the file to be uploaded.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>MIME type of the file to be attached.</div>
                        <div>If not specified, the module will try to guess the file&#x27;s type from its extension.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>category</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Category of the configuration item, for instance <code>Hardware</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>environment</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>development</li>
                                    <li>production</li>
                                    <li>test</li>
                        </ul>
                </td>
                <td>
                        <div>The environment to which this configuration item belongs.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>install_status</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>implementing</li>
                                    <li>installed</li>
                                    <li>on_order</li>
                                    <li>in_maintenance</li>
                                    <li>pending_install</li>
                                    <li>pending_repair</li>
                                    <li>in_stock</li>
                                    <li>retired</li>
                                    <li>stolen</li>
                                    <li>absent</li>
                        </ul>
                </td>
                <td>
                        <div>The functional status of the configuration item.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>instance</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>ServiceNow instance information.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>ID of the client application used for OAuth authentication.</div>
                        <div>If not set, the value of the <code>SN_CLIENT_ID</code> environment variable will be used.</div>
                        <div>If provided, it requires <em>client_secret</em>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Secret associated with <em>client_id</em>. Used for OAuth authentication.</div>
                        <div>If not set, the value of the <code>SN_CLIENT_SECRET</code> environment variable will be used.</div>
                        <div>If provided, it requires <em>client_id</em>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>grant_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.1.0</div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>password</b>&nbsp;&larr;</div></li>
                                    <li>refresh_token</li>
                        </ul>
                </td>
                <td>
                        <div>Grant type used for OAuth authentication.</div>
                        <div>If not set, the value of the <code>SN_GRANT_TYPE</code> environment variable will be used.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>The ServiceNow host name.</div>
                        <div>If not set, the value of the <code>SN_HOST</code> environment variable will be used.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Password used for authentication.</div>
                        <div>If not set, the value of the <code>SN_PASSWORD</code> environment variable will be used.</div>
                        <div>Required when using basic authentication or when <em>grant_type=password</em>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>refresh_token</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.1.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>Refresh token used for OAuth authentication.</div>
                        <div>If not set, the value of the <code>SN_REFRESH_TOKEN</code> environment variable will be used.</div>
                        <div>Required when <em>grant_type=refresh_token</em>.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>Timeout in seconds for the connection with the ServiceNow instance.</div>
                        <div>If not set, the value of the <code>SN_TIMEOUT</code> environment variable will be used.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>username</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Username used for authentication.</div>
                        <div>If not set, the value of the <code>SN_USERNAME</code> environment variable will be used.</div>
                        <div>Required when using basic authentication or when <em>grant_type=password</em>.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ip_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Primary IP address used by the configuration item.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>mac_address</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>MAC address of the configuration item.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name of the configuration item.</div>
                        <div>Required if the configuration item does not yet exist.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>operational_status</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>operational</li>
                                    <li>non_operational</li>
                                    <li>repair_in_progress</li>
                                    <li>dr_standby</li>
                                    <li>ready</li>
                                    <li>retired</li>
                                    <li>pipeline</li>
                                    <li>catalog</li>
                        </ul>
                </td>
                <td>
                        <div>The operational status of the configuration item.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>other</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Any of the remaining configuration parameters.</div>
                        <div>For the attributes of the base <code>cmdb_ci</code> table, refer to the ServiceNow documentation on <a href='https://docs.servicenow.com/bundle/paris-servicenow-platform/page/product/configuration-management/reference/cmdb-table-property-descriptions.html'>https://docs.servicenow.com/bundle/paris-servicenow-platform/page/product/configuration-management/reference/cmdb-table-property-descriptions.html</a>.</div>
                        <div>For the attributes of configuration items specific to <em>sys_class_name</em>, please consult the relevant ServiceNow documentation.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>serial_number</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Serial number of the configuration item.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>short_description</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Short description of the configuration item.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                    <li>absent</li>
                        </ul>
                </td>
                <td>
                        <div>State of the configuration item.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sys_class_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>ServiceNow configuration item class.</div>
                        <div>The value of this parameter should point to a ServiceNow CMDB configuration item table, for instance <code>cmdb_ci_server</code>.</div>
                        <div>For a list of valid CMDB tables, refer to ServiceNow documentation on <a href='https://docs.servicenow.com/bundle/paris-servicenow-platform/page/product/configuration-management/reference/cmdb-tables-details.html'>https://docs.servicenow.com/bundle/paris-servicenow-platform/page/product/configuration-management/reference/cmdb-tables-details.html</a>.</div>
                        <div>If this parameter is unset when a new configuration item needs to be created, the default value <code>cmdb_ci</code> will be used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sys_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Unique identifier of the record to operate on.</div>
                </td>
            </tr>
    </table>
    <br/>



See Also
--------

.. seealso::

   :ref:`servicenow.itsm.configuration_item_info_module`
      The official documentation on the **servicenow.itsm.configuration_item_info** module.


Examples
--------

.. code-block:: yaml

    - name: Create a configuration item
      servicenow.itsm.configuration_item:
        name: HPE ProLiant BL465C G7
        short_description: HPE ProLiant Server G7
        serial_number: ECE-164-E10834-NO
        asset_tag: P1000613
        sys_class_name: cmdb_ci_server
        assigned_to: some.user
        environment: production
        category: Hardware
        attachments:
          - path: path/to/attachment.txt
        other:
          model_number: BL465C G7
      register: server

    - name: Update a configuration item
      servicenow.itsm.configuration_item:
        sys_id: "{{ server.record.sys_id }}"
        install_status: in_maintenance
        operational_status: repair_in_progress
        other:
          fault_count: 1
          classification: Development

    - name: Delete a configuration item
      servicenow.itsm.configuration_item:
        sys_id: "{{ server.record.sys_id }}"
        state: absent



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>record</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>The configuration item record.</div>
                            <div>Note that the fields of the returned record depend on the configuration item&#x27;s <em>sys_class_name</em>.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;asset&#x27;: &#x27;05a9ec0d3790200044e0bfc8bcbe5dc2&#x27;, &#x27;asset_tag&#x27;: &#x27;P1000440&#x27;, &#x27;assigned&#x27;: &#x27;2019-02-28 08:00:00&#x27;, &#x27;assigned_to&#x27;: &#x27;8a826bf03710200044e0bfc8bcbe5d96&#x27;, &#x27;assignment_group&#x27;: &#x27;&#x27;, &#x27;attachments&#x27;: [{&#x27;average_image_color&#x27;: &#x27;&#x27;, &#x27;chunk_size_bytes&#x27;: &#x27;700000&#x27;, &#x27;compressed&#x27;: &#x27;true&#x27;, &#x27;content_type&#x27;: &#x27;text/plain&#x27;, &#x27;download_link&#x27;: &#x27;https://www.example.com/api/now/attachment/919d34d50706301022f9ffa08c1ed047/file&#x27;, &#x27;file_name&#x27;: &#x27;sample_file1.txt&#x27;, &#x27;hash&#x27;: &#x27;6f2b0dec698566114435a23f15dcac848a40e1fd3e0eda4afe24a663dda23f2e&#x27;, &#x27;image_height&#x27;: &#x27;&#x27;, &#x27;image_width&#x27;: &#x27;&#x27;, &#x27;size_bytes&#x27;: &#x27;210&#x27;, &#x27;size_compressed&#x27;: &#x27;206&#x27;, &#x27;state&#x27;: &#x27;pending&#x27;, &#x27;sys_created_by&#x27;: &#x27;admin&#x27;, &#x27;sys_created_on&#x27;: &#x27;2021-08-17 11:18:58&#x27;, &#x27;sys_id&#x27;: &#x27;919d34d50706301022f9ffa08c1ed047&#x27;, &#x27;sys_mod_count&#x27;: &#x27;0&#x27;, &#x27;sys_tags&#x27;: &#x27;&#x27;, &#x27;sys_updated_by&#x27;: &#x27;admin&#x27;, &#x27;sys_updated_on&#x27;: &#x27;2021-08-17 11:18:58&#x27;, &#x27;table_name&#x27;: &#x27;cmdb_ci&#x27;, &#x27;table_sys_id&#x27;: &#x27;459d34d50706301022f9ffa08c1ed06a&#x27;}], &#x27;attestation_score&#x27;: &#x27;&#x27;, &#x27;attested&#x27;: &#x27;false&#x27;, &#x27;attested_by&#x27;: &#x27;&#x27;, &#x27;attested_date&#x27;: &#x27;&#x27;, &#x27;attributes&#x27;: &#x27;&#x27;, &#x27;can_print&#x27;: &#x27;false&#x27;, &#x27;category&#x27;: &#x27;Hardware&#x27;, &#x27;change_control&#x27;: &#x27;&#x27;, &#x27;checked_in&#x27;: &#x27;&#x27;, &#x27;checked_out&#x27;: &#x27;&#x27;, &#x27;comments&#x27;: &#x27;&#x27;, &#x27;company&#x27;: &#x27;81fca4cbac1d55eb355b4b6db0e3c80f&#x27;, &#x27;correlation_id&#x27;: &#x27;&#x27;, &#x27;cost&#x27;: &#x27;1699.99&#x27;, &#x27;cost_cc&#x27;: &#x27;USD&#x27;, &#x27;cost_center&#x27;: &#x27;d9d01546c0a80a6403e18b82250c80a1&#x27;, &#x27;delivery_date&#x27;: &#x27;2018-07-05 07:00:00&#x27;, &#x27;department&#x27;: &#x27;a581ab703710200044e0bfc8bcbe5de8&#x27;, &#x27;discovery_source&#x27;: &#x27;&#x27;, &#x27;dns_domain&#x27;: &#x27;&#x27;, &#x27;due&#x27;: &#x27;&#x27;, &#x27;due_in&#x27;: &#x27;&#x27;, &#x27;duplicate_of&#x27;: &#x27;&#x27;, &#x27;environment&#x27;: &#x27;&#x27;, &#x27;fault_count&#x27;: &#x27;0&#x27;, &#x27;first_discovered&#x27;: &#x27;&#x27;, &#x27;fqdn&#x27;: &#x27;&#x27;, &#x27;gl_account&#x27;: &#x27;&#x27;, &#x27;install_date&#x27;: &#x27;2018-10-02 07:00:00&#x27;, &#x27;install_status&#x27;: &#x27;installed&#x27;, &#x27;invoice_number&#x27;: &#x27;&#x27;, &#x27;ip_address&#x27;: &#x27;&#x27;, &#x27;justification&#x27;: &#x27;&#x27;, &#x27;last_discovered&#x27;: &#x27;&#x27;, &#x27;lease_id&#x27;: &#x27;&#x27;, &#x27;life_cycle_stage&#x27;: &#x27;&#x27;, &#x27;life_cycle_stage_status&#x27;: &#x27;&#x27;, &#x27;location&#x27;: &#x27;8228cda2ac1d55eb7029baf443945c37&#x27;, &#x27;mac_address&#x27;: &#x27;&#x27;, &#x27;maintenance_schedule&#x27;: &#x27;&#x27;, &#x27;managed_by&#x27;: &#x27;&#x27;, &#x27;managed_by_group&#x27;: &#x27;&#x27;, &#x27;manufacturer&#x27;: &#x27;aa0a6df8c611227601cd2ed45989e0ac&#x27;, &#x27;model_id&#x27;: &#x27;0c43b858c611227501522de20c61ac75&#x27;, &#x27;model_number&#x27;: &#x27;&#x27;, &#x27;monitor&#x27;: &#x27;false&#x27;, &#x27;name&#x27;: &#x27;ThinkStation S20&#x27;, &#x27;operational_status&#x27;: &#x27;operational&#x27;, &#x27;order_date&#x27;: &#x27;2018-06-07 07:00:00&#x27;, &#x27;owned_by&#x27;: &#x27;&#x27;, &#x27;po_number&#x27;: &#x27;PO100005&#x27;, &#x27;purchase_date&#x27;: &#x27;2018-06-22&#x27;, &#x27;schedule&#x27;: &#x27;&#x27;, &#x27;serial_number&#x27;: &#x27;WCL-206-Q10853-BF&#x27;, &#x27;short_description&#x27;: &#x27;&#x27;, &#x27;skip_sync&#x27;: &#x27;false&#x27;, &#x27;start_date&#x27;: &#x27;&#x27;, &#x27;subcategory&#x27;: &#x27;Computer&#x27;, &#x27;support_group&#x27;: &#x27;&#x27;, &#x27;supported_by&#x27;: &#x27;&#x27;, &#x27;sys_class_name&#x27;: &#x27;cmdb_ci_computer&#x27;, &#x27;sys_class_path&#x27;: &#x27;/!!/!2/!(&#x27;, &#x27;sys_created_by&#x27;: &#x27;admin&#x27;, &#x27;sys_created_on&#x27;: &#x27;2012-02-18 08:14:42&#x27;, &#x27;sys_domain&#x27;: &#x27;global&#x27;, &#x27;sys_domain_path&#x27;: &#x27;/&#x27;, &#x27;sys_id&#x27;: &#x27;01a9ec0d3790200044e0bfc8bcbe5dc3&#x27;, &#x27;sys_mod_count&#x27;: &#x27;6&#x27;, &#x27;sys_tags&#x27;: &#x27;&#x27;, &#x27;sys_updated_by&#x27;: &#x27;system&#x27;, &#x27;sys_updated_on&#x27;: &#x27;2021-01-16 05:50:31&#x27;, &#x27;unverified&#x27;: &#x27;false&#x27;, &#x27;vendor&#x27;: &#x27;aa0a6df8c611227601cd2ed45989e0ac&#x27;, &#x27;warranty_expiration&#x27;: &#x27;2021-10-01&#x27;}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Manca Bizjak (@mancabizjak)
- Miha Dolinar (@mdolin)
- Tadej Borovsak (@tadeboro)
- Matej Pevec (@mysteriouswolf)
