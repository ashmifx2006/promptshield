"""
Action Sensitivity Analyzer

Prototype module for estimating how sensitive or potentially
dangerous an AI-agent action is.
"""

from typing import Dict


# Prototype action-sensitivity mapping.
ACTION_SENSITIVITY = {
    "read": 10,
    "search": 10,
    "summarize": 15,
    "analyze": 20,
    "create": 25,
    "modify": 45,
    "send_email": 65,
    "upload": 70,
    "share_data": 75,
    "delete": 90,
    "execute_command": 95,
    "transfer_data": 95,
    "change_permissions": 100,
    "unknown": 60,
}


def analyze_action(action_type: str) -> Dict:
    """
    Estimate the sensitivity of a proposed AI-agent action.

    This is a prototype heuristic and does not represent
    a validated production security classification.
    """

    action = action_type.lower().strip()

    action_sensitivity = ACTION_SENSITIVITY.get(
        action,
        ACTION_SENSITIVITY["unknown"]
    )

    return {
        "action_type": action_type,
        "action_sensitivity": action_sensitivity,
    }


if __name__ == "__main__":
    result = analyze_action("send_email")

    print("Action Sensitivity Analysis")
    print("---------------------------")
    print(f"Action Type: {result['action_type']}")
    print(f"Action Sensitivity: {result['action_sensitivity']}")