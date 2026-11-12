# study-mode

**Socratic study companion for agentic skills.** Wrap any shared agentic skill in a
learning gate so students producing coursework with coding agents demonstrably learn
instead of just shipping results.

## The problem

Instructor shares a skill (e.g. `read-qc-trimming`) with students; a coding agent
executes it end-to-end; the student submits a correct report without absorbing any of
the underlying basics. Agentic skills optimize for task completion — the friction a
human learner needs is exactly the friction the agent removes.

## How it works

study-mode does **not** replace the target skill. The agent still runs the real
pipeline and produces the real assignment artifacts. But progress is gated:

1. **Pre-flight quiz** — 5–8 must-know basics (file formats, core flags). Threshold
   (default ≥ 70%) before analysis starts.
2. **Socratic checkpoints** — during the run, the agent pauses at stage boundaries,
   consequential commands, and real parameter choices to ask the student *why*.
   Student parameters win when defensible.
3. **Teach-back + artifacts** — after completion: a structured debrief and four
   hand-in artifacts:
   - `study-ledger.md` — append-only, verbatim student answers with provenance tags
   - `quiz.md` — auto-generated from THIS run (copy-resistant)
   - `defense-pack.md` — viva questions tied to specific run events, for live oral defense
   - `report.html` — one-file learning summary for the submission cover

**Integrity by visibility, not enforcement:** the agent never writes the student's
answers (verbatim transcription only), reveals are flagged as gaps, "I don't know" is
never penalized, and any bypass is flagged `[escape]` in the ledger. The instructor's
graders: ledger verbatim spot-checks + defense-pack oral questions.

## For students

```
study mode with read-qc-trimming for assignment 3
```

Escape when in a hurry: "study off" — finishes normally, ledger records the flag.

## For instructors

Annotate shared skills with learning objectives (one markdown file per skill):

```
<skill-root>/teaching/objectives.md    # must-know / good-to-know / pre-flight bank
```

Or per assignment: `study-config.md` (checkpoint density, thresholds, artifact set,
course tag). Format: `references/objectives-contract.md`. Unannotated skills work
too — objectives are derived from the skill's own docs.

## Install

Clone into your harness's skills directory (Pi reads `~/.agents/skills/`):

```bash
git clone https://github.com/cheahhl814/study-mode ~/.agents/skills/study-mode
```

No external dependencies; harness-agnostic (Pi, Claude Code, or any agent that reads
SKILL.md files). Lints under the AiX-BIO `tool-skill` profile.

## Files

```
SKILL.md                             main workflow (Phases 0–3, integrity rules)
references/ledger-format.md          ledger schema + provenance tag glossary
references/objectives-contract.md    instructor annotation formats
```

## Design notes (pedagogy)

- **Generation effect:** students answer before the agent proceeds → retrieval
  practice built into the workflow, not bolted on.
- **Copy-resistance:** quiz/defense items derive from the student's own run events,
  so generic answer-sharing fails.
- **Honesty over guessing:** "I don't know" is recorded as a gap, not a failure —
  the system is designed so bluffing is worse than ignorance.
- **Escape with trace:** a student can always bypass; the trace is what the
  instructor grades the *process* on.
