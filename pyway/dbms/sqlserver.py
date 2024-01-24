from pyway.migration import Migration
import pyodbc

CREATE_VERSION_MIGRATIONS = "if OBJECT_ID(N'%s', N'U') IS NULL " \
    "create table %s ("\
    "installed_rank int NOT NULL IDENTITY PRIMARY KEY,"\
    "version varchar(20) NOT NULL,"\
    "extension varchar(20) NOT NULL,"\
    "name varchar(125) NOT NULL,"\
    "checksum varchar(25) NOT NULL,"\
    "apply_timestamp datetime DEFAULT getutcdate()"\
    ");"
SELECT_FIELDS = ("version", "extension", "name", "checksum", "apply_timestamp")
ORDER_BY_FIELD_ASC = "installed_rank"
ORDER_BY_FIELD_DESC = "installed_rank desc"
INSERT_VERSION_MIGRATE = "insert into %s (version, extension, name, checksum) values ('%s', '%s', '%s', '%s');"
UPDATE_CHECKSUM = "update %s set checksum='%s' where version='%s';"

class Sqlserver():

    def __init__(self, config):
        self.config = config
        self.version_table = config.database_table
        self.create_version_table_if_not_exists()


    def connect(self):
        server_str = f"DRIVER={{{self.config.database_driver}}};" \
            f"SERVER={self.config.database_host};" \
            f"DATABASE={self.config.database_name};"
        
        if self.config.database_trusted_connection.lower() == 'yes':
            server_str = f"{server_str}MARS_Connection=yes;" \
                          "TrustServerCertificate=yes;INTEGRATED " \
                          "SECURITY=yes;ENCRYPT=no;"
        else:
            server_str = f"{server_str}" \
                         f"UID={self.config.database_username};" \
                         f"PWD={self.config.database_password};"
        
        return pyodbc.connect(server_str)
    
    
    def create_version_table_if_not_exists(self):
        self.execute(CREATE_VERSION_MIGRATIONS % (self.version_table, self.version_table))


    def execute(self, script):
        cnx = self.connect()
        with cnx.cursor() as cur:
            cur.execute(script)

        cnx.commit()
        cnx.close()


    def get_all_schema_migrations(self):
        cnx = self.connect()
        cursor = cnx.cursor()
        cursor.execute(f"SELECT {','.join(SELECT_FIELDS)} FROM {self.version_table} ORDER BY {ORDER_BY_FIELD_ASC}")
        migrations = []
        for row in cursor.fetchall():
            migrations.append(Migration(row[0], row[1], row[2], row[3], row[4]))
        cursor.close()
        cnx.close()
        return migrations


    def get_schema_migration(self, version):
        cnx = self.connect()
        cursor = cnx.cursor()
        cursor.execute(f"SELECT {','.join(SELECT_FIELDS)} FROM {self.version_table} WHERE version=%s", [version])
        row = cursor.fetchone()
        migration = Migration(row[0], row[1], row[2], row[3], row[4])
        cursor.close()
        cnx.close()
        return migration


    def upgrade_version(self, migration):
        self.execute(INSERT_VERSION_MIGRATE % (self.version_table, migration.version,
                                               migration.extension, migration.name,
                                               migration.checksum))


    def update_checksum(self, migration):
        self.execute(UPDATE_CHECKSUM % (self.version_table, migration.checksum, migration.version))

