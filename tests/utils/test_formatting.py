import unittest

from src.utils.formatting import numeric_to_percentage


class TestFormattingUtils(unittest.TestCase):

    def test_numeric_to_percentage_default_precision(self):
        """Verify that omitting the decimal parameter defaults safely to 1 decimal point."""
        # 0.045 should scale to 4.5%
        self.assertEqual(numeric_to_percentage(0.045), "4.5%")
        # 0.1234 should round to 12.3%
        self.assertEqual(numeric_to_percentage(0.1234), "12.3%")

    def test_numeric_to_percentage_high_precision(self):
        """Verify the formatter accurately preserves deep fractional limits for small rates."""
        # Testing typical micro-financial spreads or conversion adjustments
        self.assertEqual(numeric_to_percentage(0.04567, decimal=3), "4.567%")
        self.assertEqual(numeric_to_percentage(0.001234, decimal=4), "0.1234%")

    def test_numeric_to_percentage_zero_precision(self):
        """Verify that setting decimal=0 cleanly truncates the string to a whole integer percentage."""
        # Useful for macro high-level metrics like whole order shifts or flat tax changes
        self.assertEqual(numeric_to_percentage(1.25, decimal=0), "125%")
        self.assertEqual(numeric_to_percentage(0.8, decimal=0), "80%")

    def test_numeric_to_percentage_flat_zero(self):
        """Verify that absolute zero formats cleanly without string errors or unexpected behavior."""
        self.assertEqual(numeric_to_percentage(0.0, decimal=2), "0.00%")
        self.assertEqual(numeric_to_percentage(0, decimal=0), "0%")


if __name__ == "__main__":
    unittest.main()
