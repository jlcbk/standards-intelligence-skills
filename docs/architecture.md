# Architecture

This repo keeps the agent small and moves repeatable domain work into durable
assets.

## Layers

1. **PI-agent harness**
   - Accept a task.
   - Select and load a skill.
   - Execute tools or scripts.
   - Persist artifacts and a run log.

2. **Skills**
   - Describe one reusable workflow.
   - Include trigger conditions, inputs, outputs, guardrails, and quality gates.
   - Avoid embedding large reference corpora in the prompt.

3. **Schemas**
   - Define the durable outputs that later agents and tools can trust.
   - Keep outputs diffable, reviewable, and CI-checkable.

4. **Examples**
   - Provide minimal synthetic fixtures.
   - Never contain restricted standards text.

5. **Validation**
   - Check skill metadata and JSON artifacts.
   - Prevent silent drift in artifact contracts.

## Why Not a Heavy Agent

`standards-llm-wiki` showed that the domain needs provenance, version safety,
clause-level modeling, and evaluation. Those are durable capabilities, not a
reason to run a large autonomous agent all the time.

The intended model is:

```text
task -> PI agent -> skill -> code/schema/data -> validated artifact -> run log
```

The PI agent can remain interchangeable as long as it follows the contract in
`docs/pi-agent-contract.md`.
