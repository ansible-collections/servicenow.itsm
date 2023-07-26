.. _servicenow.itsm.api_info_module:


************************
servicenow.itsm.api_info
************************

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
                    <b>columns</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">[]</div>
                </td>
                <td>
                        <div>List of fields/columns to return in the response.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>display_value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>true</li>
                                    <li><div style="color: blue"><b>false</b>&nbsp;&larr;</div></li>
                                    <li>all</li>
                        </ul>
                </td>
                <td>
                        <div>Return field display values <code>true</code>, actual values <code>false</code>, or both <code>all</code>.</div>
                        <div>Default value is set to <code>false</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>exclude_reference_link</b>
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
                        <div><code>true</code> to exclude Table API links for reference fields.</div>
                        <div>The default is <code>false</code>.</div>
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
                    <b>no_count</b>
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
                        <div>Do not execute a select count(*) on table.</div>
                        <div>Default is set to <code>false</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>query_category</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the query category to use for queries.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>query_no_domain</b>
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
                        <div>If set to <code>true</code> to access data across domains if authorized.</div>
                        <div>Default is set to <code>false</code>.</div>
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
                        <div>The name of the table that we want to obtain records from.</div>
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
                        <div>Unique identifier of the record to retrieve.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sysparm_query</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>An encoded query string used to filter the results.</div>
                        <div>List of all possible operators and a guide on how to map them to form a query may be found at <a href='https://docs.servicenow.com/en-US/bundle/sandiego-platform-user-interface/page/use/common-ui-elements/reference/r_OpAvailableFiltersQueries.html'>https://docs.servicenow.com/en-US/bundle/sandiego-platform-user-interface/page/use/common-ui-elements/reference/r_OpAvailableFiltersQueries.html</a>. and <a href='https://developer.servicenow.com/dev.do#!/reference/api/sandiego/rest/c_TableAPI'>https://developer.servicenow.com/dev.do#!/reference/api/sandiego/rest/c_TableAPI</a> under &#x27;sysparm_query&#x27;.</div>
                </td>
            </tr>
    </table>
    <br/>



See Also
--------

.. seealso::

   :ref:`servicenow.itsm.api_module`
      The official documentation on the **servicenow.itsm.api** module.


Examples
--------

