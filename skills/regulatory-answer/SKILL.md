---
name: regulatory-answer
description: Answer questions about standards, regulations, policy notices, provisions, applicability, dates, exceptions, and compliance implications using citation-backed answer packets. Use when PI agent needs to produce a traceable answer with version safety and unresolved issues.
---

# Regulatory Answer

Use this skill to answer a user or workflow question from structured provisions
and source manifests.

## Workflow

1. Restate the question as a scoped query: jurisdiction, document family,
   product/process, date, and version constraints.
2. Search reviewed or verified provisions first.
3. Use candidate provisions only when explicitly allowed and label the answer as
   provisional.
4. Separate primary source text, interpretation, and workflow recommendation.
5. Build an answer packet with citations, conditions, exceptions, version status,
   confidence, and unresolved issues.
6. If source coverage is incomplete, say what is missing instead of guessing.

## Quality Gate

- Every normative answer has at least one citation.
- Version status is explicit.
- Conditions and exceptions are not omitted.
- The answer does not claim legal or certification sign-off.

## Output

Use `schemas/answer-packet.schema.json`.
