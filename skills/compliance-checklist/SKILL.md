---
name: compliance-checklist
description: Convert reviewed provisions and requirements into compliance checklist items, controls, evidence requests, owners, due dates, and review status. Use when PI agent needs to connect standards intelligence to a practical compliance workflow.
---

# Compliance Checklist

Use this skill to turn reviewed provisions into actionable compliance work.

## Workflow

1. Start only from reviewed or verified provisions unless the user explicitly
   asks for a draft checklist.
2. Extract requirement fields: subject, action, object, condition, exception,
   evidence, frequency, and responsible role.
3. Map each requirement to one or more controls.
4. Define required evidence and acceptance criteria.
5. Track owner, due date, status, and unresolved questions.
6. Preserve provision citations on every checklist item.

## Quality Gate

- Each checklist item traces to a provision.
- Evidence requirements are concrete and inspectable.
- Ambiguous applicability is marked for review.
- Draft checklists do not claim final compliance.

## Output

Compliance checklist schema will be added in P3. Until then, use a JSON object
with:

- `checklist_id`
- `scope`
- `items`
- `citations`
- `unresolved_issues`
