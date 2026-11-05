# The builder's yard

A small, made-up building firm to practise on before you build on your own data. You take the
same steps as week one: start from a dashboard, generate metrics and evals, run your agent, and
see the score.

## The firm

Fixit & Co. has ten jobs from July to October 2026: a pergola, a barn, a skate park, a cat flap,
and one very expensive wind turbine base. Rob runs the yard, Wanda does the building, and Sprout
"helps". The machines are crew too, and they bill by the hour: Dig digs, Tipper hauls, Whirl
mixes, Flatt rolls and Lanky lifts. Kipper the cat isn't crew, but turns up in the snag log more
than anyone would like.

## Set up (2 minutes)

In your coding agent, from the repository root:

```text
Set up the builder's yard and show me its dashboard
```

Or by hand:

```bash
pip install duckdb        # or prefix each command with: uv run --with duckdb
python yard/load.py
python yard/q.py "SELECT crew_name, catchphrase FROM fixit.site.crew"
```

## Build an agent on it

The dashboard is a Power BI report saved as files in `yard/powerbi`, so no Power BI account is
needed. With the Atlan analytics plugin installed:

```text
Convert this Power BI report to an agent: yard/powerbi
The warehouse is yard/fixit.duckdb (run SQL with python yard/q.py),
and the query history is yard/history/querylog.jsonl.
```

The plugin turns the dashboard's four tiles into metrics, writes eval questions, registers your
agent and runs a baseline.

## The question to finish on

**Which job ate our margin last quarter, and what ate it?**

## What's in the yard

| Table | Rows | One row is |
|---|---|---|
| `site.projects` | 10 | a job |
| `site.crew` | 8 | a person or a machine |
| `site.work_logs` | 746 | one crew member, one job, one day, one task |
| `site.material_orders` | 51 | an order |
| `site.site_snags` | 11 | something that went wrong |

The dashboard, *Fix It First Time: Site Performance*, has four tiles: gross margin, rework cost,
material waste and late jobs. Its model is in `powerbi/definition` (`model.tmdl`, `report.json`),
and `powerbi/rowsets.json` holds the SQL each table is built from. The 110 queries in
`history/querylog.jsonl` are what the yard's analysts ran.
