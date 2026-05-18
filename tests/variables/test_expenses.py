import unittest
import numpy as np
from tests.fixtures.variables_pool import get_test_variable_portfolio
from src.config import variable_names


class TestExpenseVariables(unittest.TestCase):

    def setUp(self):
        """Load a fresh copy of the shared test portfolio before every execution."""
        self.portfolio = get_test_variable_portfolio()

        # Extract expense variables for clean local references
        self.expense = self.portfolio[variable_names.EXPENSE]
        self.rent = self.portfolio[variable_names.EXPENSE_MONTHLY_RENT]
        self.travel = self.portfolio[variable_names.EXPENSE_TRAVEL_FEE]
        self.render = self.portfolio[variable_names.EXPENSE_RENDER_FEE]

    # =====================================================================
    # IDENTITY & NAMING TESTS
    # =====================================================================

    def test_expense_identity_mappings(self):
        """Verify that each class properly assigns its respective global config key name."""
        self.assertEqual(self.expense.name, variable_names.EXPENSE)
        self.assertEqual(self.rent.name, variable_names.EXPENSE_MONTHLY_RENT)
        self.assertEqual(self.travel.name, variable_names.EXPENSE_TRAVEL_FEE)
        self.assertEqual(self.render.name, variable_names.EXPENSE_RENDER_FEE)

    # =====================================================================
    # BOUNDARY CONFIGURATION TESTS (Based on portfolio presets)
    # =====================================================================

    def test_base_expense_range(self):
        """Verify the generic Expense class respects Rule 1 (Full Window Explicitly Provided)."""
        # Preset: expected_value=1000, min_value=500, max_value=2000
        self.assertEqual(self.expense.min_value, 500)
        self.assertEqual(self.expense.max_value, 2000)
        self.assertEqual(self.expense.expected_value, 1000)

    def test_rent_range(self):
        """Verify Rent respects Rule 3 (Range Bound) and computes midpoint expected value."""
        # Preset: min_value=1000, max_value=3000
        self.assertEqual(self.rent.min_value, 1000)
        self.assertEqual(self.rent.max_value, 3000)
        self.assertEqual(self.rent.expected_value, 2000.0)  # Midpoint

    def test_travel_fee_range(self):
        """Verify TravelFee respects Rule 4 (Only max provided, min floors to 0, expected is midpoint)."""
        # Preset: max_value=1500
        self.assertEqual(self.travel.min_value, 0)
        self.assertEqual(self.travel.max_value, 1500)
        self.assertEqual(self.travel.expected_value, 750.0)  # Midpoint of 0 and 1500

    def test_render_fee_range(self):
        """Verify RenderFee respects Rule 3 and computes midpoint expected value."""
        # Preset: min_value=1000, max_value=2000
        self.assertEqual(self.render.min_value, 1000)
        self.assertEqual(self.render.max_value, 2000)
        self.assertEqual(self.render.expected_value, 1500.0)  # Midpoint

    # =====================================================================
    # BEHAVIORAL METHOD TESTS
    # =====================================================================

    def test_expense_range_generation(self):
        """Verify get_range_values creates linear partitions across explicitly bounded ranges."""
        # Test partitioning RenderFee (1000 to 2000) into 3 discrete milestones: [1000, 1500, 2000]
        steps = self.render.get_range_values(num=3, digits=0)
        expected_steps = np.array([1000, 1500, 2000])
        np.testing.assert_array_equal(steps, expected_steps)

    def test_expense_stochastic_sampling(self):
        """Verify get_random_value stays strictly inside defined operational boundaries."""
        for _ in range(50):
            rand_expense = self.expense.get_random_value()
            rand_travel = self.travel.get_random_value()

            self.assertTrue(500 <= rand_expense <= 2000)
            self.assertTrue(0 <= rand_travel <= 1500)


if __name__ == "__main__":
    unittest.main()