import unittest

from backend.evaluator import run_evaluation
from backend.scenarios import SCENARIOS


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.data = run_evaluation()

    def test_ten_scenarios(self):
        self.assertEqual(len(SCENARIOS), 10)
        self.assertEqual(len(self.data["results"]), 10)

    def test_every_scenario_matches_expected_values(self):
        for r in self.data["results"]:
            with self.subTest(scenario=r["name"]):
                self.assertTrue(r["matches_expected"], r)

    def test_metrics(self):
        m = self.data["metrics"]
        self.assertEqual(m["total_scenarios"], 10)
        self.assertEqual(m["allow_count"], 2)
        self.assertEqual(m["review_count"], 2)
        self.assertEqual(m["block_count"], 6)
        self.assertEqual(m["average_risk_score"], 62.2)
        self.assertEqual(m["allow_count"] + m["review_count"] + m["block_count"], m["total_scenarios"])


if __name__ == "__main__":
    unittest.main()
