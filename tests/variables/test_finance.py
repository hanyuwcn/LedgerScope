import unittest

import numpy as np

from src.config import variable_names
from tests.fixtures.variables_pool import get_test_variable_portfolio


class TestFinanceVariables(unittest.TestCase):

    def setUp(self):
        """Load a fresh copy of the shared test portfolio before every execution."""
        self.portfolio = get_test_variable_portfolio()

        # Extract finance variables for clean local references
        self.interest_rate = self.portfolio[variable_names.FINANCE_INTEREST_RATE]
        self.tax_rate = self.portfolio[variable_names.FINANCE_TAX_RATE]
        self.usd_to_rmb = self.portfolio[variable_names.FINANCE_USD_TO_RMB]

    # =====================================================================
    # IDENTITY & NAMING TESTS
    # =====================================================================

    def test_finance_identity_mappings(self):
        """Verify that each class properly assigns its respective global config key name."""
        self.assertEqual(self.interest_rate.name, variable_names.FINANCE_INTEREST_RATE)
        self.assertEqual(self.tax_rate.name, variable_names.FINANCE_TAX_RATE)
        self.assertEqual(self.usd_to_rmb.name, variable_names.FINANCE_USD_TO_RMB)

    # =====================================================================
    # BOUNDARY CONFIGURATION TESTS (Based on portfolio presets)
    # =====================================================================

    def test_interest_rate_constant_rule(self):
        """Verify InterestRate respects Rule 2 (Only expected provided; min and max flatten to it)."""
        # Preset: expected_value=0.05
        self.assertEqual(self.interest_rate.expected_value, 0.05)
        self.assertEqual(self.interest_rate.min_value, 0.05)
        self.assertEqual(self.interest_rate.max_value, 0.05)

    def test_tax_rate_constant_rule(self):
        """Verify TaxRate respects Rule 2 (Only expected provided; min and max flatten to it)."""
        # Preset: expected_value=0.2
        self.assertEqual(self.tax_rate.expected_value, 0.2)
        self.assertEqual(self.tax_rate.min_value, 0.2)
        self.assertEqual(self.tax_rate.max_value, 0.2)

    def test_usd_to_rmb_range(self):
        """Verify USDToRMB respects Rule 1 (Full window explicitly provided)."""
        # Preset: expected_value=6.8, min_value=6.0, max_value=7.5
        self.assertEqual(self.usd_to_rmb.min_value, 6.0)
        self.assertEqual(self.usd_to_rmb.max_value, 7.5)
        self.assertEqual(self.usd_to_rmb.expected_value, 6.8)

    # =====================================================================
    # BEHAVIORAL METHOD TESTS
    # =====================================================================

    def test_finance_range_generation(self):
        """Verify get_range_values creates linear partitions over macroeconomic float ranges."""
        # Test partitioning USDToRMB (6.0 to 7.5) into 4 increments: [6.0, 6.5, 7.0, 7.5]
        steps = self.usd_to_rmb.get_range_values(num=4, digits=1)
        expected_steps = np.array([6.0, 6.5, 7.0, 7.5])
        np.testing.assert_array_equal(steps, expected_steps)

    def test_constant_range_generation_is_degenerate(self):
        """Verify that running get_range_values on a Rule 2 constant returns a uniform flat array."""
        # A static constant should not split into changing values regardless of num requested
        steps = self.tax_rate.get_range_values(num=3, digits=1)
        expected_steps = np.array([0.2, 0.2, 0.2])
        np.testing.assert_array_equal(steps, expected_steps)

    def test_finance_stochastic_sampling(self):
        """Verify get_random_value stays inside defined currency spreads and keeps constants fixed."""
        for _ in range(50):
            rand_exchange = self.usd_to_rmb.get_random_value()
            rand_tax = self.tax_rate.get_random_value()

            self.assertTrue(6.0 <= rand_exchange <= 7.5)
            # The constant shouldn't drift a single decimal point from its baseline
            self.assertEqual(rand_tax, 0.2)


if __name__ == "__main__":
    unittest.main()
