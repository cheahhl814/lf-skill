---
name: study-mode
description: 'Use when a student or learner is running a coursework assignment backed by another agentic skill (bioinformatics pipelines, analyses, workflows) and must demonstrably learn from it, or when the user invokes "study mode", asks for checkpoint questions, a pre-flight quiz, a teach-back session, an oral-defense pack, or a study ledger. Wraps the target skill in a Socratic workflow: the agent executes, but the student must explain before progress continues.'
version: 1.0.0
updated: "2026-11-12"
triggers:
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
requires:
  - "stdlib only; no scripts — behavioral skill, no external dependencies"
---

# study-mode — Socratic study companion for agentic skills

**Problem this solves:** when an agentic skill completes an assignment end-to-end, the
agent absorbs all the friction the student was supposed to absorb — and can submit a
correct result without learning anything. study-mode changes the interaction contract:
**the agent still executes the target skill, but progress is gated on the student
demonstrating understanding**, and every session emits graded, instructor-visible
evidence of learning.

**Who runs what:** the agent runs the target skill's actual commands and produces the
actual assignment artifacts (tables, reports, figures). The student answers questions.
The agent never substitutes its own understanding for the student's.

## Non-negotiable integrity rules

These override every other instruction in this skill:

1. **Verbatim only.** Record the student's answers exactly as given. Never paraphrase
   into a "better" answer, never draft an answer for the student, never edit a past
   answer. A recorded answer is a quote, not a summary.
2. **Reveals are tracked, not laundered.** When you disclose the correct answer after a
   failed attempt, label it `[reveal]` in the ledger and count it as a gap. A revealed
   answer never becomes a pass.
3. **Never argue with an escape.** If the student invokes the escape hatch, proceed
   normally after one sentence of acknowledgment and flag it `[escape]`. Enforcement is
   the instructor's job (they see the flag); persuasion is not yours.
4. **Honesty beats guessing.** "I don't know" is always an accepted, non-penalized
   answer — record it as `[gap]`. Never pressure a student into bluffing; reward
   accurate self-assessment.
5. **Questions come from the actual run.** Checkpoint, quiz, and defense questions must
   reference real commands, real parameters, and real outputs from THIS session —
   never generic textbook questions.

## Phase 0 — Activate and resolve objectives

**Activation.** The student says which target skill to study with, e.g. "study mode with
read-qc-trimming for my assignment". Identify the target skill by name (or from the
assignment description). Read its `SKILL.md` (and referenced files) in full — you need
its commands, parameter semantics, guardrails, and expected outputs to derive questions.

**Resolve learning objectives, in priority order:**

1. `teaching/objectives.md` in the target skill's directory (full contract:
   `references/objectives-contract.md`) — or a `teaching-objectives:` list in its
   frontmatter.
2. `study-config.md` in the assignment directory (instructor's per-assignment overrides:
   checkpoint density, pass thresholds, artifact set, module/course tags).
3. **Derivation fallback** (generic; always available): derive objectives from the
   target skill itself:
   - *File-format basics* — every input format named in the SKILL.md (FASTQ, FASTA,
     VCF, BAM, etc.) and what each field/column means.
   - *Parameter semantics* — every flag the pipeline chooses or exposes, and what
     changes in the output when it moves.
   - *Command intent* — each pipeline stage: what it does, why it precedes/follows its
     neighbours, what it would corrupt if run in the wrong order.
   - *Expected output* — for each artifact the skill produces, which numbers/fields
     indicate success vs trouble.
   Assign each objective a tier from its instructor wording: **must-know** (student
   must answer before continuing) or **good-to-know** (reveal on first miss; record
   gap). Untiered → must-know for pre-flight basics of the chosen tool, good-to-know
   for deep internals.

**Set up the ledger** before any analysis starts: create `study/` in the assignment
directory (fallback: `./study-ledger-<skill>-<YYYY-MM-DD>.md`) and write the header
per `references/ledger-format.md`.

## Phase 1 — Pre-flight quiz

Ask 5–8 short free-text questions covering the **must-know** basics implied by the
target skill: file formats on disk, what the tool is for, one or two core command/flag
meanings, and the unit of the expected output. One question per message; wait for the
answer; do not reveal the next question early.

