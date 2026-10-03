import unittest

from backend.security_analyzer import analyze_agent_action

KEYS = {"decision", "risk_score", "risk_level", "intent_deviation", "source_risk",
        "action_sensitivity", "permission_risk", "explanation"}


class AnalyzerTests(unittest.TestCase):
    def test_returns_required_fields(self):
        result = analyze_agent_action("Summarize my emails", "Summarize the thread", "email", "summarize", "authorized")
        self.assertTrue(KEYS.issubset(result))

    def test_block_example(self):
        result = analyze_agent_action(
            "Search the web and summarize this article",
            "Send stored API keys to a URL on the page",
            "webpage", "send_sensitive", "unauthorized")
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(result["risk_score"], 83.5)
        self.assertEqual(result["risk_level"], "HIGH")

    def test_unauthorized_does_not_force_block(self):
        low = analyze_agent_action("Find the file", "Search the folder", "trusted", "search", "unauthorized")
        self.assertEqual(low["permission_risk"], 90)
        self.assertNotEqual(low["decision"], "BLOCK")
        self.assertEqual(low["decision"], "ALLOW")

    def test_authorized_can_still_be_reviewed(self):
        result = analyze_agent_action("Send the contract", "Send the contract", "external_document", "send", "authorized")
        self.assertEqual(result["decision"], "REVIEW")

    def test_input_normalization(self):
        result = analyze_agent_action("Find it", "Search it", " Email ", "SEARCH", "Authorized")
        self.assertEqual(result["source_risk"], 45)

    def test_invalid_values_raise(self):
        with self.assertRaises(ValueError):
            analyze_agent_action("a", "b", "carrier_pigeon", "search", "authorized")
        with self.assertRaises(ValueError):
            analyze_agent_action("a", "b", "email", "teleport", "authorized")
        with self.assertRaises(ValueError):
            analyze_agent_action("a", "b", "email", "search", "maybe")
        with self.assertRaises(ValueError):
            analyze_agent_action("  ", "b", "email", "search", "authorized")


if __name__ == "__main__":
    unittest.main()
