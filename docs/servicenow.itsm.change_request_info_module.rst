.. _servicenow.itsm.change_request_info_module:


***********************************
servicenow.itsm.change_request_info
***********************************

**List ServiceNow change requests**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Retrieve information about ServiceNow change requests.
- For more information, refer to the ServiceNow change management documentation at https://docs.servicenow.com/bundle/paris-it-service-management/page/product/change-management/concept/c_ITILChangeManagement.html.




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

   :ref:`servicenow.itsm.change_request_module`
      The official documentation on the **servicenow.itsm.change_request** module.


Examples
--------

.. code-block:: yaml

    - name: Retrieve all change requests
      servicenow.itsm.change_request_info:
      register: result

    - name: Retrieve a specific change request by its sys_id
      servicenow.itsm.change_request_info:
        sys_id: 471bfbc7a9fe198101e77a3e10e5d47f
      register: result

    - name: Retrieve change requests by number
      servicenow.itsm.change_request_info:
        number: PRB0007601
      register: result

    - name: Retrieve change requests that contain SAP in its short description
      servicenow.itsm.change_request_info:
        query:
          - short_description: LIKE SAP
      register: result

    - name: Retrieve new change requests assigned to abel.tuter or bertie.luby
      servicenow.itsm.change_request_info:
        query:
          - state: = new
            assigned_to: = abel.tuter
          - state: = new
            assigned_to: = bertie.luby



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
                            <div>A list of change request records.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;active&#x27;: &#x27;false&#x27;, &#x27;activity_due&#x27;: &#x27;&#x27;, &#x27;additional_assignee_list&#x27;: &#x27;&#x27;, &#x27;approval&#x27;: &#x27;approved&#x27;, &#x27;approval_history&#x27;: &#x27;&#x27;, &#x27;approval_set&#x27;: &#x27;&#x27;, &#x27;assigned_to&#x27;: &#x27;&#x27;, &#x27;assignment_group&#x27;: &#x27;d625dccec0a8016700a222a0f7900d06&#x27;, &#x27;attachments&#x27;: [{&#x27;average_image_color&#x27;: &#x27;&#x27;, &#x27;chunk_size_bytes&#x27;: &#x27;700000&#x27;, &#x27;compressed&#x27;: &#x27;true&#x27;, &#x27;content_type&#x27;: &#x27;text/plain&#x27;, &#x27;download_link&#x27;: &#x27;https://www.example.com/api/now/attachment/5f7d3c950706301022f9ffa08c1ed062/file&#x27;, &#x27;file_name&#x27;: &#x27;sample_file1.txt&#x27;, &#x27;hash&#x27;: &#x27;6f2b0dec698566114435a23f15dcac848a40e1fd3e0eda4afe24a663dda23f2e&#x27;, &#x27;image_height&#x27;: &#x27;&#x27;, &#x27;image_width&#x27;: &#x27;&#x27;, &#x27;size_bytes&#x27;: &#x27;210&#x27;, &#x27;size_compressed&#x27;: &#x27;206&#x27;, &#x27;state&#x27;: &#x27;pending&#x27;, &#x27;sys_created_by&#x27;: &#x27;admin&#x27;, &#x27;sys_created_on&#x27;: &#x27;2021-08-17 11:18:33&#x27;, &#x27;sys_id&#x27;: &#x27;5f7d3c950706301022f9ffa08c1ed062&#x27;, &#x27;sys_mod_count&#x27;: &#x27;0&#x27;, &#x27;sys_tags&#x27;: &#x27;&#x27;, &#x27;sys_updated_by&#x27;: &#x27;admin&#x27;, &#x27;sys_updated_on&#x27;: &#x27;2021-08-17 11:18:33&#x27;, &#x27;table_name&#x27;: &#x27;change_request&#x27;, &#x27;table_sys_id&#x27;: &#x27;3a7db0d50706301022f9ffa08c1ed092&#x27;}], &#x27;backout_plan&#x27;: &#x27;&#x27;, &#x27;business_duration&#x27;: &#x27;&#x27;, &#x27;business_service&#x27;: &#x27;&#x27;, &#x27;cab_date&#x27;: &#x27;&#x27;, &#x27;cab_delegate&#x27;: &#x27;&#x27;, &#x27;cab_recommendation&#x27;: &#x27;&#x27;, &#x27;cab_required&#x27;: &#x27;false&#x27;, &#x27;calendar_duration&#x27;: &#x27;&#x27;, &#x27;category&#x27;: &#x27;Other&#x27;, &#x27;change_plan&#x27;: &#x27;&#x27;, &#x27;close_code&#x27;: &#x27;successful&#x27;, &#x27;close_notes&#x27;: &#x27;Completed successfully&#x27;, &#x27;closed_at&#x27;: &#x27;2015-07-06 18:18:53&#x27;, &#x27;closed_by&#x27;: &#x27;6816f79cc0a8016401c5a33be04be441&#x27;, &#x27;cmdb_ci&#x27;: &#x27;&#x27;, &#x27;comments&#x27;: &#x27;&#x27;, &#x27;comments_and_work_notes&#x27;: &#x27;&#x27;, &#x27;company&#x27;: &#x27;&#x27;, &#x27;conflict_last_run&#x27;: &#x27;&#x27;, &#x27;conflict_status&#x27;: &#x27;Not Run&#x27;, &#x27;contact_type&#x27;: &#x27;phone&#x27;, &#x27;contract&#x27;: &#x27;&#x27;, &#x27;correlation_display&#x27;: &#x27;&#x27;, &#x27;correlation_id&#x27;: &#x27;&#x27;, &#x27;delivery_plan&#x27;: &#x27;&#x27;, &#x27;delivery_task&#x27;: &#x27;&#x27;, &#x27;description&#x27;: &#x27;Decommission a server&#x27;, &#x27;due_date&#x27;: &#x27;&#x27;, &#x27;end_date&#x27;: &#x27;&#x27;, &#x27;escalation&#x27;: &#x27;0&#x27;, &#x27;expected_start&#x27;: &#x27;&#x27;, &#x27;follow_up&#x27;: &#x27;&#x27;, &#x27;group_list&#x27;: &#x27;&#x27;, &#x27;impact&#x27;: &#x27;3&#x27;, &#x27;implementation_plan&#x27;: &#x27;Implementation plan&#x27;, &#x27;justification&#x27;: &#x27;&#x27;, &#x27;knowledge&#x27;: &#x27;false&#x27;, &#x27;location&#x27;: &#x27;&#x27;, &#x27;made_sla&#x27;: &#x27;true&#x27;, &#x27;number&#x27;: &#x27;CHG0000023&#x27;, &#x27;on_hold&#x27;: &#x27;false&#x27;, &#x27;on_hold_reason&#x27;: &#x27;&#x27;, &#x27;on_hold_task&#x27;: &#x27;&#x27;, &#x27;opened_at&#x27;: &#x27;2015-07-06 18:17:21&#x27;, &#x27;opened_by&#x27;: &#x27;6816f79cc0a8016401c5a33be04be441&#x27;, &#x27;order&#x27;: &#x27;&#x27;, &#x27;outside_maintenance_schedule&#x27;: &#x27;false&#x27;, &#x27;parent&#x27;: &#x27;&#x27;, &#x27;phase&#x27;: &#x27;requested&#x27;, &#x27;phase_state&#x27;: &#x27;open&#x27;, &#x27;priority&#x27;: &#x27;4&#x27;, &#x27;production_system&#x27;: &#x27;false&#x27;, &#x27;reason&#x27;: &#x27;&#x27;, &#x27;reassignment_count&#x27;: &#x27;2&#x27;, &#x27;requested_by&#x27;: &#x27;6816f79cc0a8016401c5a33be04be441&#x27;, &#x27;requested_by_date&#x27;: &#x27;&#x27;, &#x27;review_comments&#x27;: &#x27;&#x27;, &#x27;review_date&#x27;: &#x27;&#x27;, &#x27;review_status&#x27;: &#x27;&#x27;, &#x27;risk&#x27;: &#x27;3&#x27;, &#x27;risk_impact_analysis&#x27;: &#x27;&#x27;, &#x27;route_reason&#x27;: &#x27;&#x27;, &#x27;scope&#x27;: &#x27;3&#x27;, &#x27;service_offering&#x27;: &#x27;&#x27;, &#x27;short_description&#x27;: &#x27;Decommission server&#x27;, &#x27;sla_due&#x27;: &#x27;&#x27;, &#x27;start_date&#x27;: &#x27;&#x27;, &#x27;state&#x27;: &#x27;3&#x27;, &#x27;std_change_producer_version&#x27;: &#x27;deb8544047810200e90d87e8dee490af&#x27;, &#x27;sys_class_name&#x27;: &#x27;change_request&#x27;, &#x27;sys_created_by&#x27;: &#x27;admin&#x27;, &#x27;sys_created_on&#x27;: &#x27;2015-07-06 18:17:22&#x27;, &#x27;sys_domain&#x27;: &#x27;global&#x27;, &#x27;sys_domain_path&#x27;: &#x27;/&#x27;, &#x27;sys_id&#x27;: &#x27;70ad699e47410200e90d87e8dee4907d&#x27;, &#x27;sys_mod_count&#x27;: &#x27;8&#x27;, &#x27;sys_tags&#x27;: &#x27;&#x27;, &#x27;sys_updated_by&#x27;: &#x27;admin&#x27;, &#x27;sys_updated_on&#x27;: &#x27;2015-07-06 18:18:53&#x27;, &#x27;task_effective_number&#x27;: &#x27;CHG0000023&#x27;, &#x27;test_plan&#x27;: &#x27;Test plan&#x27;, &#x27;time_worked&#x27;: &#x27;&#x27;, &#x27;type&#x27;: &#x27;standard&#x27;, &#x27;unauthorized&#x27;: &#x27;false&#x27;, &#x27;universal_request&#x27;: &#x27;&#x27;, &#x27;upon_approval&#x27;: &#x27;proceed&#x27;, &#x27;upon_reject&#x27;: &#x27;cancel&#x27;, &#x27;urgency&#x27;: &#x27;3&#x27;, &#x27;user_input&#x27;: &#x27;&#x27;, &#x27;watch_list&#x27;: &#x27;&#x27;, &#x27;work_end&#x27;: &#x27;2015-07-06 18:18:34&#x27;, &#x27;work_notes&#x27;: &#x27;&#x27;, &#x27;work_notes_list&#x27;: &#x27;&#x27;, &#x27;work_start&#x27;: &#x27;2015-07-06 18:17:41&#x27;}]</div>
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
