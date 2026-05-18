import unittest
import numpy as np
from tests.fixtures.variables_pool import get_test_variable_portfolio
from src.config import variable_names


class TestCostVariables(unittest.TestCase):

    def setUp(self):
        """Load a fresh copy of the shared test portfolio before every execution."""
        self.portfolio = get_test_variable_portfolio()

        # Extract cost variables for easier local reference
        self.cost = self.portfolio[variable_names.COST]
        self.ad_cost = self.portfolio[variable_names.COST_ADVERTISING]
        self.cpa = self.portfolio[variable_names.COST_CPA]
        self.conv_rate = self.portfolio[variable_names.COST_CONVERSION_RATE]

    # =====================================================================
    # IDENTITY & NAMING TESTS
    # =====================================================================

    def test_cost_identity_mappings(self):
        """Verify that each class properly assigns its respective global config key name."""
        self.assertEqual(self.cost.name, variable_names.COST)
        self.assertEqual(self.ad_cost.name, variable_names.COST_ADVERTISING)
        self.assertEqual(self.cpa.name, variable_names.COST_CPA)
        self.assertEqual(self.conv_rate.name, variable_names.COST_CONVERSION_RATE)

    # =====================================================================
    # BOUNDARY CONFIGURATION TESTS (Based on portfolio presets)
    # =====================================================================

    def test_cost_placeholder_rule(self):
        """Verify Cost defaults to Rule 5 (Pure Placeholder with all None values)."""
        self.assertIsNone(self.cost.min_value)
        self.assertIsNone(self.cost.max_value)
        self.assertIsNone(self.cost.expected_value)

    def test_advertising_cost_range(self):
        """Verify AdvertisingCost respects Rule 3 (Range Bound) and computes midpoint expected value."""
        # Preset: min_value=10000, max_value=30000
        self.assertEqual(self.ad_cost.min_value, 10000)
        self.assertEqual(self.ad_cost.max_value, 30000)
        self.assertEqual(self.ad_cost.expected_value, 20000.0)  # Midpoint

    def test_cpa_range(self):
        """Verify CostPerAcquisition respects Rule 3 and computes midpoint expected value."""
        # Preset: min_value=12, max_value=36
        self.assertEqual(self.cpa.min_value, 12)
        self.assertEqual(self.cpa.max_value, 36)
        self.assertEqual(self.cpa.expected_value, 24.0)  # Midpoint

    def test_conversion_rate_range(self):
        """Verify ConversionRate respects Rule 3 and computes midpoint expected value."""
        # Preset: min_value=0.04, max_value=0.2
        self.assertEqual(self.conv_rate.min_value, 0.04)
        self.assertEqual(self.conv_rate.max_value, 0.2)
        self.assertAlmostEqual(self.conv_rate.expected_value, 0.12, delta=0.0001)  # Midpoint

    # =====================================================================
    # BEHAVIORAL METHOD TESTS
    # =====================================================================

    def test_cost_range_generation(self):
        """Verify get_range_values creates linear partitions suitable for sensitivity analysis."""
        # Test partitioning conversion rate into 3 chunks: [0.04, 0.12, 0.20]
        steps = self.conv_rate.get_range_values(num=3, digits=2)
        expected_steps = np.array([0.04, 0.12, 0.20])
        np.testing.assert_array_equal(steps, expected_steps)

    def test_cost_stochastic_sampling(self):
        """Verify get_random_value stays strictly inside defined parameter bounds."""
        for _ in range(50):
            rand_ad = self.ad_cost.get_random_value()
            rand_cpa = self.cpa.get_random_value()

            self.assertTrue(10000 <= rand_ad <= 30000)
            self.assertTrue(12 <= rand_cpa <= 36)


if __name__ == "__main__":
    unittest.main()