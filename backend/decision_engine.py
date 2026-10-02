"""
Decision Engine

Combines the risk components and determines whether
an AI-agent action should be allowed, reviewed, or blocked.
"""

from typing import Dict

from backend.risk_engine import calculate_risk, get_risk_level

def make_decision(
    intent_deviation: float,
    source_risk: float,
    action_sensitivity: float,
    permission_risk: float,
) -> Dict:
    """
    Calculate overall risk and convert it into
    an ALLOW, REVIEW, or BLOCK decision.
    """

    risk_result = calculate_risk(
        intent_deviation=intent_deviation,
        source_risk=source_risk,
        action_sensitivity=action_sensitivity,
        permission_risk=permission_risk,
    )

    risk_score = risk_result["risk_score"]
    risk_level = get_risk_level(risk_score)

    # Prototype decision thresholds.
    if risk_score < 40:
        decision = "ALLOW"

    elif risk_score < 70:
        decision = "REVIEW"

    else:
        decision = "BLOCK"

    return {
        "decision": decision,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "component_scores": risk_result["component_scores"],
    }


if __name__ == "__main__":
    result = make_decision(
        intent_deviation=85,
        source_risk=45,
        action_sensitivity=65,
        permission_risk=90,
    )

    print("Security Decision")
    print("-----------------")
    print(f"Risk Score: {result['risk_score']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Decision: {result['decision']}")
    print("Component Scores:")

    for name, score in result["component_scores"].items():
        print(f"  {name}: {score}")