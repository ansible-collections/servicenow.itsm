#!/bin/sh

set -e

teardown() {
    ansible-playbook teardown.yml
    rm -f "roles"
}

symlink_roles_path() {
    # ansible-test copies what it *thinks* the test needs to a temp working directory.
    # This causes issues since this test uses runme.sh instead of a psuedo ansible role
    # with a meta/main.yml for dependencies. So we hack out a symlink to the other test
    # targets. Then the playbooks can import setup_* roles without issue
    currentDir="$(pwd)"
    case "$(pwd)" in
        # running via ansible-test
        *"tests/output/.tmp/integration"*)
            rolesPath=${currentDir%"/output/.tmp/integration"*};
            rolesPath="$rolesPath/integration/targets"
            ;;
        # running some other way, likely calling ./runme.sh
        *)
            rolesPath="$currentDir/.."
            ;;
    esac
    ln -s "$rolesPath/" "roles"
}

export ANSIBLE_INVENTORY_ENABLED=servicenow.itsm.now
trap teardown EXIT

symlink_roles_path
ansible-playbook "setup.yml"

for test in tests/*.yml; do
    testName=${test#"tests/"}
    testName=${testName%".yml"}
    ansible-playbook \
        -i "test_session/inventories/$testName.now.yml" \
        -e "{\"test_name\":\"$testName\"}" \
        test.yml
done

teardown
