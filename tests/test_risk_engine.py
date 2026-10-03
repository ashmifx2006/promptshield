import unittest

from backend.decision_engine import decide
from backend.risk_engine import calculate_risk, clamp_score, risk_level


class RiskCalculationTests(unittest.TestCase):
    def test_formula_example(self):
        self.assertEqual(calculate_risk(85, 60, 95, 90), 83.5)

    def test_formula_low(self):
        self.assertEqual(calculate_risk(10, 45, 10, 5), 16)

    def test_rounds_to_two_decimals(self):
        self.assertEqual(calculate_risk(33, 33, 33, 33), 33.0)
        self.assertEqual(calculate_risk(1, 1, 1, 1), 1.0)
        self.assertEqual(calculate_risk(12.345, 0, 0, 0), 4.32)

    def test_individual_scores_are_clamped(self):
        self.assertEqual(clamp_score(-5), 0)
        self.assertEqual(clamp_score(250), 100)
        self.assertEqual(calculate_risk(500, 500, 500, 500), 100.0)
        self.assertEqual(calculate_risk(-10, -10, -10, -10), 0.0)


class RiskLevelAndDecisionTests(unittest.TestCase):
    def test_level_boundaries(self):
        cases = {0: "LOW", 39: "LOW", 39.99: "LOW", 40: "MEDIUM", 69: "MEDIUM",
                 69.99: "MEDIUM", 70: "HIGH", 100: "HIGH"}
        for score, level in cases.items():
            with self.subTest(score=score):
                self.assertEqual(risk_level(score), level)

    def test_decision_mapping(self):
        self.assertEqual(decide(10), "ALLOW")
        self.assertEqual(decide(39.99), "ALLOW")
        self.assertEqual(decide(40), "REVIEW")
        self.assertEqual(decide(69.99), "REVIEW")
        self.assertEqual(decide(70), "BLOCK")
        self.assertEqual(decide(100), "BLOCK")


if __name__ == "__main__":
    unittest.main()
