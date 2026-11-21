# Primer contract (zero-knowledge path)

The primer is the student's learning material — it exists so that a learner with
zero knowledge of the target has something to study before the pre-flight quiz.
It is teaching material: the quiz still grades against the target's docs, never
the primer. Issued per SKILL.md Phase 0 (declared newness or "teach me first"),
or upgraded from the Phase-1 weak-area summary when newness surfaces at a failed
item.

## Rendering: slide decks via external skills

The primer is rendered as **slide decks**, not prose files. Two external skills
are declared in SKILL.md frontmatter (`skills:`) for this:

- **design-pack** (default) — renders each deck as a self-contained HTML file
  with real SVG diagrams; opens in any browser, no dependencies.
- **genoffice** (on request) — produces a `.pptx` from the same deck outline
  when the student or instructor wants a portable, editable file.

If neither skill is available, fall back to markdown (map `study/primer.md` plus
`study/primer/<slug>.md` depth files, Mermaid blocks for diagrams) — same content
model, lower fidelity. Never block a study session on deck rendering.

## Structure: map deck + depth decks

The **map deck** is always the entry point and stays small (≤ 8 slides):

1. Title + what you must be able to do after studying (the must-know objectives).
2. Reading path — the ordered list of depth decks.
3–8. One orientation slide per must-know objective: 2–3 sentences, one visual,
   citation in the footer, pointer to its depth deck.

**Depth decks** live at `study/primer/<slug>.html` (`slug` = kebab-case of the
objective), one small deck per must-know objective:

- **Pre-generate all depth decks** when the target has more than 4 must-know
  objectives, or when the target material is long (book, >30-min video,
  multi-stage pipeline).
- Otherwise issue on demand: when the student asks for more, or when a Phase-1
  item fails and its weak-area summary becomes a deck.
- Every slide carries its per-medium citation in the footer (skill: doc pointer;
  code: rule/`file:line`; document: §/page; timed media: timestamp range) so the
  instructor can trace teaching back to the material.

## Slide discipline

- **One idea per slide.** Concept slides: one diagram (SVG via design-pack) plus
  at most ~40 words of prose. Never a wall of text.
- **Technique slides are runnable**: the command in a terminal-style block, the
  expected output (or its shape) beside it, and the instruction to run it now —
  the quiz anchors on the student's real output.
- **Timed media:** do not re-explain what the video already teaches — the slide
  cites the timestamp range to watch (`[12:40]–[15:10]`) and adds only what the
  speaker skipped or got wrong.
- **Documents:** quote the load-bearing passage (verbatim, cited), then explain
  in at most as many words as the quote.
- Citations are not decoration: a slide that cannot cite its anchor is not
  issued.

## Strategy: concepts vs. techniques

Tag every must-know objective `concept` or `technique` when objectives are
resolved (Phase 0); mixed targets (a skill that is part theory, part procedure)
get both tags. The tag drives deck treatment, quiz question form, and teach-back
mode:

| | concept (declarative) | technique (procedural) |
|---|---|---|
| Deck treatment | read + analogy + diagram | minimal read, then **do it** — runnable slide with expected output |
| Quiz question form | why / what-if / interpret-this | predict-the-output / spot-the-error / which-flag-and-why |
| Teach-back mode | explains (2–4 sentences per stage) | demonstrates (runs or walks the command and its output) |
| Grading anchor | the target's docs | the student's own run/output from this session |

Concepts the student can learn from slides; techniques they only learn by
executing — a deck that only describes a technique invites passive failure, so
its runnable slide is not optional.

## Anti-tamper notes

- The primer never contains student answers or grades — it is written before
  Phase 1 and only extended (append-only depth decks), never rewritten to match
  what the student later said.
- Depth decks cite the material they derive from; a deck that cannot cite its
  anchor is not issued.
- Deck regeneration changes style, never content: re-rendering after an edit to
  the same outline must preserve every citation.
