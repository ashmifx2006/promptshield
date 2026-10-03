(function () {
  "use strict";

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function fmt(n) {
    return String(Number(n));
  }

  var SEGMENTS = [
    ["intent_deviation", "intent"],
    ["source_risk", "source"],
    ["action_sensitivity", "action"],
    ["permission_risk", "perm"]
  ];

  function renderMetrics(m) {
    document.getElementById("m-total").textContent = m.total_scenarios;
    document.getElementById("m-allow").textContent = m.allow_count;
    document.getElementById("m-review").textContent = m.review_count;
    document.getElementById("m-block").textContent = m.block_count;
    document.getElementById("m-avg").textContent = Number(m.average_risk_score).toFixed(2);
  }

  function renderBreakdown(results) {
    var host = document.getElementById("breakdown");
    host.textContent = "";
    results.forEach(function (r) {
      var row = el("div", "brow");
      row.setAttribute("role", "listitem");
      row.appendChild(el("div", "name", r.id + ". " + r.name));
      var bar = el("div", "bar");
      bar.setAttribute("aria-hidden", "true");
      SEGMENTS.forEach(function (seg) {
        var s = el("span", "seg " + seg[1]);
        s.style.width = r.contributions[seg[0]] + "%";
        s.title = seg[0].replace("_", " ") + ": " + r.contributions[seg[0]].toFixed(2) + " points";
        bar.appendChild(s);
      });
      [40, 70].forEach(function (t) {
        var tick = el("span", "tick");
        tick.style.left = t + "%";
        bar.appendChild(tick);
      });
      row.appendChild(bar);
      var scoreCell = el("div", "score-cell");
      scoreCell.appendChild(el("span", "score", fmt(r.risk_score)));
      scoreCell.appendChild(el("span", "badge " + r.decision.toLowerCase(), r.decision));
      row.appendChild(scoreCell);
      host.appendChild(row);
    });
  }

  function renderTable(results) {
    var body = document.getElementById("scenario-rows");
    body.textContent = "";
    results.forEach(function (r) {
      var tr = document.createElement("tr");
      [r.id, r.name, r.source_type, r.action_type, r.permission_status].forEach(function (v) {
        tr.appendChild(el("td", "", v));
      });
      [r.intent_deviation, r.source_risk, r.action_sensitivity, r.permission_risk, fmt(r.risk_score)].forEach(function (v) {
        tr.appendChild(el("td", "num", v));
      });
      var td = document.createElement("td");
      td.appendChild(el("span", "badge " + r.decision.toLowerCase(), r.decision));
      tr.appendChild(td);
      body.appendChild(tr);
    });
  }

  fetch("/api/evaluate")
    .then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.json();
    })
    .then(function (data) {
      renderMetrics(data.metrics);
      renderBreakdown(data.results);
      renderTable(data.results);
    })
    .catch(function () {
      document.getElementById("load-error").hidden = false;
      document.getElementById("scenario-rows").innerHTML = "";
    });
})();
