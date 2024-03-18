import pytest
import os
from pyway.helpers import Utils
from pyway.migration import Migration


@pytest.mark.helpers_test
def test_get_local_files() -> None:
    files = Utils.get_local_files(os.path.join('tests', 'data', 'schema'))
    assert len(files) == 3


@pytest.mark.helpers_test
def test_get_local_files_notfound() -> None:
    with pytest.raises(Exception):
        _ = Utils.get_local_files(os.path.join('tests', 'datanotfound'))
    assert True


@pytest.mark.helpers_test
def test_subtract_result() -> None:
    a = [Migration.from_name('V01_01__test1.sql', os.path.join('tests', 'data', 'schema')),
         Migration.from_name('V01_02__test2.sql', os.path.join('tests', 'data', 'schema'))]
    b = [Migration.from_name('V01_01__test1.sql', os.path.join('tests', 'data', 'schema'))]
    c = [Migration.from_name('V01_02__test2.sql', os.path.join('tests', 'data', 'schema'))]
    d = Utils.subtract(a, b)

    assert c[0].name == d[0].name


@pytest.mark.helpers_test
def test_subtract_noresult() -> None:
    a = [Migration.from_name('V01_01__test1.sql', os.path.join('tests', 'data', 'schema'))]
    b = [Migration.from_name('V01_01__test1.sql', os.path.join('tests', 'data', 'schema'))]
    c = Utils.subtract(a, b)

    assert c == []


@pytest.mark.helpers_test
def test_subtract_onlyonearray() -> None:
    a = [Migration.from_name('V01_01__test1.sql', os.path.join('tests', 'data', 'schema'))]
    b = []
    c = Utils.subtract(a, b)

    assert c == a


@pytest.mark.helpers_test
def test_expected_pattern() -> None:
    pattern = Utils.expected_pattern()
    assert pattern == "V{major}_{minor}__{description}.sql"


@pytest.mark.helpers_test
def test_get_version_from_name() -> None:
    with pytest.raises(Exception):
        _ = Utils.get_version_from_name("test1.sql")
    assert True


@pytest.mark.helpers_test
def test_load_checksum_from_name_failed() -> None:
    with pytest.raises(Exception):
        _ = Utils.load_checksum_from_name('test', 'test')
    assert True


@pytest.mark.helpers_test
def test_version_name() -> None:
    assert Utils.is_file_name_valid('V1_1__test1.sql')


@pytest.mark.helpers_test
def test_semantic_version_name() -> None:
    assert Utils.is_file_name_valid('V1_0_1__test1.sql')


@pytest.mark.helpers_test
def test_semantic_version_name_major_period() -> None:
    assert Utils.is_file_name_valid('V1.0_1__test1.sql')


@pytest.mark.helpers_test
def test_semantic_version_name_minor_period() -> None:
    assert Utils.is_file_name_valid('V1_0.1__test1.sql')


@pytest.mark.helpers_test
def test_semantic_version_name_major_minor_period() -> None:
    assert Utils.is_file_name_valid('V1.0.1__test1.sql')


@pytest.mark.helpers_test
def test_split_on_go_no_splits():
    with open(os.path.join('tests', 'data', 'sql_server_go_separator', '0_no_go_statement.sql')) as f:
        scripts = Utils.split_script_on_go(f.read())
        assert len(scripts) == 1
        assert scripts[0] == "SELECT * FROM table1;\n\nSELECT * FROM table2;"


@pytest.mark.helpers_test
def test_semantic_version_name_minor_over_2digits() -> None:
    assert Utils.is_file_name_valid('V1_0_100__test1.sql')


@pytest.mark.helpers_test
def test_get_two_statements():
    with open(os.path.join('tests', 'data', 'sql_server_go_separator', '1_two_statements.sql')) as f:
        scripts = Utils.split_script_on_go(f.read())
        assert len(scripts) == 2
        assert scripts[0] == "SELECT * FROM table1;"
        assert scripts[1] == "SELECT * FROM table2;"


@pytest.mark.helpers_test
def test_split_script_on_go_padding_variants():
   with open(os.path.join('tests', 'data', 'sql_server_go_separator', '2_go_padding_variants.sql')) as f:
      scripts = Utils.split_script_on_go(f.read())
      assert len(scripts) == 4
      assert scripts[0] == "SELECT * FROM table1;"
      assert scripts[1] == "SELECT * FROM table2;"
      assert scripts[2] == "SELECT * FROM table3;"
      assert scripts[3] == "SELECT * FROM table4;"


@pytest.mark.helpers_test
def test_split_script_on_go_repetitive_statements():
   with open(os.path.join('tests', 'data', 'sql_server_go_separator', '3_repetitive_go_statements.sql')) as f:
      scripts = Utils.split_script_on_go(f.read())
      assert len(scripts) == 5
      assert scripts[0] == "SELECT * FROM table1;"
      assert scripts[1] == "SELECT * FROM table1;"
      assert scripts[2] == "SELECT * FROM table2;"
      assert scripts[3] == "SELECT * FROM table2;"
      assert scripts[4] == "SELECT * FROM table2;"
