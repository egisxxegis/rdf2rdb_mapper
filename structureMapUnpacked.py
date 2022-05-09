from settings import Settings


class StructureMapUnpacked:
    def __init__(self, structure_map):
        self.uri_map_table = structure_map.uri_map_table
        self.uri_as_property_map_tables_arr = {}  # unused
        self.property_map_tables_arr = {}
        self.class_tables = []

        self.process_properties(structure_map.table_map_properties_arr)
        self.process_uri_map_tables(structure_map.uri_map_table)

    def process_properties(self, table_map_properties_arr: dict) -> None:
        to_return = {}

        for table, properties in table_map_properties_arr.items():
            for prop in properties:
                uri = prop["uri"]
                name = prop["name"]

                # is uri set?
                if uri != Settings.uriIfNotFound:
                    if self.uri_as_property_map_tables_arr.get(uri) is None:
                        self.uri_as_property_map_tables_arr[uri] = []
                    self.uri_as_property_map_tables_arr[uri].append(table)
                    continue

                # uri not set, so ...
                if to_return.get(name) is None:
                    to_return[name] = []
                to_return[name].append(table)
        self.property_map_tables_arr = to_return

    def process_uri_map_tables(self, uri_map_table: dict) -> None:
        for table in uri_map_table.values():
            self.class_tables.append(table)
