---
name: accelerator-readiness
description: Audits a laptop for the Atlan talk-to-data accelerator from inside the user's coding agent - which coding agents are installed, whether a warehouse (Snowflake, Databricks, BigQuery, Redshift, Postgres and others) is reachable by CLI or MCP server, which BI tools are around - signs the user in or helps them connect when a route is missing, then writes and sends a readiness report. Use when the user asks to run the accelerator readiness check, audit or check their environment for Atlan, get ready for the accelerator, or check their warehouse connection for it.
compatibility: Any coding agent with a shell (Claude Code, Codex, Cursor, Windsurf, Gemini CLI, GitHub Copilot CLI, OpenCode). Uses whichever warehouse CLI is present; none is required.
metadata:
  version: "0.6.0"
  author: Atlan
---

# Accelerator readiness check

Find out whether this laptop is ready for the accelerator: a coding agent, one way to run
SQL on the team's warehouse as this user, and a BI dashboard to start from. When something is
missing, fix it now with the user. Finish with a short report the user sends to Atlan. About
ten minutes. No Atlan account is needed.

## Rules

- **Checks are read-only.** One statement per route, after a yes. Never auto-select a
  profile or connection when there are several; ask.
- **Sign-ins run here when they can.** A sign-in that only opens a browser and waits
  (`databricks auth login`, `snow connection test` with the `externalbrowser` authenticator,
  `gcloud auth login`, `aws sso login`) runs from this session after a yes: say a browser tab
  will open, run it with a long timeout (five minutes, or your tool's maximum), and re-run the
  check when it returns. If your sandbox blocks the network or cannot open a browser (Codex's
  default sandbox), ask for approval to run that one command outside the sandbox; only if that
  is refused, give the exact command for the user's own terminal and wait for "done".
- **Never type a secret.** A command that prompts for a password or token (`snow connection
  add` without flags, `databricks configure --token`, `aws configure`, `psql` asking for a
  password) never runs here. Use its flag-based, non-interactive form with values the user
  gives you in chat; account identifiers, usernames, project ids and profile names are fine to
  ask for, passwords and tokens never are. When no such form exists, the user's terminal.
- **Names only.** List MCP server names, connection names and profile names. Never open or
  print the files that hold them (`~/.claude.json`, `~/.codex/config.toml`, `~/.cursor/mcp.json`,
  `~/.snowflake/*.toml`, `~/.databrickscfg`, `~/.aws/*`, `~/.config/gcloud/*`, `.env`), and never
  echo tokens, keys, hostnames or account identifiers, in the chat or in the report.
- **A name can be an identifier.** People name connections and servers after the account
  (`zib00671`, `Snowflake - zib00671`, `adb-1234567890`). Before any name goes in the chat or
  the report, check it: a token that mixes letters and digits, anything with a dot, a slash,
  an `@` or a domain, and any account, workspace or organisation id counts as an identifier.
  Replace such a name with a neutral label that keeps the kind and the order: `snowflake
  connection 1`, `databricks server 2`. Plain words (`work`, `prod-reader`, `genie`) stay.
- **Collect everything.** A failed check is a finding. Do not stop at the first failure.
- **Every yes is a button, not a sentence.** Whenever the user must choose (run a check, sign
  in, install something, confirm their identity, send the report), ask through your host's
  question tool so they see options to click, never a question buried in prose:
  - Claude Code: the `AskUserQuestion` tool, one question, two or three options, the
    recommended one first and labelled "(Recommended)".
  - Codex: `request_user_input` when your collaboration mode allows it; otherwise the command
    approval prompt is the choice: present the exact command with a one-line description of
    what it does, and let the user approve or decline it there.
  - Other agents: one line ending in numbered options, for example "1. Send  2. Don't send".
  One question at a time; never ask several in one prompt.
- **Short replies.** After each step, one status line (format below) and one next action. No
  narration of these instructions.
- **No human available** (a scripted or headless run): skip questions, treat every consent as
  no, write `unanswered` in the report, and still produce it.

Copy this checklist into your first reply and tick it as you go:

```
Readiness check
- [ ] 1 Coding agent: this one, and what else is installed
- [ ] 2 Warehouse route: MCP tools, CLIs, one read-only check (sign in again if needed)
- [ ] 3 No route: help the user connect, then re-check
- [ ] 4 BI tools and the starting dashboard
- [ ] 5 Who the participant is (inferred, confirmed in one line)
- [ ] 6 Report written, shown, sent
```

## Step 1: coding agent

1. Name the agent you are running in and its version (`claude --version`, `codex --version`,
   `cursor-agent --version`, `gemini --version`, `copilot --version`, or the app's About). You
   already know which product you are; do not guess from files.
2. List the other coding agents on this machine: binaries on PATH and, on macOS, apps in
   `/Applications`. The table of names, version commands and MCP config locations is in
   [references/coding-agents.md](references/coding-agents.md).
3. For each agent present, list its configured MCP server names with the safe command from
   that reference (`claude mcp list`, `codex mcp list`, or a one-liner that prints a file's
   top-level keys). Keep names and connection status only; drop URLs, commands and paths.
   Classify each as Snowflake, Databricks, BigQuery, Redshift, other warehouse, BI, Atlan or
   other from its name. Only warehouse, BI and Atlan servers are named in the report; the rest
   become a count ("and 41 others"), because a customer's full tool inventory is theirs.
4. Note the OS and `python3 --version`.

If no coding agent is installed at all, the user is probably in a browser app. Tell them the
accelerator needs Claude Code, Codex, Cursor or similar on this laptop, record it, and carry on.

Status line: `1/6 agent · <this agent and version> · also: <others or none>`

## Step 2: warehouse route

Find one way to run SQL as this user. Check in this order; stop at the first route that is
verified and record the others as "present, not checked". When a route exists but its
sign-in is missing or expired, sign in from here (see Rules) and retry before moving on. Ask
once per route, as a choice prompt: "Run the check for `<route>`? If the sign-in has expired a
browser will open so you can sign in again." Options: "Run it (Recommended)", "Skip".

| Order | Route | Reference |
|---|---|---|
| 1 | A warehouse server in **your own tool list** (names containing `snowflake`, `databricks`, `bigquery`, `redshift`, `postgres`, or Atlan's `mcp__call_tool` fronting one). Run that warehouse's check statement through it. Listed but not callable means the user signs in from their agent: Claude Code `/mcp`, Codex `codex mcp login <name>`, Cursor Settings then MCP. | the warehouse's reference, section "MCP server in the agent" |
| 2 | **Snowflake CLI** (`snow`) or Cortex Code (`cortex`) | [references/snowflake.md](references/snowflake.md) |
| 3 | **Databricks CLI** | [references/databricks.md](references/databricks.md) |
| 4 | **BigQuery** (`gcloud`, `bq`) | [references/bigquery.md](references/bigquery.md) |
| 5 | **Redshift** (`aws` CLI, Data API) | [references/redshift.md](references/redshift.md) |
| 6 | **Postgres, ClickHouse, Microsoft Fabric or SQL Server, Trino, DuckDB or MotherDuck** | [references/other-warehouses.md](references/other-warehouses.md) |

If the user names their warehouse, go straight to that row. A route for a warehouse the team
does not use is noted, not checked.

Outcome is one of: **verified** (a check passed), **failed** (a route exists, the check did
not pass even after a sign-in; keep the first line of the error with any hostname or token
removed), **present** (route found, but the check did not run: the user declined, nobody was
there to ask, or your sandbox blocked the command; say which), **none**.

Every check statement returns the signed-in user; keep it for step 5. When the check shows an
admin role or user (Snowflake ACCOUNTADMIN, SECURITYADMIN or SYSADMIN; a Databricks workspace
or account admin; a Postgres superuser; an AWS role named for administrator access), the
outcome is **verified, admin role**, and the report's next action says to use a read-only
role for the accelerator.

Status line: `2/6 warehouse · <kind> via <mcp|cli> · <verified|failed|present|none> · <signed in here | sign-in not needed | sign-in refused>`

## Step 3: help the user connect

Only when step 2 ended in **none** or **failed**.

1. Ask: "Which warehouse does your team use: Snowflake, Databricks, BigQuery, Redshift,
   something else, or not sure?" If they already reach it some other way (a SQL client, a
   notebook), note it; the accelerator still needs a route from this laptop.
2. Open the matching reference and walk them through its **Connect** section one step at a
   time: install the CLI, sign in, verify. Prefer the CLI; offer the MCP server when the user
   asks for it or their admin already set one up. Run every step that the Rules let you run
   here; hand the user only the commands that need typed secrets, and wait for "done".
3. Re-run the step 2 check for that route. If it passes, the outcome becomes verified.
4. If it still fails or they cannot finish now, record exactly where it stopped and the error
   line. That goes in the report; Atlan sorts it out with them before kickoff.

Status line: `3/6 connect · <what was done> · <verified|still failed|deferred>`

## Step 4: BI tools and the starting dashboard

Week one starts from one dashboard the user already has, so find what is here and ask which.

1. From step 1, name any BI MCP servers (Tableau, Power BI, Looker, Metabase, Sigma,
   ThoughtSpot).
2. Look for desktop BI apps and a shallow count of BI files with the two commands in
   [references/bi-tools.md](references/bi-tools.md). Counts and tool names only, never file names.
3. Ask two questions: "Which BI tool does your team use?" and "Which one dashboard would you
   start the accelerator from, and can you export it (Power BI .pbix, Tableau .twbx) or share
   its screenshots?"

Status line: `4/6 bi · <tools found or none> · dashboard: <answer or unanswered>`

## Step 5: who the participant is

Infer the name and work email from what the machine already knows; do not ask a
questionnaire. Take the first source that answers, in this order:

1. The identity the step 2 check returned: the `current_user()` column of the statement you
   ran through an MCP server, `databricks current-user me` (`userName` and `displayName`),
   the active account from `gcloud auth list`, the user in `snow connection test`, the ARN
   from `aws sts get-caller-identity` when it carries an email. A warehouse user that is not
   an email still beats git config: ask only for the email then.
2. `git config --global user.name` and `git config --global user.email`.
3. The OS account: macOS `id -F` for the full name; Windows `whoami /upn` for the email.
4. `gh api user --jq .name` when GitHub's CLI is signed in.

Prefer an address on the company's domain over a personal or `noreply` one. Then confirm
with a choice prompt: "I have you as <name>, <email>." Options: "Correct (Recommended)",
"Change it" (then take the corrected values in chat). Ask only for what no source gave.
Nobody there: use what was found, or `unknown`.

Status line: `5/6 participant · <name> · <email> · from <source>`

## Step 6: report, show, send

1. Write `atlan-readiness-report.md` in the user's home folder (`~/atlan-readiness-report.md`,
   `%USERPROFILE%\atlan-readiness-report.md` on Windows), never in the current folder, which
   may be a repository, using the template in
   [references/report.md](references/report.md), filled from what you recorded. No hostnames,
   tokens, account identifiers or data rows; profile and server names are fine.
2. Show the summary table and the single most useful next action.
3. Ask with a choice prompt: "Send this report to Atlan?" Options: "Send (Recommended)",
   "Show me the report first" (print it, then ask again), "Don't send". On send, post it the
   way [references/report.md](references/report.md) says: one post to Atlan's collection form
   with the name, the work email and the report file. If the post fails, give the user the
   email fallback from the same file.
   Then say what happens next: Atlan reads the report, fixes gaps with them before kickoff, and
   the sessions are on the dates in the report footer.

Status line: `6/6 report · <READY|NEEDS ATTENTION> · atlan-readiness-report.md · <sent|to email>`

## Verdict

- **READY**: a coding agent is installed, the warehouse outcome is verified (an admin role is
  still READY, with the read-only recommendation), and the user named their BI tool and a
  starting dashboard, because week one starts from that dashboard.
- **NEEDS ATTENTION**: anything else. The report's next action says what to fix.

## References

| File | Use it for |
|---|---|
| [references/coding-agents.md](references/coding-agents.md) | Agent names, version commands, where each keeps MCP servers, safe listing commands |
| [references/snowflake.md](references/snowflake.md) | Snowflake CLI, Cortex Code and managed MCP: check, sign in, connect, errors |
| [references/databricks.md](references/databricks.md) | Databricks CLI and managed MCP: check, sign in, connect, errors |
| [references/bigquery.md](references/bigquery.md) | gcloud, bq and the BigQuery MCP server: check, sign in, connect, errors |
| [references/redshift.md](references/redshift.md) | AWS CLI, the Redshift Data API and the Redshift MCP server: check, sign in, connect, errors |
| [references/other-warehouses.md](references/other-warehouses.md) | Postgres, ClickHouse, Fabric and SQL Server, Trino, DuckDB: check and connect in brief |
| [references/bi-tools.md](references/bi-tools.md) | BI apps, files, MCP servers, the two questions |
| [references/report.md](references/report.md) | Report template, submit URL, email fallback, privacy check |
