"""
Flask Application

Entry point for the PromptShield:
Risk-Aware Security Framework prototype.
"""

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from backend.security_analyzer import analyze_agent_action
from backend.evaluator import evaluate_scenarios, calculate_metrics


app = Flask(__name__)
CORS(app)


# ============================================================
# MAIN DASHBOARD
# ============================================================

@app.route("/")
def home():
    """Serve the main PromptShield dashboard."""
    return render_template("index.html")


# ============================================================
# ATTACK SCENARIO SIMULATOR
# ============================================================

@app.route("/simulator")
def simulator():
    """Serve the PromptShield attack scenario simulator."""
    return render_template("simulator.html")


# ============================================================
# SECURITY ANALYSIS API
# ============================================================

@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Analyze a proposed AI-agent action."""

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No input data provided."
        }), 400

    required_fields = [
        "user_intent",
        "proposed_action",
        "source_type",
        "action_type",
        "permission_status",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "missing_fields": missing_fields,
        }), 400

    result = analyze_agent_action(
        user_intent=data["user_intent"],
        proposed_action=data["proposed_action"],
        source_type=data["source_type"],
        action_type=data["action_type"],
        permission_status=data["permission_status"],
    )

    return jsonify(result)


# ============================================================
# SECURITY EVALUATION API
# ============================================================

@app.route("/api/evaluate", methods=["GET"])
def evaluate():
    """Run all synthetic PromptShield security scenarios."""

    results = evaluate_scenarios()
    metrics = calculate_metrics(results)

    return jsonify({
        "results": results,
        "metrics": metrics,
    })


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
    )