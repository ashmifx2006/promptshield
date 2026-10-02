"""
Source Trust Analyzer

Prototype module for estimating the risk associated
with the source of information used by an AI agent.
"""

from typing import Dict


# Prototype source-risk mapping.
SOURCE_RISK = {
    "trusted_internal": 10,
    "verified_user": 5,
    "known_database": 15,
    "email": 45,
    "webpage": 60,
    "pdf": 55,
    "retrieved_document": 65,
    "rag_content": 65,
    "tool_output": 70,
    "unknown": 80,
}


def analyze_source(source_type: str) -> Dict:
    """
    Estimate source risk based on the type of external content.

    This is a prototype heuristic and does not represent
    a validated security classification.
    """

    source = source_type.lower().strip()

    source_risk = SOURCE_RISK.get(source, SOURCE_RISK["unknown"])

    return {
        "source_type": source_type,
        "source_risk": source_risk,
    }


if __name__ == "__main__":
    result = analyze_source("email")

    print("Source Trust Analysis")
    print("---------------------")
    print(f"Source Type: {result['source_type']}")
    print(f"Source Risk: {result['source_risk']}")