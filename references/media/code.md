# Medium adapter — code (Nextflow, Snakemake, shell scripts)

Loaded by `SKILL.md` Phase 0 when the study target is a pipeline or script rather than
a skill. The loop, integrity rules and ledger are unchanged; this file only says what to
anchor on and what counts as understanding.

## Intake

Read the whole script/workflow plus its config (`nextflow.config`, `config.yaml`,
profiles) and any sample sheet. If the student is also running it, use real commands
and outputs from the run; if not, ask the student to run or dry-run it first
(`nextflow run -stub-run`, `snakemake -n`, `bash -n`).

## Objectives (derivation fallback)

- **Data flow** — what each process/rule/step consumes and produces; channel or
  wildcard semantics; what runs in parallel vs in sequence.
- **Parameters and config** — every value the script exposes or hard-codes, and what
  moves in the output when it changes.
- **Failure and resume** — what happens on error, what `-resume` / `--rerun-incomplete`
  reuses, what `set -euo pipefail` (or its absence) changes.
- **Environment** — containers, conda/pixi envs, resource directives, and why they are
  pinned.

## Anchors (checkpoints)

- Each process/rule/step boundary (consumes → produces).
- Before any destructive or long command (`rm`, overwrite, cluster submit).
- Each real parameter choice the author made.
- First output of a stage: one number or file the student must interpret.

## Evidence of understanding

- **Predict the output:** show a command or snippet and ask for its output before running.
- **Spot the error:** alter one line (wrong channel, swapped flag, missing quote) and ask
  what breaks.
- **What-if:** change one parameter or input and ask what changes downstream.
