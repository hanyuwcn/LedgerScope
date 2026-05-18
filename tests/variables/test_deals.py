import unittest

import numpy as np

from src.config import variable_names
from tests.fixtures.variables_pool import get_test_variable_portfolio


class TestDealVariables(unittest.TestCase):

    def setUp(self):
        """Load a fresh copy of the shared test portfolio before every execution."""
        self.portfolio = get_test_variable_portfolio()

        # Extract deal variables for clean local references
        self.orders = self.portfolio[variable_names.DEAL_ORDERS]
        self.items_per_order = self.portfolio[variable_names.DEAL_ITEMS_PER_ORDER]
        self.selling_price = self.portfolio[variable_names.DEAL_SELLING_PRICE]
        self.purchasing_price = self.portfolio[variable_names.DEAL_PURCHASING_PRICE]

    # =====================================================================
    # IDENTITY & NAMING TESTS
    # =====================================================================

    def test_deal_identity_mappings(self):
        """Verify that each class properly assigns its respective global config key name."""
        self.assertEqual(self.orders.name, variable_names.DEAL_ORDERS)
        self.assertEqual(self.items_per_order.name, variable_names.DEAL_ITEMS_PER_ORDER)
        self.assertEqual(self.selling_price.name, variable_names.DEAL_SELLING_PRICE)
        self.assertEqual(self.purchasing_price.name, variable_names.DEAL_PURCHASING_PRICE)

    # =====================================================================
    # BOUNDARY CONFIGURATION TESTS (Based on portfolio presets)
    # =====================================================================

    def test_orders_range(self):
        """Verify Orders respects Rule 3 (Range Bound) and computes midpoint expected value."""
        # Preset: min_value=20, max_value=30
        self.assertEqual(self.orders.min_value, 20)
        self.assertEqual(self.orders.max_value, 30)
        self.assertEqual(self.orders.expected_value, 25.0)  # Midpoint

    def test_items_per_order_range(self):
        """Verify ItemsPerOrder respects Rule 3 and computes midpoint expected value."""
        # Preset: min_value=1, max_value=5
        self.assertEqual(self.items_per_order.min_value, 1)
        self.assertEqual(self.items_per_order.max_value, 5)
        self.assertEqual(self.items_per_order.expected_value, 3.0)  # Midpoint

    def test_selling_price_range(self):
        """Verify SellingPrice respects Rule 3 and computes midpoint expected value."""
        # Preset: min_value=3000, max_value=6000
        self.assertEqual(self.selling_price.min_value, 3000)
        self.assertEqual(self.selling_price.max_value, 6000)
        self.assertEqual(self.selling_price.expected_value, 4500.0)  # Midpoint

    def test_purchasing_price_range(self):
        """Verify PurchasingPrice respects Rule 3 and computes midpoint expected value."""
        # Preset: min_value=1000, max_value=2000
        self.assertEqual(self.purchasing_price.min_value, 1000)
        self.assertEqual(self.purchasing_price.max_value, 2000)
        self.assertEqual(self.purchasing_price.expected_value, 1500.0)  # Midpoint

    def test_revenue_raw_scalar_state(self):
        """Ensure Revenue is tracked strictly as a scalar fallback integer, not a Variable."""
        revenue_val = self.portfolio[variable_names.REVENUE]
        self.assertEqual(revenue_val, 0)
        self.assertNotIsInstance(revenue_val, type(self.orders))

    # =====================================================================
    # BEHAVIORAL METHOD TESTS
    # =====================================================================

    def test_deal_range_generation(self):
        """Verify get_range_values creates linear partitions for discrete count limits."""
        # Test partitioning ItemsPerOrder (1 to 5) into 3 discrete milestones: [1, 3, 5]
        steps = self.items_per_order.get_range_values(num=3, digits=0)
        expected_steps = np.array([1, 3, 5])
        np.testing.assert_array_equal(steps, expected_steps)

    def test_deal_stochastic_sampling(self):
        """Verify get_random_value stays strictly inside defined transaction boundaries."""
        for _ in range(50):
            rand_orders = self.orders.get_random_value()
            rand_selling = self.selling_price.get_random_value()

            self.assertTrue(20 <= rand_orders <= 30)
            self.assertTrue(3000 <= rand_selling <= 6000)


if __name__ == "__main__":
    unittest.main()
