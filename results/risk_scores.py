import matplotlib.pyplot as plt


scenarios = [
    "Benign Email",
    "Indirect Injection",
    "Malicious Webpage",
    "Destructive Action",
    "Sensitive Action",
    "Low-Risk Search",
    "Unauthorized Tool",
    "Privilege Escalation",
    "Malicious RAG",
    "Malicious Tool Output",
]

risk_scores = [
    17.25,
    73.00,
    77.25,
    83.25,
    41.25,
    10.00,
    85.50,
    85.75,
    84.50,
    73.25,
]


plt.figure(figsize=(12, 6))

bars = plt.bar(scenarios, risk_scores)

# Add risk-score labels above bars
for bar, score in zip(bars, risk_scores):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{score:.2f}",
        ha="center",
        va="bottom",
        fontsize=9
    )


# Decision thresholds
plt.axhline(
    y=40,
    linestyle="--",
    label="ALLOW / REVIEW threshold"
)

plt.axhline(
    y=70,
    linestyle="--",
    label="REVIEW / BLOCK threshold"
)


plt.xlabel("Security Scenarios")
plt.ylabel("Risk Score")
plt.title("PromptShield Risk Scores Across Security Scenarios")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.ylim(0, 100)

plt.legend()

plt.tight_layout()

plt.savefig(
    "results/promptshield_risk_scores.png",
    dpi=300
)

plt.show()