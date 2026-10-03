"""Run the synthetic validation scenarios and compute summary metrics."""

import json
from pathlib import Path

from .scenarios import SCENARIOS
from .security_analyzer import analyze_agent_action

COMPONENTS = ("intent_deviation", "source_risk", "action_sensitivity", "permission_risk")


def run_scenario(scenario):
    """Analyze a single scenario and compare it with its expected values."""
    analysis = analyze_agent_action(
        scenario["user_intent"],
        scenario["proposed_action"],
        scenario["source_type"],
        scenario["action_type"],
        scenario["permission_status"],
    )
    expected = scenario["expected"]
    matches = analysis["decision"] == expected["decision"] and all(
        abs(analysis[key] - expected[key]) < 1e-9 for key in ("risk_score",) + COMPONENTS
    )
    return {
        "id": scenario["id"],
        "name": scenario["name"],
        "description": scenario["description"],
        "user_intent": scenario["user_intent"],
        "proposed_action": scenario["proposed_action"],
        "source_type": scenario["source_type"],
        "action_type": scenario["action_type"],
        "permission_status": scenario["permission_status"],
        **analysis,
        "expected_decision": expected["decision"],
        "expected_risk_score": expected["risk_score"],
        "matches_expected": matches,
    }


def run_evaluation(scenarios=None):
    """Run all scenarios. Returns {"results": [...], "metrics": {...}}."""
    results = [run_scenario(s) for s in (scenarios or SCENARIOS)]
    total = len(results)
    scores = [r["risk_score"] for r in results]
    metrics = {
        "total_scenarios": total,
        "allow_count": sum(r["decision"] == "ALLOW" for r in results),
        "review_count": sum(r["decision"] == "REVIEW" for r in results),
        "block_count": sum(r["decision"] == "BLOCK" for r in results),
        "average_risk_score": round(sum(scores) / total, 2) if total else 0.0,
        "matched_expected": sum(r["matches_expected"] for r in results),
        "data_note": "Results from synthetic prototype validation scenarios, not real-world data.",
    }
    return {"results": results, "metrics": metrics}


def save_results(path=None):
    """Write evaluation JSON to results/evaluation_results.json (or a given path)."""
    path = Path(path) if path else Path(__file__).resolve().parent.parent / "results" / "evaluation_results.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(run_evaluation(), indent=2), encoding="utf-8")
    return path


def save_chart(path=None):
    """Save a risk-score bar chart with matplotlib (imported lazily; optional at runtime)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    path = Path(path) if path else Path(__file__).resolve().parent.parent / "results" / "risk_scores.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = run_evaluation()["results"]
    colors = {"ALLOW": "#3fb27f", "REVIEW": "#e0a73a", "BLOCK": "#e5584f"}
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar([f"S{r['id']}" for r in data], [r["risk_score"] for r in data],
           color=[colors[r["decision"]] for r in data])
    ax.axhline(40, color="#888", linestyle="--", linewidth=0.8)
    ax.axhline(70, color="#888", linestyle="--", linewidth=0.8)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Risk score")
    ax.set_title("PromptShield: risk score per synthetic validation scenario")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


if __name__ == "__main__":
    print("Saved", save_results())
    try:
        print("Saved", save_chart())
    except ImportError:
        print("matplotlib not installed; skipped chart")
