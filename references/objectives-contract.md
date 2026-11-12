# Instructor contract: annotating shared skills with learning objectives

study-mode is generic by design. To get domain-precise questions, an instructor who
maintains a shared agentic skill (read-qc-trimming, bacterial-genome-analysis, …) can
optionally ship a teaching block with the skill. This file is the format contract.

## Option A — `teaching/objectives.md` (preferred)

Create `teaching/objectives.md` in the skill's root directory:

```markdown
# Teaching objectives — read-qc-trimming

## Must-know (gate progress until answered)
- must-know: What a FASTQ record is (4 lines) and which lines carry sequence vs quality.
- must-know: Why raw nanopore reads need adapter removal before filtering.
- must-know: What the Q-score means physically (P(error) ≈ 10^(-Q/10)).

## Good-to-know (reveal on first miss; recorded as gap)
- good-to-know: How the read-length histogram changes after trimming and why.
- good-to-know: Difference between Q-avg filtering and length filtering failure modes.

## Pre-flight bank (5–8 questions; agent may sample or use all)
- q: "In this course's reads, what does a N50 of 500 bp on a 500 bp read set tell you?"
- q: "Why is a gzipped FASTQ still 'text data' to a pipeline?"
- q: "Which file do you give the QC step: raw or demultiplexed — and what's the difference?"

## Difficulty note
Audience: first-semester bio students, no CLI experience. Keep questions concrete;
avoid statistics beyond proportions.
```

Rules for the block:

- `must-know:` items are progress gates; `good-to-know:` items reveal-and-record.
- `pre-flight bank:` items seed Phase 1; if absent, the agent derives the quiz from
  the skill's input/output formats.
- `difficulty note:` is free text consumed verbatim by the agent.

## Option B — frontmatter list (lighter)

In the target skill's `SKILL.md` frontmatter:

```yaml
teaching-objectives:
  - "must-know: explain each quality metric in qc_report.md"
  - "good-to-know: what the multiQC aggregate hides about per-sample outliers"
```

Only objectives are supported here — no pre-flight bank.

## Option C — assignment-dir `study-config.md` (per assignment, per cohort)

```markdown
# study-config — assignment 3 (Read QC)

- target-skill: read-qc-trimming
- checkpoint-density: per-stage, max 4 (shorter lab session)
- preflight-threshold: 0.8
- artifacts: ledger, quiz, defense-pack, report
- course-tag: BIOL6250 / week 5
- instructor note: this cohort struggles with Phred scores — weight pre-flight there.
```

Precedence: `study-config.md` (assignment dir) overrides the target skill's
`teaching/` block, which overrides built-in defaults.

## Derivation fallback (no annotations present)

The agent derives objectives from the target skill itself (SKILL.md Phase 0), tiering
tool basics as must-know and deep internals as good-to-know. This is sufficient for
one-off use; instructors maintaining cohort-critical skills should still add Option A —
annotated questions will match the skills they teach with, week after week.
