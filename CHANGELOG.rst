=============================
servicenow.itsm Release Notes
=============================

.. contents:: Topics


v2.2.0
======

Release Summary
---------------

This is the minor release of the ``servicenow.itsm`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``servicenow.itsm`` 2.1.0.


Minor Changes
-------------

- Added attachment_upload module (https://github.com/ansible-collections/servicenow.itsm/pull/248).

New Modules
-----------

- servicenow.itsm.attachment_upload - Upload attachment to the selected table

v2.1.0
======

Release Summary
---------------

This is the minor release of the ``servicenow.itsm`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``servicenow.itsm`` 2.0.0.


Minor Changes
-------------

- api - Added parameter query_params to api module (https://github.com/ansible-collections/servicenow.itsm/pull/225).
- inventory plugin - Plugin now supports mapping of reference fields inside 'compose' block.

Bugfixes
--------

- inventory plugin - sysparm_query attribute is taken into account.
- mapping - When creating custom mapping, one can list unknown fields and map them to values. Before the fix there was a bug, where one could only rename fields inside mapping.

v2.0.0
======

Release Summary
---------------

This is the major release of the ``servicenow.itsm`` collection.

Minor Changes
-------------

- Attachment integration tests - Add missing register variables (https://github.com/ansible-collections/servicenow.itsm/pull/194)
- TableClient - Remove hardcoded value of sysparm_exclude_reference_link when querying on table api.
- \*_info modules - Added additional module parameter sysparm_display_value to all info modules, which, if set to either true or all, enables the user to see the values of sys_tags.
- \*_info modules - Added field sysparm_query, which represents an encoded query string used to filter the results as an alternative to C(query) (https://github.com/ansible-collections/servicenow.itsm/pull/190).
- api - Added module api, which essentially codifies the ServiceNow REST API explorer in Ansible-native way for POST, PATCH and DELETE operations.
- api - Enhanced api module with template processing capabilities as an alternative to its data parameter for creating or updating a resource (https://github.com/ansible-collections/servicenow.itsm/pull/201).
- api_info - Added module api_info, which essentially codifies the ServiceNow REST API explorer in Ansible-native way for retrieving records (GET operations).
- attachment integration tests - Adapt integration tests for attachment module due to changes on PR 192 (https://github.com/ansible-collections/servicenow.itsm/pull/193)
- configuration_batch_item - now returns result instead only if something was changed or not.
- configuration_item_info - Added option name to simplify queries based on that parameter.
- module_utils/attachments.py - Add ``get_attachment`` and ``save_attachment`` (https://github.com/ansible-collections/servicenow.itsm/pull/186).
- module_utils/problem.py - Added problem client for requesting problem state updates from the I(API for Red Hat Ansible Automation Platform Certified Content Collection) Scripted REST API Service.
- module_utils/util.py - Added optional Boolean parameter C(implicit) to C(get_mapper) function to provide default values for missing keys in the mapping.
- modules/problem.py - Added module parameters validation to match the mapping specification.
- modules/problem.py - Added optional module parameter C(base_api_path) to control the URI prefix of the endpoint exposed by the I(API for Red Hat Ansible Automation Platform Certified Content Collection) Scripted REST API Service.
- now - Added field sysparm_query, which represents an encoded query string used to filter the results as an alternative to C(query) (https://github.com/ansible-collections/servicenow.itsm/pull/190).
- test_api - Remove unused import which caused sanity error. (https://github.com/ansible-collections/servicenow.itsm/pull/204)

Breaking Changes / Porting Guide
--------------------------------

- configuration_item - Added name as a unique identifier. This means that the idempotence is based on name, while previously there was no idempotence (except for sys_id). When state=present if a configuration item with given name does not exist, the item is created. If it already exists, it is updated. (https://github.com/ansible-collections/servicenow.itsm/pull/192)
- plugins/inventory/now.py - Removed parameters ``ansible_host_source``, ``named_groups`` and ``group_by`` (https://github.com/ansible-collections/servicenow.itsm/pull/213).

Bugfixes
--------

- modules/problem.py - Uses I(API for Red Hat Ansible Automation Platform Certified Content Collection) Scripted REST API Service for transitioning problem state in case of Table API fails.

New Modules
-----------

- servicenow.itsm.api - Manage ServiceNow POST, PATCH and DELETE requests
- servicenow.itsm.api_info - Manage ServiceNow GET requests
- servicenow.itsm.attachment - a module that users can use to download attachment using sys_id

v1.4.0
======

Release Summary
---------------

This is the minor release of the ``servicenow.itsm`` collection.


Minor Changes
-------------

- added ignore.txt for Ansible 2.14 devel branch.
- now - Updated documents to make clear how AND OR queries operate.
- now - fix mapped attributes in now modules.
- now - fix validate-modules errors in now inventory plugins.
- now - inventory plugin updated to support ``refresh_token`` and ``grant_type`` (https://github.com/ansible-collections/servicenow.itsm/issues/168).

v1.3.3
======

Release Summary
---------------

This is the patch release of the ``servicenow.itsm`` collection.


v1.3.2
======

Release Summary
---------------

This is the patch release of the ``servicenow.itsm`` collection.


v1.3.1
======

Release Summary
---------------

This is the patch release of the ``servicenow.itsm`` collection.


v1.3.0
======

Release Summary
---------------

This is the minor release of the ``servicenow.itsm`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``servicenow.itsm`` 1.2.0.


Minor Changes
-------------

- client - Changed the base URL path of the HTTP client for all requests from `/api/now` to `/`
- now - Enhance inventory with additional groups from CMDB relations (https://github.com/ansible-collections/servicenow.itsm/issues/108).
- table.py - add change_request and configuration item search options.

New Modules
-----------

- servicenow.itsm.change_request_task - Manage ServiceNow change request tasks
- servicenow.itsm.change_request_task_info - List ServiceNow change request tasks
- servicenow.itsm.problem_task - Manage ServiceNow problem tasks
- servicenow.itsm.problem_task_info - List ServiceNow problem tasks

v1.2.0
======

Release Summary
---------------

This is the minor release of the ``servicenow.itsm`` collection.
This changelog contains all changes to the modules in this collection that
have been added after the release of ``servicenow.itsm`` 1.1.0.

Minor Changes
-------------

- attachments - Add a client for attachment management. Add support for attachments in change_request, configuration_item, incident and problem modules, including their info counterparts. (https://github.com/ansible-collections/servicenow.itsm/pull/91)

Deprecated Features
-------------------

- now inventory plugin - deprecate non constructed features (https://github.com/ansible-collections/servicenow.itsm/pull/97).

Bugfixes
--------

- change_request - validates on_hold with its respective field instead of a non-existent "on_hold" state when requiring a hold_reason (https://github.com/ansible-collections/servicenow.itsm/pull/86).
- client - Lowercase all header dict keys on Response initialization for better consistency across Python versions. Fix tests and table client accordingly (https://github.com/ansible-collections/servicenow.itsm/pull/98).
- now - add support for constructed feature in inventory plugin (https://github.com/ansible-collections/servicenow.itsm/issues/35).

New Modules
-----------

- servicenow.itsm.configuration_item_batch - Manage ServiceNow configuration items in batch mode

v1.1.0
======

Release Summary
---------------

v1.1.0 release for ServiceNow ITSM collection.

Minor Changes
-------------

- Added new query module utility to filter results in info modules (https://github.com/ansible-collections/servicenow.itsm/issues/66).
- Added query parameter to change request info module
- Added query parameter to configuration item info module
- Added query parameter to incident info module
- Added query parameter to problem info module
- Added support for ``refresh_token`` in login mechanism (https://github.com/ansible-collections/servicenow.itsm/issues/63).

Bugfixes
--------

- now - check instance host value before making REST call from the Client (https://github.com/ansible-collections/servicenow.itsm/pull/79).

v1.0.0
======

New Plugins
-----------

Inventory
~~~~~~~~~

- servicenow.itsm.now - Inventory source for ServiceNow table records.

New Modules
-----------

- servicenow.itsm.change_request - Manage ServiceNow change requests
- servicenow.itsm.change_request_info - List ServiceNow change requests
- servicenow.itsm.configuration_item - Manage ServiceNow configuration items
- servicenow.itsm.configuration_item_info - List ServiceNow configuration item
- servicenow.itsm.incident - Manage ServiceNow incidents
- servicenow.itsm.incident_info - List ServiceNow incidents
- servicenow.itsm.problem - Manage ServiceNow problems
- servicenow.itsm.problem_info - List ServiceNow problems
