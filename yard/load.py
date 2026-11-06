"""Build the yard's DuckDB from its CSVs: python yard/load.py  (needs duckdb: pip install duckdb, or uv run --with duckdb).

Also loads the analysts' query history the way a warehouse keeps it: one row per run in
account_usage.query_history (Snowflake's column names), and the grouped atlan.query_shapes view
an admin would create for the Atlan plugin.
"""
import datetime
import hashlib
import json
import pathlib

import duckdb

HERE = pathlib.Path(__file__).resolve().parent
DB = HERE / "fixit.duckdb"
TABLES = ("projects", "crew", "work_logs", "material_orders", "site_snags")
# Who ran the queries: job titles in the yard office, not people.
USERS = ("YARD_OFFICE", "QUANTITY_SURVEYOR", "SITE_PLANNER", "BOOKKEEPER", "ESTIMATOR")
START = datetime.datetime(2026, 7, 1, 8, 0)  # history spans 1 July to 31 October 2026


def pick(*key) -> int:
    """A stable number from a key, so every rebuild gives the same history."""
    return int(hashlib.sha256(repr(key).encode()).hexdigest()[:12], 16)


def history_rows():
    """Expand each {sql, exec, users} line into exec runs by exactly `users` distinct users."""
    for i, line in enumerate((HERE / "history" / "querylog.jsonl").open()):
        q = json.loads(line)
        who = [USERS[(pick("user", i) + k) % len(USERS)] for k in range(q["users"])]
        for run in range(q["exec"]):
            start = START + datetime.timedelta(days=pick("day", i, run) % 123, hours=pick("hour", i, run) % 10,
                                               seconds=pick("sec", i, run) % 3600)
            elapsed_ms = 120 + pick("ms", i, run) % 2900
            yield (f"01b{pick('id', i, run):012x}", q["sql"], "FIXIT", "SITE", "SELECT", who[run % len(who)],
                   "ANALYST", "YARD_WH", "SUCCESS", start, start + datetime.timedelta(milliseconds=elapsed_ms), elapsed_ms)


if DB.exists():
    DB.unlink()
con = duckdb.connect(str(DB))
con.execute("CREATE SCHEMA site")
for t in TABLES:
    con.execute(f"CREATE TABLE site.{t} AS SELECT * FROM read_csv_auto(?, header = true)", [str(HERE / "data" / f"{t}.csv")])
    print(f"site.{t}: {con.execute(f'SELECT COUNT(*) FROM site.{t}').fetchone()[0]} rows")

con.execute("CREATE SCHEMA account_usage")
con.execute("""CREATE TABLE account_usage.query_history (
    query_id VARCHAR, query_text VARCHAR, database_name VARCHAR, schema_name VARCHAR, query_type VARCHAR,
    user_name VARCHAR, role_name VARCHAR, warehouse_name VARCHAR, execution_status VARCHAR,
    start_time TIMESTAMP, end_time TIMESTAMP, total_elapsed_time BIGINT)""")
con.executemany("INSERT INTO account_usage.query_history VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", list(history_rows()))
print(f"account_usage.query_history: {con.execute('SELECT COUNT(*) FROM account_usage.query_history').fetchone()[0]} runs")

# The same grouping as the plugin's one-time admin view, without a rolling window: the yard's history is fixed.
con.execute("CREATE SCHEMA atlan")
con.execute("""CREATE VIEW atlan.query_shapes AS
    SELECT query_text AS sql, COUNT(*) AS exec, COUNT(DISTINCT user_name) AS users, MAX(start_time) AS last_run
    FROM account_usage.query_history
    WHERE execution_status = 'SUCCESS' AND query_type = 'SELECT' AND database_name = 'FIXIT'
    GROUP BY query_text""")
print(f"atlan.query_shapes: {con.execute('SELECT COUNT(*) FROM atlan.query_shapes').fetchone()[0]} statements")
con.close()
print(f"built {DB.relative_to(HERE.parent)}")
