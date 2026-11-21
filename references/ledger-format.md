# study-ledger.md format contract

The ledger is the graded evidence of learning. It is built append-only during the
session and finalized at Phase 3. Keep every line timestamped ISO-8601; keep answers
verbatim (rule 1 of SKILL.md).

## Header (written at Phase 0)

```markdown
# Study ledger — <target-skill>

- date: YYYY-MM-DD
- student input: <name/ID if provided, else "not recorded">
- course/module: <from study-config.md, else unstated>
- run directory: <absolute path>
- mode: study | escaped (set at session end from escape flags)
- artifacts: quiz.md, defense-pack.md, report.html (primer decks per references/primer.md if issued)
```

## Entry grammar

Append one block per question/answer, in order of occurrence:

```markdown
## [phase2] 2026-11-12T14:03Z — checkpoint: stage trimmomatic

**Trigger:** before running trimmomatic on SRR1234567 (consequential command).
**Question:** "What are the four lines of a FASTQ record, and why is the
quality line the same length as the sequence line?"
**Tier:** must-know

**[student-verbatim]** 2026-11-12T14:05Z
> id line, then the sequence, then a plus line, then a quality line. they
> have to match or the pairing between base and score would be lost

**[tutor pass]** 2026-11-12T14:05Z — correct; accepted "plus line" without
the @/+ detail note.
```

Tag semantics:

| Tag | Meaning | Counts as |
|---|---|---|
| `[student-verbatim]` | The student's answer, quoted exactly | — |
| `[tutor pass]` | Graded correct in substance | pass |
| `[tutor hint]` | One hint given, re-ask pending | — |
| `[tutor fail]` | Second failed attempt | gap |
| `[reveal]` | Correct answer disclosed by tutor | gap (never a pass) |
| `[gap]` | "I don't know" / blank | gap (honest; not penalized) |
| `[bluff]` | Confidently wrong; concept re-tested later | gap + follow-up required |
| `[escape]` | Study gate bypassed by student request | instructor flag |
| `[config]` | Instructor/config override applied | — |

## Source citations per medium

Every **Trigger:** line (or quiz/defense item) must cite the anchor the question
derives from, so an instructor can find it without the transcript of the session.
For a skill target this is a command or output excerpt from this run. For non-skill
media (loaded via the Phase 0 adapters), use the medium's citation format:

| Medium | Citation format | Example |
|---|---|---|
| agentic skill | command or output excerpt from this run | `trimmomatic PE SRR1234567…` |
| pipeline / script | process/rule name or `file:line`, plus the snippet | `process TRIMMOMATIC (main.nf:14): "trimmomatic PE …"` |
| document | section/page/table/figure + verbatim quoted passage (books: chapter-qualified, e.g. `ch. 3, §2, p.87`) | `§4.2, p.12 — "we used k = 31"` |
| timed media | timestamp `[mm:ss]` (`[hh:mm:ss]` beyond one hour) + verbatim transcript quote | `[12:40] — "the min length is 500"` |

Rules:

- Quotes are verbatim from the source material — same standard as
  `[student-verbatim]`, applied to the anchor.
- The citation alone must locate the anchor: a file and line, a section number, or a
  timestamp; "the part about trimming" is not a citation.
- Timestamps are cited as they appear in the transcript used at intake; if intake
  produced no timestamped transcript, the timed-media adapter requires one before
  questions start — the ledger never carries uncited moments.

## Finalization block (Phase 3, appended at top as a summary, not interleaved)

```markdown
## Summary

- pre-flight: 6/8 must-know correct (75%, threshold 70%)
- checkpoints: 5 asked — 3 pass, 1 hint→pass, 1 reveal
- gaps: [list], each mapped to a quiz.md item or defense-pack question
- bluffs re-tested: 1 concept (Q-score), re-test result: pass
- escapes: 0
- instructor read next: gaps → defense-pack Q3, Q5; ledger verbatim spot checks
```

## Anti-tamper notes

- The agent appends `[student-verbatim]` blocks by transcribing chat text only.
  If the student refuses to answer a question, record refusal/blank — never
  synthesize an answer.
- Re-grade questions and quiz/defense items must each link the run event they
  derive from (command or output excerpt), so an instructor can verify the
  question was not generic.
- Append-only: later corrections are new entries referencing the old timestamp,
  never edits in place.
