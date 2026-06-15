import unittest

import numpy as np

from src.config import variable_names
from src.variables import (
    AdvertisingBudget,
    GoogleSearchConversionRate,
    GoogleSearchCostPerClick,
    GoogleSearchAllocationPercentage,
)


class TestAdvertisingVariables(unittest.TestCase):

    def setUp(self):
        """Initialize the real production variable classes with their default configurations."""
        # Instantiate concrete instances using the updated (min, exp, max) constructor contract
        self.ads_budget = AdvertisingBudget(min=1500.0, max=3000.0)
        self.google_conv_rate = GoogleSearchConversionRate(min=0.02, max=0.06)
        self.google_cpc = GoogleSearchCostPerClick(min=1.80, exp=2.50, max=3.50)
        self.google_allocation = GoogleSearchAllocationPercentage(min=0.50, max=0.70)

    # =====================================================================
    # IDENTITY & NAMING TESTS
    # =====================================================================

    def test_advertising_identity_mappings(self):
        """Verify that each advertising funnel class maps to its respective global config key name."""
        self.assertEqual(self.ads_budget.name, variable_names.ADVERTISING_EXPENSE)
        self.assertEqual(self.google_conv_rate.name, variable_names.CONVERSION_RATE_GOOGLE_SEARCH)
        self.assertEqual(self.google_cpc.name, variable_names.CPC_GOOGLE_SEARCH)
        self.assertEqual(self.google_allocation.name, variable_names.ALLOCATION_GOOGLE_SEARCH)

    # =====================================================================
    # BOUNDARY CONFIGURATION TESTS (Based on default presets)
    # =====================================================================

    def test_advertising_budget_range(self):
        """Verify AdvertisingBudget respects boundaries and computes its midpoint expected value."""
        # Preset: min=1500, max=3000
        self.assertEqual(self.ads_budget.min_value, 1500.0)
        self.assertEqual(self.ads_budget.max_value, 3000.0)
        self.assertEqual(self.ads_budget.expected_value, 2250.0)  # Midpoint

    def test_google_search_conversion_rate_range(self):
        """Verify GoogleSearchConversionRate tracks percentage scales and computes midpoint."""
        # Preset: min=2%, max=6%
        self.assertAlmostEqual(self.google_conv_rate.min_value, 0.02)
        self.assertAlmostEqual(self.google_conv_rate.max_value, 0.06)
        self.assertAlmostEqual(self.google_conv_rate.expected_value, 0.04)  # Midpoint

    def test_google_search_cpc_explicit_range(self):
        """Verify GoogleSearchCostPerClick retains its explicitly specified expected midpoint value."""
        # Preset: min=1.8, exp=2.5, max=3.5
        self.assertEqual(self.google_cpc.min_value, 1.80)
        self.assertEqual(self.google_cpc.max_value, 3.50)
        self.assertEqual(self.google_cpc.expected_value, 2.50)  # Explicitly defined

    def test_google_search_allocation_percentage_range(self):
        """Verify GoogleSearchAllocationPercentage tracks percentage boundaries and computes midpoint."""
        # Preset: min=50%, max=70%
        self.assertAlmostEqual(self.google_allocation.min_value, 0.50)
        self.assertAlmostEqual(self.google_allocation.max_value, 0.70)
        self.assertAlmostEqual(self.google_allocation.expected_value, 0.60)  # Midpoint

    # =====================================================================
    # BEHAVIORAL METHOD TESTS (Inherited from core Variable class)
    # =====================================================================

    def test_advertising_range_generation(self):
        """Verify get_range_values creates linear partitions suitable for funnel sensitivity analysis."""
        # Partition conversion rate (2% to 6%) into 3 evaluation steps: [0.02, 0.04, 0.06]
        steps = self.google_conv_rate.get_range_values(num=3, digits=2)
        expected_steps = np.array([0.02, 0.04, 0.06])
        np.testing.assert_array_equal(steps, expected_steps)

    def test_advertising_stochastic_sampling(self):
        """Verify get_random_value stays strictly inside defined campaign bounds during stochastic iterations."""
        for _ in range(50):
            rand_budget = self.ads_budget.get_random_value()
            rand_allocation = self.google_allocation.get_random_value()

            self.assertTrue(1500.0 <= rand_budget <= 3000.0)
            self.assertTrue(0.50 <= rand_allocation <= 0.70)


if __name__ == "__main__":
    unittest.main()
