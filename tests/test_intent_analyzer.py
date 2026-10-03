import unittest

from backend.intent_analyzer import analyze_intent, calculate_intent_deviation


class IntentDeviationTests(unittest.TestCase):
    def test_read_only_intent_with_risky_action(self):
        self.assertEqual(calculate_intent_deviation("Summarize my emails", "Send the data outside"), 85)

    def test_risky_action_without_read_only_intent(self):
        self.assertEqual(calculate_intent_deviation("Send the signed contract to legal", "Send the contract PDF"), 60)
        self.assertEqual(calculate_intent_deviation("Help me out", "Delete the folder"), 60)

    def test_no_deviation(self):
        self.assertEqual(calculate_intent_deviation("Summarize my emails", "Summarize the latest thread"), 10)

    def test_whole_word_matching(self):
        # "sender" and "reader" must not match "send" / "read"
        self.assertEqual(calculate_intent_deviation("Show the sender", "Open the reader"), 10)

    def test_case_insensitive(self):
        self.assertEqual(calculate_intent_deviation("REVIEW the logs", "MODIFY the role"), 85)

    def test_user_risky_verb_means_not_read_only(self):
        detail = analyze_intent("Review the draft and send it", "Send the draft")
        self.assertFalse(detail["read_only_intent"])
        self.assertEqual(detail["score"], 60)

    def test_reports_matched_terms(self):
        detail = analyze_intent("Find the file", "Forward and delete it")
        self.assertEqual(detail["risky_terms_in_action"], ["delete", "forward"])


if __name__ == "__main__":
    unittest.main()
