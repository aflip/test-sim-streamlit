import unittest
import polars as pl
import numpy as np
from src.simulation_functions import perform_test

class TestPerformTest(unittest.TestCase):

    def test_valid_condition(self):
        """
        Tests perform_test with a valid condition and expected outcomes.
        """
        # Create a test DataFrame
        data = pl.DataFrame(
            {
                "condition_A": [True, False, True, False],
                "condition_B": [False, True, False, True],
            }
        )
        
        # Define test parameters
        condition = "condition_A"
        sensitivity = 0.8
        specificity = 0.9

        # Expected results based on sensitivity and specificity
        expected_results = np.array([True, False, True, False])  # Matches true conditions
        
        # Run the test
        result_df, messages = perform_test(data, condition, sensitivity, specificity)

        # Assertions
        self.assertIsNotNone(result_df, "Test should return a DataFrame")
        self.assertEqual(result_df.shape, (4, 2), "DataFrame should have correct shape")
        np.testing.assert_array_equal(result_df["test_result"].to_numpy(), expected_results, "Test results should match expected")
        self.assertEqual(messages, "", "Should be no error messages")

    def test_invalid_condition(self):
        """
        Tests perform_test with an invalid condition.
        """
        # Create a test DataFrame
        data = pl.DataFrame(
            {
                "condition_A": [True, False, True, False],
                "condition_B": [False, True, False, True],
            }
        )
        
        # Define test parameters
        condition = "condition_C"  # Invalid condition
        sensitivity = 0.8
        specificity = 0.9

        # Run the test
        result_df, messages = perform_test(data, condition, sensitivity, specificity)

        # Assertions
        self.assertIsNone(result_df, "Test should return None for invalid condition")
        self.assertIn("condition_C not found", messages, "Error message should contain invalid condition")

if __name__ == '__main__':
    unittest.main()