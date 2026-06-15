import unittest

from src.config import variable_names as vn
from src.variables import (
    Orders,
    CloseRate,
    UnitsPerOrder,
    UnitsSold,
    UnitExwPrice,
    UnitFobPrice,
)


class TestBrandVariables(unittest.TestCase):

    def setUp(self):
        """Initialize brand variables with explicit configuration thresholds."""
        self.orders = Orders(min=20, max=30)
        self.close_rate = CloseRate(min=0.08, exp=0.12, max=0.18)
        self.units_per_order = UnitsPerOrder(min=1, max=5)
        self.units_sold = UnitsSold(min=100, max=500)

        # Pricing matrix
        self.unit_exw = UnitExwPrice(min=30, exp=50, max=70)
        self.unit_fob = UnitFobPrice(min=60, exp=80, max=100)

    # =====================================================================
    # IDENTITY & NAMING TESTS
    # =====================================================================

    def test_brand_identity_mappings(self):
        """Verify that each class assigns its respective global config key name."""
        self.assertEqual(self.orders.name, vn.ORDERS)
        self.assertEqual(self.close_rate.name, vn.CLOSE_RATE)
        self.assertEqual(self.units_per_order.name, vn.UNITS_PER_ORDER)
        self.assertEqual(self.units_sold.name, vn.UNITS_SOLD)
        self.assertEqual(self.unit_exw.name, vn.UNIT_EXW_PRICE)
        self.assertEqual(self.unit_fob.name, vn.UNIT_FOB_PRICE)

    # =====================================================================
    # BOUNDARY CONFIGURATION TESTS
    # =====================================================================

    def test_units_sold_range(self):
        """Verify UnitsSold computes midpoint expected value."""
        self.assertEqual(self.units_sold.min_value, 100)
        self.assertEqual(self.units_sold.max_value, 500)
        self.assertEqual(self.units_sold.expected_value, 300.0)

    def test_unit_exw_range(self):
        """Verify UnitExwPrice retains its explicit base matrix setup."""
        self.assertEqual(self.unit_exw.min_value, 30)
        self.assertEqual(self.unit_exw.expected_value, 50)
        self.assertEqual(self.unit_exw.max_value, 70)

    def test_unit_fob_range(self):
        """Verify UnitFobPrice maps port valuation correctly."""
        self.assertEqual(self.unit_fob.min_value, 60)
        self.assertEqual(self.unit_fob.expected_value, 80)
        self.assertEqual(self.unit_fob.max_value, 100)

    # =====================================================================
    # BEHAVIORAL METHOD TESTS
    # =====================================================================

    def test_brand_stochastic_sampling(self):
        """Verify get_random_value stays strictly inside defined brand boundaries."""
        for _ in range(50):
            rand_units = self.units_sold.get_random_value()
            rand_exw = self.unit_exw.get_random_value()

            self.assertTrue(100 <= rand_units <= 500)
            self.assertTrue(30 <= rand_exw <= 70)


if __name__ == "__main__":
    unittest.main()
