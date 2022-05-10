class Settings(object):
    dbHost = 'localhost'
    dbName = 'sp2b_rdf2rdb_clean'
    dbUser = 'root'
    dbPassword = ''

    outputFile = f"map_{dbName}.yaml"

    tableUris = "uris"
    tableLabels = "labels"

    colUris = "uri"
    colClass = "class"
    colIdPrefix = ""
    colIdSuffix = "_id"

    uriIfNotFound = " "
