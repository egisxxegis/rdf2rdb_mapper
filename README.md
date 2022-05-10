# rdf2rdb_mapper
Extension to existing project: <br />
https://github.com/michaelbrunnbauer/rdf2rdb <br />

# Purpose
Generate mapping file (YAML) from database. <br />
It maps: <br />
&nbsp;&nbsp;class uri --> class table <br />
&nbsp;&nbsp;functional property --> class table <br />

# how-to
1. Configure settings.py file <br />
2. Make sure to satisfy requirements.txt
3. Launch main.py with Python 3.7

# Format
Program generates two files with different format styles: <br />
&nbsp;&nbsp;default format; <br />
&nbsp;&nbsp;unpacked format. <br />
Both format files are generated. Both contain same information.

[//]: # ## default format
[//]: # class table --> array of dictionaries of properties <br />
[//]: # &nbsp;&nbsp;as dictionary[classTable] = [{"name": propertyName, "uri": Settings.uriIfNotFound}, {...}, ...] <br />
[//]: #   <br />
[//]: # class uri --> class table <br />
[//]: # &nbsp;&nbsp;as dictionary[uri] = classTable <br />
[//]: # ## unpacked_default format
[//]: # list of class tables <br />
[//]: # &nbsp;&nbsp;as [classTable1, classTable2, ...] <br />
[//]: #   <br />
[//]: # functional property short name --> array of class tables (where is it used) <br />
[//]: # &nbsp;&nbsp;as dictionary[propertyName] = [classTable1, classTable2, ...] <br />
[//]: #   <br />
[//]: # functional property uri --> array of class tables (where is it used) <br />
[//]: # &nbsp;&nbsp;as *unused* and *not generated* <br />
[//]: #   <br />
[//]: # class uri --> class table <br />
[//]: # &nbsp;&nbsp;as dictionary[uri] = classTable <br />
