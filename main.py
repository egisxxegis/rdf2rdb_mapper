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
    structureMap = structureMiner.get_structure_map()

    with open(Settings.outputFile, "w") as output:
        yaml.dump(structureMap, output)

    with open("unpacked_" + Settings.outputFile, "w") as output:
        yaml.dump(StructureMapUnpacked(structureMap), output)
