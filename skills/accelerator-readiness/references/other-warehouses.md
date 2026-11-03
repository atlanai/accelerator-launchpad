# Other warehouses: check and connect in brief

## Contents
- Postgres and Postgres-compatible (Aurora, Supabase, Neon, AlloyDB)
- ClickHouse
- Microsoft Fabric and SQL Server
- Trino and Starburst
- DuckDB and MotherDuck
- Anything else

Each row follows the same shape as the main references: a presence check, a sign-in that
can or cannot run here, one read-only statement. Passwords are never typed by you; a route
that needs one uses a file the user writes (`~/.pgpass`, a connection string in their shell)
or runs in their terminal.

## Postgres and Postgres-compatible

- Present: `psql --version`.
- Sign in: a password in `~/.pgpass` (the user writes it: `host:port:db:user:password`, mode
  `0600`), or `PGPASSWORD` exported in their shell before they start the agent. No browser
  flow exists, so nothing to run here.
- Check, with a yes: `psql "host=<host> port=5432 dbname=<db> user=<user> sslmode=require" -Atc "select current_user, current_setting('is_superuser')"`.
  A user back means verified; `on` in the second column is a superuser, so `verified, admin role`. A password prompt means `.pgpass` is missing or does not match;
  hand the command to the user's terminal.
- MCP: a server named `postgres` in the agent, usually configured with a connection URL that
  holds the password; never read that config. Run `select current_user` through it.

## ClickHouse

- Present: `clickhouse --version` or `clickhouse-client --version`.
- Sign in: host, user and password as flags or in `~/.clickhouse-client/config.xml`; the
  password part is the user's, in their terminal.
- Check: `clickhouse-client --host <host> --secure --user <user> --query "select currentUser()"` (ClickHouse
  Cloud needs `--secure`). MCP: the `mcp-clickhouse` server, same statement through it.

## Microsoft Fabric and SQL Server

- Present: `sqlcmd --version` (the Go `sqlcmd`), `az --version`.
- Sign in from here: `az login` opens a browser and waits; run it after a yes with a
  five-minute timeout. Then `sqlcmd -S <server> -d <database> --authentication-method ActiveDirectoryAzCli -Q "select suser_sname()"`.
- Check: the `sqlcmd` line above. A Fabric SQL endpoint takes the same form.

## Trino and Starburst

- Present: `trino --version`.
- Sign in: `trino --server https://<host> --user <user> --external-authentication` opens a
  browser; it can run here. Password auth (`--password`) prompts, so that one is the user's
  terminal.
- Check: add `--execute "select current_user"` to the sign-in line.

## DuckDB and MotherDuck

- Present: `duckdb --version`.
- A local DuckDB file needs no sign-in: `duckdb <file> "select 1"`. MotherDuck signs in with a
  token in `motherduck_token`, set by the user in their shell, then `duckdb md: "select 1"`.
- Useful as the week-one route when the team's warehouse is not reachable yet and they have
  a BI export or a CSV: not a blocker, say so in the report.

## Anything else

Record the warehouse name and how the user reaches it today, run `select current_user` (or that engine's equivalent) through whatever
tool they already use if it is in your tool list, and mark the route as "other warehouse, not
a blocker". Atlan brings the right connector to the one-on-one.
