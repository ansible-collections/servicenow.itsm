.. _servicenow.itsm.problem_module:


***********************
servicenow.itsm.problem
***********************

**Manage ServiceNow problems**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Create, delete or update a ServiceNow problem.
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
                    <b>assigned_to</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A person who will assess this problem.</div>
                        <div>Expected value for <em>assigned_to</em> is user id (usually in the form of <code>first_name.last_name</code>).</div>
                        <div>This field is required when creating new problems for all problem <em>state</em>s except <code>new</code>.</div>
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
                    <b>cause_notes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Provide information on what caused the problem.</div>
                        <div>Required if <em>state</em> is <code>in_progress</code>.</div>
                        <div>Required if <em>state</em> is <code>resolved</code> or <code>closed</code> and <em>resolution_code</em> is <code>fix_applied</code> or <code>risk_accepted</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>close_notes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The reason for closing the problem.</div>
                        <div>Required if <em>state</em> is <code>resolved</code> or <code>closed</code> and <em>resolution_code</em> is <code>risk_accepted</code> or <code>canceled</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>description</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Detailed description of the problem.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>duplicate_of</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Number of the problem of which this problem is a duplicate of.</div>
                        <div>Required if <em>state</em> is <code>resolved</code> or <code>closed</code> and <em>resolution_code</em> is <code>duplicate</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>fix_notes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Notes on how the problem was fixed.</div>
                        <div>Required if <em>state</em> is <code>in_progress</code>.</div>
                        <div>Required if <em>state</em> is <code>resolved</code> or <code>closed</code> and <em>resolution_code</em> is <code>fix_applied</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>impact</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>low</li>
                                    <li>medium</li>
                                    <li>high</li>
                        </ul>
                </td>
                <td>
                        <div>Effect that the problem has on business.</div>
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
                    <b>number</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Number of the record to operate on.</div>
                        <div>Note that contrary to <em>sys_id</em>, <em>number</em> may not uniquely identify a record.</div>
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
                        <div>Optional remaining parameters.</div>
                        <div>For more information on optional parameters, refer to the ServiceNow documentation on creating problems at <a href='https://docs.servicenow.com/bundle/paris-it-service-management/page/product/problem-management/task/create-a-problem-v2.html'>https://docs.servicenow.com/bundle/paris-it-service-management/page/product/problem-management/task/create-a-problem-v2.html</a>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>resolution_code</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>fix_applied</li>
                                    <li>risk_accepted</li>
                                    <li>duplicate</li>
                                    <li>canceled</li>
                        </ul>
                </td>
                <td>
                        <div>The reason for problem resolution.</div>
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
                        <div>Short description of the problem that the problem-solving team should address.</div>
                        <div>Required if the problem does not exist yet.</div>
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
                                    <li>new</li>
                                    <li>assess</li>
                                    <li>root_cause_analysis</li>
                                    <li>fix_in_progress</li>
                                    <li>resolved</li>
                                    <li>closed</li>
                                    <li>absent</li>
                        </ul>
                </td>
                <td>
                        <div>State of the problem.</div>
                        <div>If a problem does not yet exist, all states except for <code>new</code> require setting of <em>assigned_to</em> parameter.</div>
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
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>urgency</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>low</li>
                                    <li>medium</li>
                                    <li>high</li>
                        </ul>
                </td>
                <td>
                        <div>The extent to which the problem resolution can bear delay.</div>
                </td>
            </tr>
    </table>
    <br/>



See Also
--------

.. seealso::

   :ref:`servicenow.itsm.problem_info_module`
      The official documentation on the **servicenow.itsm.problem_info** module.


Examples
--------

