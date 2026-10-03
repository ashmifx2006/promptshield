"""Permission check.

Maps an authorization state to a permission-risk value (0-100).

PROTOTYPE ASSUMPTIONS: values are illustrative. An unauthorized action carries
high permission risk, but that alone does not force a BLOCK: the final decision
is based on the complete risk score.
"""

PERMISSION_RISK = {
    "authorized": 5,
    "unknown": 50,
    "unauthorized": 90,
}

PERMISSION_STATES = tuple(PERMISSION_RISK)


def normalize(value):
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def get_permission_risk(permission_status):
    """Return the permission-risk score for an authorization state."""
    key = normalize(permission_status)
    if key not in PERMISSION_RISK:
        raise ValueError(
            f"Unsupported permission_status '{permission_status}'. "
            f"Valid values: {', '.join(PERMISSION_STATES)}"
        )
    return PERMISSION_RISK[key]
