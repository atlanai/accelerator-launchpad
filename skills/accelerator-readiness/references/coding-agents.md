# Coding agents: what to look for

## Contents
- Which agent you are
- Agents to look for, with version commands
- Where each agent keeps MCP servers, and how to list names safely
- Classifying a server from its name

## Which agent you are

You know your own product. Say it plainly ("Claude Code 2.1", "Codex 0.154", "Cursor") and get
the version with the command in the table. Environment hints if you need them: Claude Code
sets `CLAUDECODE`; Codex sets `CODEX_THREAD_ID` and `CODEX_SANDBOX`; Cursor's agent sets
`CURSOR_AGENT`.

## Agents to look for

Run `which <binary>` for each, or `ls /Applications` on macOS (`dir "%LOCALAPPDATA%\Programs"`
on Windows). Note the version only for agents that are present.

| Agent | Binary | Version | macOS app |
|---|---|---|---|
| Claude Code | `claude` | `claude --version` | `Claude.app` (desktop app with the Code tab) |
| Codex | `codex` | `codex --version` | `Codex.app`, or inside `ChatGPT.app` |
| Cursor | `cursor-agent`, `cursor` | `cursor-agent --version` | `Cursor.app` |
| Windsurf | `windsurf` | `windsurf --version` | `Windsurf.app` |
| Gemini CLI | `gemini` | `gemini --version` | |
| GitHub Copilot CLI | `copilot` | `copilot --version` | |
| VS Code (Copilot, Cline) | `code` | `code --version` | `Visual Studio Code.app` |
| OpenCode | `opencode` | `opencode --version` | |
| Amp | `amp` | `amp --version` | |
| Kiro | `kiro` | | `Kiro.app` |
| Aider | `aider` | `aider --version` | |

## Where each agent keeps MCP servers

List **names only**. `claude mcp list` and `codex mcp list` print more than names (URLs,
commands, masked environment, paths): keep the name and the connection status, drop the rest.
The one-liners open the file only to print its top-level keys, which is allowed; what is not
allowed is reading or printing the file's contents (`cat`, `Read`, `jq .`), because the values
hold tokens. A missing file prints `no file`, which means no servers configured there.

| Agent | Safe listing command | File it reads (do not open) |
|---|---|---|
| Claude Code | `claude mcp list` (also shows connection status) | `~/.claude.json`, project `.mcp.json` |
| Codex | `codex mcp list` | `~/.codex/config.toml`, project `.codex/config.toml` |
| Cursor | `python3 -c "import json,os;p=os.path.expanduser('~/.cursor/mcp.json');print(sorted(json.load(open(p)).get('mcpServers',{})) if os.path.exists(p) else 'no file')"` | `~/.cursor/mcp.json`, project `.cursor/mcp.json` |
| Windsurf | same one-liner with `~/.codeium/windsurf/mcp_config.json` | that file |
| Gemini CLI | `gemini mcp list`, or the one-liner with `~/.gemini/settings.json` | `~/.gemini/settings.json` |
| GitHub Copilot CLI | the one-liner with `~/.copilot/mcp-config.json` | that file |
| VS Code | the one-liner with the user `mcp.json`, key `servers` (macOS `~/Library/Application Support/Code/User/mcp.json`) | that file, project `.vscode/mcp.json` |
| OpenCode | the one-liner with `~/.config/opencode/opencode.json`, key `mcp` | that file |
| Amp | the one-liner with `~/.config/amp/settings.json`, key `amp.mcpServers` | that file |
| Kiro | the one-liner with `~/.kiro/settings/mcp.json` | that file |
| Claude desktop app | the one-liner with `~/Library/Application Support/Claude/claude_desktop_config.json` | that file |

On Windows replace `~` with `%USERPROFILE%` and `~/Library/Application Support/Code/User` with
`%APPDATA%\Code\User`.

## Classifying a server from its name

| Name contains | Record as |
|---|---|
| `snowflake`, `snowflakecomputing`, `cortex` | Snowflake |
| `databricks`, `azuredatabricks`, `genie`, `unity` | Databricks |
| `bigquery`, `gcp`, `google-cloud` | BigQuery |
| `redshift` | Redshift |
| `postgres`, `pg`, `supabase`, `neon`, `clickhouse`, `fabric`, `mssql`, `trino`, `starburst`, `duckdb`, `motherduck` | other warehouse |
| `tableau`, `powerbi`, `power-bi`, `pbi`, `looker`, `metabase`, `sigma`, `thoughtspot`, `superset` | BI |
| `atlan` | Atlan |
| anything else | other |

The name is a hint, not proof. Your own tool list is the ground truth for what you can call
right now: a server configured in a file but absent from your tools is "configured, not
connected" and needs the user to sign in from their agent (`/mcp` in Claude Code,
`codex mcp login <name>` for Codex, Cursor Settings then MCP).
