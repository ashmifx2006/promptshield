"""PromptShield Flask application (research/demo prototype)."""

import os

from flask import Flask, jsonify, render_template, request

from backend.action_sensitivity import ACTION_LABELS, ACTION_SENSITIVITY, ACTION_TYPES
from backend.evaluator import run_evaluation
from backend.permission_checker import PERMISSION_RISK, PERMISSION_STATES
from backend.risk_engine import HIGH_THRESHOLD, MEDIUM_THRESHOLD, WEIGHTS
from backend.scenarios import SCENARIOS
from backend.security_analyzer import analyze_agent_action
from backend.source_trust import SOURCE_RISK, SOURCE_TYPES

try:
    from flask_cors import CORS
except ImportError:  # pragma: no cover - flask-cors is listed in requirements.txt
    CORS = None


def create_app():
    app = Flask(__name__)

    if CORS is not None:
        CORS(app)
    else:
        @app.after_request
        def _basic_cors(response):
            response.headers.setdefault("Access-Control-Allow-Origin", "*")
            response.headers.setdefault("Access-Control-Allow-Headers", "Content-Type")
            response.headers.setdefault("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            return response

    @app.route("/")
    def dashboard():
        return render_template(
            "index.html",
            weights=WEIGHTS,
            medium_threshold=MEDIUM_THRESHOLD,
            high_threshold=HIGH_THRESHOLD,
            source_risk=SOURCE_RISK,
            action_sensitivity=ACTION_SENSITIVITY,
            permission_risk=PERMISSION_RISK,
        )

    @app.route("/simulator")
    def simulator():
        return render_template(
            "simulator.html",
            source_types=SOURCE_TYPES,
            action_types=ACTION_TYPES,
            action_labels=ACTION_LABELS,
            permission_states=PERMISSION_STATES,
        )

    @app.route("/api/analyze", methods=["POST"])
    def api_analyze():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object"}), 400
        required = ("user_intent", "proposed_action", "source_type", "action_type", "permission_status")
        missing = [name for name in required if name not in payload]
        if missing:
            return jsonify({"error": f"Missing required field(s): {', '.join(missing)}"}), 400
        try:
            result = analyze_agent_action(*(payload[name] for name in required))
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify(result)

    @app.route("/api/evaluate")
    def api_evaluate():
        return jsonify(run_evaluation())

    @app.route("/api/scenarios")
    def api_scenarios():
        return jsonify({"scenarios": SCENARIOS})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=False)
