import unittest

import numpy as np

from src.config import variable_names
from src.variables import (
    Orders,
    CloseRate,
    UnitExw,
    UnitRetail,
    ChannelMarkupRate,
    ShippingRate,
    DeductionRate,
    UnitFob,
    UnitsPerOrder,
)


class TestDealVariables(unittest.TestCase):

    def setUp(self):
        """Initialize the refactored deal variables with explicit default configuration thresholds."""
        # Baseline legacy parameters
        self.orders = Orders(min=20, max=30)
        self.close_rate = CloseRate(min=0.08, exp=0.12, max=0.18)
        self.units_per_order = UnitsPerOrder(min=1, max=5)

        # New pricing matrix components initialized in strict (min, exp, max) order
        self.unit_exw = UnitExw(min=3000, exp=5000, max=7000)
        self.unit_retail = UnitRetail(min=5000, exp=8000, max=12000)
        self.channel_markup = ChannelMarkupRate(min=0.15, exp=0.20, max=0.30)
        self.shipping_rate = ShippingRate(min=0.04, exp=0.08, max=0.15)
        self.deduction_rate = DeductionRate(min=0.25, exp=0.42, max=0.62)
        self.unit_fob = UnitFob(min=3000, exp=4500, max=6000)

    # =====================================================================
    # IDENTITY & NAMING TESTS
    # =====================================================================

    def test_deal_identity_mappings(self):
        """Verify that each class properly assigns its respective global config key name."""
        self.assertEqual(self.orders.name, variable_names.ORDERS)
        self.assertEqual(self.close_rate.name, variable_names.CLOSE_RATE)
        self.assertEqual(self.units_per_order.name, variable_names.UNITS_PER_ORDER)
        self.assertEqual(self.unit_exw.name, variable_names.UNIT_EXW)
        self.assertEqual(self.unit_retail.name, variable_names.UNIT_RETAIL)
        self.assertEqual(self.channel_markup.name, variable_names.CHANNEL_MARKUP_RATE)
        self.assertEqual(self.shipping_rate.name, variable_names.SHIPPING_RATE)
        self.assertEqual(self.deduction_rate.name, variable_names.DEDUCTION_RATE)
        self.assertEqual(self.unit_fob.name, variable_names.UNIT_FOB)

    # =====================================================================
    # BOUNDARY CONFIGURATION TESTS (Based on default comments)
    # =====================================================================

    def test_orders_range(self):
        """Verify Orders computes midpoint expected value dynamically when missing."""
        self.assertEqual(self.orders.min_value, 20)
        self.assertEqual(self.orders.max_value, 30)
        self.assertEqual(self.orders.expected_value, 25.0)

    def test_close_rate_explicit_range(self):
        """Verify CloseRate retains its explicitly specified expected performance value."""
        self.assertAlmostEqual(self.close_rate.min_value, 0.08)
        self.assertAlmostEqual(self.close_rate.max_value, 0.18)
        self.assertAlmostEqual(self.close_rate.expected_value, 0.12)

    def test_units_per_order_range(self):
        """Verify UnitsPerOrder computes midpoint expected value dynamically when missing."""
        self.assertEqual(self.units_per_order.min_value, 1)
        self.assertEqual(self.units_per_order.max_value, 5)
        self.assertEqual(self.units_per_order.expected_value, 3.0)

    def test_unit_exw_range(self):
        """Verify UnitExw retains its explicit base matrix setup configurations."""
        self.assertEqual(self.unit_exw.min_value, 3000)
        self.assertEqual(self.unit_exw.expected_value, 5000)
        self.assertEqual(self.unit_exw.max_value, 7000)

    def test_unit_retail_range(self):
        """Verify UnitRetail maps correctly to strict numerical range dimensions."""
        self.assertEqual(self.unit_retail.min_value, 5000)
        self.assertEqual(self.unit_retail.expected_value, 8000)
        self.assertEqual(self.unit_retail.max_value, 12000)

    def test_channel_markup_range(self):
        """Verify ChannelMarkupRate maps percent limits cleanly."""
        self.assertAlmostEqual(self.channel_markup.min_value, 0.15)
        self.assertAlmostEqual(self.channel_markup.expected_value, 0.20)
        self.assertAlmostEqual(self.channel_markup.max_value, 0.30)

    def test_shipping_rate_range(self):
        """Verify ShippingRate tracks localized logistics overhead metrics cleanly."""
        self.assertAlmostEqual(self.shipping_rate.min_value, 0.04)
        self.assertAlmostEqual(self.shipping_rate.expected_value, 0.08)
        self.assertAlmostEqual(self.shipping_rate.max_value, 0.15)

    def test_deduction_rate_range(self):
        """Verify DeductionRate captures standard rate limits correctly."""
        self.assertAlmostEqual(self.deduction_rate.min_value, 0.25)
        self.assertAlmostEqual(self.deduction_rate.expected_value, 0.42)
        self.assertAlmostEqual(self.deduction_rate.max_value, 0.62)

    def test_unit_fob_range(self):
        """Verify UnitFob maps point-of-origin ports valuation correctly."""
        self.assertEqual(self.unit_fob.min_value, 3000)
        self.assertEqual(self.unit_fob.expected_value, 4500)
        self.assertEqual(self.unit_fob.max_value, 6000)

    # =====================================================================
    # BEHAVIORAL METHOD TESTS
    # =====================================================================

    def test_deal_range_generation(self):
        """Verify get_range_values creates linear partitions for discrete count limits."""
        steps = self.units_per_order.get_range_values(num=3, digits=0)
        expected_steps = np.array([1, 3, 5])
        np.testing.assert_array_equal(steps, expected_steps)

    def test_deal_stochastic_sampling(self):
        """Verify get_random_value stays strictly inside defined transaction boundaries."""
        for _ in range(50):
            rand_orders = self.orders.get_random_value()
            rand_exw = self.unit_exw.get_random_value()

            self.assertTrue(20 <= rand_orders <= 30)
            self.assertTrue(3000 <= rand_exw <= 7000)


if __name__ == "__main__":
    unittest.main()
