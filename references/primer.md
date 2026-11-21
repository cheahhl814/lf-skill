# Primer contract (zero-knowledge path)

The primer is the student's reading material — it exists so that a learner with
zero knowledge of the target has something to read before the pre-flight quiz.
It is teaching material: the quiz still grades against the target's docs, never
the primer. Issued per SKILL.md Phase 0 (declared newness or "teach me first"),
or upgraded from the Phase-1 weak-area summary when newness surfaces at a failed
item.

## Structure: map + depth files

`study/primer.md` is always the entry point and stays one page:

```markdown
# Primer — <target>

- reading path: <ordered list of depth sections, or "none needed">
- what you must be able to do after reading: <the must-know objectives, restated>

## <Objective 1> (2–3 sentences + pointer into the target material)
...

## What to read next
<exact doc lines / sections / timestamps>
```

Depth sections live in `study/primer/<slug>.md`, one file per must-know
objective, one screen each (`slug` = kebab-case of the objective):

- **Pre-generate all depth sections** when the target has more than 4 must-know
  objectives, or when the target material is long (book, >30-min video,
  multi-stage pipeline).
- Otherwise issue on demand: when the student asks for more, or when a Phase-1
  item fails and the weak-area summary needs a section.
- Every depth section carries its per-medium citation (skill: doc pointer; code:
  rule/`file:line`; document: §/page; timed media: timestamp range) so the
  instructor can trace teaching back to the material.

## Media: use what renders, point at what already teaches

- **Diagrams:** where a section explains a flow or structure, include one Mermaid
  diagram (` ```mermaid ` block) instead of prose — pipeline DAGs, data-flow,
  state transitions. One per section; never decorate.
- **Runnable blocks:** for technique objectives, embed the exact command(s) to
  run with the expected output (or its shape) as a comment. The student runs
  them; the quiz anchors on their real output.
- **Timed media:** do not re-explain what the video already teaches — cite the
  timestamp range to watch (`[12:40]–[15:10]`) and add only what the speaker
  skipped or got wrong.
- **Documents:** quote the load-bearing passage (verbatim, cited), then explain
  in at most as many words as the quote.

## Strategy: concepts vs. techniques

Tag every must-know objective `concept` or `technique` when objectives are
resolved (Phase 0); mixed targets (a skill that is part theory, part procedure)
get both tags. The tag drives primer treatment, quiz question form, and
teach-back mode:

| | concept (declarative) | technique (procedural) |
|---|---|---|
| Primer treatment | read + analogy + diagram | minimal read, then **do it** — guided command with expected output |
| Quiz question form | why / what-if / interpret-this | predict-the-output / spot-the-error / which-flag-and-why |
| Teach-back mode | explains (2–4 sentences per stage) | demonstrates (runs or walks the command and its output) |
| Grading anchor | the target's docs | the student's own run/output from this session |

Concepts the student can learn from reading; techniques they only learn by
executing — a primer that only describes a technique invites passive failure,
so its "do it" block is not optional.

## Anti-tamper notes

- The primer never contains student answers or grades — it is written before
  Phase 1 and only extended (append-only depth sections), never rewritten to
  match what the student later said.
- Depth sections cite the material they derive from; a section that cannot cite
  its anchor is not issued.
