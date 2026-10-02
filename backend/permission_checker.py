"""
Permission Checker

Prototype module for checking whether an AI-agent action
is authorized.
"""

from typing import Dict


# Prototype permission-risk mapping.
PERMISSION_RISK = {
    "authorized": 5,
    "user_approved": 10,
    "restricted": 60,
    "unauthorized": 90,
    "unknown": 70,
}


def check_permission(permission_status: str) -> Dict:
    """
    Estimate permission risk for a proposed agent action.

    This is a prototype heuristic and does not represent
    a production authorization system.
    """

    status = permission_status.lower().strip()

    permission_risk = PERMISSION_RISK.get(
        status,
        PERMISSION_RISK["unknown"]
    )

    return {
        "permission_status": permission_status,
        "permission_risk": permission_risk,
    }


if __name__ == "__main__":
    result = check_permission("unauthorized")

    print("Permission Analysis")
    print("-------------------")
    print(f"Permission Status: {result['permission_status']}")
    print(f"Permission Risk: {result['permission_risk']}")