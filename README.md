#  Ansible Collection for ServiceNow ITSM

The Ansible Collection for ServiceNow IT Service Management ([ITSM](https://www.servicenow.com/products/itsm.html)) includes a variety of Ansible content to help automate the management of ServiceNow IT Service Management.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## Python version compatibility

This collection requires Python 2.7 or greater.

## Included content

<!--start collection content-->
### Modules
Name | Description
--- | ---
[servicenow.itsm.change_request](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.change_request_module.rst)|Manage ServiceNow change requests
[servicenow.itsm.change_request_info](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.change_request_info_module.rst)|List ServiceNow change requests
[servicenow.itsm.incident](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.incident_module.rst)|Manage ServiceNow incidents
[servicenow.itsm.incident_info](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.incident_info_module.rst)|List ServiceNow incidents
[servicenow.itsm.problem](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.problem_module.rst)|Manage ServiceNow problems
[servicenow.itsm.problem_info](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.problem_info_module.rst)|List ServiceNow problems

### Inventory plugins
Name | Description
--- | ---
[servicenow.itsm.servicenow.itsm.now](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.servicenow.itsm.now_inventory.rst)|Inventory source for ServiceNow table records.

<!--end collection content-->

## Installing this collection

You can install the ServiceNow ITSM collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install servicenow.itsm

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: servicenow.itsm
```

## Using this collection

You can either call modules by their Fully Qualified Collection Namespace (FQCN), such as `servicenow.itsm.incident_info`, or you can call modules by their short name if you list the `servicenow.itsm` collection in the playbook's `collections` keyword:

TODO: INCIDENT_INFO module example.


### See Also:

* [ServiceNow IT Service Management](https://www.servicenow.com/products/itsm.html)
* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.


## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [ServiceNow ITSM collection repository](https://github.com/ansible-collections/servicenow.itsm). See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for more details.

You can also join us on:

- Freenode IRC - ``#ansible-devel`` Freenode channel

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.


## Release notes
<!--Add a link to a changelog.rst file or an external docsite to cover this information. -->

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
