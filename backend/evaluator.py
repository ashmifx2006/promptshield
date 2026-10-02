"""
Security Evaluation Engine

Runs synthetic AI-agent attack scenarios through the
Risk-Aware Security Framework and calculates
prototype evaluation metrics.
"""

from backend.security_analyzer import analyze_agent_action
from backend.scenarios import get_scenarios
from backend.security_analyzer import analyze_agent_action

def evaluate_scenarios():
    """
    Run every scenario through the security analyzer.
    """

    scenarios = get_scenarios()
    results = []

    for scenario in scenarios:
        analysis = analyze_agent_action(
            user_intent=scenario["user_intent"],
            proposed_action=scenario["proposed_action"],
            source_type=scenario["source_type"],
            action_type=scenario["action_type"],
            permission_status=scenario["permission_status"],
        )

        decision = analysis["decision"]

        results.append({
            "id": scenario["id"],
            "name": scenario["name"],
            "attack_type": scenario["attack_type"],
            "risk_score": decision["risk_score"],
            "risk_level": decision["risk_level"],
            "decision": decision["decision"],
        })

    return results


def calculate_metrics(results):
    """
    Calculate basic prototype evaluation metrics.
    """

    total = len(results)

    allow_count = sum(
        result["decision"] == "ALLOW"
        for result in results
    )

    review_count = sum(
        result["decision"] == "REVIEW"
        for result in results
    )

    block_count = sum(
        result["decision"] == "BLOCK"
        for result in results
    )

    high_risk_count = sum(
        result["risk_level"] == "HIGH"
        for result in results
    )

    attack_results = [
        result
        for result in results
        if result["attack_type"] != "Benign"
    ]

    benign_results = [
        result
        for result in results
        if result["attack_type"] == "Benign"
    ]

    attacks_blocked = sum(
        result["decision"] == "BLOCK"
        for result in attack_results
    )

    benign_allowed = sum(
        result["decision"] == "ALLOW"
        for result in benign_results
    )

    average_risk = (
        sum(result["risk_score"] for result in results) / total
        if total > 0
        else 0
    )

    return {
        "total_scenarios": total,
        "allow_count": allow_count,
        "review_count": review_count,
        "block_count": block_count,
        "high_risk_count": high_risk_count,
        "attack_scenarios": len(attack_results),
        "attacks_blocked": attacks_blocked,
        "benign_scenarios": len(benign_results),
        "benign_allowed": benign_allowed,
        "average_risk": round(average_risk, 2),
    }


if __name__ == "__main__":
    results = evaluate_scenarios()
    metrics = calculate_metrics(results)

    print("Security Evaluation")
    print("===================")

    for result in results:
        print(
            f"{result['id']}. "
            f"{result['name']} | "
            f"Risk: {result['risk_score']} | "
            f"Level: {result['risk_level']} | "
            f"Decision: {result['decision']}"
        )

    print("\nEvaluation Metrics")
    print("==================")
    print(f"Total Scenarios: {metrics['total_scenarios']}")
    print(f"ALLOW: {metrics['allow_count']}")
    print(f"REVIEW: {metrics['review_count']}")
    print(f"BLOCK: {metrics['block_count']}")
    print(f"High-Risk Scenarios: {metrics['high_risk_count']}")
    print(f"Attack Scenarios: {metrics['attack_scenarios']}")
    print(f"Attacks Blocked: {metrics['attacks_blocked']}")
    print(f"Benign Scenarios: {metrics['benign_scenarios']}")
    print(f"Benign Scenarios Allowed: {metrics['benign_allowed']}")
    print(f"Average Risk Score: {metrics['average_risk']}")