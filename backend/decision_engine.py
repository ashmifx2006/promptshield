"""Decision engine: maps a risk level to ALLOW / REVIEW / BLOCK.

The decision depends on the complete risk score. No single factor (for example,
an unauthorized permission status) forces a BLOCK on its own.
"""

from .risk_engine import risk_level

DECISION_BY_LEVEL = {
    "LOW": "ALLOW",
    "MEDIUM": "REVIEW",
    "HIGH": "BLOCK",
}


def decide(score):
    """Return ALLOW, REVIEW or BLOCK for a risk score."""
    return DECISION_BY_LEVEL[risk_level(score)]
