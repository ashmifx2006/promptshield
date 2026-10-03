"""Action sensitivity analysis.

Deterministic lookup from an action category to a sensitivity score (0-100).

PROTOTYPE ASSUMPTIONS: values are illustrative. Bands: low < 40, medium 40-69,
high >= 70. Ordinary send/share/forward sits at the top of the medium band;
sending sensitive information, deleting, publishing, transferring and privileged
operations sit in the high band.
"""

ACTION_SENSITIVITY = {
    # Low sensitivity
    "search": 10,
    "read": 10,
    "summarize": 10,
    "inspect": 10,
    # Medium sensitivity
    "modify": 60,
    "upload": 60,
    "execute": 60,
    "send": 65,
    "share": 65,
    "forward": 65,
    # High sensitivity
    "delete": 90,
    "publish": 90,
    "transfer": 95,
    "send_sensitive": 95,
    "privileged": 95,
}

ACTION_TYPES = tuple(ACTION_SENSITIVITY)

ACTION_LABELS = {
    "send_sensitive": "send sensitive information",
    "privileged": "privileged operation",
}


def normalize(value):
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def get_action_sensitivity(action_type):
    """Return the sensitivity score for an action category."""
    key = normalize(action_type)
    if key not in ACTION_SENSITIVITY:
        raise ValueError(
            f"Unsupported action_type '{action_type}'. Valid values: {', '.join(ACTION_TYPES)}"
        )
    return ACTION_SENSITIVITY[key]
