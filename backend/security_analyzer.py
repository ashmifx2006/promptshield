"""Central entry point: analyze one proposed AI-agent action before tool execution."""

from .action_sensitivity import get_action_sensitivity
from .decision_engine import decide
from .intent_analyzer import analyze_intent
from .permission_checker import get_permission_risk
from .risk_engine import calculate_risk, risk_level, weighted_contributions
from .source_trust import get_source_risk

FACTOR_LABELS = {
    "intent_deviation": "intent deviation",
    "source_risk": "source risk",
    "action_sensitivity": "action sensitivity",
    "permission_risk": "permission risk",
}


def _require_text(name, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"'{name}' is required and must be a non-empty string")
    return value.strip()


def _build_explanation(decision, score, level, factors, intent_detail, contributions):
    parts = []
    if intent_detail["read_only_intent"] and intent_detail["risky_terms_in_action"]:
        parts.append(
            "The request looks read-only, but the proposed action uses risky verbs "
            f"({', '.join(intent_detail['risky_terms_in_action'])})."
        )
    elif intent_detail["risky_terms_in_action"]:
        parts.append(
            "The proposed action uses risky verbs "
            f"({', '.join(intent_detail['risky_terms_in_action'])})."
        )
    else:
        parts.append("No risky verbs were found in the proposed action.")

    top = sorted(contributions.items(), key=lambda kv: kv[1], reverse=True)[:2]
    drivers = ", ".join(
        f"{FACTOR_LABELS[name]} ({factors[name]:g} -> {value:.2f} points)" for name, value in top
    )
    parts.append(f"Largest contributors: {drivers}.")
    parts.append(
        f"Weighted risk is {score:.2f} ({level}), so the decision is {decision}. "
        "The decision uses the complete score, not any single factor."
    )
    parts.append("Prototype heuristics only; not a guarantee of security.")
    return " ".join(parts)


def analyze_agent_action(user_intent, proposed_action, source_type, action_type, permission_status):
    """Evaluate a proposed agent action and return a structured result.

    Raises ValueError for empty text fields or unsupported category values.
    """
    user_intent = _require_text("user_intent", user_intent)
    proposed_action = _require_text("proposed_action", proposed_action)

    intent_detail = analyze_intent(user_intent, proposed_action)
    factors = {
        "intent_deviation": intent_detail["score"],
        "source_risk": get_source_risk(source_type),
        "action_sensitivity": get_action_sensitivity(action_type),
        "permission_risk": get_permission_risk(permission_status),
    }

    score = calculate_risk(**factors)
    level = risk_level(score)
    decision = decide(score)
    contributions = weighted_contributions(**factors)

    return {
        "decision": decision,
        "risk_score": score,
        "risk_level": level,
        "intent_deviation": factors["intent_deviation"],
        "source_risk": factors["source_risk"],
        "action_sensitivity": factors["action_sensitivity"],
        "permission_risk": factors["permission_risk"],
        "contributions": contributions,
        "explanation": _build_explanation(
            decision, score, level, factors, intent_detail, contributions
        ),
    }
