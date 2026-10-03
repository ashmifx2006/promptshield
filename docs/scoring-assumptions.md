# Scoring assumptions

All values are prototype assumptions chosen for demonstration. None are scientifically validated.

## Intent deviation (`backend/intent_analyzer.py`)

Whole-word keyword matching, case-insensitive.

- Risky action terms: send, delete, transfer, share, publish, execute, modify, change, upload, forward (plus common inflections).
- Read-only intent terms: summarize/summary, read, analyze/analyse, review, inspect, find, search (plus common inflections).

| Condition | Score |
|---|---|
| User intent is read-only and the proposed action contains a risky term | 85 |
| Proposed action contains a risky term (otherwise) | 60 |
| Neither | 10 |

Added assumption: if the user's own text already contains a risky verb (for example "Review the draft and send it"), the intent is not treated as read-only.

## Source risk (`backend/source_trust.py`)

| Source | Risk | Rationale |
|---|---|---|
| trusted | 10 | direct user or first-party instruction |
| email | 45 | authored by third parties |
| webpage | 60 | arbitrary public content |
| tool_output | 70 | may embed third-party text |
| external_document | 80 | files from outside the organization |
| rag_document | 80 | retrieved chunks can carry planted instructions |
| unknown | 90 | provenance cannot be established |

## Action sensitivity (`backend/action_sensitivity.py`)

Lookup by action type.

| Band | Actions | Score |
|---|---|---|
| Low | search, read, summarize, inspect | 10 |
| Medium | modify, upload, execute | 60 |
| Medium (upper) | send, share, forward | 65 |
| High | delete, publish | 90 |
| High | transfer, send_sensitive, privileged | 95 |

Note: scenario 4 ("Destructive Action") uses action type `modify` (score 60) so that it reproduces the specified sub-scores. A direct `delete` would score 90.

## Permission risk (`backend/permission_checker.py`)

| Status | Risk |
|---|---|
| authorized | 5 |
| unknown | 50 |
| unauthorized | 90 |

Unauthorized does not force BLOCK; the decision depends on the full score.

## Combination and thresholds (`backend/risk_engine.py`)

Weights 0.35 / 0.20 / 0.25 / 0.20. LOW < 40, MEDIUM 40-69, HIGH >= 70. Each factor is clamped to 0-100 and the result is rounded to 2 decimals.
