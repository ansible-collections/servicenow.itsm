=============================
servicenow.itsm Release Notes
=============================

.. contents:: Topics


v1.4.1
======

Release Summary
---------------

This is the minor release of the ``servicenow.itsm`` collection.

Minor Changes
-------------

- added documentation for user mapping (https://github.com/ansible-collections/servicenow.itsm/pull/202).

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
