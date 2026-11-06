"""Build the yard's DuckDB from its CSVs: python yard/load.py  (needs duckdb: pip install duckdb, or uv run --with duckdb)."""
import pathlib

import duckdb

HERE = pathlib.Path(__file__).resolve().parent
DB = HERE / "fixit.duckdb"
TABLES = ("projects", "crew", "work_logs", "material_orders", "site_snags")

if DB.exists():
    DB.unlink()
con = duckdb.connect(str(DB))
con.execute("CREATE SCHEMA site")
for t in TABLES:
    con.execute(f"CREATE TABLE site.{t} AS SELECT * FROM read_csv_auto(?, header = true)", [str(HERE / "data" / f"{t}.csv")])
    print(f"site.{t}: {con.execute(f'SELECT COUNT(*) FROM site.{t}').fetchone()[0]} rows")
con.close()
print(f"built {DB.relative_to(HERE.parent)}")
