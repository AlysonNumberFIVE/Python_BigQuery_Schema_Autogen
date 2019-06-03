
# BigQuery Autogen Schema

This is a tool used to convert .JSON strings (inside JSON files) into acceptable Python BigQuery schema lists.

It's not completely full proof as support for key/value pairs in JSON files where the value is a whitespace delimited string fails to parse properly. Open to any patches (or I'll just patch it sometime).

### Example:
JSON input file
```
cat testcase/test.json
{"elements_0_role": "ADMINISTRATOR", "elements_0_roleAssignee": "urn:li:person:AFnCO-Sd9a", "elements_0_state": "APPROVED", "elements_0_organizationalTarget": "dotmodus", "paging_count": 10, "paging_start": 0, "fake_field": {"name": "Sephiroth", "age": 99}, "final_record": 42 }
```
Output :
```
python3 bigquery_schema_gen.py testcase/test.json
schema = [
            {
                "mode": "NULLABLE",
                "name": "elements_0_role",
                "type": "STRING"
            },
            {
                "mode": "NULLABLE",
                "name": "elements_0_roleAssignee",
                "type": "STRING"
            },
            {
                "mode": "NULLABLE",
                "name": "elements_0_state",
                "type": "STRING"
            },
            {
                "mode": "NULLABLE",
                "name": "elements_0_organizationalTarget",
                "type": "STRING"
            },
            {
                "mode": "NULLABLE",
                "name": "paging_count",
                "type": "INTEGER"
            },
            {
                "mode": "NULLABLE",
                "name": "paging_start",
                "type": "INTEGER"
            },
            {
                "mode": "REPEATED",
                "name": "fake_field",
                "type": "RECORD",
                "fields": [
                    {
                        "mode": "NULLABLE",
                        "name": "name",
                        "type": "STRING"
                    },
                    {
                        "mode": "NULLABLE",
                        "name": "age",
                        "type": "INTEGER"
                    },
                ]
            },
            {
                "mode": "NULLABLE",
                "name": "final_record",
                "type": "INTEGER"
            },
]
```
## Important
A lot of the parsing will be handled for basic fields, but the resulting Python schema must be looked over for inconsisencies.


- Brutally hacked together on a Friday afternoon by AlysonNgonyama



