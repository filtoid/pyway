import pytest
import os

from pyway.checksum import Checksum
from pyway.migrate import Migrate
from pyway.settings import ConfigFile

# from mysqld_integration_test import Mysqld
import pyodbc

class MsSql():
    def __init__(self, host, db_name, driver, username=None, password=None, port=1433):
        if host is None:
            raise ValueError("Host cannot be None")
        
        if db_name is None:
            raise ValueError("Database Name cannot be None")

        if driver is None:
            raise ValueError("Driver cannot be None")

        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password
        self.driver = driver

        self.__engine__ = None
        self.__conn__ = None

    def connect(self):
        if self.__conn__ is None:
            conn_str  = f"DRIVER={{{self.driver}}};SERVER={self.host},{self.port};" \
                        f"DATABASE={self.db_name};"
            if self.username is not None and self.password is not None:
                conn_str = f"{conn_str}UID={self.username};PWD={self.password};" \
                            "TrustServerCertificate=yes;"
            else:
                conn_str = f"{conn_str}Trusted_Connection=yes;" \
                            "TrustServerCertificate=yes;INTEGRATED " \
                            "SECURITY=yes;ENCRYPT=no;"
            self.__conn__ = pyodbc.connect(conn_str)
        return self.__conn__


@pytest.fixture
def mssql_connect(autouse: bool = True) -> MsSql:
    mssql = MsSql(host='mssql', db_name='PywayTests',  driver='ODBC Driver 18 for SQL Server', username='sa', password='p@ssw0rd!')
    return mssql.connect()


@pytest.mark.checksum_test
@pytest.mark.mssql_test
def test_pyway_table_checksum(mssql_connect: MsSql) -> None:
    config = ConfigFile()
    config.database_type = "mysql"
    config.database_host = mssql_connect.host
    config.database_username = mssql_connect.username
    config.database_password = mssql_connect.password
    config.database_port = mssql_connect.port
    config.database_name = 'test'
    config.database_table = 'pyway'
    config.database_migration_dir = os.path.join('tests', 'data', 'schema')
    config.checksum_file = "V01_01__test1.sql"

    # Add migration
    _ = Migrate(config).run()

    # Test once migration is complete
    name, checksum = Checksum(config).run()
    assert name == "V01_01__test1.sql"
    assert checksum == "8327AD7B"


# @pytest.mark.checksum_test
# @pytest.mark.mysqld_test
# def test_pyway_table_checksum_fileinvalid(mysqld_connect: Mysqld) -> None:
#     config = ConfigFile()
#     config.database_type = "mysql"
#     config.database_host = mysqld_connect.host
#     config.database_username = mysqld_connect.username
#     config.database_password = mysqld_connect.password
#     config.database_port = mysqld_connect.port
#     config.database_name = 'test'
#     config.database_table = 'pyway'
#     config.database_migration_dir = os.path.join('tests', 'data', 'schema')

#     # Add migration
#     _ = Migrate(config).run()

#     # Test once migration is complete
#     with pytest.raises(AttributeError):
#         _, _ = Checksum(config).run()

#     assert True


# @pytest.mark.checksum_test
# @pytest.mark.mysqld_test
# def test_pyway_table_checksum_fullpath(mysqld_connect: Mysqld) -> None:
#     config = ConfigFile()
#     config.database_type = "mysql"
#     config.database_host = mysqld_connect.host
#     config.database_username = mysqld_connect.username
#     config.database_password = mysqld_connect.password
#     config.database_port = mysqld_connect.port
#     config.database_name = 'test'
#     config.database_table = 'pyway'
#     config.database_migration_dir = os.path.join('tests', 'data', 'schema')
#     config.checksum_file = "schema/V01_01__test1.sql"

#     # Add migration
#     _ = Migrate(config).run()

#     # Test once migration is complete
#     name, checksum = Checksum(config).run()
#     assert name == "V01_01__test1.sql"
#     assert checksum == "8327AD7B"


# @pytest.mark.checksum_test
# @pytest.mark.mysqld_test
# def test_pyway_table_checksum_invalid_filename(mysqld_connect: Mysqld) -> None:
#     config = ConfigFile()
#     config.database_type = "mysql"
#     config.database_host = mysqld_connect.host
#     config.database_username = mysqld_connect.username
#     config.database_password = mysqld_connect.password
#     config.database_port = mysqld_connect.port
#     config.database_name = 'test'
#     config.database_table = 'pyway'
#     config.database_migration_dir = os.path.join('tests', 'data', 'schema')
#     config.checksum_file = "invalidfilename.sql"

#     # Add migration
#     _ = Migrate(config).run()

#     # Test once migration is complete
#     with pytest.raises(FileNotFoundError):
#         _, _ = Checksum(config).run()

#     assert True
