.. _servicenow.itsm.api_module:


*******************
servicenow.itsm.api
*******************

**Manage ServiceNow POST, PATCH and DELETE requests**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Create, delete or update a ServiceNow record from the given resource.
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
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                <td>
                        <div>The data that we want to update or create the resource with.</div>
                        <div>Mutually exclusive with <em>template</em>.</div>
                        <div>Only relevant if <em>action==patch</em> or <em>action==post</em>.</div>
                        <div>A Dict consists of resource&#x27;s column names as keys (such as description, number, priority, and so on) and the patching values as values (the value we want to change the column to).</div>
                        <div>When updating a resource&#x27;s record, if no datum is specified for a specific column, the value of that column will remain intact.</div>
                        <div>When creating a resource&#x27;s record, if no datum is specified for a specific column, the default value of the column will be used.</div>
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
                    <b>query_params</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.1.0 </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                <td>
                        <div>Query parameters that may be used on POST or PATCH request.</div>
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
                        <div>Required if <em>action==patch</em> or <em>action==delete</em>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>template</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Provide a valid YAML template definition file for creating or updating a record.</div>
                        <div>Provides built-in template processing capabilities as an alternative to its data parameter.</div>
                        <div>Mutually exclusive with <em>data</em>.</div>
                        <div>If template starts with <code>&quot;/&quot;</code>, it is assumed you have specified absolute path to the file. Otherwise, it is assumed you have specified relative path to the file.</div>
                        <div>Template file needs to be present on the Ansible Controller&#x27;s system. Otherwise, an error is raised.</div>
                </td>
            </tr>
    </table>
    <br/>



See Also
--------

