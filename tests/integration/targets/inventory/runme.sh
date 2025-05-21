#!/bin/sh

set -e
export ANSIBLE_INVENTORY_ENABLED=servicenow.itsm.now

teardown() {
    ansible-playbook teardown.yml
    rm -f ./roles
}

trap teardown ERR

ln -s ../ roles
ansible-playbook setup.yml

for test in tests/*.yml; do
    testName=${test#"tests/"}
    testName=${testName%".yml"}
    ansible-playbook \
        -i test_session/inventories/$testName.now.yml \
        -e "{\"test_name\":\"$testName\"}" \
        test.yml
done

teardown
