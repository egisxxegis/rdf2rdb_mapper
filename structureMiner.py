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
        self.tableLabels = Settings.tableLabels
        self.tableLabelsPacked = self.pack_source(self.tableLabels)

        self.colUris = Settings.colUris
        self.colIdPrefix = Settings.colIdPrefix
        self.colIdSuffix = Settings.colIdSuffix
        self.colClass = Settings.colClass

        self.uriIfNotFound = Settings.uriIfNotFound

        self.tableNames = []
        self.classMapTable = {}
        self.tableMapPropertiesArr = {}
        self.linkingTableMapObjectPropertiesDict = {}

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

    def get_uri_by_property(self, prop: str) -> str:
        cursor = self.connector.cursor()
        cursor.execute(f"SELECT {self.colUris} FROM {self.tableLabelsPacked} WHERE dblabel = %s LIMIT 2", (prop,))
        result = cursor.fetchall()
        if len(result) == 0:
            print(f"uri not found for property {prop}. Returning default uri")
            return self.uriIfNotFound
        if len(result) == 2:
            print(f"too many uris found for property {prop}. Returning default uri")
            return self.uriIfNotFound
        return result[0][0]

    def process_linking_table(self, table: str, columns: [str]) -> None:
        if len(columns) != 2:
            raise Exception(f"Unexpected table {table} encountered. Is it created not by a tool?")

        def extract_class_name(col_name: str) -> str:
            to_return = col_name[len(self.colIdPrefix):]  # no prefix
            to_return = to_return[0:-1 * (len(self.colIdSuffix) + 1)]  # no suffix and number (id2)
            return to_return

        # extract subject and object from columns
        table_subject = extract_class_name(columns[0])
        table_object = extract_class_name(columns[1])
        if str(columns[1]).endswith("1"):
            table_subject, table_object = table_object, table_subject

        # extract prop name from table name
        to_search = table_subject + "_"
        prop_name = table[len(to_search):]
        to_search = "_" + table_object
        prop_name = prop_name[0:prop_name.rindex(to_search)]

        self.linkingTableMapObjectPropertiesDict[table] = {
            "subject": table_subject,
            "predicate": prop_name,
            "predicate_uri": self.get_uri_by_property(prop_name),
            "object": table_object
        }

    def make_maps(self, tables: [str]) -> None:
        for table in tables:

            # skip table of uris
            if table == self.tableUris or table == self.tableLabels:
                continue

            # if table is of class1_property_class2 type, skip
            columns = self.get_table_columns(table)
            col_id = self.colIdPrefix + table + self.colIdSuffix
            if columns.count(self.colUris) != 1 or columns.count(col_id) != 1:
                self.process_linking_table(table, columns)
                continue

            # table to columns
            columns.remove(self.colUris)
            columns.remove(col_id)
            columns_arr = [{"name": col, "uri": self.get_uri_by_property(col)} for col in columns]

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
        return StructureMap(self.classMapTable, self.tableMapPropertiesArr, self.linkingTableMapObjectPropertiesDict)
