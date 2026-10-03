"""Intent analysis (HEURISTIC PROTOTYPE).

Compares what the user asked for with what the agent now proposes to do, using
simple keyword matching. This is not a semantic model and is easy to evade; it
exists to demonstrate where an intent-deviation signal fits in the pipeline.

Rules:
  * read-only user intent + risky proposed action -> 85
  * risky proposed action (otherwise)             -> 60
  * anything else                                 -> 10

Assumption added by this prototype: if the user's own request already contains a
risky verb ("send the contract..."), the user asked for that kind of action, so
the intent is not treated as read-only.
"""

import re

RISKY_ACTION_TERMS = frozenset({
    "send", "sends", "sending", "sent",
    "delete", "deletes", "deleting", "deleted",
    "transfer", "transfers", "transferring", "transferred",
    "share", "shares", "sharing", "shared",
    "publish", "publishes", "publishing", "published",
    "execute", "executes", "executing", "executed",
    "modify", "modifies", "modifying", "modified",
    "change", "changes", "changing", "changed",
    "upload", "uploads", "uploading", "uploaded",
    "forward", "forwards", "forwarding", "forwarded",
})

READ_ONLY_INTENT_TERMS = frozenset({
    "summarize", "summarizes", "summarizing", "summarise", "summary", "summaries",
    "read", "reads", "reading",
    "analyze", "analyzes", "analyzing", "analyse", "analyses", "analysing",
    "review", "reviews", "reviewing",
    "inspect", "inspects", "inspecting",
    "find", "finds", "finding",
    "search", "searches", "searching",
})

INTENT_DEVIATION_READONLY_VS_RISKY = 85
INTENT_DEVIATION_RISKY = 60
INTENT_DEVIATION_NONE = 10


def _tokens(text):
    return re.findall(r"[a-z]+", (text or "").lower())


def find_terms(text, vocabulary):
    """Return the sorted vocabulary terms that appear as whole words in text."""
    return sorted(set(_tokens(text)) & vocabulary)


def analyze_intent(user_intent, proposed_action):
    """Return the intent-deviation score plus the terms that triggered it."""
    risky_in_action = find_terms(proposed_action, RISKY_ACTION_TERMS)
    risky_in_intent = find_terms(user_intent, RISKY_ACTION_TERMS)
    readonly_in_intent = find_terms(user_intent, READ_ONLY_INTENT_TERMS)

    read_only_intent = bool(readonly_in_intent) and not risky_in_intent

    if read_only_intent and risky_in_action:
        score, label = INTENT_DEVIATION_READONLY_VS_RISKY, "read-only intent vs risky action"
    elif risky_in_action:
        score, label = INTENT_DEVIATION_RISKY, "risky action"
    else:
        score, label = INTENT_DEVIATION_NONE, "no deviation detected"

    return {
        "score": score,
        "label": label,
        "read_only_intent": read_only_intent,
        "risky_terms_in_action": risky_in_action,
        "read_only_terms_in_intent": readonly_in_intent,
    }


def calculate_intent_deviation(user_intent, proposed_action):
    """Return only the intent-deviation score (10, 60 or 85)."""
    return analyze_intent(user_intent, proposed_action)["score"]
