"""Source trust analysis.

Maps where the content that influenced the agent came from to a source-risk
value (0-100, higher = less trusted).

PROTOTYPE ASSUMPTIONS: these values are illustrative, chosen so that content an
outsider can author (web pages, shared documents, indexed RAG content, tool
output) is rated riskier than first-party instructions.
"""

SOURCE_RISK = {
    "trusted": 10,            # direct user / first-party system instruction
    "email": 45,              # inbound mail: authored by third parties
    "webpage": 60,            # arbitrary public content
    "tool_output": 70,        # data returned by tools may embed third-party text
    "external_document": 80,  # uploaded / shared files from outside the org
    "rag_document": 80,       # retrieved chunks can carry planted instructions
    "unknown": 90,            # provenance cannot be established
}

SOURCE_TYPES = tuple(SOURCE_RISK)


def normalize(value):
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def get_source_risk(source_type):
    """Return the source-risk score for a source category."""
    key = normalize(source_type)
    if key not in SOURCE_RISK:
        raise ValueError(
            f"Unsupported source_type '{source_type}'. Valid values: {', '.join(SOURCE_TYPES)}"
        )
    return SOURCE_RISK[key]
