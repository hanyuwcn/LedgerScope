import unittest

from src.utils.formatting import numeric_to_percentage, list_to_element_string


class TestFormattingUtils(unittest.TestCase):

    # =====================================================================
    # NUMERIC TO PERCENTAGE TESTS
    # =====================================================================

    def test_numeric_to_percentage_default_precision(self):
        """Verify that omitting the decimal parameter defaults safely to 1 decimal point."""
        # 0.045 should scale to 4.5%
        self.assertEqual(numeric_to_percentage(0.045), "4.5%")
        # 0.1234 should round to 12.3%
        self.assertEqual(numeric_to_percentage(0.1234), "12.3%")

    def test_numeric_to_percentage_high_precision(self):
        """Verify the formatter accurately preserves deep fractional limits for small rates."""
        self.assertEqual(numeric_to_percentage(0.04567, decimal=3), "4.567%")
        self.assertEqual(numeric_to_percentage(0.001234, decimal=4), "0.1234%")

    def test_numeric_to_percentage_zero_precision(self):
        """Verify that setting decimal=0 cleanly truncates the string to a whole integer percentage."""
        self.assertEqual(numeric_to_percentage(1.25, decimal=0), "125%")
        self.assertEqual(numeric_to_percentage(0.8, decimal=0), "80%")

    def test_numeric_to_percentage_flat_zero(self):
        """Verify that absolute zero formats cleanly across different explicit precisions."""
        self.assertEqual(numeric_to_percentage(0.0, decimal=2), "0.00%")
        self.assertEqual(numeric_to_percentage(0, decimal=0), "0%")

    # =====================================================================
    # LIST TO ELEMENT STRING TESTS
    # =====================================================================

    def test_list_to_element_string_with_multiple_elements(self):
        """Verify that multiple strings are joined with a space following each comma separator."""
        elements = ["COST_CPA", "FINANCE_TAX_RATE", "DEAL_ORDERS"]
        result = list_to_element_string(elements)
        self.assertEqual(result, "COST_CPA, FINANCE_TAX_RATE, DEAL_ORDERS")

    def test_list_to_element_string_with_single_element(self):
        """Verify that a list with one item returns just that item string without trailing commas."""
        elements = ["EXPENSE_MONTHLY_RENT"]
        result = list_to_element_string(elements)
        self.assertEqual(result, "EXPENSE_MONTHLY_RENT")

    def test_list_to_element_string_with_empty_list(self):
        """Verify that an empty input list returns a pristine empty string instantly."""
        self.assertEqual(list_to_element_string([]), "")


if __name__ == "__main__":
    unittest.main()
