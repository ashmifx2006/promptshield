"""Risk engine: weighted combination of the four factor scores.

PROTOTYPE ASSUMPTION: the weights and thresholds below are illustrative choices,
not scientifically validated values.

    Risk = 0.35 * IntentDeviation
         + 0.20 * SourceRisk
         + 0.25 * ActionSensitivity
         + 0.20 * PermissionRisk
"""

WEIGHTS = {
    "intent_deviation": 0.35,
    "source_risk": 0.20,
    "action_sensitivity": 0.25,
    "permission_risk": 0.20,
}

# Scores below MEDIUM_THRESHOLD are LOW; below HIGH_THRESHOLD are MEDIUM; the rest HIGH.
MEDIUM_THRESHOLD = 40
HIGH_THRESHOLD = 70


def clamp_score(value, low=0.0, high=100.0):
    """Clamp a numeric score into [low, high]."""
    value = float(value)
    return max(low, min(high, value))


def weighted_contributions(intent_deviation, source_risk, action_sensitivity, permission_risk):
    """Return each factor's weighted contribution to the final risk score."""
    scores = {
        "intent_deviation": clamp_score(intent_deviation),
        "source_risk": clamp_score(source_risk),
        "action_sensitivity": clamp_score(action_sensitivity),
        "permission_risk": clamp_score(permission_risk),
    }
    return {name: round(WEIGHTS[name] * score, 4) for name, score in scores.items()}


def calculate_risk(intent_deviation, source_risk, action_sensitivity, permission_risk):
    """Compute the overall risk score (0-100), rounded to 2 decimal places.

    Each input is clamped to 0-100 before weighting.
    """
    total = (
        WEIGHTS["intent_deviation"] * clamp_score(intent_deviation)
        + WEIGHTS["source_risk"] * clamp_score(source_risk)
        + WEIGHTS["action_sensitivity"] * clamp_score(action_sensitivity)
        + WEIGHTS["permission_risk"] * clamp_score(permission_risk)
    )
    return round(total, 2)


def risk_level(score):
    """Map a risk score to LOW (0-39), MEDIUM (40-69) or HIGH (70-100)."""
    score = clamp_score(score)
    if score < MEDIUM_THRESHOLD:
        return "LOW"
    if score < HIGH_THRESHOLD:
        return "MEDIUM"
    return "HIGH"
