"""Read-only SQL on the yard: python yard/q.py "SELECT ..."  (tables are fixit.site.*, history is
fixit.account_usage.query_history and fixit.atlan.query_shapes). Prints columns and up to 50 rows as JSON."""
import json
import pathlib
import sys

import duckdb

DB = pathlib.Path(__file__).resolve().parent / "fixit.duckdb"
if not DB.exists():
    sys.exit("No yard yet: run python yard/load.py first.")
sql = sys.argv[1]
if not sql.lstrip().lower().startswith(("select", "with", "describe", "show")):
    sys.exit("Read-only: SELECT, WITH, DESCRIBE or SHOW only.")
cur = duckdb.connect(str(DB), read_only=True).execute(sql)
print(json.dumps({"columns": [d[0] for d in cur.description], "rows": cur.fetchmany(50)}, default=str))
