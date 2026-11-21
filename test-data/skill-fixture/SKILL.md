---
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
