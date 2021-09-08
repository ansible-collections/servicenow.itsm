.. _servicenow.itsm.incident_info_module:


*****************************
servicenow.itsm.incident_info
*****************************

**List ServiceNow incidents**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Retrieve information about ServiceNow incidents.
- For more information, refer to the ServiceNow incident management documentation at https://docs.servicenow.com/bundle/paris-it-service-management/page/product/incident-management/concept/c_IncidentManagement.html.




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
                    <b>number</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Number of the record to retrieve.</div>
                        <div>Note that contrary to <em>sys_id</em>, <em>number</em> may not uniquely identify a record.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
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
                        <div>Provides a set of operators for use with filters, condition builders, and encoded queries.</div>
                        <div>The data type of a field determines what operators are available for it. Refer to the ServiceNow Available Filters Queries documentation at <a href='https://docs.servicenow.com/bundle/quebec-platform-user-interface/page/use/common-ui-elements/reference/r_OpAvailableFiltersQueries.html'>https://docs.servicenow.com/bundle/quebec-platform-user-interface/page/use/common-ui-elements/reference/r_OpAvailableFiltersQueries.html</a>.</div>
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
    </table>
    <br/>



See Also
--------

.. seealso::

   :ref:`servicenow.itsm.incident_module`
      The official documentation on the **servicenow.itsm.incident** module.


Examples
--------

