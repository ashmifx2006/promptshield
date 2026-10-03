"""PromptShield backend: heuristic, risk-aware checks on proposed AI-agent actions.

Research/demo prototype. Weights, thresholds and detection rules are prototype
assumptions and are not scientifically validated.
"""

from .security_analyzer import analyze_agent_action  # noqa: F401

__all__ = ["analyze_agent_action"]
