# PI-Agent Contract

The PI agent is a thin harness. It coordinates work but does not hide policy or
domain workflow inside ad hoc prompts.

## Required Loop

For every task:

1. Identify the requested outcome.
2. Select one primary skill from `skills/index.json`.
3. Load that skill's `SKILL.md`.
4. Read only the extra references or source files needed for the task.
5. Produce artifacts that match the relevant schemas.
6. Run validation.
7. Write a run log.
8. Propose a skill update when the task reveals a reusable improvement.

## Inputs

The PI agent should pass each skill a task packet:

```json
{
  "task_id": "human-or-system-task-id",
  "requested_outcome": "plain-language outcome",
  "source_refs": [],
  "constraints": [],
  "allowed_outputs": []
}
```

## Outputs

Each run should produce at least one of:

- `source_manifest` records
- `provision` records
- `answer_packet` records
- `change_packet` records
- `compliance_checklist` records
- `skill_run_log` records

## Guardrails

- Do not treat candidate content as reviewed or verified.
- Do not redistribute restricted standards text in public artifacts.
- Do not answer without citations when the question depends on source text.
- Do not mix draft, superseded, and effective versions without saying so.
- Do not convert interpretation into primary law or primary standard text.

## Handoff Format

When GitHub work is needed, the PI agent should hand a concrete request to the
GitHub operator:

```text
Please create/update repo <name>.
Push artifact <attachment or branch>.
Open issue/PR with title <title>.
Use this summary and validation log: <summary>.
```
