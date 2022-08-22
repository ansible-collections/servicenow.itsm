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
                        <div>The name of the table that we want to obtain records from.</div>
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
                        <div><a href='https://docs.servicenow.com/en-US/bundle/sandiego-platform-user-interface/page/use/common-ui-elements/reference/r_OpAvailableFiltersQueries.html'>https://docs.servicenow.com/en-US/bundle/sandiego-platform-user-interface/page/use/common-ui-elements/reference/r_OpAvailableFiltersQueries.html</a> and <a href='https://developer.servicenow.com/dev.do#!/reference/api/sandiego/rest/c_TableAPI'>https://developer.servicenow.com/dev.do#!/reference/api/sandiego/rest/c_TableAPI</a> under 'sysparm_query'.</div>
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
                        <div>Return field display values <em>(true)</em>, actual values <em>(false)</em>, or both <em>(all)</em>.</div>
                        <div>Default value is set to <em>false</em>.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>exclude_reference_link</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>true</li>
                                    <li><div style="color: blue"><b>false</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div><em>true</em> to exclude Table API links for reference fields.</div>
                        <div>The default is <em>false</em>.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>columns</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of fields/columns to return in the response.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>query_category</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">str</span>
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
                        <span style="color: purple">bool</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>true</li>
                                    <li><div style="color: blue"><b>false</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>If set to <em>true</em> to access data across domains if authorized.</div>
                        <div>Default is set to <em>false</em>.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>no_count</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">bool</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>true</li>
                                    <li><div style="color: blue"><b>false</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Do not execute a select <em>count(*)</em> on table.</div>
                        <div>Default is set to <em>false</em>.</div>
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{"active": "false", "activity_due": "2016-12-13 01:26:36", "additional_assignee_list": "", "approval": "not requested", "approval_history": "", "approval_set": "", "assigned_to": {"link": "https://dev128746.service-now.com/api/now/table/sys_user/5137153cc611227c000bbd1bd8cd2007", "value": "5137153cc611227c000bbd1bd8cd2007"}, "assignment_group": {"link": "https://dev128746.service-now.com/api/now/table/sys_user_group/287ebd7da9fe198100f92cc8d1d2154e", "value": "287ebd7da9fe198100f92cc8d1d2154e"}, "business_duration": "1970-01-01 08:00:00", "business_impact": "", "business_service": {"link": "https://dev128746.service-now.com/api/now/table/cmdb_ci_service/27d32778c0a8000b00db970eeaa60f16", "value": "27d32778c0a8000b00db970eeaa60f16"}, "business_stc": "28800", "calendar_duration": "1970-01-02 04:23:17", "calendar_stc": "102197", "caller_id": {"link": "https://dev128746.service-now.com/api/now/table/sys_user/681ccaf9c0a8016400b98a06818d57c7", "value": "681ccaf9c0a8016400b98a06818d57c7"}, "category": "inquiry", "cause": "", "caused_by": "", "child_incidents": "0", "close_code": "Solved (Permanently)", "close_notes": "This incident is resolved.", "closed_at": "2016-12-14 02:46:44", "closed_by": {"link": "https://dev128746.service-now.com/api/now/table/sys_user/681ccaf9c0a8016400b98a06818d57c7", "value": "681ccaf9c0a8016400b98a06818d57c7"}, "cmdb_ci": {"link": "https://dev128746.service-now.com/api/now/table/cmdb_ci/109562a3c611227500a7b7ff98cc0dc7", "value": "109562a3c611227500a7b7ff98cc0dc7"}, "comments": "", "comments_and_work_notes": "", "company": {"link": "https://dev128746.service-now.com/api/now/table/core_company/31bea3d53790200044e0bfc8bcbe5dec", "value": "31bea3d53790200044e0bfc8bcbe5dec"}, "contact_type": "self-service", "contract": "", "correlation_display": "", "correlation_id": "", "delivery_plan": "", "delivery_task": "", "description": "I am unable to connect to the email server. It appears to be down.", "due_date": "", "escalation": "0", "expected_start": "", "follow_up": "", "group_list": "", "hold_reason": "", "impact": "2", "incident_state": "7", "knowledge": "false", "location": "", "made_sla": "true", "notify": "1", "number": "INC0000060", "opened_at": "2016-12-12 15:19:57", "opened_by": {"link": "https://dev128746.service-now.com/api/now/table/sys_user/681ccaf9c0a8016400b98a06818d57c7", "value": "681ccaf9c0a8016400b98a06818d57c7"}, "order": "", "origin_id": "", "origin_table": "", "parent": "", "parent_incident": "", "priority": "3", "problem_id": "", "reassignment_count": "2", "reopen_count": "0", "reopened_by": "", "reopened_time": "", "resolved_at": "2016-12-13 21:43:14", "resolved_by": {"link": "https://dev128746.service-now.com/api/now/table/sys_user/5137153cc611227c000bbd1bd8cd2007", "value": "5137153cc611227c000bbd1bd8cd2007"}, "rfc": "", "route_reason": "", "service_offering": "", "severity": "3", "short_description": "Unable to connect to email", "sla_due": "", "state": "7", "subcategory": "email", "sys_class_name": "incident", "sys_created_by": "employee", "sys_created_on": "2016-12-12 15:19:57", "sys_domain": {"link": "https://dev128746.service-now.com/api/now/table/sys_user_group/global", "value": "global"}, "sys_domain_path": "/", "sys_id": "1c741bd70b2322007518478d83673af3", "sys_mod_count": "15", "sys_tags": "", "sys_updated_by": "employee", "sys_updated_on": "2016-12-14 02:46:44", "task_effective_number": "INC0000060", "time_worked": "", "universal_request": "", "upon_approval": "proceed", "upon_reject": "cancel", "urgency": "2", "user_input": "", "watch_list": "", "work_end": "", "work_notes": "", "work_notes_list": "", "work_start": ""}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Tjaž Eržen (@tjazsch)
