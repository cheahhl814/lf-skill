#!/usr/bin/env python3
"""Battle-test fixtures for lf-skill — one tiny fixture per declared input type.

Regenerates every fixture deterministically (fixed embedded text, no RNG, no
timestamps, no gzip) and verifies it against test-data/MANIFEST.tsv (sha256 of
file content). Battle-test check 12a of skill-forge: regenerating into a temp
dir and comparing against the manifest must be reproducible byte-for-byte.

Usage:
    python3 make_fixtures.py            # verify fixtures on disk + manifest (exit 0/1)
    python3 make_fixtures.py --write    # write fixtures + regenerate MANIFEST.tsv

Fixtures are inert text (tracked in git) — they are study-material samples for
Phase-0 dry runs, never run artifacts. Provenance: code/Snakefile is the minimal
workflow from the Snakemake 9.x tutorial (snakemake.readthedocs.io, MIT-licensed
project); the other three are synthetic.
"""
import hashlib
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

SNAKEFILE = '''SAMPLES = ["A", "B"]


rule all:
    input:
        "plots/quals.svg"


rule bwa_map:
    input:
        "data/genome.fa",
        "data/samples/{sample}.fastq"
    output:
        "mapped_reads/{sample}.bam"
    shell:
        "bwa mem {input} | samtools view -Sb - > {output}"


rule samtools_sort:
    input:
        "mapped_reads/{sample}.bam"
    output:
        "sorted_reads/{sample}.bam"
    shell:
        "samtools sort -T sorted_reads/{wildcards.sample} "
        "-O bam {input} > {output}"


rule samtools_index:
    input:
        "sorted_reads/{sample}.bam"
    output:
        "sorted_reads/{sample}.bam.bai"
    shell:
        "samtools index {input}"


rule bcftools_call:
    input:
        fa="data/genome.fa",
        bam=expand("sorted_reads/{sample}.bam", sample=SAMPLES),
        bai=expand("sorted_reads/{sample}.bam.bai", sample=SAMPLES)
    output:
        "calls/all.vcf"
    shell:
        "bcftools mpileup -f {input.fa} {input.bam} | "
        "bcftools call -mv - > {output}"


rule plot_quals:
    input:
        "calls/all.vcf"
    output:
        "plots/quals.svg"
    script:
        "scripts/plot-quals.py"
'''

TOY_SKILL = '''---
name: toy-trimmer
description: 'Use when a demo FASTQ trimming step is needed: minimal toy skill used as a study-target fixture by lf-skill battle tests.'
version: 0.1.0
triggers:
  - "toy-trimmer"
teaching-objectives:
  must-know:
    - the four lines of a FASTQ record
    - why quality trimming uses a cutoff on Q-scores
  good-to-know:
    - how adapter contamination differs from low-quality tails
---

# toy-trimmer

Filters reads: drops bases below a quality cutoff from both ends, then drops
reads that became too short.

## Steps

1. Read `input.fastq` (four-line records: id, sequence, +, quality).
2. Drop leading and trailing bases with Q < MINQ.
3. Drop reads shorter than MINLEN after trimming.
4. Write `output.fastq`.

## Parameters

- MINQ: quality cutoff, default 20 (1% error probability).
- MINLEN: minimum read length after trimming, default 50.
'''

MINI_SOP = '''# SOP-TEST-001 — Buffer exchange by centrifugal ultrafiltration (toy fixture)

- version: 1.0 | effective: 2026-01-01 | author: fixture | approver: fixture

## Purpose and scope

Exchange the buffer of a 500 µL protein sample. This SOP does not cover
denatured or precipitated samples; see the lab's refolding SOP instead.

## Procedure

1. Load 500 µL sample into a 10 kDa MWCO centrifugal filter unit.
2. Centrifuge at 14,000 × g for 10 min at 4 °C.
3. Discard flow-through; refill the unit to 500 µL with target buffer.
4. Repeat steps 2–3 twice (three washes total).
5. Recover the retentate; final volume 100–200 µL.

## Quality control / acceptance criteria

Accept if final conductivity is within 5% of the target buffer's conductivity.

## Troubleshooting

If protein recovery is below 80%, inspect the membrane for tears before
repeating the washes.
'''

TRANSCRIPT = '''{
  "video_id": "fixture-0001",
  "url": "file://fixture/toy-fastq-talk",
  "language": "en",
  "transcript_type": "manual",
  "extraction_backend": "fixture",
  "num_snippets": 5,
  "total_duration_seconds": 95.0,
  "word_count": 74,
  "snippets": [
    {"start": 4.0,  "duration": 6.0, "text": "A FASTQ record is four lines: id, sequence, a plus line, and the quality line."},
    {"start": 20.0, "duration": 6.0, "text": "The quality line encodes one Phred score per base, one ASCII character each."},
    {"start": 41.0, "duration": 6.0, "text": "We store the Phred score plus 33, so even a score of zero stays a visible character."},
    {"start": 62.0, "duration": 7.0, "text": "A Phred score of 40 becomes the character I, and it means a 1 in 10,000 chance of a wrong base."},
    {"start": 84.0, "duration": 6.0, "text": "If the quality line is not the same length as the sequence line, the file is corrupt."}
  ]
}
'''

FIXTURES = {
    "code/Snakefile": SNAKEFILE,
    "skill-fixture/SKILL.md": TOY_SKILL,
    "document/mini-sop.md": MINI_SOP,
    "media/transcript-timestamped.json": TRANSCRIPT,
}


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def check() -> int:
    manifest = {}
    manifest_path = HERE / "MANIFEST.tsv"
    for line in manifest_path.read_text().splitlines():
        if line.strip() and not line.startswith("#"):
            path, digest = line.split("\t")
            manifest[path] = digest
    ok = True
    for rel, content in FIXTURES.items():
        expected = manifest.get(rel)
        if expected is None:
            print(f"MISSING from MANIFEST.tsv: {rel}")
            ok = False
            continue
        on_disk = (HERE / rel)
        if not on_disk.exists():
            print(f"MISSING on disk: {rel}")
            ok = False
            continue
        if sha256(content) != expected:
            print(f"MANIFEST mismatch (regenerated != manifest): {rel}")
            ok = False
        if sha256(on_disk.read_text()) != expected:
            print(f"ON-DISK mismatch (file != manifest): {rel}")
            ok = False
        if sha256(on_disk.read_text()) != sha256(content):
            print(f"ON-DISK drift (file != regenerated): {rel}")
            ok = False
    for rel in manifest:
        if rel not in FIXTURES:
            print(f"STALE manifest entry: {rel}")
            ok = False
    print("FIXTURES-OK" if ok else "FIXTURES-FAILED")
    return 0 if ok else 1


def write() -> int:
    lines = ["# sha256 of fixture files — regenerate with: python3 make_fixtures.py --write"]
    for rel, content in FIXTURES.items():
        path = HERE / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        lines.append(f"{rel}\t{sha256(content)}")
        print(f"wrote {rel}")
    (HERE / "MANIFEST.tsv").write_text("\n".join(lines) + "\n")
    print("wrote MANIFEST.tsv")
    return 0


if __name__ == "__main__":
    sys.exit(write() if "--write" in sys.argv else check())
