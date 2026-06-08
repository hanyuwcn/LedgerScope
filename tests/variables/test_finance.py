import unittest

import numpy as np

from src.config import variable_names
from src.variables.finance import InterestRate, TaxRate, USDToRMB, PriceToEarningsRatio


class TestFinanceVariables(unittest.TestCase):

    def setUp(self):
        """Initialize local production finance variables with test boundaries."""
        # InterestRate: Only expected provided (Rule 2)
        self.interest_rate = InterestRate(exp=0.05)

        # TaxRate: Only expected provided (Rule 2)
        self.tax_rate = TaxRate(exp=0.20)

        # USDToRMB: Full parameter window explicitly provided (Rule 1)
        self.usd_to_rmb = USDToRMB(min=6.0, exp=6.8, max=7.5)

        # PriceToEarningsRatio: Explicit test window override (Rule 1)
        self.pe_ratio = PriceToEarningsRatio(min=5, exp=8, max=10)

    # =====================================================================
    # IDENTITY & NAMING TESTS
    # =====================================================================

    def test_finance_identity_mappings(self):
        """Verify that each class properly assigns its respective global config key name."""
        self.assertEqual(self.interest_rate.name, variable_names.INTEREST_RATE)
        self.assertEqual(self.tax_rate.name, variable_names.TAX_RATE)
        self.assertEqual(self.usd_to_rmb.name, variable_names.USD_TO_RMB)
        self.assertEqual(self.pe_ratio.name, variable_names.PE_RATIO)

    # =====================================================================
    # BOUNDARY CONFIGURATION TESTS (Based on presets)
    # =====================================================================

    def test_interest_rate_constant_rule(self):
        """Verify InterestRate respects Rule 2 (Only expected provided; min and max flatten to it)."""
        self.assertEqual(self.interest_rate.expected_value, 0.05)
        self.assertEqual(self.interest_rate.min_value, 0.05)
        self.assertEqual(self.interest_rate.max_value, 0.05)

    def test_tax_rate_constant_rule(self):
        """Verify TaxRate respects Rule 2 (Only expected provided; min and max flatten to it)."""
        self.assertEqual(self.tax_rate.expected_value, 0.20)
        self.assertEqual(self.tax_rate.min_value, 0.20)
        self.assertEqual(self.tax_rate.max_value, 0.20)

    def test_usd_to_rmb_range(self):
        """Verify USDToRMB respects Rule 1 (Full window explicitly provided)."""
        self.assertEqual(self.usd_to_rmb.min_value, 6.0)
        self.assertEqual(self.usd_to_rmb.max_value, 7.5)
        self.assertEqual(self.usd_to_rmb.expected_value, 6.8)

    def test_price_to_earnings_ratio_range(self):
        """Verify PriceToEarningsRatio captures specified testing scale coordinates exactly."""
        self.assertEqual(self.pe_ratio.min_value, 5)
        self.assertEqual(self.pe_ratio.expected_value, 8)
        self.assertEqual(self.pe_ratio.max_value, 10)

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
        steps = self.tax_rate.get_range_values(num=3, digits=1)
        expected_steps = np.array([0.2, 0.2, 0.2])
        np.testing.assert_array_equal(steps, expected_steps)

    def test_finance_stochastic_sampling(self):
        """Verify get_random_value stays inside defined currency spreads and keeps constants fixed."""
        for _ in range(50):
            rand_exchange = self.usd_to_rmb.get_random_value()
            rand_tax = self.tax_rate.get_random_value()
            rand_pe = self.pe_ratio.get_random_value()

            self.assertTrue(6.0 <= rand_exchange <= 7.5)
            self.assertTrue(5 <= rand_pe <= 10)
            self.assertEqual(rand_tax, 0.20)


if __name__ == "__main__":
    unittest.main()
