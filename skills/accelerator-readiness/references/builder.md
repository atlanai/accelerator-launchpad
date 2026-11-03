# The Builder

A small ASCII builder who appears at three moments of the check: the start, a few real
events along the way, and the end. The point is one moment of delight, so keep it rare and
keep it honest.

## Rules

- Print every frame inside a fenced code block (` ```text `) so the spacing survives. Copy the
  frame exactly; only the fields in `<angle brackets>` change.
- Box lines must keep their width. Pad or trim each field so the right-hand border stays in
  the same column. Trim long values with `...` (for example a use case over 22 characters).
- Fields only ever hold what the check already collected: the participant's name, their use
  case in their own words, and outcomes. Never an email, a hostname, an account identifier or
  anything the Rules in SKILL.md keep out of the chat.
- At most three quips in a whole run, each only after the event it names actually happened.
  No quip is better than a forced one.
- The Builder never appears in the report file. It is chat only.
- No human available (a headless run): skip every frame.
- Kickoff date for this cohort: **nov 9**. Change it here for the next cohort.

## 1. Start (show once, before the use case question)

```text
     ▄███▄
    ▀▀▀▀▀▀▀      THE BUILDER
     ( •_• )     clocking in. about ten minutes.
    ╭┤ ▓▓▓ ├╮
     │ ╥ ╥ │     first job: what are we building?
     ┘     └
```

## 2. Quips (optional, at most three per run)

One line each, straight after the status line of the step where the event happened. Pick from
these; do not invent new ones.

| Event | Quip |
|---|---|
| Warehouse verified through a CLI | `▀▀▀(•_•)  found your warehouse. it was in the CLI the whole time.` |
| Warehouse verified through an MCP server | `▀▀▀(•_•)  found your warehouse. it was in the toolbox all along.` |
| A browser sign-in ran and succeeded | `▀▀▀(•_•)  sign-in renewed. hard hats on.` |
| More than one coding agent installed | `▀▀▀(•_•)  <n> coding agents on this laptop. a well-stocked site.` |
| The user named the tables behind their dashboard | `▀▀▀(•_•)  you know your tables. the foreman approves.` |

## 3. End (show after the step 6 status line, before the closing message)

### Verdict READY: the site pass

```text
╔══ SITE PASS ════════════════════════╗
║ builder    <name>                   ║
║ building   <use case>               ║
║ warehouse ok   agent ok   BI ok     ║
║                                     ║
║ FOUNDATION POURED · CLEARED TO BUILD║
╚═════════════════════════════════════╝
     ▄███▄
    ▀▀▀▀▀▀▀
     ( ^‿^ )b    see you on site, nov 9.
    ╭┤ ▓▓▓ │     bring the dashboard.
     ┘     └
```

`<name>` and `<use case>` are padded or trimmed to 22 characters. If the use case was "not
sure yet", write `to be shaped together`.

### Verdict NEEDS ATTENTION: the site inspection

Tick `[x]` for each item that passed and leave `[ ]` for each that did not. Point
`<- this beam` at the first unticked item only. If one item is unticked, the message is the
one below; if two or more are, replace "one beam short" with "a few beams short".

```text
┌ SITE INSPECTION ───────────────┐
│ [x] use case                   │
│ [x] coding agent               │
│ [ ] warehouse   <- this beam   │
│ [x] dashboard                  │
│                                │
│ one beam short. it's in the    │
│ report; the crew fixes it with │
│ you before kickoff.            │
└────────────────────────────────┘
     ▄███▄
    ▀▀▀▀▀▀▀      ▲
     ( •_• )    ▟█▙   cone stays up
    ╭┤ ▓▓▓ ├╮   ▀▀▀   till it's fixed.
     ┘     └
```

Items and when they pass: **use case** when the user gave one (a "not sure yet" still passes,
since Atlan shapes it with them); **coding agent** when one is installed; **warehouse** when
the outcome is verified; **dashboard** when the user named a BI tool and a starting
dashboard. These match the verdict rules in SKILL.md, so a READY run never shows this frame.
If the user chose "Don't send" in step 6, add a line under the box: `report not sent. reply to
the acceptance email and we'll help.`
