.. _servicenow.itsm.api_info_module:


*****************************
servicenow.itsm.api_info
*****************************

**Manage ServiceNow GET requests**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Retrieve records via ServiceNow REST Table API for an arbitrary table.
- For more information, refer to the ServiceNow REST Table API documentation at https://docs.servicenow.com/bundle/sandiego-application-development/page/integrate/inbound-rest/concept/c_TableAPI.html.




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
                    <b>resource</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name of the table in which a record is to be created, updated or deleted from.</div>
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
                        <div>Required if <em>action=patch</em> or <em>action=delete</em>.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>action</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>post</li>
                                    <li>patch</li>
                                    <li>delete</li>
                        </ul>
                </td>
                <td>
                        <div>The action to perform.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>data</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dict</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The data that we want to update or create the resource with.</div>
                        <div>Mutually exclusive with template.</div>
                        <div>Only relevant if patching or deleting a resource.</div>
                        <div>A Dict consists of resource's column names as keys (such as description, number, priority, and so on) and the patching values as values (the value we want to change the column to).</div>
                        <div>When updating a resource's record, if no datum is specified for a specific column, the value of that column will remain intact.</div>
                        <div>When creating a resource's record, if no datum is specified for a specific column, the default value of the column will be used.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>template</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dict</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Provide a valid YAML template definition file for creating or updating a record.</div>
                        <div>Provides built-in template processing capabilities as an alternative to its data parameter.</div>
                        <div>Mutually exclusive with data.</div>
                        <div>If template starts with <code>"/"</code>, it is assumed you have specified absolute path to the file. Otherwise, it is assumed you have specified relative path to the file.</div>
                        <div>Template file needs to be present on the Ansible Controller's system. Otherwise, an error is raised.</div>
                </td>
            </tr>


    </table>
    <br/>



See Also
--------

.. seealso::

   :ref:`servicenow.itsm.api_info_module`
      The official documentation on the **servicenow.itsm.api** module.


Examples
--------

.. code-block:: yaml

    - name: Create a record in table incident with specified short_description (which is read from data)
      servicenow.itsm.api:
        resource: incident
        action: post
        data:
          short_description: my-incident
      register: result

    - name: Create a record in table incident with column values set in template, located in Ansible controller file system
      servicenow.itsm.api:
        resource: incident
        action: post
        template: '/testing/deployment.j2'
      register: result

    - name: Update a record with given sys_id in table incident with template, located in Ansible controller file system
      servicenow.itsm.api:
        resource: incident
        action: patch
        sys_id: 46b66a40a9fe198101f243dfbc79033d
        template: '/testing/deployment.j2'
      register: result

    - name: Update column short_description (specified in data) in table incident of a record with given sys_id
      servicenow.itsm.api:
        resource: incident
        action: patch
        sys_id: 46b66a40a9fe198101f243dfbc79033d
        data:
          short_description: my-incident-updated
      register: result

    - name: Delete the resource the table incident with given sys_id
      servicenow.itsm.api:
        resource: incident
        action: delete
        sys_id: 46b66a40a9fe198101f243dfbc79033d
      register: result

    - name: Create a record in the table sc_req_item and set short_description's value to demo-description2
      servicenow.itsm.api:
        resource: sc_req_item
        action: post
        data:
          short_description: demo-description2
      register: result

    - name: Create a record in the table sc_req_item and set short_description's value to demo-description2
      servicenow.itsm.api:
        resource: sc_req_item
        action: post
        data:
          short_description: demo-description2
      register: result

    - name: Create a record in sc_req_item with column values set in template, located in Ansible controller file system
      servicenow.itsm.api:
        resource: sc_req_item
        action: post
        template: '/testing/deployment.j2'
      register: result

    - name: Delete a record by sys_id from table sc_req_item
      servicenow.itsm.api:
        resource: sc_req_item
        action: delete
        sys_id: b82adae197201110949235dfe153afec
      register: result


Status
------


Authors
~~~~~~~

- Tjaž Eržen (@tjazsch)
