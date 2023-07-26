.. _servicenow.itsm.configuration_item_batch_module:


****************************************
servicenow.itsm.configuration_item_batch
****************************************

**Manage ServiceNow configuration items in batch mode**


Version added: 1.2.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Create, update ServiceNow configuration items in batch mode.
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
                    <b>dataset</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of dictionaries that will be used as a data source.</div>
                        <div>Each item in a list represents one CMDB item.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>id_column_set</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Columns that should be used to identify an existing record that we need to update.</div>
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
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.1.0 of servicenow.itsm</div>
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
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 1.1.0 of servicenow.itsm</div>
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
                    <b>map</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Transformation instructions on how to convert input data to CMDB items.</div>
                        <div>Keys represent the CMDB item column names and the values are Jinja expressions that extract the value from the source data.</div>
                        <div>Data is returned as string because ServiceNow API expect this</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sys_class_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Table name (configuration item type) that we would like to manipulate.</div>
                </td>
            </tr>
    </table>
    <br/>



See Also
--------

.. seealso::

   :ref:`servicenow.itsm.configuration_item_module`
      The official documentation on the **servicenow.itsm.configuration_item** module.
   :ref:`servicenow.itsm.configuration_item_info_module`
      The official documentation on the **servicenow.itsm.configuration_item_info** module.


Examples
--------

