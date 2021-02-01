# ServiceNow module template

ServiceNow Ansible Collection modules all have the same high-level structure.
To keep things consistent, use the following template when creating new
modules:

    #!/usr/bin/python
    # -*- coding: utf-8 -*-
    # Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
    #
    # GNU General Public License v3.0+
    # (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

    from __future__ import absolute_import, division, print_function
    __metaclass__ = type

    ANSIBLE_METADATA = {
        "metadata_version": "1.1",
        "status": ["stableinterface"],
        "supported_by": "certified",
    }

    DOCUMENTATION = """
    module: module_name
    author:
      - John Doe (@johndoe)
    short_description: A short description
    description:
      - Longer description that can contain more than one paragraph.
      - Links to relevant upstream sources should also go here. For example,
        like this: U(https://steampunk.si/).
    version_added: 1.0.0
    extends_documentation_fragment:
      - servicenow.itsm.fragment1
      - servicenow.itsm.fragment2
    seealso:
      - module: servicenow.itsm.module_name_info
    options:
      check:
        description:
          - The name of the check the entry should match.
          - If left empty a silencing entry will contain an asterisk in the
            check position.
        type: str
        required: true
    """

    EXAMPLES = """
    - name: Sample 1 (always use FQCN)
      servicenow.itsm.module_name:
        check: check-disk
    """

    RETURN = """
    response:
      description: API response
      returned: success
      type: dict
      sample:
        check: 123
    '''

    from ansible.module_utils.basic import AnsibleModule

    from ..module_utils import local_module


    # Add module-specific helpers here


    def run(module).
        # Main workhorse of the module. Add business logic here. Return back
        # changed indicator, API response (or mocked response in check mode),
        # and diff information.

        # In case of any kind of error, module should raise ServiceNow error
        # and set an appropriate error message that main method will return
        # back to the playbook user.

        return changed, response, dict(before=a, after=b)


    def main():
        # The first part of main method is dedicated to parsing and validating
        # module parameters.
        module = AnsibleModule(
            supports_check_mode=True,
            argument_spec=dict(
                check=dict(),
            # Other stuff here
        )
        # Any validation that does not require accessing remote also goes
        # here.

        # The second part is a wrapper around the run method that exits
        # gracefully on expected errors. Unexpected errors should be left
        # unhandled - stack trace is good in that case because we have a bug
        # somewhere.
        #
        # We should probably split this into a separate helper method, but
        # we will do that once we have more than two modules.
        try:
            changed, response, diff = run(module)
            module.exit_json(changed=changed, response=response, diff=diff)
        except errors.ServiceNowError as e:
            module.fail_json(msg=str(e))


    if __name__ == '__main__':
        main()

There are a few reasons for this kind of structure, but the main one is ease of
testing. Such structure minimizes the amount of mocking required when unit
testing modules, which is great news since we will unit test a lot once we fix
our API.
