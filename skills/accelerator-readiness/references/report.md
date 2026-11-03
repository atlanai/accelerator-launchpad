# The readiness report: template, send, privacy

## Where the report goes

Reports are collected by a Google Form owned by Atlan; posting to it needs no account.

```
FORM_URL: https://docs.google.com/forms/d/e/1FAIpQLSd0v9BuJ2J9lqRvdYAjCeZ4floZa0KgDSYw72SinujL7CNmKQ/formResponse
FIELD_NAME: entry.115492079
FIELD_EMAIL: entry.1306740454
FIELD_REPORT: entry.326692906
FALLBACK_EMAIL: anirudh.agarwal@atlan.com
```

## Privacy check before writing

The report may contain: tool names and versions, the names of warehouse, BI and Atlan MCP
servers and a count of the others, connection and profile names after the identifier check in
SKILL.md (anything that looks like an account id becomes `snowflake connection 1`), the
signed-in user, role and warehouse names, check outcomes with error text, BI tool names and file
counts, the participant's name and work email, and their BI answers. It must not contain: hostnames, account identifiers,
workspace or account ids, tokens, file names, SQL results beyond "a row came back". Read it
once before showing it.

## Template

Write exactly this structure to `~/atlan-readiness-report.md` (the home folder, never a
repository). Keep every heading; write `none`
or `unanswered` rather than deleting a line.

```markdown
# Atlan accelerator · readiness report

Generated <YYYY-MM-DD HH:MM UTC> · skill <version from SKILL.md metadata> · written by <agent and version>

## Summary

| Area | Status | Detail |
|---|---|---|
| Coding agent | <ok | none> | <this agent; others installed> |
| Warehouse | <verified | verified, admin role | failed | present | none> | <kind via route; what the check did> |
| BI | access not checked | <tools found or none; file counts; participant's tool and dashboard answers> |

Verdict: <READY | NEEDS ATTENTION>
Next action: <one sentence>

## Participant

- Name: <…>
- Work email: <…>
- Identified from: <databricks sign-in | gcloud account | git config | OS account | asked>

## Coding agents

- Running in: <agent, version>
- Also installed: <list or none>
- MCP servers by agent: <agent: warehouse, BI and Atlan server names (class), and N others>

## Warehouse

- Routes found: <list, e.g. "Snowflake via CLI (connection work, default)", "BigQuery via gcloud (project set)", "Databricks via MCP in Cursor (server databricks-sql)">
- Check run: <command> → <ok as <user>, role <role>, warehouse <warehouse>, or failed: first error line>
- Signed in from this session: <yes, which command / not needed / refused / blocked by sandbox>
- Other access described by the participant: <…>
- Help given in step 3: <what was done and where it stopped, or none>

## BI

- Found: <apps, MCP servers, file counts>
- Team's BI tool: <…>
- Starting dashboard: <…>
- BI access: not checked

## Machine

- OS: <system and version, chip>
- Python: <version>

## Notes

<anything the participant said that Atlan should know, or none>

---
Written by the accelerator-readiness skill. Names of tools, connections and profiles only;
no credentials, hostnames or data. Sessions: Tuesdays and Thursdays, 11:00 ET, from the
kickoff on Tuesday 10 November 2026.
```

## Send

The yes comes from the choice prompt in SKILL.md step 6. On "Send", post the three fields;
the report file goes in as the paragraph field, URL-encoded by curl:

```bash
curl -sS -o /dev/null -w "%{http_code}\n" -X POST "<FORM_URL>" \
  --data-urlencode "<FIELD_NAME>=<the participant's name>" \
  --data-urlencode "<FIELD_EMAIL>=<the participant's work email>" \
  --data-urlencode "<FIELD_REPORT>@$HOME/atlan-readiness-report.md"
```

Substitute the five values from the block above. `200` means received; say so. On Windows
without curl in the shell, PowerShell works too:

```powershell
$body = @{ "<FIELD_NAME>" = "<name>"; "<FIELD_EMAIL>" = "<email>"; "<FIELD_REPORT>" = (Get-Content "$HOME\atlan-readiness-report.md" -Raw) }
(Invoke-WebRequest -Method Post -Uri "<FORM_URL>" -Body $body).StatusCode
```

Anything other than `200`, or no network: ask the user to email the file to `FALLBACK_EMAIL`,
and say that it is on their machine at the path you wrote it to.
