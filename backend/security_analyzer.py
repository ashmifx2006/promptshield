"""
Security Analyzer

Combines intent analysis, source trust, action sensitivity,
permission checking, and the risk-based decision engine.
"""

from backend.intent_analyzer import analyze_intent
from backend.source_trust import analyze_source
from backend.action_sensitivity import analyze_action
from backend.permission_checker import check_permission
from backend.decision_engine import make_decision

def analyze_agent_action(
    user_intent: str,
    proposed_action: str,
    source_type: str,
    action_type: str,
    permission_status: str,
) -> dict:
    """
    Perform a complete risk-aware security analysis
    of a proposed AI-agent action.
    """

    # Step 1: Analyze user's intent versus proposed action.
    intent_result = analyze_intent(
        user_intent,
        proposed_action,
    )

    # Step 2: Analyze the source of the information.
    source_result = analyze_source(source_type)

    # Step 3: Analyze how sensitive the proposed action is.
    action_result = analyze_action(action_type)

    # Step 4: Check authorization.
    permission_result = check_permission(permission_status)

    # Step 5: Combine all risk factors.
    decision_result = make_decision(
        intent_deviation=intent_result["intent_deviation"],
        source_risk=source_result["source_risk"],
        action_sensitivity=action_result["action_sensitivity"],
        permission_risk=permission_result["permission_risk"],
    )

    return {
        "intent_analysis": intent_result,
        "source_analysis": source_result,
        "action_analysis": action_result,
        "permission_analysis": permission_result,
        "decision": decision_result,
    }


if __name__ == "__main__":
    result = analyze_agent_action(
        user_intent="Summarize my emails",
        proposed_action="Send confidential email contents to an external address",
        source_type="email",
        action_type="send_email",
        permission_status="unauthorized",
    )

    print("Complete Security Analysis")
    print("===========================")

    print(f"Risk Score: {result['decision']['risk_score']}")
    print(f"Risk Level: {result['decision']['risk_level']}")
    print(f"Decision: {result['decision']['decision']}")

    print("\nComponent Scores:")
    print(
        f"  Intent Deviation: "
        f"{result['intent_analysis']['intent_deviation']}"
    )
    print(
        f"  Source Risk: "
        f"{result['source_analysis']['source_risk']}"
    )
    print(
        f"  Action Sensitivity: "
        f"{result['action_analysis']['action_sensitivity']}"
    )
    print(
        f"  Permission Risk: "
        f"{result['permission_analysis']['permission_risk']}"
    )