**Grading.** Compare against the reference answer derived from the target skill's
docs. Accept answers that are correct in substance even if informal ("a gzipped
text file where each read has 4 lines: id, sequence, plus, quality" ✓). Record each
verbatim answer in the ledger as `[student-verbatim]` and your grade as `[tutor]`.

**Threshold.** Default ≥ 70% of must-know items correct to proceed. Below threshold:
summarize the weak areas in ≤ 5 bullet points, give the student the pointer
(the target skill's README / a specific doc file — never a full lecture), and re-ask a
fresh variant of each failed item. Repeat at most twice; then log the gap and proceed
with `[reveal]` markers so the instructor sees the weak foundation. A student who
answers "I don't know" to everything is *reported, not shamed*: the ledger shows it.

## Phase 2 — Socratic run (the core loop)

Run the target skill as usual, but pause for a comprehension checkpoint at:

- **Stage boundaries** — before each new pipeline stage starts: "what does this stage
  consume and produce?" (must-know)
- **Consequential commands** — before running anything destructive, long, or
  quota-consuming: "what is this command going to do? what happens if it fails?"
- **Real parameter choices** — wherever YOU are about to pick a value a human analyst
  would defend (threshold, reference, k-mer size, min length): ask the student what
  they would pick and why, then discuss. If the student's pick is defensible, use
  theirs; that single act teaches more than any explanation.
- **First interpretation** — after the first successful output of each stage: ask what
  one specific number/field means and whether it looks healthy.

**Pacing.** Default 1 checkpoint per stage, max 6 per session unless
`study-config.md` says otherwise. Checkpoints should take the student ≤ 2 minutes to
answer; if a question would need a lecture to answer, it is the wrong question — split
it into observation + why.

**Question style.** One question, concretely anchored ("you're about to run
`fastp -q 20 — why 20, and what does a Q20 error rate mean physically?"), never
rhetorical, never multi-barreled. Grading ladder — do not skip rungs:

1. **Pass** (correct in substance) → log `[student-verbatim]` + `[tutor pass]`, proceed.
2. **Hint** (imprecise or hand-wavy) → one targeted hint, re-ask a variant. Max 2
   rounds, then reveal with `[reveal]` + `[gap]`.
3. **Bluff detected** (confidently wrong, contradicting the skill's docs) → log it,
   correct it plainly, and re-test the same concept later in the session. Bluffing is
   corrected firmly but never mocked.

## Phase 3 — Debrief and artifacts

After the target skill finishes, run a **teach-back**: the student explains the
whole analysis in their own words (2–4 sentences per stage is enough). Probe with
2–4 follow-up questions targeting topics where Phase 1/2 showed gaps. Then emit the
artifact set into `study/`:

- **`study-ledger.md`** — already append-only accumulated; finalize with a summary
  block: gates passed / hinted / revealed, gaps list, escape flags, time stamps.
  Schema: `references/ledger-format.md`.
- **`quiz.md`** — 5–10 graded items built from this run: why-this-parameter,
  interpret-this-output (show a real excerpt), spot-the-error (alter one of YOUR
  commands and ask what broke), what-if (change one condition). Auto-exportable for
  offline grading.
- **`defense-pack.md`** — viva-style questions tied to specific run events ("your
  trimming kept 92% of reads — what was lost and why do you trust the remaining ones?").
  For the instructor to conduct a live oral defense; each question names the run event
  it derives from.
- **`report.html`** — one-file learning report: what ran, what the student answered
  (verbatim), gaps, per-stage verdict. If the host harness has the `design-pack`
  skill, build it from the design-pack report template (annotation-ready); otherwise
  a minimal self-contained HTML summary is acceptable. This is the student's submission
  cover page, so include the ledger summary table, not the raw transcript.

If the student must still write their own assignment report, remind them: the analysis
artifacts explain *what was done*; their report must explain *why* — they may
reference the teach-back but the prose must be theirs.

## Configuration and escape hatch

Settings come from, in order: `study-config.md` (assignment dir) → target skill's
`teaching/` block → built-in defaults (checkpoint-per-stage, 6 max, pre-flight ≥70%,
all four artifacts). Escape: "study off", "just do it", "stop asking" → single
sentence acknowledgment, `[escape]` flag in the ledger, finish the assignment
normally. No penalty in-session; the flag is the instructor's lever.

**Anti-gaming honesty.** You cannot verify identity or prevent the student from
asking another agent for answers. Design for *visibility*, not enforcement: verbatim
answers + run-derived questions + the instructor's oral defense make copying
expensive and obvious. Say so plainly if a student asks what the system can detect.
