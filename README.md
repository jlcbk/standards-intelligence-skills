# Standards Intelligence Skills

`standards-intelligence-skills` is a lightweight skill pack for standards and
regulatory intelligence work. It is designed to replace a heavy always-on agent
with a thin PI-agent harness plus durable skills, schemas, and quality gates.

The project is inspired by the lessons from `standards-llm-wiki`: keep the
valuable clause-level regulatory intelligence model, but move repeated agent
behavior into reusable skills and machine-checkable artifacts.

## Core Idea

Use this repo as a "fat skills, thin harness" layer:

- **Thin PI agent**: routes a task, loads the relevant skill, calls tools, and
  writes a run log.
- **Fat skills**: preserve domain workflow, guardrails, expected inputs, and
  quality gates in `skills/*/SKILL.md`.
- **Fat data**: persist source manifests, provisions, answer packets, change
  packets, and run logs as JSON/JSONL.
- **Fat code**: keep validation and repetitive transformations in scripts or
  library code instead of prompt text.

## What This Repo Does First

The initial version focuses on five workflows:

1. `source-intake`: register sources without violating access or redistribution
   boundaries.
2. `provision-compiler`: compile documents into clause-level provisions.
3. `regulatory-answer`: answer questions with citations and version safety.
4. `change-impact`: turn source/version changes into impact packets.
5. `compliance-checklist`: map provisions to controls and evidence.

It intentionally does not ship copyrighted standards text. Public examples are
synthetic and small.

The initial durable artifact contracts cover source manifests, provisions,
answer packets, change packets, coverage reports, and skill run logs.

## Repository Layout

```text
skills/       Reusable PI-agent skills
schemas/      JSON Schema contracts for durable artifacts
examples/     Small synthetic examples for validation
demos/        End-to-end demo packages with safe source boundaries
docs/         Architecture, PI-agent contract, policies, roadmap
src/          Small stdlib CLI
tests/        Validation tests
```

## Quick Start

```bash
python3.10 -m venv .venv
. .venv/bin/activate
pip install -e .
standards-skills list
standards-skills validate
python -m unittest discover -s tests
```

Without installing the package:

```bash
PYTHONPATH=src python -m standards_intelligence_skills.cli list
PYTHONPATH=src python -m standards_intelligence_skills.cli validate
```

## PI-Agent Usage Pattern

1. Read the task and choose one skill from `skills/index.json`.
2. Load that skill's `SKILL.md`.
3. Produce artifacts that match `schemas/*.schema.json`.
4. Run `standards-skills validate`.
5. Write a run log with `standards-skills new-run-log`.
6. If the task succeeded, consider whether the skill itself should be improved.

See [docs/pi-agent-contract.md](docs/pi-agent-contract.md).

## Demo Packages

The first demo package is [demos/gb-vehicle-safety](demos/gb-vehicle-safety).
It uses official metadata for GB 7258-2017 and GB 1589-2016, then adds
synthetic/paraphrased provisions and answer packets to exercise the workflow
without storing standards PDF text or large verbatim standard excerpts.

## Safety Boundary

This project is a research and workflow assistant. It is not legal advice, a
certification authority, or a public redistribution channel for copyrighted
standards. The default rule is metadata-only public storage and private
bring-your-own-document processing for restricted standards.

See [docs/source-access-policy.md](docs/source-access-policy.md).
