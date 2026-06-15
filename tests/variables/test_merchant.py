import unittest

from src.config import variable_names as vn
from src.variables import (
    UnitRetailPrice,
    DeductionRate,
    RetailMarginRate,
    FreightRate,
    UnitFreightExpense,
    UnitTariff,
    UnitRetailMargin
)


class TestMerchantVariables(unittest.TestCase):

    def setUp(self):
        """Initialize merchant variables with explicit threshold configurations."""
        self.retail_price = UnitRetailPrice(min=8000, exp=10000, max=12000)
        self.deduction_rate = DeductionRate(min=0.20, exp=0.30, max=0.40)
        self.margin_rate = RetailMarginRate(min=0.10, exp=0.15, max=0.20)
        self.freight_rate = FreightRate(min=0.02, exp=0.05, max=0.08)
        self.freight_expense = UnitFreightExpense(min=50, exp=100, max=150)
        self.tariff = UnitTariff(min=20, exp=40, max=60)
        self.retail_margin = UnitRetailMargin(min=200, exp=400, max=600)

    # =====================================================================
    # IDENTITY & NAMING TESTS
    # =====================================================================

    def test_merchant_identity_mappings(self):
        """Verify each class maps to the correct vn constant."""
        self.assertEqual(self.retail_price.name, vn.UNIT_RETAIL_PRICE)
        self.assertEqual(self.deduction_rate.name, vn.DEDUCTION_RATE)
        self.assertEqual(self.margin_rate.name, vn.CHANNEL_MARKUP_RATE)
        self.assertEqual(self.freight_rate.name, vn.FREIGHT_RATE)
        self.assertEqual(self.freight_expense.name, vn.UNIT_FREIGHT_EXPENSE)
        self.assertEqual(self.tariff.name, vn.UNIT_TARIFF)
        self.assertEqual(self.retail_margin.name, vn.UNIT_RETAIL_MARGIN)

    # =====================================================================
    # BOUNDARY CONFIGURATION TESTS
    # =====================================================================

    def test_merchant_boundary_logic(self):
        """Verify mid-point calculation and range boundaries."""
        # Test Rate variables (e.g., DeductionRate)
        self.assertEqual(self.deduction_rate.expected_value, 0.30)

        # Test Expense variables (e.g., UnitFreightExpense)
        self.assertEqual(self.freight_expense.expected_value, 100.0)

        # Test Margin variables (e.g., UnitRetailMargin)
        self.assertEqual(self.retail_margin.min_value, 200)
        self.assertEqual(self.retail_margin.max_value, 600)

    # =====================================================================
    # BEHAVIORAL METHOD TESTS
    # =====================================================================

    def test_stochastic_sampling(self):
        """Verify that stochastic sampling respects the defined operational limits."""
        for _ in range(50):
            rand_price = self.retail_price.get_random_value()
            self.assertTrue(8000 <= rand_price <= 12000)

            rand_rate = self.deduction_rate.get_random_value()
            self.assertTrue(0.20 <= rand_rate <= 0.40)


if __name__ == "__main__":
    unittest.main()
