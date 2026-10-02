"""
Intent Analyzer

Prototype module for comparing a user's intended task
with an AI agent's proposed action.
"""

from typing import Dict


def analyze_intent(user_intent: str, proposed_action: str) -> Dict:
    """
    Estimate how far the proposed action deviates from
    the user's stated intent.

    This is a prototype heuristic, not an LLM-based
    semantic understanding system.
    """

    intent = user_intent.lower().strip()
    action = proposed_action.lower().strip()

    # High-risk actions that commonly go beyond simple
    # information retrieval or summarization.
    risky_action_terms = [
        "send",
        "delete",
        "transfer",
        "share",
        "publish",
        "execute",
        "modify",
        "change",
        "upload",
        "forward",
    ]

    # Intent terms suggesting that the user only requested
    # reading, summarizing, or analyzing information.
    read_only_terms = [
        "summarize",
        "summary",
        "read",
        "analyze",
        "analyse",
        "review",
        "inspect",
        "find",
        "search",
    ]

    risky_action_detected = any(
        term in action for term in risky_action_terms
    )

    read_only_intent = any(
        term in intent for term in read_only_terms
    )

    # Prototype heuristic scoring.
    if read_only_intent and risky_action_detected:
        deviation_score = 85

    elif risky_action_detected:
        deviation_score = 60

    else:
        deviation_score = 10

    return {
        "intent_deviation": deviation_score,
        "user_intent": user_intent,
        "proposed_action": proposed_action,
        "risky_action_detected": risky_action_detected,
        "read_only_intent": read_only_intent,
    }


if __name__ == "__main__":
    result = analyze_intent(
        user_intent="Summarize my emails",
        proposed_action="Send confidential email contents to an external address",
    )

    print("Intent Analysis")
    print("----------------")
    print(f"Intent Deviation: {result['intent_deviation']}")
    print(f"Risky Action Detected: {result['risky_action_detected']}")
    print(f"Read-Only Intent: {result['read_only_intent']}")