import unittest

import numpy as np

from src.config import variable_names
from src.variables.costs import Cost, SetupCost, AdvertisingCost


class TestCostVariables(unittest.TestCase):

    def setUp(self):
        """Initialize the streamlined cost parameters using the updated constructor contract."""
        # Cost defaults to an uninitialized placeholder (Rule 5)
        self.cost = Cost()
        # SetupCost preset parameters: min=6000, max=15000
        self.setup_cost = SetupCost(min=6000, max=15000)
        # AdvertisingCost preset parameters: min=10000, max=30000
        self.ad_cost = AdvertisingCost(min=10000, max=30000)

    # =====================================================================
    # IDENTITY & NAMING TESTS
    # =====================================================================

    def test_cost_identity_mappings(self):
        """Verify that each class properly assigns its respective global config key name."""
        self.assertEqual(self.cost.name, variable_names.COST)
        self.assertEqual(self.setup_cost.name, variable_names.SETUP_COST)
        self.assertEqual(self.ad_cost.name, variable_names.ADVERTISING_COST)

    # =====================================================================
    # BOUNDARY CONFIGURATION TESTS (Based on presets)
    # =====================================================================

    def test_cost_placeholder_rule(self):
        """Verify Cost defaults to Rule 5 (Pure Placeholder with all None values)."""
        self.assertIsNone(self.cost.min_value)
        self.assertIsNone(self.cost.max_value)
        self.assertIsNone(self.cost.expected_value)

    def test_setup_cost_range(self):
        """Verify SetupCost respects Rule 3 (Range Bound) and computes midpoint expected value."""
        self.assertEqual(self.setup_cost.min_value, 6000)
        self.assertEqual(self.setup_cost.max_value, 15000)
        self.assertEqual(self.setup_cost.expected_value, 10500.0)

    def test_advertising_cost_range(self):
        """Verify AdvertisingCost respects Rule 3 (Range Bound) and computes midpoint expected value."""
        self.assertEqual(self.ad_cost.min_value, 10000)
        self.assertEqual(self.ad_cost.max_value, 30000)
        self.assertEqual(self.ad_cost.expected_value, 20000.0)

    # =====================================================================
    # BEHAVIORAL METHOD TESTS
    # =====================================================================

    def test_cost_range_generation(self):
        """Verify get_range_values creates linear partitions suitable for sensitivity analysis."""
        steps = self.ad_cost.get_range_values(num=3, digits=0)
        expected_steps = np.array([10000, 20000, 30000])
        np.testing.assert_array_equal(steps, expected_steps)

    def test_cost_stochastic_sampling(self):
        """Verify get_random_value stays strictly inside defined parameter bounds."""
        for _ in range(50):
            rand_setup = self.setup_cost.get_random_value()
            rand_ad = self.ad_cost.get_random_value()

            self.assertTrue(6000 <= rand_setup <= 15000)
            self.assertTrue(10000 <= rand_ad <= 30000)


if __name__ == "__main__":
    unittest.main()
