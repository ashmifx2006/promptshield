"""
Risk-Aware Security Engine

Prototype risk model for evaluating AI-agent actions.

Risk =
    0.35 * Intent Deviation
    + 0.20 * Source Risk
    + 0.25 * Action Sensitivity
    + 0.20 * Permission Risk

Scores are normalized from 0 to 100.
"""

from typing import Dict


# Prototype weights
WEIGHTS = {
    "intent_deviation": 0.35,
    "source_risk": 0.20,
    "action_sensitivity": 0.25,
    "permission_risk": 0.20,
}


def calculate_risk(
    intent_deviation: float,
    source_risk: float,
    action_sensitivity: float,
    permission_risk: float,
) -> Dict:
    """
    Calculate the overall risk score for a proposed AI-agent action.

    Each input should be between 0 and 100.
    """

    scores = {
        "intent_deviation": intent_deviation,
        "source_risk": source_risk,
        "action_sensitivity": action_sensitivity,
        "permission_risk": permission_risk,
    }

    # Keep scores within the valid range.
    scores = {
        key: max(0, min(100, value))
        for key, value in scores.items()
    }

    risk_score = (
        WEIGHTS["intent_deviation"] * scores["intent_deviation"]
        + WEIGHTS["source_risk"] * scores["source_risk"]
        + WEIGHTS["action_sensitivity"] * scores["action_sensitivity"]
        + WEIGHTS["permission_risk"] * scores["permission_risk"]
    )

    risk_score = round(risk_score, 2)

    return {
        "risk_score": risk_score,
        "component_scores": scores,
        "weights": WEIGHTS,
    }


def get_risk_level(risk_score: float) -> str:
    """
    Convert the risk score into a prototype risk level.
    """

    if risk_score < 40:
        return "LOW"

    if risk_score < 70:
        return "MEDIUM"

    return "HIGH"


if __name__ == "__main__":
    result = calculate_risk(
        intent_deviation=80,
        source_risk=90,
        action_sensitivity=95,
        permission_risk=85,
    )

    print("Risk Assessment")
    print("----------------")
    print(f"Risk Score: {result['risk_score']}")
    print(f"Risk Level: {get_risk_level(result['risk_score'])}")
    print("Component Scores:")
    
    for name, score in result["component_scores"].items():
        print(f"  {name}: {score}")