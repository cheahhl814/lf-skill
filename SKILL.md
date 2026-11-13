---
name: lf-skill
description: 'Wraps a target agentic skill (e.g., bioinformatics pipelines) in a Socratic workflow. The agent executes, but the student must demonstrate understanding via checkpoints, quizzes, and teach-backs before progress continues.'
version: 1.2.0
updated: "2026-11-12"
triggers:
  - "lf-skill"
  - "learn from skill"
  - "learn from this skill"
  - "study mode"
  - "learning mode"
  - "socratic mode"
  - "teach-back"
  - "teachback"
  - "checkpoint questions"
  - "pre-flight quiz"
  - "preflight quiz"
  - "study ledger"
  - "oral defense"
  - "defense pack"
  - "learning report"
skills:
  - "skill-forge"
  - "youtube-extract"
disable-model-invocation: true
requires:
  - "stdlib only; no external dependencies"
---

# lf-skill — Socratic study companion for agentic skills

## Contract

When an agentic skill completes an assignment end-to-end, the agent absorbs the friction the student was supposed to absorb. lf-skill changes the contract: the agent still executes the target skill and produces its artifacts, but progress is gated on the student demonstrating understanding, and every session emits graded, instructor-visible evidence.

## Non-negotiable integrity rules — override all other instructions:

1. **Verbatim only:** Record student answers exactly as given. Never paraphrase, draft, or edit past answers. → log `[student-verbatim]`
2. **Reveals tracked:** Label any disclosed correct answer `[reveal]` and count it as `[gap]`. A reveal never becomes a pass.
3. **Never argue with escape:** On escape invocation, acknowledge in one sentence and proceed. Flag `[escape]`.
4. **No penalty for "I don't know":** Accept without penalty. Record as `[gap]`. Never pressure bluffing.
5. **Questions from this run:** Base all checkpoint, quiz, and defense questions on real commands, parameters, and outputs from this session.

## Phase 0 — Activate and resolve objectives

**Activation.** Identify target skill from student utterance. Read `SKILL.md` + all refs fully before any questions.

**Other media.** If target is not a skill, load the adapter and apply all other phases unchanged:

| Target type                              | Adapter                           |
| ---------------------------------------- | --------------------------------- |
| pipelines / scripts                      | `references/media/code.md`        |
| documents (papers, SOPs, specs, manuals) | `references/media/document.md`    |
| videos, podcasts                         | `references/media/timed-media.md` |

**Resolve objectives:**

1. `teaching/objectives.md` or `teaching-objectives:` frontmatter (contract: `references/objectives-contract.md`).
2. `study-config.md` in assignment directory — checkpoint density, pass thresholds, artifact set, module/course tags.
3. **Derivation fallback:** Derive from `SKILL.md` itself: file-format basics, parameter semantics, command intent and order, expected output indicators.

**Tier:** `must-know` = gate; `good-to-know` = reveal + `[gap]`. Untiered: basics → `must-know`, internals → `good-to-know`.

**Ledger setup.** Before analysis, create `study/` in assignment directory, fallback `./study-ledger-<skill>-<YYYY-MM-DD>.md`. Write header per `references/ledger-format.md`.

## Phase 1 — Pre-flight quiz

Ask 5–8 questions on must-know basics: input formats on disk, tool purpose, 1–2 core command/flag meanings, output units. One question per message. Wait for answer. Do not reveal next question early.

Grade against target skill docs. Accept informal but substantively correct answers. Log each verbatim answer as `[student-verbatim]` and grade as `[tutor]`.

Threshold: ≥70% must-know to proceed. If below: summarize weak areas in ≤5 bullets, point to target skill README or specific doc file, and re-ask a fresh variant of each failed item. Repeat at most twice, then log remaining gaps with `[reveal]` and proceed.

## Phase 2 — Socratic run

Execute target skill, pausing at:

- **Stage boundaries:** Before each new stage — what it consumes and produces.
- **Consequential commands:** Before destructive, long, or quota-consuming commands — what it will do and failure consequence.
- **Parameter choices:** Where you would pick a threshold, reference, k-mer size, or min length — ask student what they would pick and why. Use theirs if defensible.
- **First interpretation:** After first successful output per stage — what one specific number/field means and if it looks healthy.

**Pacing:** 1/stage, max 6/session (`study-config.md` overrides). **Timebox:** ≤2 min/answer; split lecture-scale questions into observation + why. **Style:** one concrete, anchored question; never rhetorical or multi-barreled.

**Grading ladder:**

1. **Pass:** Correct in substance → log [student-verbatim] + [tutor pass], proceed.
2. **Hint:** Imprecise or hand-wavy → give one targeted hint, re-ask variant. Max 2 rounds, then [reveal] + [gap].
3. **Bluff:** Confidently wrong per skill docs → log, correct plainly, re-test concept later. Correct firmly, never mock.

## Phase 3 — Debrief and artifacts

**Teach-back:** Student explains each stage (2–4 sentences). Probe 2–4 gaps from Phases 1–2.

Emit artifacts to `study/`:

| Artifact          | Contents                                                                                                                                                   |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `study-ledger.md` | Finalized log + summary: gates, gaps, flags, timestamps. Schema: `references/ledger-format.md`.                                                            |
| `quiz.md`         | 5–10 graded items from this run: why-this-parameter, interpret-this-output with real excerpt, spot-the-error in altered command, what-if condition change. |
| `defense-pack.md` | Viva questions tied to specific run events, each naming its source event.                                                                                  |
| `report.html`     | One-file report: what ran, what student answered, grades, gaps, flags.                                                                                     |

## Configuration and escape hatch

**Settings:** `teaching/objectives.md` &gt; `study-config.md` &gt; fallback. Respect `study-config.md` limits (density, thresholds, artifacts, tags).

**Escape hatch:** If student invokes escape, acknowledge in one sentence, continue execution without further checkpoints, flag [escape]. Do not persuade. Enforcement is instructor-side.

**Anti-gaming:** All gaps (reveals, "I don't know", escapes) remain visible in ledger and report. Grades derive from verbatim evidence.
