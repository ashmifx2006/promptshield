(function () {
  "use strict";

  var FIELDS = ["user_intent", "proposed_action", "source_type", "action_type", "permission_status"];
  var scenarios = [];

  function $(id) { return document.getElementById(id); }

  function showError(message) {
    var box = $("error");
    box.textContent = message;
    box.hidden = !message;
  }

  function showResult(r) {
    var cls = r.decision.toLowerCase();
    var score = Number(r.risk_score);
    $("empty").hidden = true;
    $("result").hidden = false;
    $("result").dataset.decision = cls;
    $("verdict").className = "verdict " + cls;
    $("r-decision").textContent = r.decision;
    $("r-score").textContent = score.toFixed(2);
    $("r-level").textContent = r.risk_level + " risk";
    $("r-gauge").style.setProperty("--score-value", Math.max(0, Math.min(100, score)));
    $("r-gauge").setAttribute("aria-label", "Risk score " + score.toFixed(2) + " out of 100, " + r.risk_level + " risk, decision " + r.decision);
    $("r-meter").style.width = Math.min(100, score) + "%";
    $("r-intent").textContent = r.intent_deviation;
    $("r-source").textContent = r.source_risk;
    $("r-action").textContent = r.action_sensitivity;
    $("r-perm").textContent = r.permission_risk;
    $("r-explanation").textContent = r.explanation;
  }

  function runAnalysis() {
    showError("");
    var payload = {};
    FIELDS.forEach(function (f) { payload[f] = $(f).value; });
    var button = $("run");
    button.disabled = true;

    fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (res) {
        return res.json().then(function (body) { return { ok: res.ok, body: body }; });
      })
      .then(function (out) {
        if (!out.ok) throw new Error(out.body.error || "Request failed");
        showResult(out.body);
      })
      .catch(function (err) { showError(err.message); })
      .then(function () { button.disabled = false; });
  }

  function loadPresets() {
    fetch("/api/scenarios")
      .then(function (res) { return res.json(); })
      .then(function (data) {
        scenarios = data.scenarios;
        var select = $("preset");
        scenarios.forEach(function (s, i) {
          var opt = document.createElement("option");
          opt.value = String(i);
          opt.textContent = s.id + ". " + s.name;
          select.appendChild(opt);
        });
      })
      .catch(function () { /* presets are optional */ });
  }

  $("preset").addEventListener("change", function () {
    if (this.value === "") return;
    var s = scenarios[Number(this.value)];
    FIELDS.forEach(function (f) { $(f).value = s[f]; });
  });
  $("run").addEventListener("click", runAnalysis);
  loadPresets();
})();
