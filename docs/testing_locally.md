# Testing locally

While developing, it may be useful to run the integration or unit tests locally. Each test run is designed to be unique and non-destructive. Still, be aware that tests (integration tests primarily) can create and destroy resources in your environment.

### Setup

All tests required `ansible-test`, `ansible-galaxy`, `make`, and some container provider on your local machine (like podman).

Unit tests will require that you install the `coverage` python package in your current python environment.

If you run the integration tests, you will also need to configure authentication environment variables for your SNOW test instance. You can export the required variables like this:
```bash
export SN_HOST="https://foo.service-now.com"
export SN_USERNAME="my_user"
export SN_PASSWORD="SomeCrazyPassword"
export SN_CLIENT_ID="11111111111111111111111111111111111111111"
export SN_CLIENT_SECRET="SomeSecret"
```

Note that the `SN_CLIENT_ID` and `SN_CLIENT_SECRET` are required for the `api_authentication` and `inventory` tests. You can create an OAUTH provider as described in this [document](https://www.servicenow.com/community/developer-blog/up-your-oauth2-0-game-inbound-client-credentials-with-washington/ba-p/2816891).

### Running tests

Make sure your working directory is where ever you check the repository out. There should be a `galaxy.yml` and `Makefile` in your current directory, for example.

Then, simply run the following commands to test.

```bash
make sanity       # run sanity tests
make units        # run unit tests
make integration  # run integration tests
```

For unit and integration tests, you can optionally pass in a python version and/or test target name to modify the tests.

```bash
make units PYTHON_VERSION="3.12"   # test using python 3.12
make integration PYTHON_VERSION="3.12" TARGET="api_authentication"   # run only the api_authentication test, and test using python 3.12
```