.. code-block:: yaml

    - name: Create a problem
      servicenow.itsm.problem:
        state: new
        short_description: Issue with the network printer
        description: Since this morning, all printer jobs are stuck.
        attachments:
          - path: path/to/attachment.txt
        impact: medium
        urgency: low
        other:
          user_input: notes

    - name: Assign a problem to a user for assessment
      servicenow.itsm.problem:
        number: PRB0000010
        state: assess
        assigned_to: problem.manager

    - name: Mark a problem for root cause analysis
      servicenow.itsm.problem:
        number: PRB0000010
        state: root_cause_analysis

    - name: Work on fixing a problem
      servicenow.itsm.problem:
        number: PRB0000010
        state: fix_in_progress
        cause_notes: I identified the issue.
        fix_notes: Fix here.


    - name: Close a problem as fixed
      servicenow.itsm.problem:
        number: PRB0000010
        state: closed
        resolution_code: fix_applied
        cause_notes: I found that this doesn't work.
        fix_notes: I solved it like this.

    - name: Close a problem as duplicate
      servicenow.itsm.problem:
        number: PRB0000010
        state: closed
        resolution_code: duplicate
        duplicate_of: PRB0000001

    - name: Cancel a problem
      servicenow.itsm.problem:
        number: PRB0000010
        state: closed
        resolution_code: canceled
        close_notes: The problem seems to have resolved itself.

    - name: Delete a problem
      servicenow.itsm.problem:
        number: PRB0000010
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
                            <div>The problem record.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;active&#x27;: &#x27;true&#x27;, &#x27;activity_due&#x27;: &#x27;&#x27;, &#x27;additional_assignee_list&#x27;: &#x27;&#x27;, &#x27;approval&#x27;: &#x27;not requested&#x27;, &#x27;approval_history&#x27;: &#x27;&#x27;, &#x27;approval_set&#x27;: &#x27;&#x27;, &#x27;assigned_to&#x27;: &#x27;73ab3f173b331300ad3cc9bb34efc4df&#x27;, &#x27;assignment_group&#x27;: &#x27;&#x27;, &#x27;attachments&#x27;: [{&#x27;average_image_color&#x27;: &#x27;&#x27;, &#x27;chunk_size_bytes&#x27;: &#x27;700000&#x27;, &#x27;compressed&#x27;: &#x27;true&#x27;, &#x27;content_type&#x27;: &#x27;text/plain&#x27;, &#x27;download_link&#x27;: &#x27;https://www.example.com/api/now/attachment/31cdf4d50706301022f9ffa08c1ed07f/file&#x27;, &#x27;file_name&#x27;: &#x27;sample_file1.txt&#x27;, &#x27;hash&#x27;: &#x27;6f2b0dec698566114435a23f15dcac848a40e1fd3e0eda4afe24a663dda23f2e&#x27;, &#x27;image_height&#x27;: &#x27;&#x27;, &#x27;image_width&#x27;: &#x27;&#x27;, &#x27;size_bytes&#x27;: &#x27;210&#x27;, &#x27;size_compressed&#x27;: &#x27;206&#x27;, &#x27;state&#x27;: &#x27;pending&#x27;, &#x27;sys_created_by&#x27;: &#x27;admin&#x27;, &#x27;sys_created_on&#x27;: &#x27;2021-08-17 11:19:49&#x27;, &#x27;sys_id&#x27;: &#x27;31cdf4d50706301022f9ffa08c1ed07f&#x27;, &#x27;sys_mod_count&#x27;: &#x27;0&#x27;, &#x27;sys_tags&#x27;: &#x27;&#x27;, &#x27;sys_updated_by&#x27;: &#x27;admin&#x27;, &#x27;sys_updated_on&#x27;: &#x27;2021-08-17 11:19:49&#x27;, &#x27;table_name&#x27;: &#x27;problem&#x27;, &#x27;table_sys_id&#x27;: &#x27;6dcdb4d50706301022f9ffa08c1ed0fb&#x27;}], &#x27;business_duration&#x27;: &#x27;&#x27;, &#x27;business_service&#x27;: &#x27;&#x27;, &#x27;calendar_duration&#x27;: &#x27;&#x27;, &#x27;category&#x27;: &#x27;software&#x27;, &#x27;cause_notes&#x27;: &#x27;&#x27;, &#x27;close_notes&#x27;: &#x27;&#x27;, &#x27;closed_at&#x27;: &#x27;&#x27;, &#x27;closed_by&#x27;: &#x27;&#x27;, &#x27;cmdb_ci&#x27;: &#x27;27d32778c0a8000b00db970eeaa60f16&#x27;, &#x27;comments&#x27;: &#x27;&#x27;, &#x27;comments_and_work_notes&#x27;: &#x27;&#x27;, &#x27;company&#x27;: &#x27;&#x27;, &#x27;confirmed_at&#x27;: &#x27;&#x27;, &#x27;confirmed_by&#x27;: &#x27;&#x27;, &#x27;contact_type&#x27;: &#x27;&#x27;, &#x27;contract&#x27;: &#x27;&#x27;, &#x27;correlation_display&#x27;: &#x27;&#x27;, &#x27;correlation_id&#x27;: &#x27;&#x27;, &#x27;delivery_plan&#x27;: &#x27;&#x27;, &#x27;delivery_task&#x27;: &#x27;&#x27;, &#x27;description&#x27;: &#x27;Unable to send or receive emails.&#x27;, &#x27;due_date&#x27;: &#x27;&#x27;, &#x27;duplicate_of&#x27;: &#x27;&#x27;, &#x27;escalation&#x27;: &#x27;0&#x27;, &#x27;expected_start&#x27;: &#x27;&#x27;, &#x27;first_reported_by_task&#x27;: &#x27;&#x27;, &#x27;fix_communicated_at&#x27;: &#x27;&#x27;, &#x27;fix_communicated_by&#x27;: &#x27;&#x27;, &#x27;fix_notes&#x27;: &#x27;&#x27;, &#x27;follow_up&#x27;: &#x27;&#x27;, &#x27;group_list&#x27;: &#x27;&#x27;, &#x27;impact&#x27;: &#x27;low&#x27;, &#x27;knowledge&#x27;: &#x27;false&#x27;, &#x27;known_error&#x27;: &#x27;false&#x27;, &#x27;location&#x27;: &#x27;&#x27;, &#x27;made_sla&#x27;: &#x27;true&#x27;, &#x27;major_problem&#x27;: &#x27;false&#x27;, &#x27;number&#x27;: &#x27;PRB0007601&#x27;, &#x27;opened_at&#x27;: &#x27;2018-08-30 08:08:39&#x27;, &#x27;opened_by&#x27;: &#x27;6816f79cc0a8016401c5a33be04be441&#x27;, &#x27;order&#x27;: &#x27;&#x27;, &#x27;parent&#x27;: &#x27;&#x27;, &#x27;priority&#x27;: &#x27;5&#x27;, &#x27;problem_state&#x27;: &#x27;new&#x27;, &#x27;reassignment_count&#x27;: &#x27;0&#x27;, &#x27;related_incidents&#x27;: &#x27;0&#x27;, &#x27;reopen_count&#x27;: &#x27;0&#x27;, &#x27;reopened_at&#x27;: &#x27;&#x27;, &#x27;reopened_by&#x27;: &#x27;&#x27;, &#x27;resolution_code&#x27;: &#x27;&#x27;, &#x27;resolved_at&#x27;: &#x27;&#x27;, &#x27;resolved_by&#x27;: &#x27;&#x27;, &#x27;review_outcome&#x27;: &#x27;&#x27;, &#x27;rfc&#x27;: &#x27;&#x27;, &#x27;route_reason&#x27;: &#x27;&#x27;, &#x27;service_offering&#x27;: &#x27;&#x27;, &#x27;short_description&#x27;: &#x27;Unable to send or receive emails.&#x27;, &#x27;sla_due&#x27;: &#x27;&#x27;, &#x27;state&#x27;: &#x27;new&#x27;, &#x27;subcategory&#x27;: &#x27;email&#x27;, &#x27;sys_class_name&#x27;: &#x27;problem&#x27;, &#x27;sys_created_by&#x27;: &#x27;admin&#x27;, &#x27;sys_created_on&#x27;: &#x27;2018-08-30 08:09:05&#x27;, &#x27;sys_domain&#x27;: &#x27;global&#x27;, &#x27;sys_domain_path&#x27;: &#x27;/&#x27;, &#x27;sys_id&#x27;: &#x27;62304320731823002728660c4cf6a7e8&#x27;, &#x27;sys_mod_count&#x27;: &#x27;1&#x27;, &#x27;sys_tags&#x27;: &#x27;&#x27;, &#x27;sys_updated_by&#x27;: &#x27;admin&#x27;, &#x27;sys_updated_on&#x27;: &#x27;2018-12-12 07:16:57&#x27;, &#x27;task_effective_number&#x27;: &#x27;PRB0007601&#x27;, &#x27;time_worked&#x27;: &#x27;&#x27;, &#x27;universal_request&#x27;: &#x27;&#x27;, &#x27;upon_approval&#x27;: &#x27;proceed&#x27;, &#x27;upon_reject&#x27;: &#x27;cancel&#x27;, &#x27;urgency&#x27;: &#x27;low&#x27;, &#x27;user_input&#x27;: &#x27;&#x27;, &#x27;watch_list&#x27;: &#x27;&#x27;, &#x27;work_end&#x27;: &#x27;&#x27;, &#x27;work_notes&#x27;: &#x27;&#x27;, &#x27;work_notes_list&#x27;: &#x27;&#x27;, &#x27;work_start&#x27;: &#x27;&#x27;, &#x27;workaround&#x27;: &#x27;&#x27;, &#x27;workaround_applied&#x27;: &#x27;false&#x27;, &#x27;workaround_communicated_at&#x27;: &#x27;&#x27;, &#x27;workaround_communicated_by&#x27;: &#x27;&#x27;}</div>
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
