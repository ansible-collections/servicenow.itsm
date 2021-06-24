=============================
servicenow.itsm Release Notes
=============================

.. contents:: Topics


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
