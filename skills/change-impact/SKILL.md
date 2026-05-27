---
name: change-impact
description: Analyze changes across standards, regulations, policy notices, and document versions. Use when PI agent needs to detect source changes, compare versions, identify affected provisions/topics/entities, or prepare a change impact packet for review.
---

# Change Impact

Use this skill when a source, version, or document family has changed.

## Workflow

1. Confirm old and new source manifest records.
2. Compare document metadata first: issuer, status, publication date, effective
   date, replacement relation, and official locator.
3. Compare provisions by stable locator before using semantic similarity.
4. Classify changes as added, removed, modified, renumbered, clarified, or
   unknown.
5. Identify affected topics, entities, controls, evidence, and answer packets.
6. Produce review tasks for high-risk or low-confidence changes.

## Quality Gate

- Do not mark a change as substantive without evidence.
- Preserve both old and new citations.
- Escalate replacement and effective-date uncertainty.
- Generate review tasks when affected compliance evidence exists.

## Output

Change packet schema will be added in P2. Until then, use a JSON object with:

- `change_id`
- `source_ids`
- `version_relation`
- `changed_provisions`
- `affected_topics`
- `review_tasks`
- `confidence`
