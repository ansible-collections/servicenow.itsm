.. _servicenow.itsm.problem_info_module:


****************************
servicenow.itsm.problem_info
****************************

**List ServiceNow problems**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Retrieve information about ServiceNow problems.
- For more information, refer to the ServiceNow problem management documentation at https://docs.servicenow.com/bundle/paris-it-service-management/page/product/problem-management/concept/c_ProblemManagement.html.




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
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Password used for authentication.</div>
                        <div>If not set, the value of the <code>SN_PASSWORD</code> environment variable will be used.</div>
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
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Username used for authentication.</div>
                        <div>If not set, the value of the <code>SN_USERNAME</code> environment variable will be used.</div>
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

   :ref:`servicenow.itsm.problem_module`
      The official documentation on the **servicenow.itsm.problem** module.


Examples
--------

.. code-block:: yaml+jinja

    - name: Retrieve all problems
      servicenow.itsm.problem_info:
      register: result

    - name: Retrieve a specific problem by its sys_id
      servicenow.itsm.problem_info:
        sys_id: 471bfbc7a9fe198101e77a3e10e5d47f
      register: result

    - name: Retrieve problems by number
      servicenow.itsm.problem_info:
        number: PRB0007601
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
                            <div>A list of problem records.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;active&#x27;: &#x27;true&#x27;, &#x27;activity_due&#x27;: &#x27;&#x27;, &#x27;additional_assignee_list&#x27;: &#x27;&#x27;, &#x27;approval&#x27;: &#x27;not requested&#x27;, &#x27;approval_history&#x27;: &#x27;&#x27;, &#x27;approval_set&#x27;: &#x27;&#x27;, &#x27;assigned_to&#x27;: &#x27;73ab3f173b331300ad3cc9bb34efc4df&#x27;, &#x27;assignment_group&#x27;: &#x27;&#x27;, &#x27;business_duration&#x27;: &#x27;&#x27;, &#x27;business_service&#x27;: &#x27;&#x27;, &#x27;calendar_duration&#x27;: &#x27;&#x27;, &#x27;category&#x27;: &#x27;software&#x27;, &#x27;cause_notes&#x27;: &#x27;&#x27;, &#x27;close_notes&#x27;: &#x27;&#x27;, &#x27;closed_at&#x27;: &#x27;&#x27;, &#x27;closed_by&#x27;: &#x27;&#x27;, &#x27;cmdb_ci&#x27;: &#x27;27d32778c0a8000b00db970eeaa60f16&#x27;, &#x27;comments&#x27;: &#x27;&#x27;, &#x27;comments_and_work_notes&#x27;: &#x27;&#x27;, &#x27;company&#x27;: &#x27;&#x27;, &#x27;confirmed_at&#x27;: &#x27;&#x27;, &#x27;confirmed_by&#x27;: &#x27;&#x27;, &#x27;contact_type&#x27;: &#x27;&#x27;, &#x27;contract&#x27;: &#x27;&#x27;, &#x27;correlation_display&#x27;: &#x27;&#x27;, &#x27;correlation_id&#x27;: &#x27;&#x27;, &#x27;delivery_plan&#x27;: &#x27;&#x27;, &#x27;delivery_task&#x27;: &#x27;&#x27;, &#x27;description&#x27;: &#x27;Unable to send or receive emails.&#x27;, &#x27;due_date&#x27;: &#x27;&#x27;, &#x27;duplicate_of&#x27;: &#x27;&#x27;, &#x27;escalation&#x27;: &#x27;0&#x27;, &#x27;expected_start&#x27;: &#x27;&#x27;, &#x27;first_reported_by_task&#x27;: &#x27;&#x27;, &#x27;fix_communicated_at&#x27;: &#x27;&#x27;, &#x27;fix_communicated_by&#x27;: &#x27;&#x27;, &#x27;fix_notes&#x27;: &#x27;&#x27;, &#x27;follow_up&#x27;: &#x27;&#x27;, &#x27;group_list&#x27;: &#x27;&#x27;, &#x27;impact&#x27;: &#x27;low&#x27;, &#x27;knowledge&#x27;: &#x27;false&#x27;, &#x27;known_error&#x27;: &#x27;false&#x27;, &#x27;location&#x27;: &#x27;&#x27;, &#x27;made_sla&#x27;: &#x27;true&#x27;, &#x27;major_problem&#x27;: &#x27;false&#x27;, &#x27;number&#x27;: &#x27;PRB0007601&#x27;, &#x27;opened_at&#x27;: &#x27;2018-08-30 08:08:39&#x27;, &#x27;opened_by&#x27;: &#x27;6816f79cc0a8016401c5a33be04be441&#x27;, &#x27;order&#x27;: &#x27;&#x27;, &#x27;parent&#x27;: &#x27;&#x27;, &#x27;priority&#x27;: &#x27;5&#x27;, &#x27;problem_state&#x27;: &#x27;new&#x27;, &#x27;reassignment_count&#x27;: &#x27;0&#x27;, &#x27;related_incidents&#x27;: &#x27;0&#x27;, &#x27;reopen_count&#x27;: &#x27;0&#x27;, &#x27;reopened_at&#x27;: &#x27;&#x27;, &#x27;reopened_by&#x27;: &#x27;&#x27;, &#x27;resolution_code&#x27;: &#x27;&#x27;, &#x27;resolved_at&#x27;: &#x27;&#x27;, &#x27;resolved_by&#x27;: &#x27;&#x27;, &#x27;review_outcome&#x27;: &#x27;&#x27;, &#x27;rfc&#x27;: &#x27;&#x27;, &#x27;route_reason&#x27;: &#x27;&#x27;, &#x27;service_offering&#x27;: &#x27;&#x27;, &#x27;short_description&#x27;: &#x27;Unable to send or receive emails.&#x27;, &#x27;sla_due&#x27;: &#x27;&#x27;, &#x27;state&#x27;: &#x27;new&#x27;, &#x27;subcategory&#x27;: &#x27;email&#x27;, &#x27;sys_class_name&#x27;: &#x27;problem&#x27;, &#x27;sys_created_by&#x27;: &#x27;admin&#x27;, &#x27;sys_created_on&#x27;: &#x27;2018-08-30 08:09:05&#x27;, &#x27;sys_domain&#x27;: &#x27;global&#x27;, &#x27;sys_domain_path&#x27;: &#x27;/&#x27;, &#x27;sys_id&#x27;: &#x27;62304320731823002728660c4cf6a7e8&#x27;, &#x27;sys_mod_count&#x27;: &#x27;1&#x27;, &#x27;sys_tags&#x27;: &#x27;&#x27;, &#x27;sys_updated_by&#x27;: &#x27;admin&#x27;, &#x27;sys_updated_on&#x27;: &#x27;2018-12-12 07:16:57&#x27;, &#x27;task_effective_number&#x27;: &#x27;PRB0007601&#x27;, &#x27;time_worked&#x27;: &#x27;&#x27;, &#x27;universal_request&#x27;: &#x27;&#x27;, &#x27;upon_approval&#x27;: &#x27;proceed&#x27;, &#x27;upon_reject&#x27;: &#x27;cancel&#x27;, &#x27;urgency&#x27;: &#x27;low&#x27;, &#x27;user_input&#x27;: &#x27;&#x27;, &#x27;watch_list&#x27;: &#x27;&#x27;, &#x27;work_end&#x27;: &#x27;&#x27;, &#x27;work_notes&#x27;: &#x27;&#x27;, &#x27;work_notes_list&#x27;: &#x27;&#x27;, &#x27;work_start&#x27;: &#x27;&#x27;, &#x27;workaround&#x27;: &#x27;&#x27;, &#x27;workaround_applied&#x27;: &#x27;false&#x27;, &#x27;workaround_communicated_at&#x27;: &#x27;&#x27;, &#x27;workaround_communicated_by&#x27;: &#x27;&#x27;}]</div>
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
