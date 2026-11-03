# Amazon Redshift: check, sign in, connect

## Contents
- Check: AWS CLI and the Redshift Data API
- Sign in from this session
- Check: Redshift MCP server in the agent
- Connect: AWS CLI (recommended)
- Connect: Redshift MCP server (alternative)
- Errors you will see

## Check: AWS CLI and the Redshift Data API

The Data API runs SQL over HTTPS with the user's AWS identity, so no database password is
needed. It needs the Redshift Data API permissions on the user's role.

```bash
aws --version
aws configure list-profiles
aws sts get-caller-identity --profile <profile> --query Arn --output text
```

`list-profiles` prints profile names; with one profile confirm it, with several ask. The
`get-caller-identity` call proves the sign-in; keep "signed in" and the role name, never the
account number. An expired SSO session fails here: go to Sign in.

With a yes, one read-only statement. Serverless workgroup:

```bash
aws redshift-data execute-statement --profile <profile> --workgroup-name <workgroup> --database <db> --sql "select 1 as ok" --query Id --output text
```

Provisioned cluster, temporary credentials for the user's database identity:

```bash
aws redshift-data execute-statement --profile <profile> --cluster-identifier <cluster> --database <db> --sql "select 1 as ok" --query Id --output text
```

Then, with the returned id:

```bash
aws redshift-data describe-statement --profile <profile> --id <id> --query Status --output text
aws redshift-data get-statement-result --profile <profile> --id <id> --query 'Records[0]' --output text
```

`FINISHED` with a row means verified. Ask the user for the workgroup or cluster name and the
database; these are not secrets. If they only know the host from a SQL client, the workgroup
or cluster is the first label of that host.

## Sign in from this session

With an SSO profile, `aws sso login` opens a browser and waits; run it here after a yes,
with a five-minute timeout:

```bash
aws sso login --profile <profile>
```

If the sandbox blocks the browser or the network, ask to run that one command outside the
sandbox; the fallback is the same command in the user's terminal. Profiles with long-lived
access keys never expire this way; if `get-caller-identity` fails for one, the keys are wrong
or revoked, and only the user's terminal (`aws configure --profile <profile>`) can fix it,
because it asks for the secret key.

## Check: Redshift MCP server in the agent

A server in your tool list whose name contains `redshift`. Ask, then run once:

```sql
select 1 as ok
```

AWS's own server is `awslabs.redshift-mcp-server`, started with `uvx` and the user's AWS
profile; it runs as the database user tied to their IAM identity. Listed but not callable
usually means the AWS session behind it expired: sign in as above and restart the agent.

## Connect: AWS CLI (recommended)

1. Install, in the user's terminal: macOS `brew install awscli`; Windows
   `winget install Amazon.AWSCLI`; Linux the AWS installer. Verify with `aws --version`.
2. Create an SSO profile. This prompts, so the user runs it themselves:
   ```bash
   aws configure sso --profile <name>
   ```
   They need their SSO start URL and region (from their AWS access portal). Then sign in from
   here with `aws sso login --profile <name>`.
3. Verify with `get-caller-identity`, then the Data API check. The user's role needs
   `redshift-data:ExecuteStatement`, `DescribeStatement` and `GetStatementResult`, and for a
   provisioned cluster `redshift:GetClusterCredentialsWithIAM`; a `403` or
   `AccessDeniedException` means their admin grants those.

A direct `psql` connection with a database password is a second-best route: it works, but
the password has to be typed in the user's terminal (or stored in `~/.pgpass`), and the agent
should never see it. See [other-warehouses.md](other-warehouses.md) for the `psql` check.

## Connect: Redshift MCP server (alternative)

AWS publishes the server; the agent runs it locally with the user's profile:

| Agent | Command or file |
|---|---|
| Claude Code | `claude mcp add redshift --env AWS_PROFILE=<profile> --env AWS_REGION=<region> -- uvx awslabs.redshift-mcp-server@latest` |
| Codex | `codex mcp add redshift --env AWS_PROFILE=<profile> --env AWS_REGION=<region> -- uvx awslabs.redshift-mcp-server@latest` |
| Cursor | In `~/.cursor/mcp.json`: `{"mcpServers": {"redshift": {"command": "uvx", "args": ["awslabs.redshift-mcp-server@latest"], "env": {"AWS_PROFILE": "<profile>", "AWS_REGION": "<region>"}}}}` |

Needs `uv` installed. The server's own read-only guard applies only to queries routed through
it, not to direct CLI calls.

## Errors you will see

| Error text | Meaning and fix |
|---|---|
| `The SSO session associated with this profile has expired` | Sign in from here: `aws sso login --profile <profile>`. |
| `Unable to locate credentials` | No profile or wrong name. `aws configure list-profiles`; create one in the user's terminal. |
| `AccessDeniedException` on `redshift-data` | Missing Data API permissions. Their admin grants them. |
| `ValidationException: ... workgroup` or `cluster` | Wrong workgroup or cluster name. Ask the user to check it in the Redshift console. |
| `FAILED` status with `permission denied for relation` | The Data API works; the database user lacks grants on that object. Not a blocker for `select 1`. |
