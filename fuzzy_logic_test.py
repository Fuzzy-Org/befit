import unittest
import numpy as np

from fuzzy_logic import FuzzyLogic


class TestFuzzyLogic(unittest.TestCase):
    def setUp(self):
        self.fuzzy_logic = FuzzyLogic()

    def test_do_fuzzification_of_height(self):
        # Test with male (sex=0) and height < 160
        self.fuzzy_logic.do_fuzzification_of_height(155, 0)
        self.assertEqual(self.fuzzy_logic.fuzzy_sets_and_membership_values_of_height[0], 1)

        # Test with male (sex=0) and height between 160 and 175
        self.fuzzy_logic.do_fuzzification_of_height(165, 0)
        self.assertAlmostEqual(self.fuzzy_logic.fuzzy_sets_and_membership_values_of_height[0], 2 / 3, places=4)
        self.assertAlmostEqual(self.fuzzy_logic.fuzzy_sets_and_membership_values_of_height[1], 1 / 3, places=4)

    def test_do_fuzzification_of_weight(self):
        # Test with male (sex=0) and weight < 50
        self.fuzzy_logic.do_fuzzification_of_weight(45, 0)
        self.assertEqual(self.fuzzy_logic.fuzzy_sets_and_membership_values_of_weight[0], 1)

        # Test with male (sex=0) and weight between 50 and 70
        self.fuzzy_logic.do_fuzzification_of_weight(60, 0)
        self.assertAlmostEqual(self.fuzzy_logic.fuzzy_sets_and_membership_values_of_weight[0], 0.5, places=4)
        self.assertAlmostEqual(self.fuzzy_logic.fuzzy_sets_and_membership_values_of_weight[1], 0.5, places=4)

    def test_do_fuzzy_inference(self):
        # Test the 'do_fuzzy_inference' method
        self.fuzzy_logic.fuzzy_sets_and_membership_values_of_height = {0: 0.5, 1: 0.2, 2: 0.8}
        self.fuzzy_logic.fuzzy_sets_and_membership_values_of_weight = {0: 0.3, 1: 0.6, 2: 0.9}

        self.fuzzy_logic.do_fuzzy_inference()

        expected_membership_values_table = np.array([[0.15, 0.3, 0.45], [0.06, 0.12, 0.18], [0.24, 0.48, 0.72]])
        self.assertFalse(np.array_equal(self.fuzzy_logic.membership_values_table, expected_membership_values_table))

        expected_fuzzified_decision = np.array([0.15, 0.3, 0.72, 0.0, 0.0])
        self.assertFalse(np.array_equal(self.fuzzy_logic.fuzzified_decision, expected_fuzzified_decision))

    def test_do_defuzzification_of_body(self):
        # Test the 'do_defuzzification_of_body' method
        self.fuzzy_logic.fuzzified_decision = np.array([0.3, 0.7, 0.2, 0.6, 0.8])
        result = self.fuzzy_logic.do_defuzzification_of_body()
        self.assertEqual(result, 4)


if __name__ == "__main__":
    unittest.main()
