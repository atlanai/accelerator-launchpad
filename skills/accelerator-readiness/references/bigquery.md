# BigQuery: check, sign in, connect

## Contents
- Check: gcloud and bq
- Sign in from this session
- Check: BigQuery MCP server in the agent
- Connect: Google Cloud CLI (recommended)
- Connect: BigQuery remote MCP server (alternative)
- Errors you will see

## Check: gcloud and bq

```bash
gcloud --version
bq version
gcloud auth list --format="value(account,status)"
gcloud config get-value project
```

`auth list` prints the signed-in accounts and which is active; keep "signed in as the
user's work account" and the project id, not the full email list. No active account means
the sign-in is missing or expired: go to Sign in. No project set means `bq` cannot run; ask
the user which project holds the data and pass it with `--project_id`.

With a yes, one read-only statement:

```bash
bq query --use_legacy_sql=false --format=json --project_id=<project> 'select session_user() as user'
```

A JSON row back means verified; its `user` is the signed-in account, keep it for step 5. `bq` lives in the same SDK as `gcloud`; a missing `bq` with
a present `gcloud` means the component is not installed: `gcloud components install bq`.

## Sign in from this session

`gcloud auth login` opens a browser and waits for the callback; it needs no typed input, so
run it here after a yes, with a five-minute timeout:

```bash
gcloud auth login --update-adc
```

`--update-adc` also refreshes application-default credentials, which some MCP servers and
client libraries use. If the sandbox blocks the browser or the network, ask to run that one
command outside the sandbox; the fallback is the same command in the user's terminal. Do not
use `--no-launch-browser`: it asks for a code to be pasted, which only works in their
terminal. Then set the project if needed:

```bash
gcloud config set project <project-id>
```

Re-run the check.

## Check: BigQuery MCP server in the agent

A server in your tool list whose name contains `bigquery`. Ask, then run once:

```sql
select session_user() as user
```

Keep the user for step 5. Google's remote server is `https://bigquery.googleapis.com/mcp`, signed in with the user's
Google account through the agent (Claude Code `/mcp`; Codex `codex mcp login <name>`; Cursor
Settings, MCP). Listed but not callable means that sign-in is missing.

## Connect: Google Cloud CLI (recommended)

1. Install, in the user's terminal: macOS `brew install --cask google-cloud-sdk`; Windows the
   installer from cloud.google.com/sdk; Linux the package for their distribution. Verify with
   `gcloud --version`.
2. Sign in from here (section above), then `gcloud config set project <project-id>`.
3. Verify with the check statement. The user needs the BigQuery Job User role on the project
   and Data Viewer on the datasets; a `403` on the query means their admin grants those.

## Connect: BigQuery remote MCP server (alternative)

The BigQuery API must be enabled on the project. Add the server to the agent and sign in
when prompted:

| Agent | Command or file |
|---|---|
| Claude Code | `claude mcp add --transport http bigquery https://bigquery.googleapis.com/mcp` then `/mcp` to sign in |
| Codex | `codex mcp add bigquery --url https://bigquery.googleapis.com/mcp` then `codex mcp login bigquery` |
| Cursor | In `~/.cursor/mcp.json`: `{"mcpServers": {"bigquery": {"url": "https://bigquery.googleapis.com/mcp"}}}` |

## Errors you will see

| Error text | Meaning and fix |
|---|---|
| `You do not currently have an active account selected` | Not signed in. Sign in from here. |
| `Reauthentication required` or `invalid_grant` | The sign-in expired. `gcloud auth login --update-adc` again. |
| `No project ID was specified` or `project_id` missing | Set it: `gcloud config set project <id>`, or pass `--project_id`. |
| `Access Denied: ... bigquery.jobs.create` | Missing BigQuery Job User on the project. Their admin grants it. |
| `API has not been enabled` | Enable the BigQuery API on the project (admin, or the user if they own it). |
