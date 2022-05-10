import yaml

from settings import Settings


class StructureMap(yaml.YAMLObject):
    yaml_tag = u'!StructureMap'

    def __init__(self, uri_map_table: dict, table_map_properties_arr: dict, table_map_object_properties_dict: dict):
        self.uri_map_table = uri_map_table
        self.table_map_properties_arr = table_map_properties_arr
        self.table_map_object_properties_dict = table_map_object_properties_dict

        self.meta = {
            "table_uris": Settings.tableUris,
            "col_uris": Settings.colUris,
            "col_id_prefix": Settings.colIdPrefix,
            "col_id_suffix": Settings.colIdSuffix,
            "uri_if_not_found": Settings.uriIfNotFound,
            "col_class": Settings.colClass
        }
