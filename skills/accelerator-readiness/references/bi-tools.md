# BI tools: what to look for and what to ask

## Why

Week one of the accelerator starts from one dashboard the participant already has. Its
measures and filters become the first metrics; its numbers become the first evals. So the
audit needs to know which BI tool they use, which dashboard they would pick, and whether
they can get it out of the tool (an export file or screenshots).

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
   project names.

## Ask

Two questions, in one message:

1. Which BI tool does your team use day to day (Tableau, Power BI, Looker, Sigma, other)?
2. Which one dashboard would you start the accelerator from, and can you export it
   (Power BI `.pbix` or `.pbip`, Tableau `.twbx`, LookML files) or share its screenshots?

A "not sure" is a fine answer; Atlan picks one with them in the one-on-one.

## Record

- Tools found (apps, MCP servers), file counts by type
- The BI tool they named, the dashboard, and whether an export is possible
