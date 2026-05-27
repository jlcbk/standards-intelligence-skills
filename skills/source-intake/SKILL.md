---
name: source-intake
description: Register standards, regulations, policy notices, and private documents for standards intelligence workflows. Use when PI agent needs to add or review a source, decide public/private handling, record provenance, hash/locator metadata, or prepare a source manifest before compiling clauses.
---

# Source Intake

Use this skill to create safe, traceable source records before any extraction or
question answering happens.

## Workflow

1. Identify the source owner, issuer, jurisdiction, document type, title,
   publication date, effective date, and official locator.
2. Classify access with `docs/source-access-policy.md`.
3. Assign a stable `source_id`.
4. Record retrieval metadata: URL/path, retrieved time, hash if available, byte
   size if available, and extractor notes.
5. Set `redistribution_policy` before storing any content.
6. Emit records matching `schemas/source-manifest.schema.json`.
7. If access is unknown or restricted, store metadata only in public artifacts.

## Quality Gate

- Every source has an issuer and locator.
- Every source has `access_level` and `redistribution_policy`.
- Restricted sources do not place full text in public paths.
- The run log records who made the access decision and why.

## Output

Write JSONL records shaped like:

```json
{
  "source_id": "src-demo-001",
  "title": "Synthetic vehicle safety notice",
  "source_type": "policy_notice",
  "issuer": "Example Authority",
  "jurisdiction": "EX",
  "access_level": "public_web",
  "redistribution_policy": "public_ok",
  "locator": {"url": "https://example.invalid/notice"},
  "retrieved_at": "2026-05-27T00:00:00Z"
}
```
