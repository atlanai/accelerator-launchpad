# Databricks: check and connect

## Contents
- Check: Databricks CLI
- Check: Databricks MCP server in the agent
- Connect: Databricks CLI (recommended)
- Connect: managed MCP server (alternative)
- Errors you will see

## Check: Databricks CLI

```bash
databricks version
databricks auth profiles --skip-validate
```

`auth profiles` lists each profile with its host; `--skip-validate` keeps this step offline
(validation is a network call, and that belongs to the check below, after a yes). Keep the
Name column only, never the Host column. The first line of `databricks version` may be a note about
installing Databricks skills; ignore it. No profiles, or the CLI missing, means no CLI route;
go to Connect. `DATABRICKS_HOST` with `DATABRICKS_TOKEN` in the environment also counts as a
profile called `environment`; note that they are set, never their values.

With one profile, ask "Use the Databricks profile `<name>` for the check?" With several, ask
which; never pick for the user. Then prove the sign-in with the one call that does:

```bash
databricks current-user me --profile <name>
```

It returns the signed-in user. If it fails with an expired or invalid token, sign in from
here (next section) and run it again. Then, with a yes, one read-only statement:

```bash
databricks experimental aitools tools query "select 1 as ok" --profile <name>
```

A row back means verified. If that subcommand is missing (older CLI), use
`databricks warehouses list --profile <name>` to find a warehouse id and run
`databricks api post /api/2.0/sql/statements --json '{"warehouse_id":"<id>","statement":"select 1","wait_timeout":"30s"}' --profile <name>`;
`status.state` of `SUCCEEDED` is verified, `PENDING` means the warehouse is starting and the
access itself works. No SQL warehouse visible to the user is a finding: "signed in, no SQL
warehouse", and their admin needs to grant one.

Each command is a separate shell: always pass `--profile <name>`; an exported
`DATABRICKS_CONFIG_PROFILE` does not carry over.

## Sign in from this session

`databricks auth login` opens a browser and waits (up to an hour by default) for the user to
finish; it needs no typed input, so run it here after a yes, with a five-minute timeout. For
an existing profile the host is already stored:

```bash
databricks auth login --profile <name> --timeout 5m
```

For a new profile add `--host https://<workspace-url>`; without a known URL, plain
`databricks auth login --profile <name>` opens login.databricks.com to pick a workspace. If the
sandbox blocks the browser or the network, ask to run that one command outside the sandbox;
the fallback is the same command in the user's terminal, then "done". A personal access
token path (`databricks configure --token`) prompts for the token, so that one is always the
user's terminal. Re-run `current-user me` afterwards.

## Check: Databricks MCP server in the agent

A server in your tool list whose name contains `databricks` or `genie`. Ask, then run once:

```sql
select current_catalog(), current_schema()
```

Listed but not callable means the user has to sign in from their agent (Claude Code `/mcp`;
Codex `codex mcp login <name>`; Cursor Settings, MCP).

## Connect: Databricks CLI (recommended)

One step at a time; wait for the user between steps.

1. Install, in the user's terminal:
   - macOS: `brew install databricks/tap/databricks` (Homebrew 6 asks for `brew trust databricks/tap` first)
   - Windows: `winget install Databricks.DatabricksCLI`
   - Linux: Databricks' own installer, `curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh`
     (the user runs it; never pipe a download into a shell yourself)

   Verify with `databricks version`.
2. Sign in from here (section above):
   ```bash
   databricks auth login --host https://<workspace-url> --profile <name> --timeout 5m
   ```
   URLs copied from the browser may carry `?w=...`; quote them. A personal access token works
   too, in the user's terminal: `databricks configure --token --profile <name>`.
3. Verify:
   ```bash
   databricks auth profiles
   databricks current-user me --profile <name>
   databricks warehouses list --profile <name>
   ```
   The last one must show at least one SQL warehouse the user can use.
4. Re-run the step 2 check.

Profiles are stored in `~/.databrickscfg`; browser tokens go to the OS keychain. Do not open
the file. Optional, not needed for the accelerator: `databricks aitools install` adds
Databricks' own skills to the user's coding agents.

## Connect: managed MCP server (alternative)

Their workspace admin enables **Managed MCP Servers** on the workspace Previews page first.
The SQL server is `https://<workspace-url>/api/2.0/mcp/sql`; a Genie space is
`https://<workspace-url>/api/2.0/mcp/genie/<space-id>`. Databricks also ships the Unity
Gateway CLI (`ug claude`, `ug codex`, `ug cursor`, `ug copilot`, `ug gemini`) that configures the
agent in one command; see "Connect MCPs to coding agents" on docs.databricks.com.

| Agent | By hand |
|---|---|
| Claude Code | `claude mcp add --transport http databricks-sql https://<workspace-url>/api/2.0/mcp/sql` then `/mcp` to sign in |
| Codex | `codex mcp add databricks-sql --url https://<workspace-url>/api/2.0/mcp/sql` then `codex mcp login databricks-sql` |
| Cursor | In `~/.cursor/mcp.json`: `{"mcpServers": {"databricks-sql": {"url": "https://<workspace-url>/api/2.0/mcp/sql"}}}` |

## Errors you will see

| Error text | Meaning and fix |
|---|---|
| `cannot configure default credentials` | No profile passed and no default. Add `--profile <name>`. |
| `refresh token is invalid` or `A new access token could not be retrieved` | The sign-in expired. Run `databricks auth login --profile <name> --timeout 5m` from here; a browser tab opens. |
| `configuration does not support OAuth tokens` | The profile uses a token where OAuth is required. Re-sign in with `auth login`. |
| `PERMISSION_DENIED` on `warehouses list` or the query | Signed in, but no SQL warehouse or no catalog access. Their workspace admin grants it. |
| `Managed MCP Servers` 404 or OAuth discovery 404 | The preview is not enabled on the workspace. Admin enables it; use the CLI meanwhile. |
