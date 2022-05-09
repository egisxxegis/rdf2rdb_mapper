import mysql.connector
from settings import Settings
from structureMap import StructureMap


class StructureMiner:
    def __init__(self, connector: mysql.connector):
        self.connector = connector

        self.dbName = connector.database
        self.dbNamePacked = self.pack_source(self.dbName)

        self.tableUris = Settings.tableUris
        self.tableUrisPacked = self.pack_source(self.tableUris)

        self.colUris = Settings.colUris
        self.colIdPrefix = Settings.colIdPrefix
        self.colIdSuffix = Settings.colIdSuffix
        self.colClass = Settings.colClass

        self.uriIfNotFound = Settings.uriIfNotFound

        self.tableNames = []
        self.classMapTable = {}
        self.tableMapPropertiesArr = {}

    def pack_source(self, source: str):
        return "`" + source.replace("`", "``") + "`"

    def get_all_table_names(self) -> [str]:
        cursor = self.connector.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = '"
                       + self.dbName + "'")
        result = cursor.fetchall()
        return [cols[0] for cols in result]

    def get_table_columns(self, table: str) -> [str]:
        cursor = self.connector.cursor()
        cursor.execute(f"SHOW COLUMNS FROM {self.dbNamePacked}.{self.pack_source(table)}")
        result = cursor.fetchall()
        return [cols[0] for cols in result]

    def get_first_row_uri(self, table: str) -> str:
        cursor = self.connector.cursor()
        cursor.execute(f"SELECT {self.colUris} FROM {self.pack_source(table)} LIMIT 1")
        result = cursor.fetchone()
        return result[0]

    def get_class_by_uri(self, uri: str) -> str:
        cursor = self.connector.cursor()
        cursor.execute(f"SELECT {self.colClass} FROM {self.tableUrisPacked} WHERE {self.colUris} = %s LIMIT 1", (uri,))
        result = cursor.fetchone()
        return result[0]

    def make_maps(self, tables: [str]) -> None:
        for table in tables:

            # skip table of uris
            if table == self.tableUris:
                continue

            # if table is of class1_property_class2 type, skip
            columns = self.get_table_columns(table)
            col_id = self.colIdPrefix + table + self.colIdSuffix
            if columns.count(self.colUris) != 1 or columns.count(col_id) != 1:
                continue

            # table to columns
            columns.remove(self.colUris)
            columns.remove(col_id)
            columns_arr = [{"name": col, "uri": self.uriIfNotFound} for col in columns]

            uri = self.get_first_row_uri(table)
            class_uri = self.get_class_by_uri(uri)

            self.classMapTable[class_uri] = table
            self.tableMapPropertiesArr[table] = columns_arr

    def process_structure(self):
        self.tableNames = self.get_all_table_names()
        if self.tableNames.count(self.tableUris) != 1:
            raise Exception("uris table not found")
        self.make_maps(self.tableNames)
        return

    def get_structure_map(self) -> StructureMap:
        if self.classMapTable == {} and self.tableMapPropertiesArr == {}:
            raise Exception("Maps not set. Are tables empty or method process_structure was not called?")
        return StructureMap(self.classMapTable, self.tableMapPropertiesArr)
