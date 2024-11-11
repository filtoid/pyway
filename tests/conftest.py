import pytest 

# Taken from https://stackoverflow.com/a/42145604 
def pytest_addoption(parser):
    parser.addoption("--skip-mysqld-tests", action="store", default="False")
    parser.addoption("--skip-postgres-tests", action="store", default="False")


# This is called for every test. Only get/set command line arguments
# if the argument is specified in the list of test "fixturenames".
def pytest_collection_modifyitems(config, items):
    if config.getoption("--skip-mysqld-tests") and config.getoption("--skip-mysqld-tests").lower() == "true":
        skip_mysqld = pytest.mark.skip(reason="skipped due to mysqld requirement")
        for item in items:
            if "mysqld_test" in item.keywords:
                item.add_marker(skip_mysqld)

    if config.getoption("--skip-postgres-tests") and config.getoption("--skip-postgres-tests").lower() == "true":
        skip_postgres = pytest.mark.skip(reason="skipped due to postgres requirement")
        for item in items:
            if "postgresql_test" in item.keywords:
                item.add_marker(skip_postgres)
