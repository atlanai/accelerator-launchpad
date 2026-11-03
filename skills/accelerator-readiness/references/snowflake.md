# Snowflake: check and connect

## Contents
- Check: Snowflake CLI
- Check: Cortex Code CLI
- Check: Snowflake MCP server in the agent
- Connect: Snowflake CLI (recommended)
- Connect: managed MCP server (alternative)
- Errors you will see

## Check: Snowflake CLI

```bash
snow --version
snow connection list --format json
```

The JSON is a list of objects with `connection_name`, `parameters` and `is_default`. Keep
only the names and which one is default; the `parameters` object carries the account and
user, so never repeat it in chat or in the report. An empty list, or `snow` missing, means no
CLI route; go to Connect. If `snow` fails with `Unable to configure handler 'file'`, your
sandbox is blocking its log folder: ask the user to run the same command in their terminal and
paste the names.

With one connection, ask "Test the Snowflake connection `<name>` now? If it uses single
sign-on, a browser tab will open." With several, ask which. On yes, run it here with a
five-minute timeout; the browser sign-in is part of the test and needs no typed input:

```bash
snow connection test -c <name>
```

`Status: OK` with User, Role and Warehouse lines means verified; keep the user for step 5 and
record role and warehouse names, nothing else from that output. ACCOUNTADMIN, SECURITYADMIN or
SYSADMIN as the role makes it `verified, admin role`. Anything else is failed; keep the first error line with the
account hostname removed. If the sandbox blocks the browser or the network, ask to run that
one command outside the sandbox; the fallback is the same command in the user's terminal.
A connection that uses a password or a key pair needs no browser and tests the same way.

Connections live in `~/.snowflake/config.toml` (or `~/Library/Application Support/snowflake/`
on a Mac without that folder), with `connections.toml` beside it taking precedence. Do not
open either file.

## Check: Cortex Code CLI

Snowflake's own coding CLI shares the same connections file.

```bash
cortex --version
cortex connections list
```

A listed connection counts as a Snowflake CLI route. The check statement is the same
`snow connection test` if `snow` is also installed; otherwise record it as present.

## Check: Snowflake MCP server in the agent

A server in your tool list whose name contains `snowflake` or `cortex`, or Atlan's
`mcp__call_tool` fronting one. Ask, then run once:

```sql
select current_user(), current_role(), current_warehouse()
```

Keep the user for step 5. A role of ACCOUNTADMIN, SECURITYADMIN or SYSADMIN makes the
outcome `verified, admin role`; recommend a read-only role in the next action. Listed but not callable means the user has to sign in: Claude Code `/mcp` then the server then
Authenticate; Codex `codex mcp login <name>`; Cursor Settings, MCP, Sign in.

## Connect: Snowflake CLI (recommended)

Needs Python 3.10 or newer. One step at a time; wait for the user between steps.

1. Install, in the user's terminal:
   ```bash
   uv tool install snowflake-cli
   ```
   Alternatives: `brew install --cask snowflake-cli` (Homebrew asks for `brew trust` first), or
   `pip install snowflake-cli`. Verify with `snow --version`.
2. Add a connection from here. Ask the user for the account identifier (`<org>-<account>`,
   shown in Snowsight under the account menu) and their username; neither is a secret. With
   single sign-on no password is stored, so the non-interactive form works from this session:
   ```bash
   snow connection add --no-interactive --connection-name <name> --account <org-account> --user <username> --authenticator externalbrowser --default
   ```
   Add `--role`, `--warehouse`, `--database` and `--schema` when the user knows them. For a
   password-based account, add `--password` only if the user runs the command in their own
   terminal; never ask for the password in chat.
3. Verify from here (a browser tab opens for SSO):
   ```bash
   snow connection test -c <name>
   ```
   On macOS and Linux the config file must be owner-only; if the CLI complains, the user runs
   `chmod 0600` on the file it names.
4. Re-run the step 2 check.

## Connect: managed MCP server (alternative)

Their Snowflake admin creates the server and shares its URL, shaped like
`https://<account>.snowflakecomputing.com/api/v2/databases/<db>/schemas/<schema>/mcp-servers/<name>`;
it must expose a `SYSTEM_EXECUTE_SQL` tool so the agent can run SQL. The user adds it to the
agent they use, then signs in when prompted:

| Agent | Command or file |
|---|---|
| Claude Code | `claude mcp add --transport http snowflake <url>` then `/mcp` to sign in. With a programmatic access token instead of OAuth: add `--header "Authorization: Bearer <token>"` (the user types this; never ask for the token in chat). |
| Codex | `codex mcp add snowflake --url <url>` then `codex mcp login snowflake`. With a token: `--bearer-token-env-var SNOWFLAKE_PAT` and the user exports that variable. |
| Cursor | In `~/.cursor/mcp.json`: `{"mcpServers": {"snowflake": {"url": "<url>"}}}`, then Cursor Settings, MCP, Sign in. |
| Windsurf, Gemini CLI, Copilot CLI | The same JSON under `mcpServers` in that agent's MCP config file. |

## Errors you will see

| Error text | Meaning and fix |
|---|---|
| `Connection default is not configured` | No default connection. `snow connection set-default <name>` or pass `-c <name>`. |
| `250001` or `Incorrect username or password` | Wrong user or auth method. Re-add the connection; for SSO use `externalbrowser`. |
| `JWT token is invalid` | Key-pair auth with the wrong key or user. Use SSO instead for the accelerator. |
| `Network policy` or `IP ... is not allowed` | The account's network policy blocks this laptop or network. Their Snowflake admin must allow it. |
| Browser opens and nothing happens | SSO completed in a different browser profile. Rerun the test with the default browser. |
| `No module named` after `uv tool install` | Python below 3.10. Install 3.10 or newer, then reinstall. |
