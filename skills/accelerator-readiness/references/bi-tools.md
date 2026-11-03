# BI tools: what to look for and what to ask

## Why

Week one of the accelerator starts from one dashboard the participant already has. Its
measures and filters become the first metrics; its numbers become the first evals. So the
audit needs to know which BI tool they use and which dashboard they would pick. Screenshots,
exports, uploads, and files are not needed; do not ask for them or whether they can be shared.

## Look

1. **MCP servers** from step 1 whose names suggest BI: Tableau, Power BI, Looker, Metabase,
   Sigma, ThoughtSpot, Superset.
2. **Desktop apps.** macOS:
   ```bash
   ls /Applications ~/Applications 2>/dev/null | grep -iE "tableau|power ?bi|qlik|dbeaver|metabase|looker|excel"
   ```
   Windows (PowerShell):
   ```powershell
   Get-ChildItem "$env:ProgramFiles", "${env:ProgramFiles(x86)}", "$env:LOCALAPPDATA\Programs" -Name | Select-String -Pattern "tableau|power bi|qlik|dbeaver"
   ```
3. **Local BI files**, counts only, shallow, in the three usual folders:
   ```bash
   find ~/Desktop ~/Documents ~/Downloads -maxdepth 3 -type f \( -iname '*.twb' -o -iname '*.twbx' -o -iname '*.hyper' -o -iname '*.pbix' -o -iname '*.pbit' -o -iname '*.pbip' -o -iname '*.lkml' -o -iname '*.qvf' \) 2>/dev/null | sed 's/.*\.//' | sort | uniq -c
   ```
   Report the counts per extension. Never list file names; they can carry customer or
   project names. Do not open, upload, or ask the user to share these files.

## Ask

Two questions, one at a time:

1. Which BI tool does your team use day to day? Options: Tableau, Power BI, Looker, Sigma,
   and Other. Always offer all four named tools, Tableau included, with any tool found on
   this machine moved to the front.
2. Which one dashboard would you start the accelerator from?

A "not sure" is a fine answer; Atlan picks one with them in the one-on-one.

Then one more: do they know which warehouse tables hold the data for that dashboard, or would
answer the questions in their use case? Options: "Yes, I can name them", "Roughly", "Not
sure". Take names in chat on yes or roughly. On not sure: "No worries, we'll work with you
1:1 if these are needed."

## Record

- Tools found (apps, MCP servers), file counts by type
- The BI tool they named and the starting dashboard
- The tables they named for the use case, or not sure
- BI access: not checked. Tool discovery and participant answers do not verify
  authentication or dashboard access; do not mark BI as verified or passed.
