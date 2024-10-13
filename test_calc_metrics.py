import unittest
import polars as pl
import numpy as np
from src.simulation_functions import calculate_test_metrics

class TestCalculateTestMetrics(unittest.TestCase):

    def test_known_values(self):
        """
        Tests the calculate_test_metrics function with a known dataset.
        """
        # Create a test DataFrame with known true conditions and test results
        true_conditions = np.array([True, True, False, True, False, False, False, True])
        test_results = np.array([True, False, False, True, True, False, False, True])
        test_df = pl.DataFrame({"true_condition": true_conditions, "test_result": test_results})

        # Calculate metrics using the function
        metrics_dict, _ = calculate_test_metrics(test_df, "true_condition")

        # Assert expected values
        self.assertEqual(metrics_dict["true_positives"], 3)  # Correctly identified as having the condition
        self.assertEqual(metrics_dict["false_positives"], 1)  # Incorrectly identified as having the condition

        # You can add more assertions for other metrics as needed.
        # ...

if __name__ == '__main__':
    unittest.main()