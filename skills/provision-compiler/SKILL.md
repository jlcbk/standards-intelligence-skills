---
name: provision-compiler
description: Compile standards, regulations, and policy documents into clause-level provisions with citations, locators, review status, and version metadata. Use when PI agent needs to transform source text into structured provisions, split clauses, preserve numbering, or prepare reviewed knowledge artifacts.
---

# Provision Compiler

Use this skill after source intake is complete and the agent is allowed to
process the source content.

## Workflow

1. Confirm the source manifest permits the intended processing.
2. Preserve document hierarchy: part, chapter, section, clause, annex, table,
   figure, and note.
3. Split by logical provisions, not arbitrary token chunks.
4. Assign stable IDs using document family and clause locator when possible.
5. Keep `review_status` as `candidate` unless a human or approved review step has
   checked the output.
6. Record source locator, version status, effective date, and extraction notes.
7. Emit records matching `schemas/provision.schema.json`.

## Quality Gate

- Each provision has a source ID and locator.
- Each normative statement keeps conditions and exceptions near the statement.
- Tables and annexes are marked when extraction confidence is low.
- Candidate provisions are not mixed with reviewed provisions in final answers.

## Output

Use `schemas/provision.schema.json`.
