# lf-skill

[![Version](https://img.shields.io/badge/version-1.2.0-blue)](#-installation)
[![Type](https://img.shields.io/badge/type-agent%20skill-blueviolet)](#-installation)
[![Built with](https://img.shields.io/badge/built%20with-skill--forge-orange)](https://github.com/cheahhl814/skill-forge)

Socratic study companion for agentic skills: it wraps any shared agentic skill the way
a student uses it for coursework — pre-flight basics quiz, mid-run Socratic checkpoints
(a defensible student parameter pick gets used), and a teach-back debrief — so that the
agent executes the pipeline while the student demonstrably learns, and every session
emits graded evidence (ledger, quiz, defense pack, learning report).

**Repository**: https://github.com/cheahhl814/lf-skill

> [!NOTE]
> Current version: **v1.2.0** (updated 2026-11-12). v1.2.0 adds per-medium adapters so the
> same Socratic loop works on pipelines/scripts, documents and timed media, not just skills.

## Contents

- [Installation](#-installation)
- [Usage](#-usage)
- [Workflow overview](#-workflow-overview)
- [Update check](#-update-check)
- [Repository layout](#-repository-layout)
- [Hard guarantees](#-hard-guarantees)
- [Depends on](#-depends-on)
- [Provenance](#provenance)

## 🚀 Installation

This is an **agent skill**: Markdown instructions plus one stdlib-only Python script.
No `pixi install` step.

**Option A — give your agent this prompt (recommended):**

```text
Install the lf-skill skill from
https://github.com/cheahhl814/lf-skill —
clone it into your agent's skills directory. Then read lf-skill's SKILL.md
to understand its three phases and the ledger/artifact contract. Confirm
when it is ready.
```

**Option B — manual install:**

```bash
git clone https://github.com/cheahhl814/lf-skill.git
# Symlink into your agent's skills directory (the path your agent watches for skills):
ln -sf "$(pwd)/lf-skill" "$SKILLS_DIR/lf-skill"
```

## 💡 Usage

The skill is **user-invoked only** (`disable-model-invocation: true`) — it never
auto-fires inside a session; the student opts in deliberately, which is the point:
the gate is the assignment.

### Natural-language prompts that trigger the skill

```text
/skill:lf-skill read-qc-trimming for assignment 3
lf-skill: wrap my assembly assignment, quiz me on the basics first
learn from skill: teach-back after this metagenomics run
give me an oral-defense pack for what the agent just ran
```

### The three phases (driven by the agent)

1. **Phase 0 — Objectives.** The agent reads the target skill's `SKILL.md` and its
   optional `teaching/objectives.md` (instructor-annotated; else it derives
   must-know/good-to-know objectives from the skill docs).
2. **Phase 1–2 — Pre-flight quiz + Socratic run.** ≥ 70% of must-know basics before
   analysis starts; checkpoints at stage boundaries, consequential commands, and real
   parameter choices. Escape: "study off" — flagged, never argued with.
3. **Phase 3 — Teach-back + artifacts** into `study/`: `study-ledger.md`
   (verbatim, provenance-tagged), `quiz.md` (built from THIS run),
   `defense-pack.md` (viva questions tied to run events), `report.html`.

Instructor per-assignment overrides (checkpoint density, thresholds, artifact set) go
in a `study-config.md`; full annotation formats are in
`references/objectives-contract.md`.

## 🔄 Update check

Ships the [skill-forge](https://github.com/cheahhl814/skill-forge) self-update check:
compares the deployed git SHA against this upstream repo via `git fetch` — no GitHub
API call, no extra dependencies.

```bash
python3 bin/skill-update-check.py
```

| Verdict | Exit | Meaning |
|:--------|:-----|:--------|
| `UP-TO-DATE` | 0 | Local HEAD matches origin/HEAD |
| `LOCAL-AHEAD` | 0 | Unpushed local commits; no action needed |
| `BEHIND-BY-N` | 1 | Upstream is N commits ahead → re-pull from this repo |
| `OFFLINE` | 2 | `git fetch` failed; informational only |
| `NO-ORIGIN` | 2 | No `origin` remote configured; informational only |

## 📁 Repository layout

```text
lf-skill/
├── SKILL.md                        # Main workflow (Phases 0–3, integrity rules — start here)
├── README.md                       # This file
├── bin/
│   └── skill-update-check.py       # Self-update check (stdlib-only)
└── references/
    ├── ledger-format.md            # Ledger schema + provenance tag glossary
    ├── media/
    │   ├── code.md                 # Adapter: Nextflow, Snakemake, shell scripts
    │   ├── document.md             # Adapter: papers, protocols, SOPs, specs, manuals
    │   └── timed-media.md          # Adapter: videos, podcasts (timestamped transcript)
    └── objectives-contract.md      # Instructor annotation formats + derivation fallback
```

## 🔒 Hard guarantees

- **Verbatim only** — student answers are recorded as quotes; the agent never drafts,
  paraphrases, or "improves" them.
- **Reveals never pass** — a disclosed answer is flagged `[reveal]` and counted as a
  gap; "I don't know" is recorded as a `[gap]`, never penalized.
- **Questions come from the actual run** — checkpoints, quiz, and defense items cite
  real commands/outputs of this session, making generic answer-sharing fail.
- **Escapes are visible** — a bypass finishes the assignment but is flagged
  `[escape]` in the ledger; enforcement belongs to the instructor, not the agent.
- **Stdlib-only tooling** — Python 3.8+, zero third-party dependencies.

## 🧩 Depends on

This skill declares a hard dependency on sibling skills (frontmatter `skills:` field —
validated by `skill-lint.py` C12; runtime prerequisites live in the separate
`requires:` field):

- **skill-forge** — the structural contract lf-skill ships under: frontmatter
  conventions, `bin/skill-lint.py` gate, and the `bin/skill-update-check.py` script
  rendered from its template.
- **youtube-extract** — external intake skill for the video medium: produces the
  timestamped transcript that `references/media/timed-media.md` requires.

At runtime it composes with whichever agentic skill the assignment uses (it reads that
skill's `SKILL.md` and optional `teaching/objectives.md`); no sibling skill is a hard
runtime dependency beyond `youtube-extract` when studying video.

## Provenance

Hand-adapted (`with_pixi = false` path) from the
[skill-forge](https://github.com/cheahhl814/skill-forge) README template (v1.8.0),
following the AiX-BIO skill convention: structural gate = `skill-lint.py`
(tool-skill profile), self-update check shipped per skill-forge §0.6.

## License

Released under the MIT License — see the
[LICENSE](https://github.com/cheahhl814/lf-skill/blob/main/LICENSE) file in this
repository for details.