.. code-block:: yaml

    - name: Update CMDB with some data
      servicenow.itsm.configuration_item_batch:
        sys_class_name: cmdb_ci_ec2_instance
        id_column_set: vm_inst_id
        dataset:
          - instance_id: 12345
            public_ip_address: 1.2.3.4
            tags:
              Name: my_name
          - instance_id: 54321
            public_ip_address: 4.3.2.1
            tags:
              Name: other_name
        map:
          vm_inst_id: instance_id
          ip_address: public_ip_address
          name: tags.Name

    - name: Identify CMDB item using combination of two columns
      servicenow.itsm.configuration_item_batch:
        sys_class_name: cmdb_ci_server
        id_column_set:
          - name
          - ip_address
        dataset: "{{ input_data }}"
        map:
          name: tags.Name
          ip_address: private_ip_address



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
                    <b>records</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>A list of configuration item records.</div>
                            <div>Note that the fields of the returned records depend on the configuration item&#x27;s <em>sys_class_name</em>.</div>
                            <div>Returning of values added in version 2.0.0.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;skip_sync&#x27;: &#x27;false&#x27;, &#x27;assignment_group&#x27;: &#x27;&#x27;, &#x27;managed_by&#x27;: &#x27;&#x27;, &#x27;sys_updated_on&#x27;: &#x27;2022-03-18 03:59:41&#x27;, &#x27;sys_class_name&#x27;: &#x27;cmdb_ci_computer&#x27;, &#x27;manufacturer&#x27;: {&#x27;link&#x27;: &#x27;https://www.example.com/api/now/table/core_company/b7e9e843c0a80169009a5a485bb2a2b5&#x27;, &#x27;value&#x27;: &#x27;b7e9e843c0a80169009a5a485bb2a2b5&#x27;}, &#x27;sys_id&#x27;: &#x27;00a96c0d3790200044e0bfc8bcbe5db4&#x27;, &#x27;po_number&#x27;: &#x27;PO100003&#x27;, &#x27;sys_updated_by&#x27;: &#x27;system&#x27;, &#x27;due_in&#x27;: &#x27;&#x27;, &#x27;checked_in&#x27;: &#x27;&#x27;, &#x27;sys_class_path&#x27;: &#x27;/!!/!2/!(&#x27;, &#x27;sys_created_on&#x27;: &#x27;2012-02-18 08:14:21&#x27;, &#x27;vendor&#x27;: {&#x27;link&#x27;: &#x27;https://www.example.com/api/now/table/core_company/b7e9e843c0a80169009a5a485bb2a2b5&#x27;, &#x27;value&#x27;: &#x27;b7e9e843c0a80169009a5a485bb2a2b5&#x27;}, &#x27;sys_domain&#x27;: {&#x27;link&#x27;: &#x27;https://www.example.com/api/now/table/sys_user_group/global&#x27;, &#x27;value&#x27;: &#x27;global&#x27;}, &#x27;company&#x27;: {&#x27;link&#x27;: &#x27;https://www.example.com/api/now/table/core_company/81fbfe03ac1d55eb286d832de58ae1fd&#x27;, &#x27;value&#x27;: &#x27;81fbfe03ac1d55eb286d832de58ae1fd&#x27;}, &#x27;install_date&#x27;: &#x27;2019-07-28 07:00:00&#x27;, &#x27;justification&#x27;: &#x27;&#x27;, &#x27;department&#x27;: {&#x27;link&#x27;: &#x27;https://www.example.com/api/now/table/cmn_department/221f79b7c6112284005d646b76ab978c&#x27;, &#x27;value&#x27;: &#x27;221f79b7c6112284005d646b76ab978c&#x27;}, &#x27;gl_account&#x27;: &#x27;&#x27;, &#x27;invoice_number&#x27;: &#x27;&#x27;, &#x27;sys_created_by&#x27;: &#x27;admin&#x27;, &#x27;assigned_to&#x27;: {&#x27;link&#x27;: &#x27;https://www.example.comapi/now/table/sys_user/92826bf03710200044e0bfc8bcbe5dbb&#x27;, &#x27;value&#x27;: &#x27;92826bf03710200044e0bfc8bcbe5dbb&#x27;}, &#x27;warranty_expiration&#x27;: &#x27;2022-07-27&#x27;, &#x27;asset_tag&#x27;: &#x27;P1000503&#x27;, &#x27;cost&#x27;: &#x27;1799.99&#x27;, &#x27;sys_mod_count&#x27;: &#x27;6&#x27;, &#x27;owned_by&#x27;: &#x27;&#x27;, &#x27;serial_number&#x27;: &#x27;ABE-486-V17263-DO&#x27;, &#x27;checked_out&#x27;: &#x27;&#x27;, &#x27;model_id&#x27;: {&#x27;link&#x27;: &#x27;https://www.example.com/api/now/table/cmdb_model/d501454f1b1310002502fbcd2c071334&#x27;, &#x27;value&#x27;: &#x27;d501454f1b1310002502fbcd2c071334&#x27;}, &#x27;sys_domain_path&#x27;: &#x27;/&#x27;, &#x27;sys_tags&#x27;: &#x27;&#x27;, &#x27;cost_cc&#x27;: &#x27;USD&#x27;, &#x27;order_date&#x27;: &#x27;2019-05-13 08:00:00&#x27;, &#x27;support_group&#x27;: &#x27;&#x27;, &#x27;delivery_date&#x27;: &#x27;2019-06-09 08:00:00&#x27;, &#x27;install_status&#x27;: &#x27;1&#x27;, &#x27;cost_center&#x27;: {&#x27;link&#x27;: &#x27;https://www.example.com/api/now/table/cmn_cost_center/d9d0a971c0a80a641c20b13d99a48576&#x27;, &#x27;value&#x27;: &#x27;d9d0a971c0a80a641c20b13d99a48576&#x27;}, &#x27;due&#x27;: &#x27;&#x27;, &#x27;supported_by&#x27;: &#x27;&#x27;, &#x27;name&#x27;: &#x27;MacBook Pro 15&quot;&#x27;, &#x27;unverified&#x27;: &#x27;false&#x27;, &#x27;assigned&#x27;: &#x27;2019-11-10 07:00:00&#x27;, &#x27;location&#x27;: {&#x27;link&#x27;: &#x27;https://www.example.com/api/now/table/cmn_location/8226baa4ac1d55eb40eb653c02649519&#x27;, &#x27;value&#x27;: &#x27;8226baa4ac1d55eb40eb653c02649519&#x27;}, &#x27;asset&#x27;: {&#x27;link&#x27;: &#x27;https://www.example.com/api/now/table/alm_asset/04a96c0d3790200044e0bfc8bcbe5db3&#x27;, &#x27;value&#x27;: &#x27;04a96c0d3790200044e0bfc8bcbe5db3&#x27;}, &#x27;purchase_date&#x27;: &#x27;2019-05-25&#x27;, &#x27;lease_id&#x27;: &#x27;&#x27;}]</div>
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
