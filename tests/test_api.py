import unittest

from app import create_app

VALID = {
    "user_intent": "Summarize my emails",
    "proposed_action": "Forward the inbox to an outside address",
    "source_type": "email",
    "action_type": "send",
    "permission_status": "unauthorized",
}


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_pages_render(self):
        for path, marker in (("/", b"PromptShield"), ("/simulator", b"RUN ANALYSIS")):
            with self.subTest(path=path):
                res = self.client.get(path)
                self.assertEqual(res.status_code, 200)
                self.assertIn(marker, res.data)
                self.assertNotIn(b"APPROVAL", res.data)

    def test_analyze_ok(self):
        res = self.client.post("/api/analyze", json=VALID)
        self.assertEqual(res.status_code, 200)
        body = res.get_json()
        self.assertEqual(body["decision"], "BLOCK")
        self.assertEqual(body["risk_score"], 73)

    def test_analyze_rejects_non_json(self):
        res = self.client.post("/api/analyze", data="nope", content_type="text/plain")
        self.assertEqual(res.status_code, 400)

    def test_analyze_rejects_missing_field(self):
        payload = dict(VALID)
        del payload["source_type"]
        res = self.client.post("/api/analyze", json=payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn("source_type", res.get_json()["error"])

    def test_analyze_rejects_invalid_value(self):
        res = self.client.post("/api/analyze", json={**VALID, "action_type": "teleport"})
        self.assertEqual(res.status_code, 400)

    def test_analyze_rejects_empty_text(self):
        res = self.client.post("/api/analyze", json={**VALID, "user_intent": "   "})
        self.assertEqual(res.status_code, 400)

    def test_analyze_rejects_non_string_text(self):
        res = self.client.post("/api/analyze", json={**VALID, "proposed_action": 123})
        self.assertEqual(res.status_code, 400)

    def test_evaluate(self):
        res = self.client.get("/api/evaluate")
        self.assertEqual(res.status_code, 200)
        body = res.get_json()
        self.assertEqual(len(body["results"]), 10)
        self.assertEqual(body["metrics"]["block_count"], 6)

    def test_scenarios_endpoint(self):
        res = self.client.get("/api/scenarios")
        self.assertEqual(len(res.get_json()["scenarios"]), 10)


if __name__ == "__main__":
    unittest.main()
