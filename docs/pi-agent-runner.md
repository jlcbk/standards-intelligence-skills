# PI-Agent Runner

`standards-skills run-task` is a minimal runner prototype. It does not execute a
heavy agent. It only performs the repeatable harness steps that should stay
deterministic:

1. read a task packet;
2. select an existing skill by name;
3. optionally validate the repository;
4. write a skill run log;
5. print a machine-readable summary.

## Example

```bash
standards-skills run-task \
  --packet examples/task-packet.example.json \
  --validate \
  --output /tmp/standards-skill-run.json
```

## Task Packet

Use `schemas/task-packet.schema.json`.

```json
{
  "task_id": "task-demo-001",
  "requested_outcome": "Create a citation-backed demo answer packet.",
  "skill_name": "regulatory-answer",
  "source_refs": ["demos/gb-vehicle-safety"],
  "constraints": ["public demo only"],
  "allowed_outputs": ["answer_packet", "skill_run_log"]
}
```

## Design Boundary

The runner should remain thin:

- no model provider integration;
- no hidden policy logic;
- no automatic publication;
- no source text extraction.

Provider calls, document processing, and GitHub operations belong in separate
tools or agents. This runner only standardizes the local task packet and run log
contract.
