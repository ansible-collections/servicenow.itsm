.. Created with antsibull-docs 2.16.3

servicenow.itsm.catalog_request_task module -- Manage ServiceNow catalog request tasks
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `servicenow.itsm collection <https://galaxy.ansible.com/ui/repo/published/servicenow/itsm/>`_ (version 2.13.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install servicenow.itsm`.

To use it in a playbook, specify: ``servicenow.itsm.catalog_request_task``.

New in servicenow.itsm 2.11.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Create, delete or update a ServiceNow catalog request task (sc\_task).
- For more information, refer to the ServiceNow service catalog documentation at \ `https://docs.servicenow.com/bundle/utah-servicenow-platform/page/product/service-catalog/concept/c\_ServiceCatalogProcess.html <https://docs.servicenow.com/bundle/utah-servicenow-platform/page/product/service-catalog/concept/c_ServiceCatalogProcess.html>`__.








Parameters
----------

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th colspan="2"><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-approval"></div>
      <p style="display: inline;"><strong>approval</strong></p>
      <a class="ansibleOptionLink" href="#parameter-approval" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Approval status of the catalog request task.</p>
      <p>Default choices are <code class='docutils literal notranslate'>requested</code>, <code class='docutils literal notranslate'>approved</code>, <code class='docutils literal notranslate'>rejected</code>, <code class='docutils literal notranslate'>not requested</code>.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;requested&#34;</code></p></li>
        <li><p><code>&#34;approved&#34;</code></p></li>
        <li><p><code>&#34;rejected&#34;</code></p></li>
        <li><p><code>&#34;not requested&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-assigned_to"></div>
      <p style="display: inline;"><strong>assigned_to</strong></p>
      <a class="ansibleOptionLink" href="#parameter-assigned_to" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>User assigned to handle this catalog request task.</p>
      <p>Expected value is user login name (user_name field).</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-assignment_group"></div>
      <p style="display: inline;"><strong>assignment_group</strong></p>
      <a class="ansibleOptionLink" href="#parameter-assignment_group" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The name of the group that the catalog request task is assigned to.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-attachments"></div>
      <p style="display: inline;"><strong>attachments</strong></p>
      <a class="ansibleOptionLink" href="#parameter-attachments" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=dictionary</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in servicenow.itsm 1.2.0</i></p>
    </td>
    <td valign="top">
      <p>ServiceNow attachments.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-attachments/name"></div>
      <p style="display: inline;"><strong>name</strong></p>
      <a class="ansibleOptionLink" href="#parameter-attachments/name" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Name of the file to be uploaded.</p>
      <p>Serves as unique identifier.</p>
      <p>If not specified, the module will use <em>path</em>&#x27;s base name.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-attachments/path"></div>
      <p style="display: inline;"><strong>path</strong></p>
      <a class="ansibleOptionLink" href="#parameter-attachments/path" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>Path to the file to be uploaded.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-attachments/type"></div>
      <p style="display: inline;"><strong>type</strong></p>
      <a class="ansibleOptionLink" href="#parameter-attachments/type" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>MIME type of the file to be attached.</p>
      <p>If not specified, the module will try to guess the file&#x27;s type from its extension.</p>
    </td>
  </tr>

  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-catalog_request_task_mapping"></div>
      <p style="display: inline;"><strong>catalog_request_task_mapping</strong></p>
      <a class="ansibleOptionLink" href="#parameter-catalog_request_task_mapping" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in servicenow.itsm 2.11.0</i></p>
    </td>
    <td valign="top">
      <p>User mapping for <em>Catalog request task</em> object, where user can override Choice Lists values for objects.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-catalog_request_task_mapping/approval"></div>
      <p style="display: inline;"><strong>approval</strong></p>
      <a class="ansibleOptionLink" href="#parameter-catalog_request_task_mapping/approval" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Approval status of the catalog request task.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-catalog_request_task_mapping/impact"></div>
      <p style="display: inline;"><strong>impact</strong></p>
      <a class="ansibleOptionLink" href="#parameter-catalog_request_task_mapping/impact" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Impact of the catalog request task.</p>
      <p>Impact 1 is the highest, 3 is the lowest impact.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-catalog_request_task_mapping/priority"></div>
      <p style="display: inline;"><strong>priority</strong></p>
      <a class="ansibleOptionLink" href="#parameter-catalog_request_task_mapping/priority" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Priority of the catalog request task.</p>
      <p>Priority 1 is the highest, 5 is the lowest priority.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-catalog_request_task_mapping/state"></div>
      <p style="display: inline;"><strong>state</strong></p>
      <a class="ansibleOptionLink" href="#parameter-catalog_request_task_mapping/state" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>The current state of the catalog request task.</p>
      <p>Special value that can not be overridden is <code class='docutils literal notranslate'>present</code> and <code class='docutils literal notranslate'>absent</code>, which would create/update or remove a catalog request task from ServiceNow.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-catalog_request_task_mapping/urgency"></div>
      <p style="display: inline;"><strong>urgency</strong></p>
      <a class="ansibleOptionLink" href="#parameter-catalog_request_task_mapping/urgency" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Urgency of the catalog request task.</p>
      <p>Urgency 1 is the highest, 3 is the lowest urgency.</p>
    </td>
  </tr>

  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-close_notes"></div>
      <p style="display: inline;"><strong>close_notes</strong></p>
      <a class="ansibleOptionLink" href="#parameter-close_notes" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Notes added when closing the catalog request task.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-comments"></div>
      <p style="display: inline;"><strong>comments</strong></p>
      <a class="ansibleOptionLink" href="#parameter-comments" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Additional comments for the catalog request task.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-delivery_plan"></div>
      <p style="display: inline;"><strong>delivery_plan</strong></p>
      <a class="ansibleOptionLink" href="#parameter-delivery_plan" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Delivery plan for the catalog request task.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-delivery_task"></div>
      <p style="display: inline;"><strong>delivery_task</strong></p>
      <a class="ansibleOptionLink" href="#parameter-delivery_task" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Delivery task reference for the catalog request task.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-description"></div>
      <p style="display: inline;"><strong>description</strong></p>
      <a class="ansibleOptionLink" href="#parameter-description" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Detailed description of the catalog request task.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-due_date"></div>
      <p style="display: inline;"><strong>due_date</strong></p>
      <a class="ansibleOptionLink" href="#parameter-due_date" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Expected due date for the catalog request task.</p>
      <p>Expected format is YYYY-MM-DD.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-impact"></div>
      <p style="display: inline;"><strong>impact</strong></p>
      <a class="ansibleOptionLink" href="#parameter-impact" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Impact of the catalog request task.</p>
      <p>Default choices are <code class='docutils literal notranslate'>1</code>, <code class='docutils literal notranslate'>2</code>, <code class='docutils literal notranslate'>3</code>.</p>
      <p>Impact 1 is the highest, 3 is the lowest impact.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;1&#34;</code></p></li>
        <li><p><code>&#34;2&#34;</code></p></li>
        <li><p><code>&#34;3&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance"></div>
      <p style="display: inline;"><strong>instance</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>ServiceNow instance information.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/access_token"></div>
      <p style="display: inline;"><strong>access_token</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/access_token" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in servicenow.itsm 2.3.0</i></p>
    </td>
    <td valign="top">
      <p>Access token obtained via OAuth authentication.</p>
      <p>Used for OAuth-generated tokens that require Authorization Bearer headers.</p>
      <p>If not set, the value of the <code class='docutils literal notranslate'>SN_ACCESS_TOKEN</code> environment variable will be used.</p>
      <p>Mutually exclusive with <em>api_key</em>.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/api_key"></div>
      <p style="display: inline;"><strong>api_key</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/api_key" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>ServiceNow API key for direct authentication.</p>
      <p>Used for direct API keys that require x-sn-apikey headers.</p>
      <p>If not set, the value of the <code class='docutils literal notranslate'>SN_API_KEY</code> environment variable will be used.</p>
      <p>Mutually exclusive with <em>access_token</em>.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/api_path"></div>
      <p style="display: inline;"><strong>api_path</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/api_path" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in servicenow.itsm 2.4.0</i></p>
    </td>
    <td valign="top">
      <p>Change the API endpoint of SNOW instance from default &#x27;api/now&#x27;.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;api/now&#34;</code></p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/client_certificate_file"></div>
      <p style="display: inline;"><strong>client_certificate_file</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/client_certificate_file" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The path to the PEM certificate file that should be used for authentication.</p>
      <p>The file must be local and accessible to the host running the module.</p>
      <p><em>client_certificate_file</em> and <em>client_key_file</em> must be provided together.</p>
      <p>If client certificate parameters are provided, they will be used instead of other authentication methods.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/client_id"></div>
      <p style="display: inline;"><strong>client_id</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/client_id" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>ID of the client application used for OAuth authentication.</p>
      <p>If not set, the value of the <code class='docutils literal notranslate'>SN_CLIENT_ID</code> environment variable will be used.</p>
      <p>If provided, it requires <em>client_secret</em>.</p>
      <p>Required when <em>grant_type=client_credentials</em>.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/client_key_file"></div>
      <p style="display: inline;"><strong>client_key_file</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/client_key_file" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The path to the certificate key file that should be used for authentication.</p>
      <p>The file must be local and accessible to the host running the module.</p>
      <p><em>client_certificate_file</em> and <em>client_key_file</em> must be provided together.</p>
      <p>If client certificate parameters are provided, they will be used instead of other authentication methods.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/client_secret"></div>
      <p style="display: inline;"><strong>client_secret</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/client_secret" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Secret associated with <em>client_id</em>. Used for OAuth authentication.</p>
      <p>If not set, the value of the <code class='docutils literal notranslate'>SN_CLIENT_SECRET</code> environment variable will be used.</p>
      <p>If provided, it requires <em>client_id</em>.</p>
      <p>Required when <em>grant_type=client_credentials</em>.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/custom_headers"></div>
      <p style="display: inline;"><strong>custom_headers</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/custom_headers" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in servicenow.itsm 2.4.0</i></p>
    </td>
    <td valign="top">
      <p>A dictionary containing any extra headers which will be passed with the request.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/grant_type"></div>
      <p style="display: inline;"><strong>grant_type</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/grant_type" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in servicenow.itsm 1.1.0</i></p>
    </td>
    <td valign="top">
      <p>Grant type used for OAuth authentication.</p>
      <p>If not set, the value of the <code class='docutils literal notranslate'>SN_GRANT_TYPE</code> environment variable will be used.</p>
      <p>Since version 2.3.0, it no longer has a default value in the argument specifications.</p>
      <p>If not set by any means, the default value (that is, <em>password</em>) will be set internally to preserve backwards compatibility.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;password&#34;</code></p></li>
        <li><p><code>&#34;refresh_token&#34;</code></p></li>
        <li><p><code>&#34;client_credentials&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/host"></div>
      <p style="display: inline;"><strong>host</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/host" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>The ServiceNow host name.</p>
      <p>If not set, the value of the <code class='docutils literal notranslate'>SN_HOST</code> environment variable will be used.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/password"></div>
      <p style="display: inline;"><strong>password</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/password" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Password used for authentication.</p>
      <p>If not set, the value of the <code class='docutils literal notranslate'>SN_PASSWORD</code> environment variable will be used.</p>
      <p>Required when using basic authentication or when <em>grant_type=password</em>.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/refresh_token"></div>
      <p style="display: inline;"><strong>refresh_token</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/refresh_token" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in servicenow.itsm 1.1.0</i></p>
    </td>
    <td valign="top">
      <p>Refresh token used for OAuth authentication.</p>
      <p>If not set, the value of the <code class='docutils literal notranslate'>SN_REFRESH_TOKEN</code> environment variable will be used.</p>
      <p>Required when <em>grant_type=refresh_token</em>.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/timeout"></div>
      <p style="display: inline;"><strong>timeout</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/timeout" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">float</span>
      </p>
    </td>
    <td valign="top">
      <p>Timeout in seconds for the connection with the ServiceNow instance.</p>
      <p>If not set, the value of the <code class='docutils literal notranslate'>SN_TIMEOUT</code> environment variable will be used.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">10.0</code></p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/username"></div>
      <p style="display: inline;"><strong>username</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/username" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Username used for authentication.</p>
      <p>If not set, the value of the <code class='docutils literal notranslate'>SN_USERNAME</code> environment variable will be used.</p>
      <p>Required when using basic authentication or when <em>grant_type=password</em>.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-instance/validate_certs"></div>
      <p style="display: inline;"><strong>validate_certs</strong></p>
      <a class="ansibleOptionLink" href="#parameter-instance/validate_certs" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in servicenow.itsm 2.3.0</i></p>
    </td>
    <td valign="top">
      <p>If host&#x27;s certificate is validated or not.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code style="color: blue;"><b>true</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

    </td>
  </tr>

  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-number"></div>
      <p style="display: inline;"><strong>number</strong></p>
      <a class="ansibleOptionLink" href="#parameter-number" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Number of the record to operate on.</p>
      <p>Note that contrary to <em>sys_id</em>, <em>number</em> may not uniquely identify a record.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-order"></div>
      <p style="display: inline;"><strong>order</strong></p>
      <a class="ansibleOptionLink" href="#parameter-order" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>
    </td>
    <td valign="top">
      <p>Order/sequence number for task execution.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-other"></div>
      <p style="display: inline;"><strong>other</strong></p>
      <a class="ansibleOptionLink" href="#parameter-other" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Optional remaining parameters.</p>
      <p>For more information on optional parameters, refer to the ServiceNow catalog request task documentation.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-priority"></div>
      <p style="display: inline;"><strong>priority</strong></p>
      <a class="ansibleOptionLink" href="#parameter-priority" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Priority of the catalog request task.</p>
      <p>Default choices are <code class='docutils literal notranslate'>1</code>, <code class='docutils literal notranslate'>2</code>, <code class='docutils literal notranslate'>3</code>, <code class='docutils literal notranslate'>4</code>, <code class='docutils literal notranslate'>5</code>.</p>
      <p>Priority 1 is the highest, 5 is the lowest priority.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;1&#34;</code></p></li>
        <li><p><code>&#34;2&#34;</code></p></li>
        <li><p><code>&#34;3&#34;</code></p></li>
        <li><p><code>&#34;4&#34;</code></p></li>
        <li><p><code>&#34;5&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-request"></div>
      <p style="display: inline;"><strong>request</strong></p>
      <a class="ansibleOptionLink" href="#parameter-request" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The catalog request (sc_request) this task belongs to.</p>
      <p>Can be specified as sys_id or number of the catalog request.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-requested_by"></div>
      <p style="display: inline;"><strong>requested_by</strong></p>
      <a class="ansibleOptionLink" href="#parameter-requested_by" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>User who requested the catalog item.</p>
      <p>Expected value is user login name (user_name field).</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-requested_for"></div>
      <p style="display: inline;"><strong>requested_for</strong></p>
      <a class="ansibleOptionLink" href="#parameter-requested_for" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>User who the catalog item is being requested for.</p>
      <p>Expected value is user login name (user_name field).</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-short_description"></div>
      <p style="display: inline;"><strong>short_description</strong></p>
      <a class="ansibleOptionLink" href="#parameter-short_description" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Brief summary of the catalog request task.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-state"></div>
      <p style="display: inline;"><strong>state</strong></p>
      <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The state of the catalog request task.</p>
      <p>If <em>state</em> value is <code class='docutils literal notranslate'>present</code>, the record is created or updated.</p>
      <p>If <em>state</em> value is <code class='docutils literal notranslate'>absent</code>, the record is deleted.</p>
      <p>Default choices are <code class='docutils literal notranslate'>present</code> and <code class='docutils literal notranslate'>absent</code>.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;present&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;absent&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-sys_id"></div>
      <p style="display: inline;"><strong>sys_id</strong></p>
      <a class="ansibleOptionLink" href="#parameter-sys_id" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Unique identifier of the record to operate on.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-task_state"></div>
      <p style="display: inline;"><strong>task_state</strong></p>
      <a class="ansibleOptionLink" href="#parameter-task_state" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The current state of the catalog request task.</p>
      <p>Default choices are <code class='docutils literal notranslate'>pending</code>, <code class='docutils literal notranslate'>open</code>, <code class='docutils literal notranslate'>work_in_progress</code>, <code class='docutils literal notranslate'>closed_complete</code>, <code class='docutils literal notranslate'>closed_incomplete</code>, <code class='docutils literal notranslate'>closed_skipped</code>.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;pending&#34;</code></p></li>
        <li><p><code>&#34;open&#34;</code></p></li>
        <li><p><code>&#34;work_in_progress&#34;</code></p></li>
        <li><p><code>&#34;closed_complete&#34;</code></p></li>
        <li><p><code>&#34;closed_incomplete&#34;</code></p></li>
        <li><p><code>&#34;closed_skipped&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-urgency"></div>
      <p style="display: inline;"><strong>urgency</strong></p>
      <a class="ansibleOptionLink" href="#parameter-urgency" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Urgency of the catalog request task.</p>
      <p>Default choices are <code class='docutils literal notranslate'>1</code>, <code class='docutils literal notranslate'>2</code>, <code class='docutils literal notranslate'>3</code>.</p>
      <p>Urgency 1 is the highest, 3 is the lowest urgency.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;1&#34;</code></p></li>
        <li><p><code>&#34;2&#34;</code></p></li>
        <li><p><code>&#34;3&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-work_notes"></div>
      <p style="display: inline;"><strong>work_notes</strong></p>
      <a class="ansibleOptionLink" href="#parameter-work_notes" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Work notes for the catalog request task (internal notes).</p>
      <p>This field is not idempotent. Any value set here will be added to the existing work notes on the task.</p>
      <p>This field is always empty in the record returned by the module.</p>
    </td>
  </tr>
  </tbody>
  </table>





See Also
--------

* `servicenow.itsm.catalog\_request\_task\_info <catalog_request_task_info_module.rst>`__

  List ServiceNow catalog request tasks.
* `servicenow.itsm.catalog\_request <catalog_request_module.rst>`__

  Manage ServiceNow catalog requests.
* `servicenow.itsm.service\_catalog <service_catalog_module.rst>`__

  Manage ServiceNow service catalog cart.

Examples
--------

.. code-block:: yaml

    - name: Create a catalog request task
      servicenow.itsm.catalog_request_task:
        instance:
          host: https://instance_id.service-now.com
          username: user
          password: pass
        state: present
        request: REQ0000123
        short_description: Configure new laptop
        description: Install required software and configure user settings
        assignment_group: IT Support
        priority: "2"
        urgency: "2"
        impact: "3"
    - name: Update catalog request task
      servicenow.itsm.catalog_request_task:
        instance:
          host: https://instance_id.service-now.com
          username: user
          password: pass
        state: present
        number: SCTASK0000456
        task_state: work_in_progress
        assigned_to: john.doe
        work_notes: Started configuration process
    - name: Close catalog request task
      servicenow.itsm.catalog_request_task:
        instance:
          host: https://instance_id.service-now.com
          username: user
          password: pass
        state: present
        number: SCTASK0000456
        task_state: closed_complete
        close_notes: Configuration completed successfully
    - name: Delete catalog request task
      servicenow.itsm.catalog_request_task:
        instance:
          host: https://instance_id.service-now.com
          username: user
          password: pass
        state: absent
        number: SCTASK0000456
    - name: Create catalog request task with other parameters
      servicenow.itsm.catalog_request_task:
        instance:
          host: https://instance_id.service-now.com
          username: user
          password: pass
        state: present
        request: REQ0000123
        short_description: Custom task
        order: 10
        other:
          special_instructions: Handle with care
          vendor: Dell




Return Values
-------------
The following are the fields unique to this module:

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Key</p></th>
    <th><p>Description</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-record"></div>
      <p style="display: inline;"><strong>record</strong></p>
      <a class="ansibleOptionLink" href="#return-record" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>The catalog request task record.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> success</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>{&#34;active&#34;: true, &#34;approval&#34;: &#34;not requested&#34;, &#34;assigned_to&#34;: &#34;john.doe&#34;, &#34;assignment_group&#34;: &#34;IT Support&#34;, &#34;close_notes&#34;: &#34;&#34;, &#34;comments&#34;: &#34;&#34;, &#34;delivery_plan&#34;: &#34;&#34;, &#34;delivery_task&#34;: &#34;&#34;, &#34;description&#34;: &#34;Install required software and configure user settings&#34;, &#34;due_date&#34;: &#34;&#34;, &#34;impact&#34;: &#34;3&#34;, &#34;number&#34;: &#34;SCTASK0000456&#34;, &#34;opened_at&#34;: &#34;2024-01-15 10:30:00&#34;, &#34;opened_by&#34;: &#34;jane.smith&#34;, &#34;order&#34;: 10, &#34;priority&#34;: &#34;2&#34;, &#34;request&#34;: &#34;REQ0000123&#34;, &#34;requested_by&#34;: &#34;jane.smith&#34;, &#34;requested_for&#34;: &#34;john.doe&#34;, &#34;short_description&#34;: &#34;Configure new laptop&#34;, &#34;state&#34;: &#34;present&#34;, &#34;sys_created_by&#34;: &#34;jane.smith&#34;, &#34;sys_created_on&#34;: &#34;2024-01-15 10:30:00&#34;, &#34;sys_id&#34;: &#34;c36d93a37b1200001c9c9b5b8a9619a9&#34;, &#34;sys_updated_by&#34;: &#34;jane.smith&#34;, &#34;sys_updated_on&#34;: &#34;2024-01-15 10:30:00&#34;, &#34;task_state&#34;: &#34;open&#34;, &#34;urgency&#34;: &#34;2&#34;, &#34;work_notes&#34;: &#34;&#34;}</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- ServiceNow ITSM Collection Contributors (@ansible-collections)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/servicenow.itsm/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/servicenow.itsm>`__