.. code-block:: yaml

    - name: Retrieve all incidents
      servicenow.itsm.incident_info:
      register: result

    - name: Retrieve a specific incident by its sys_id
      servicenow.itsm.incident_info:
        sys_id: 471bfbc7a9fe198101e77a3e10e5d47f
      register: result

    - name: Retrieve incidents by number
      servicenow.itsm.incident_info:
        number: INC0000039
      register: result

    - name: Retrieve all incidents that contain SAP in its short description
      servicenow.itsm.incident_info:
        query:
          - short_description: LIKE SAP
      register: result

    - name: Retrieve new incidents reported by abel.tuter or bertie.luby
      servicenow.itsm.incident_info:
        query:
          - state: = new
            caller: = abel.tuter
          - state: = new
            caller: = bertie.luby



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
                            <div>A list of incident records.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;active&#x27;: &#x27;false&#x27;, &#x27;activity_due&#x27;: &#x27;&#x27;, &#x27;additional_assignee_list&#x27;: &#x27;&#x27;, &#x27;approval&#x27;: &#x27;not requested&#x27;, &#x27;approval_history&#x27;: &#x27;&#x27;, &#x27;approval_set&#x27;: &#x27;&#x27;, &#x27;assigned_to&#x27;: &#x27;5137153cc611227c000bbd1bd8cd2007&#x27;, &#x27;assignment_group&#x27;: &#x27;8a4dde73c6112278017a6a4baf547aa7&#x27;, &#x27;attachments&#x27;: [{&#x27;average_image_color&#x27;: &#x27;&#x27;, &#x27;chunk_size_bytes&#x27;: &#x27;700000&#x27;, &#x27;compressed&#x27;: &#x27;true&#x27;, &#x27;content_type&#x27;: &#x27;text/plain&#x27;, &#x27;download_link&#x27;: &#x27;https://www.example.com/api/now/attachment/b7ad74d50706301022f9ffa08c1ed0ee/file&#x27;, &#x27;file_name&#x27;: &#x27;sample_file1.txt&#x27;, &#x27;hash&#x27;: &#x27;6f2b0dec698566114435a23f15dcac848a40e1fd3e0eda4afe24a663dda23f2e&#x27;, &#x27;image_height&#x27;: &#x27;&#x27;, &#x27;image_width&#x27;: &#x27;&#x27;, &#x27;size_bytes&#x27;: &#x27;210&#x27;, &#x27;size_compressed&#x27;: &#x27;206&#x27;, &#x27;state&#x27;: &#x27;pending&#x27;, &#x27;sys_created_by&#x27;: &#x27;admin&#x27;, &#x27;sys_created_on&#x27;: &#x27;2021-08-17 11:19:24&#x27;, &#x27;sys_id&#x27;: &#x27;b7ad74d50706301022f9ffa08c1ed0ee&#x27;, &#x27;sys_mod_count&#x27;: &#x27;0&#x27;, &#x27;sys_tags&#x27;: &#x27;&#x27;, &#x27;sys_updated_by&#x27;: &#x27;admin&#x27;, &#x27;sys_updated_on&#x27;: &#x27;2021-08-17 11:19:24&#x27;, &#x27;table_name&#x27;: &#x27;incident&#x27;, &#x27;table_sys_id&#x27;: &#x27;efad74d50706301022f9ffa08c1ed06d&#x27;}], &#x27;business_duration&#x27;: &#x27;1970-01-20 05:38:50&#x27;, &#x27;business_service&#x27;: &#x27;&#x27;, &#x27;business_stc&#x27;: &#x27;1661930&#x27;, &#x27;calendar_duration&#x27;: &#x27;1970-03-21 20:38:50&#x27;, &#x27;calendar_stc&#x27;: &#x27;6899930&#x27;, &#x27;caller_id&#x27;: &#x27;681ccaf9c0a8016400b98a06818d57c7&#x27;, &#x27;category&#x27;: &#x27;inquiry&#x27;, &#x27;caused_by&#x27;: &#x27;&#x27;, &#x27;child_incidents&#x27;: &#x27;&#x27;, &#x27;close_code&#x27;: &#x27;Solved (Work Around)&#x27;, &#x27;close_notes&#x27;: &#x27;Gave workaround&#x27;, &#x27;closed_at&#x27;: &#x27;2020-07-07 23:18:40&#x27;, &#x27;closed_by&#x27;: &#x27;9ee1b13dc6112271007f9d0efdb69cd0&#x27;, &#x27;cmdb_ci&#x27;: &#x27;&#x27;, &#x27;comments&#x27;: &#x27;&#x27;, &#x27;comments_and_work_notes&#x27;: &#x27;&#x27;, &#x27;company&#x27;: &#x27;31bea3d53790200044e0bfc8bcbe5dec&#x27;, &#x27;contact_type&#x27;: &#x27;phone&#x27;, &#x27;contract&#x27;: &#x27;&#x27;, &#x27;correlation_display&#x27;: &#x27;&#x27;, &#x27;correlation_id&#x27;: &#x27;&#x27;, &#x27;delivery_plan&#x27;: &#x27;&#x27;, &#x27;delivery_task&#x27;: &#x27;&#x27;, &#x27;description&#x27;: &#x27;Noticing today that any time I send an email with an attachment, it takes at least 20 seconds to send.&#x27;, &#x27;due_date&#x27;: &#x27;&#x27;, &#x27;escalation&#x27;: &#x27;0&#x27;, &#x27;expected_start&#x27;: &#x27;&#x27;, &#x27;follow_up&#x27;: &#x27;&#x27;, &#x27;group_list&#x27;: &#x27;&#x27;, &#x27;hold_reason&#x27;: &#x27;&#x27;, &#x27;impact&#x27;: &#x27;1&#x27;, &#x27;incident_state&#x27;: &#x27;7&#x27;, &#x27;knowledge&#x27;: &#x27;false&#x27;, &#x27;location&#x27;: &#x27;&#x27;, &#x27;made_sla&#x27;: &#x27;false&#x27;, &#x27;notify&#x27;: &#x27;1&#x27;, &#x27;number&#x27;: &#x27;INC0000013&#x27;, &#x27;opened_at&#x27;: &#x27;2020-07-06 23:15:58&#x27;, &#x27;opened_by&#x27;: &#x27;9ee1b13dc6112271007f9d0efdb69cd0&#x27;, &#x27;order&#x27;: &#x27;&#x27;, &#x27;parent&#x27;: &#x27;&#x27;, &#x27;parent_incident&#x27;: &#x27;&#x27;, &#x27;priority&#x27;: &#x27;1&#x27;, &#x27;problem_id&#x27;: &#x27;&#x27;, &#x27;reassignment_count&#x27;: &#x27;2&#x27;, &#x27;reopen_count&#x27;: &#x27;&#x27;, &#x27;reopened_by&#x27;: &#x27;&#x27;, &#x27;reopened_time&#x27;: &#x27;&#x27;, &#x27;resolved_at&#x27;: &#x27;2020-09-24 19:54:48&#x27;, &#x27;resolved_by&#x27;: &#x27;6816f79cc0a8016401c5a33be04be441&#x27;, &#x27;rfc&#x27;: &#x27;&#x27;, &#x27;route_reason&#x27;: &#x27;&#x27;, &#x27;service_offering&#x27;: &#x27;&#x27;, &#x27;severity&#x27;: &#x27;3&#x27;, &#x27;short_description&#x27;: &#x27;EMAIL is slow when an attachment is involved&#x27;, &#x27;sla_due&#x27;: &#x27;&#x27;, &#x27;state&#x27;: &#x27;7&#x27;, &#x27;subcategory&#x27;: &#x27;&#x27;, &#x27;sys_class_name&#x27;: &#x27;incident&#x27;, &#x27;sys_created_by&#x27;: &#x27;don.goodliffe&#x27;, &#x27;sys_created_on&#x27;: &#x27;2020-07-07 23:18:07&#x27;, &#x27;sys_domain&#x27;: &#x27;global&#x27;, &#x27;sys_domain_path&#x27;: &#x27;/&#x27;, &#x27;sys_id&#x27;: &#x27;46cebb88a9fe198101aee93734f9768b&#x27;, &#x27;sys_mod_count&#x27;: &#x27;5&#x27;, &#x27;sys_tags&#x27;: &#x27;&#x27;, &#x27;sys_updated_by&#x27;: &#x27;VALUE_SPECIFIED_IN_NO_LOG_PARAMETER&#x27;, &#x27;sys_updated_on&#x27;: &#x27;2020-09-24 19:54:48&#x27;, &#x27;task_effective_number&#x27;: &#x27;INC0000013&#x27;, &#x27;time_worked&#x27;: &#x27;&#x27;, &#x27;universal_request&#x27;: &#x27;&#x27;, &#x27;upon_approval&#x27;: &#x27;&#x27;, &#x27;upon_reject&#x27;: &#x27;&#x27;, &#x27;urgency&#x27;: &#x27;1&#x27;, &#x27;user_input&#x27;: &#x27;&#x27;, &#x27;watch_list&#x27;: &#x27;&#x27;, &#x27;work_end&#x27;: &#x27;&#x27;, &#x27;work_notes&#x27;: &#x27;&#x27;, &#x27;work_notes_list&#x27;: &#x27;&#x27;, &#x27;work_start&#x27;: &#x27;&#x27;}]</div>
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