.. seealso::

   :ref:`servicenow.itsm.api_info_module`
      The official documentation on the **servicenow.itsm.api_info** module.


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

    - name: create user (object with encrypted fields)
      servicenow.itsm.api:
        resource: sys_user
        action: post
        query_params:
          sysparm_input_display_value: true
        data:
          user_name: "demo_username"
          user_password: "demo_password"
          first_name: "first_name"
          last_name: Demouser
          department: IT
          email: "demo_username@example.com"
          title: Demo user
      register: user

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
                            <div>The created, updated or deleted record.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;active&#x27;: &#x27;true&#x27;, &#x27;activity_due&#x27;: &#x27;&#x27;, &#x27;additional_assignee_list&#x27;: &#x27;&#x27;, &#x27;approval&#x27;: &#x27;not requested&#x27;, &#x27;approval_history&#x27;: &#x27;&#x27;, &#x27;approval_set&#x27;: &#x27;&#x27;, &#x27;assigned_to&#x27;: &#x27;&#x27;, &#x27;assignment_group&#x27;: &#x27;&#x27;, &#x27;business_duration&#x27;: &#x27;&#x27;, &#x27;business_impact&#x27;: &#x27;&#x27;, &#x27;business_service&#x27;: &#x27;&#x27;, &#x27;business_stc&#x27;: &#x27;&#x27;, &#x27;calendar_duration&#x27;: &#x27;&#x27;, &#x27;calendar_stc&#x27;: &#x27;&#x27;, &#x27;caller_id&#x27;: &#x27;&#x27;, &#x27;category&#x27;: &#x27;inquiry&#x27;, &#x27;cause&#x27;: &#x27;&#x27;, &#x27;caused_by&#x27;: &#x27;&#x27;, &#x27;child_incidents&#x27;: &#x27;0&#x27;, &#x27;close_code&#x27;: &#x27;&#x27;, &#x27;close_notes&#x27;: &#x27;&#x27;, &#x27;closed_at&#x27;: &#x27;&#x27;, &#x27;closed_by&#x27;: &#x27;&#x27;, &#x27;cmdb_ci&#x27;: &#x27;&#x27;, &#x27;comments&#x27;: &#x27;&#x27;, &#x27;comments_and_work_notes&#x27;: &#x27;&#x27;, &#x27;company&#x27;: &#x27;&#x27;, &#x27;contact_type&#x27;: &#x27;&#x27;, &#x27;contract&#x27;: &#x27;&#x27;, &#x27;correlation_display&#x27;: &#x27;&#x27;, &#x27;correlation_id&#x27;: &#x27;&#x27;, &#x27;delivery_plan&#x27;: &#x27;&#x27;, &#x27;delivery_task&#x27;: &#x27;&#x27;, &#x27;description&#x27;: &#x27;&#x27;, &#x27;due_date&#x27;: &#x27;&#x27;, &#x27;escalation&#x27;: &#x27;0&#x27;, &#x27;expected_start&#x27;: &#x27;&#x27;, &#x27;follow_up&#x27;: &#x27;&#x27;, &#x27;group_list&#x27;: &#x27;&#x27;, &#x27;hold_reason&#x27;: &#x27;&#x27;, &#x27;impact&#x27;: &#x27;3&#x27;, &#x27;incident_state&#x27;: &#x27;1&#x27;, &#x27;knowledge&#x27;: &#x27;false&#x27;, &#x27;location&#x27;: &#x27;&#x27;, &#x27;made_sla&#x27;: &#x27;true&#x27;, &#x27;notify&#x27;: &#x27;1&#x27;, &#x27;number&#x27;: &#x27;INC0010204&#x27;, &#x27;opened_at&#x27;: &#x27;2022-07-06 08:53:05&#x27;, &#x27;opened_by&#x27;: &#x27;6816f79cc0a8016401c5a33be04be441&#x27;, &#x27;order&#x27;: &#x27;&#x27;, &#x27;origin_id&#x27;: &#x27;&#x27;, &#x27;origin_table&#x27;: &#x27;&#x27;, &#x27;parent&#x27;: &#x27;&#x27;, &#x27;parent_incident&#x27;: &#x27;&#x27;, &#x27;priority&#x27;: &#x27;5&#x27;, &#x27;problem_id&#x27;: &#x27;&#x27;, &#x27;reassignment_count&#x27;: &#x27;0&#x27;, &#x27;reopen_count&#x27;: &#x27;0&#x27;, &#x27;reopened_by&#x27;: &#x27;&#x27;, &#x27;reopened_time&#x27;: &#x27;&#x27;, &#x27;resolved_at&#x27;: &#x27;&#x27;, &#x27;resolved_by&#x27;: &#x27;&#x27;, &#x27;rfc&#x27;: &#x27;&#x27;, &#x27;route_reason&#x27;: &#x27;&#x27;, &#x27;service_offering&#x27;: &#x27;&#x27;, &#x27;severity&#x27;: &#x27;3&#x27;, &#x27;short_description&#x27;: &#x27;my-incident&#x27;, &#x27;sla_due&#x27;: &#x27;&#x27;, &#x27;state&#x27;: &#x27;1&#x27;, &#x27;subcategory&#x27;: &#x27;&#x27;, &#x27;sys_class_name&#x27;: &#x27;incident&#x27;, &#x27;sys_created_by&#x27;: &#x27;admin&#x27;, &#x27;sys_created_on&#x27;: &#x27;2022-07-06 08:53:05&#x27;, &#x27;sys_domain&#x27;: &#x27;global&#x27;, &#x27;sys_domain_path&#x27;: &#x27;/&#x27;, &#x27;sys_id&#x27;: &#x27;35b5fb4197245110949235dfe153af06&#x27;, &#x27;sys_mod_count&#x27;: &#x27;0&#x27;, &#x27;sys_tags&#x27;: &#x27;&#x27;, &#x27;sys_updated_by&#x27;: &#x27;admin&#x27;, &#x27;sys_updated_on&#x27;: &#x27;2022-07-06 08:53:05&#x27;, &#x27;task_effective_number&#x27;: &#x27;INC0010204&#x27;, &#x27;time_worked&#x27;: &#x27;&#x27;, &#x27;universal_request&#x27;: &#x27;&#x27;, &#x27;upon_approval&#x27;: &#x27;proceed&#x27;, &#x27;upon_reject&#x27;: &#x27;cancel&#x27;, &#x27;urgency&#x27;: &#x27;3&#x27;, &#x27;user_input&#x27;: &#x27;&#x27;, &#x27;watch_list&#x27;: &#x27;&#x27;, &#x27;work_end&#x27;: &#x27;&#x27;, &#x27;work_notes&#x27;: &#x27;&#x27;, &#x27;work_notes_list&#x27;: &#x27;&#x27;, &#x27;work_start&#x27;: &#x27;&#x27;}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Tjaž Eržen (@tjazsch)
- Jure Medvešek (@juremedvesek)