.. code-block:: yaml

    - name: Retrieve all records from table incident
      servicenow.itsm.api_info:
        resource: incident
      register: result

    - name: Retrieve a record with specified sys_id from the resource incident
      servicenow.itsm.api_info:
        resource: incident
        sys_id: 471bfbc7a9fe198101e77a3e10e5d47f
      register: result

    - name: Retrieve all incidents with properties specified in a query
      servicenow.itsm.api_info:
        resource: incident
        sysparm_query: numberSTARTSWITHINC^ORnumberSTARTSWITHABC^state!=7^stateBETWEEN1@4^short_descriptionISNOTEMPTY
      register: result

    - name: Retrieve all incidents with properties specified in a query, filtered by a few other parameters
      servicenow.itsm.api_info:
        resource: incident
        sysparm_query: numberSTARTSWITHINC^ORnumberSTARTSWITHABC^state!=7^stateBETWEEN1@4^short_descriptionISNOTEMPTY
        display_value: true
        exclude_reference_link: true
        columns:
          - state
          - number
          - sys_id
        query_no_domain: true
        no_count: false
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
                    <b>records</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>A list of records from the specified table.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;active&#x27;: &#x27;false&#x27;, &#x27;activity_due&#x27;: &#x27;&#x27;, &#x27;additional_assignee_list&#x27;: &#x27;&#x27;, &#x27;approval&#x27;: &#x27;not requested&#x27;, &#x27;approval_history&#x27;: &#x27;&#x27;, &#x27;approval_set&#x27;: &#x27;&#x27;, &#x27;assigned_to&#x27;: &#x27;5137153cc611227c000bbd1bd8cd2007&#x27;, &#x27;assignment_group&#x27;: &#x27;8a4dde73c6112278017a6a4baf547aa7&#x27;, &#x27;business_duration&#x27;: &#x27;1970-01-20 05:38:50&#x27;, &#x27;business_service&#x27;: &#x27;&#x27;, &#x27;business_stc&#x27;: &#x27;1661930&#x27;, &#x27;calendar_duration&#x27;: &#x27;1970-03-21 20:38:50&#x27;, &#x27;calendar_stc&#x27;: &#x27;6899930&#x27;, &#x27;caller_id&#x27;: &#x27;681ccaf9c0a8016400b98a06818d57c7&#x27;, &#x27;category&#x27;: &#x27;inquiry&#x27;, &#x27;caused_by&#x27;: &#x27;&#x27;, &#x27;child_incidents&#x27;: &#x27;&#x27;, &#x27;close_code&#x27;: &#x27;Solved (Work Around)&#x27;, &#x27;close_notes&#x27;: &#x27;Gave workaround&#x27;, &#x27;closed_at&#x27;: &#x27;2020-07-07 23:18:40&#x27;, &#x27;closed_by&#x27;: &#x27;9ee1b13dc6112271007f9d0efdb69cd0&#x27;, &#x27;cmdb_ci&#x27;: &#x27;&#x27;, &#x27;comments&#x27;: &#x27;&#x27;, &#x27;comments_and_work_notes&#x27;: &#x27;&#x27;, &#x27;company&#x27;: &#x27;31bea3d53790200044e0bfc8bcbe5dec&#x27;, &#x27;contact_type&#x27;: &#x27;phone&#x27;, &#x27;contract&#x27;: &#x27;&#x27;, &#x27;correlation_display&#x27;: &#x27;&#x27;, &#x27;correlation_id&#x27;: &#x27;&#x27;, &#x27;delivery_plan&#x27;: &#x27;&#x27;, &#x27;delivery_task&#x27;: &#x27;&#x27;, &#x27;description&#x27;: &#x27;Noticing today that any time I send an email with an attachment, it takes at least 20 seconds to send.&#x27;, &#x27;due_date&#x27;: &#x27;&#x27;, &#x27;escalation&#x27;: &#x27;0&#x27;, &#x27;expected_start&#x27;: &#x27;&#x27;, &#x27;follow_up&#x27;: &#x27;&#x27;, &#x27;group_list&#x27;: &#x27;&#x27;, &#x27;hold_reason&#x27;: &#x27;&#x27;, &#x27;impact&#x27;: &#x27;1&#x27;, &#x27;incident_state&#x27;: &#x27;7&#x27;, &#x27;knowledge&#x27;: &#x27;false&#x27;, &#x27;location&#x27;: &#x27;&#x27;, &#x27;made_sla&#x27;: &#x27;false&#x27;, &#x27;notify&#x27;: &#x27;1&#x27;, &#x27;number&#x27;: &#x27;INC0000013&#x27;, &#x27;opened_at&#x27;: &#x27;2020-07-06 23:15:58&#x27;, &#x27;opened_by&#x27;: &#x27;9ee1b13dc6112271007f9d0efdb69cd0&#x27;, &#x27;order&#x27;: &#x27;&#x27;, &#x27;parent&#x27;: &#x27;&#x27;, &#x27;parent_incident&#x27;: &#x27;&#x27;, &#x27;priority&#x27;: &#x27;1&#x27;, &#x27;problem_id&#x27;: &#x27;&#x27;, &#x27;reassignment_count&#x27;: &#x27;2&#x27;, &#x27;reopen_count&#x27;: &#x27;&#x27;, &#x27;reopened_by&#x27;: &#x27;&#x27;, &#x27;reopened_time&#x27;: &#x27;&#x27;, &#x27;resolved_at&#x27;: &#x27;2020-09-24 19:54:48&#x27;, &#x27;resolved_by&#x27;: &#x27;6816f79cc0a8016401c5a33be04be441&#x27;, &#x27;rfc&#x27;: &#x27;&#x27;, &#x27;route_reason&#x27;: &#x27;&#x27;, &#x27;service_offering&#x27;: &#x27;&#x27;, &#x27;severity&#x27;: &#x27;3&#x27;, &#x27;short_description&#x27;: &#x27;EMAIL is slow when an attachment is involved&#x27;, &#x27;sla_due&#x27;: &#x27;&#x27;, &#x27;state&#x27;: &#x27;7&#x27;, &#x27;subcategory&#x27;: &#x27;&#x27;, &#x27;sys_class_name&#x27;: &#x27;incident&#x27;, &#x27;sys_created_by&#x27;: &#x27;don.goodliffe&#x27;, &#x27;sys_created_on&#x27;: &#x27;2020-07-07 23:18:07&#x27;, &#x27;sys_domain&#x27;: &#x27;global&#x27;, &#x27;sys_domain_path&#x27;: &#x27;/&#x27;, &#x27;sys_id&#x27;: &#x27;46cebb88a9fe198101aee93734f9768b&#x27;, &#x27;sys_mod_count&#x27;: &#x27;5&#x27;, &#x27;sys_tags&#x27;: &#x27;&#x27;, &#x27;sys_updated_by&#x27;: &#x27;VALUE_SPECIFIED_IN_NO_LOG_PARAMETER&#x27;, &#x27;sys_updated_on&#x27;: &#x27;2020-09-24 19:54:48&#x27;, &#x27;task_effective_number&#x27;: &#x27;INC0000013&#x27;, &#x27;time_worked&#x27;: &#x27;&#x27;, &#x27;universal_request&#x27;: &#x27;&#x27;, &#x27;upon_approval&#x27;: &#x27;&#x27;, &#x27;upon_reject&#x27;: &#x27;&#x27;, &#x27;urgency&#x27;: &#x27;1&#x27;, &#x27;user_input&#x27;: &#x27;&#x27;, &#x27;watch_list&#x27;: &#x27;&#x27;, &#x27;work_end&#x27;: &#x27;&#x27;, &#x27;work_notes&#x27;: &#x27;&#x27;, &#x27;work_notes_list&#x27;: &#x27;&#x27;, &#x27;work_start&#x27;: &#x27;&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Tjaž Eržen (@tjazsch)
