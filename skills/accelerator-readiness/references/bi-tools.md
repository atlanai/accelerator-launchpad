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

Do not scan local folders for BI files.

## Ask

Two questions, one at a time:

1. Which BI tool does your team use day to day (Tableau, Power BI, Looker, Sigma, other)?
2. Which one dashboard would you start the accelerator from?

A "not sure" is a fine answer; Atlan picks one with them in the one-on-one.

## Record

- Tools found (apps, MCP servers)
- The BI tool they named and the starting dashboard
- BI access: not checked. Tool discovery and participant answers do not verify
  authentication or dashboard access; do not mark BI as verified or passed.
