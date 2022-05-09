import mysql.connector
from structureMiner import StructureMiner
from settings import Settings
from structureMapUnpacked import StructureMapUnpacked
import yaml

if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host=Settings.dbHost,
        user=Settings.dbUser,
        password=Settings.dbPassword,
        database=Settings.dbName
    )
    structureMiner = StructureMiner(mydb)
    structureMiner.process_structure()
    with open(Settings.outputFile, "w") as output:
        yaml.dump(structureMiner.get_structure_map(), output)

    with open("alt_" + Settings.outputFile, "w") as output:
        yaml.dump(StructureMapUnpacked(structureMiner.get_structure_map()), output)
