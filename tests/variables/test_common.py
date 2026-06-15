import unittest

from src.config import variable_names as vn
from src.variables import Months


class TestCommonVariables(unittest.TestCase):

    def setUp(self):
        """Initialize production common variables with rule-based boundaries."""
        # Test Rule 3 (Range Bound): Min and Max provided, exp is midpoint
        self.months = Months(min=12, max=24)

    def test_months_identity_mapping(self):
        """Verify the Months class assigns the global config key name correctly."""
        self.assertEqual(self.months.name, vn.MONTHS)

    def test_months_boundary_configurations(self):
        """Verify boundary logic (Rule 3) for the Months variable."""
        self.assertEqual(self.months.min_value, 12)
        self.assertEqual(self.months.max_value, 24)
        self.assertEqual(self.months.expected_value, 18.0)  # Midpoint of 12 and 24

    def test_months_stochastic_sampling(self):
        """Verify random sampling stays within defined operational boundaries."""
        for _ in range(50):
            val = self.months.get_random_value()
            self.assertTrue(12 <= val <= 24)


if __name__ == "__main__":
    unittest.main()
