# adverity-json-parser
## Example
```
from adverity_json_parser import parser

DATASTREAM_ID = "1234"
INSTANCE_URL = "https://reprise.datatap.adverity.com/api/columns/"
TOKEN = "qwertyuiopasdfghjklzxcvbnmqwertyu"
JSON_PATH = "/Users/example/Documents/data-streams/table_schemas/general.json"
SCPECIAL_CHARS = ",().- %:!#&*§±+=" #Optional

instance = parser.Parser(DATASTREAM_ID, INSTANCE_URL, TOKEN, JSON_PATH)
instance.transform()
```