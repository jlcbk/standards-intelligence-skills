# Answer Contract

A regulatory or standards answer must be useful, traceable, and honest about
uncertainty.

## Required Sections

1. **Short answer**: direct conclusion.
2. **Scope**: jurisdiction, document family, product/process, version, and date.
3. **Citations**: provision IDs and source locators.
4. **Conditions and exceptions**: explicit qualifiers.
5. **Version safety**: current, draft, superseded, unknown, or mixed.
6. **Unresolved issues**: missing source, low confidence, or review needed.

## Forbidden Patterns

- No uncited normative conclusion.
- No citation to candidate-only content unless the answer is clearly marked as
  provisional.
- No mixing versions without marking the answer as mixed-version.
- No legal or certification sign-off language.

## Recommended Output

Use `schemas/answer-packet.schema.json` for durable answers. A human-facing
answer can be generated from the packet after validation.
