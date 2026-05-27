# Compliance Workflow

Compliance workflow turns reviewed provisions into work that can be assigned,
evidenced, checked, and audited.

## Checklist Item Shape

Each checklist item should preserve:

- the requirement summary;
- cited provision IDs;
- the control or check to perform;
- concrete evidence required;
- owner role;
- status;
- unresolved applicability questions;
- acceptance criteria.

## Status Model

Recommended item statuses:

- `todo`: item has not started.
- `in_progress`: evidence is being collected.
- `reviewed`: evidence has been checked by the workflow.
- `blocked`: missing source text, missing evidence, or missing decision.
- `not_applicable`: scoped out with a reason.

## Public Demo Boundary

Public demo checklists can show workflow shape with synthetic provisions. They
must not claim that a vehicle, product, or process complies with a real
standard. Real compliance use requires authorized source text and human review.

## Promotion Rule

Only promote a checklist from draft to approved when:

1. every item cites reviewed or verified provisions;
2. every item has concrete evidence or a documented reason it is not applicable;
3. unresolved issues are closed or explicitly accepted by a responsible human.
