---
type: subagent-handoff-template
domain: qwen-code-pipeline
status: template
---

# <Task Title>

Use this template for non-trivial Qwen Code CLI pipeline tasks. Copy it to:

```text
docs/planning/subagent-handoff/<YYYY-MM-DD-task-slug>.md
```

The copied handoff artifact remains in the repository as durable task history.
It records execution evidence and decisions, but it is not a substitute for
`docs/specs/` when runtime contracts change.

## Status

- State: planning
- Branch/worktree:
- Main owner:
- Created:
- Last updated:
- PR:

Allowed states: `planning`, `implementing`, `blocked`, `architecture-review`,
`regulated-review`, `verifying`, `ready-for-pr`, `merged`.

## Source Of Truth

- Relevant specs:
- Relevant code:
- Relevant tests:
- Runtime boundaries:
- Forbidden shortcuts:

## Architecture Brief

Owned by: `principal-architect`

### Goal

-

### Non-Goals

-

### Baseline And Findings

- Accepted spec behavior:
- Current code behavior:
- Spec/code mismatch:
- Existing tests nearest to the behavior:

### Affected Contracts

- Runtime/API/state:
- Routing/policy/final-action:
- Prompt/LLM/RAG:
- Persistence/schema/idempotency:
- Audit/tracking/observability:
- Router/CRM/handoff:

### Allowed Edit Areas

- Implementation:
- Tests:
- Resources/config:
- Docs/specs:

### Required Harness

- Targeted commands:
- Broader commands:
- Manual/smoke checks:

### Acceptance Criteria

- Positive case:
- Negative/safety case:
- Public response expectations:
- State/audit/tracking expectations:

### Implementation Sequence

1.
2.
3.

### Open Risks Or Decisions

-

## Architecture Findings

Owned by: implementers raise findings; `principal-architect` resolves them.

| Status | Finding | Raised by | Resolution | Link |
|---|---|---|---|---|
| open | | | | |

Finding statuses: `open`, `accepted`, `rejected`, `resolved`, `deferred`.

## Implementation Notes

Owned by: `spring-runtime-implementer` or `rag-llm-prompt-specialist`

### Files Changed

-

### Tests Added Or Updated

-

### Commands Run

| Command | Result | Notes |
|---|---|---|
| | | |

### Deviations From Brief

-

### Blockers

-

## Regulated Flow Review

Owned by: `regulated-flow-reviewer`

### Review Scope

- Files reviewed:
- Specs reviewed:

### Checklist

- PII/raw dialogue exposure:
- Hidden prompt/internal policy exposure:
- Router handoff summary-only contract:
- CRM/tracking/audit payload sanitization:
- RAG evidence and no-answer handling:
- Cross-product RAG prevention:
- Final action/HITL boundary:
- Recommendations/suitability boundary:
- Inbound dialogue continuity-only invariant:

### Findings

| Severity | Finding | Required action | Status |
|---|---|---|---|
| | | | |

## Verification Evidence

Owned by: `verification-release-owner`

### Diff Scope

- Expected files:
- Unexpected files:
- Unrelated changes:

### Commands Run

| Command | Exit code | Result summary |
|---|---:|---|
| | | |

### Required Evidence Check

- Targeted tests:
- Full test suite:
- Static checks:
- Manual/smoke checks:
- Skipped checks and reason:

### PR Readiness

- Spec sections or deltas used:
- Behavior changed:
- Verification evidence included:
- Known gaps/open questions:
- Stacked PR dependency:

## Final Handoff

Owned by: main Qwen session owner

- Summary:
- Commit(s):
- PR:
- Residual risk:
- Follow-ups:
