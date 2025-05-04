# Ansible Collection for ServiceNow ITSM

The Ansible Collection for ServiceNow IT Service Management ([ITSM](https://www.servicenow.com/products/itsm.html)) provides Ansible content that enables users to automate the management of ServiceNow ITSM processes such as incidents, change requests, service catalogs, configuration items, and more.

This collection is ideal for IT administrators, DevOps engineers, and automation specialists who work with ServiceNow and want to integrate its capabilities into their infrastructure automation workflows.

## Requirements

- **Ansible-Core**: >= 2.15.0
- **Python**: >= 3.9+
- No additional Python libraries or external Ansible collections are required.
- A ServiceNow instance and user credentials are required for module authentication.

## Installation

Install the collection from Ansible Galaxy using:

```bash
ansible-galaxy collection install servicenow.itsm
```

Or include it in a `requirements.yml` file:

```yaml
collections:
  - name: servicenow.itsm
```

To upgrade the collection to the latest version:

```bash
ansible-galaxy collection install servicenow.itsm --upgrade
```

To install a specific version:

```bash
ansible-galaxy collection install servicenow.itsm:==1.0.0
```

See the full guide on [using Ansible collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more.

## Use Cases

Here are a few common automation scenarios enabled by this collection:

1. **Incident Management**: Automatically create, update, and query incidents during CI/CD pipelines or event-driven automation.
2. **Change Management**: Trigger change requests and manage their lifecycle in coordination with deployment processes.
3. **Configuration Item (CI) Updates**: Automate the creation and update of CIs in CMDB during system provisioning.
4. **Service Catalog Integration**: Provision and manage items from the service catalog through Ansible playbooks.
5. **Attachment Handling**: Upload or retrieve documents from records to streamline workflows.

### Inventory Plugins

| Name | Description |
| ---- | ----------- |
| [servicenow.itsm.now](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.now_inventory.rst) | Inventory source for ServiceNow table records. |

### Modules

| Name | Description |
| ---- | ----------- |
| [api](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.api_module.rst) | Manage ServiceNow POST, PATCH and DELETE requests |
| [api_info](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.api_info_module.rst) | Manage ServiceNow GET requests |
| [attachment_info](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.attachment_info_module.rst) | Download attachment using sys_id |
| [attachment_upload](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.attachment_upload_module.rst) | Upload attachment to a table |
| [change_request](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.change_request_module.rst) | Manage ServiceNow change requests |
| [change_request_info](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.change_request_info_module.rst) | List ServiceNow change requests |
| [change_request_task](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.change_request_task_module.rst) | Manage change request tasks |
| [change_request_task_info](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.change_request_task_info_module.rst) | List change request tasks |
| [configuration_item](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.configuration_item_module.rst) | Manage configuration items |
| [configuration_item_batch](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.configuration_item_batch_module.rst) | Manage configuration items in batch |
| [configuration_item_info](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.configuration_item_info_module.rst) | List configuration items |
| [configuration_item_relations](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.configuration_item_relations_module.rst) | Manage CI relationships |
| [configuration_item_relations_info](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.configuration_item_relations_info_module.rst) | List CI relationships |
| [incident](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.incident_module.rst) | Manage incidents |
| [incident_info](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.incident_info_module.rst) | List incidents |
| [problem](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.problem_module.rst) | Manage problems |
| [problem_info](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.problem_info_module.rst) | List problems |
| [problem_task](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.problem_task_module.rst) | Manage problem tasks |
| [problem_task_info](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.problem_task_info_module.rst) | List problem tasks |
| [service_catalog](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.service_catalog_module.rst) | Manage service catalogs |
| [service_catalog_info](https://github.com/ansible-collections/servicenow.itsm/blob/main/docs/servicenow.itsm.service_catalog_info_module.rst) | List service catalogs |

## Example Usage

Using FQCN:

```yaml
- name: Retrieve incidents by number
  servicenow.itsm.incident_info:
    instance:
      host: https://dev12345.service-now.com
      username: user
      password: pass
    number: INC0000039
  register: result
```

With `collections` keyword:

```yaml
collections:
  - servicenow.itsm

tasks:
  - incident_info:
      instance:
        host: https://dev12345.service-now.com
        username: user
        password: pass
      number: INC0000039
    register: result
```

Using environment:

```yaml
---
- name: Test SNOW with blocks
  hosts: localhost
  become: false
  gather_facts: false
  vars:
    sn_host: https://hostname.example.com
    sn_username: username
    sn_password: password
  tasks:
    - name: Perform several ServiceNow tasks with the same credentials
      block:
        - name: Create test incident with attachment
          servicenow.itsm.incident:
            caller: admin
            state: new
            short_description: Test incident
            impact: low
            urgency: low
          register: test_incident
      environment:
        SN_HOST: "{{ sn_host }}"
        SN_USERNAME: "{{ sn_username }}"
        SN_PASSWORD: "{{ sn_password }}"

```

## Testing

This collection is tested with:
- Ansible-Core >= 2.15.0
- Python >= 3.9+
- Supported ServiceNow versions (Tokyo to Xanadu)

| Release | Status     | EOL            |
|--------:|------------|----------------|
| 2       | Maintained | TBA            |
| 1       | EOL        | September 2023 |

Known exceptions or compatibility issues will be tracked via the GitHub Issues page.

| ServiceNow Release | Collection Release |   EOL   |
| ------------------ | ------------------ | ------- |
| Yokohama           | 2.9.0+             |   TBA   |
| Xanadu             | 2.7.0+             |   TBA   |
| Washington DC      | 2.5.0+             |   TBA   |
| Vancouver          | 2.5.0 - 2.8.0      | Q2 2025 |
| Utah               | 2.1.0 - 2.8.0      | Q2 2025 |
| Tokyo              | 2.1.0 - 2.6.1      | Q2 2024 |

## Contributing

We welcome contributions! Open an issue or a pull request on the GitHub repository:  
https://github.com/ansible-collections/servicenow.itsm

Guidelines:
- https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections

Join us on:
- IRC: `#ansible-community` on [irc.libera.chat](https://libera.chat/)
- [Ansible Forum](https://forum.ansible.com/?extIdCarryOver=true&sc_cid=701f2000001OH7YAAW)

More: [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) and [Communication](https://docs.ansible.com/ansible/latest/community/communication.html)

## Support

Support is provided via:
- GitHub issues: https://github.com/ansible-collections/servicenow.itsm/issues
- Community channels listed above
- Maintained versions are clearly indicated in the release table

## Release Notes and Roadmap

- [CHANGELOG.rst](https://github.com/ansible-collections/servicenow.itsm/blob/main/CHANGELOG.rst)

### Publishing New Version

```bash
# Sync with upstream
git checkout main && git pull && git fetch upstream && git merge upstream/main

# Prepare release
ansible-playbook scripts/prepare_release.yml --extra-vars "version=$VERSION"

# Push and open PR
git push --set-upstream origin prepare_$VERSION_release

# After PR is merged
git checkout main && git pull && git fetch upstream && git merge upstream/main
git tag -s $VERSION
git push upstream $VERSION
```

## Related Information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [ServiceNow ITSM](https://www.servicenow.com/products/itsm.html)

## License Information

This collection is licensed under the GNU General Public License v3.0 or later.  
See: [https://www.gnu.org/licenses/gpl-3.0.txt](https://www.gnu.org/licenses/gpl-3.0.txt)