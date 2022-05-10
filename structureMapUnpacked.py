from settings import Settings


class StructureMapUnpacked:
    def __init__(self, structure_map):
        self.uri_map_table = structure_map.uri_map_table
        self.uri_map_property = {}
        self.property_map_tables_arr = {}
        self.class_tables = []
        self.linking_tables_arr_dict = []

        self.meta = structure_map.meta

        self.process_properties(structure_map.table_map_properties_arr)
        self.process_uri_map_tables(structure_map.uri_map_table)
        self.process_linking_tables(structure_map.table_map_object_properties_dict)

    def process_properties(self, table_map_properties_arr: dict) -> None:
        to_return = {}

        for table, properties in table_map_properties_arr.items():
            for prop in properties:
                uri = prop["uri"]
                name = prop["name"]

                # is uri set?
                if uri != Settings.uriIfNotFound:
                    self.uri_map_property[uri] = name

                if to_return.get(name) is None:
                    to_return[name] = []
                to_return[name].append(table)
        self.property_map_tables_arr = to_return

    def process_uri_map_tables(self, uri_map_table: dict) -> None:
        for table in uri_map_table.values():
            self.class_tables.append(table)

    def process_linking_tables(self, table_map_object_properties_dict: dict) -> None:
        for linking_table, spo_dict in table_map_object_properties_dict.items():
            self.linking_tables_arr_dict.append({
                "subject": spo_dict["subject"],
                "predicate": spo_dict["predicate"],
                "object": spo_dict["object"],
                "table": linking_table
            })
            if spo_dict["predicate_uri"] != Settings.uriIfNotFound:
                self.uri_map_property[spo_dict["predicate_uri"]] = spo_dict["predicate"]
