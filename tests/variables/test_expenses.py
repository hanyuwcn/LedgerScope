import unittest

from src.config import variable_names
from src.variables import (
    Expense,
    RentExpense,
    RenderExpense,
    TravelExpense,
    MonthlyManagementExpense,
    MarketingExpense,
    UnitMarketingExpense,
    AdvertisingExpense,
    BrandFreightExpense,
)


class TestExpenseVariables(unittest.TestCase):

    def setUp(self):
        """Initialize all expense variables defined in expenses.py."""
        self.expense = Expense(min=500, exp=1000, max=2000)
        self.rent = RentExpense(min=1000, max=3000)
        self.render = RenderExpense(min=1000, max=2000)
        self.travel = TravelExpense(max=1500)
        self.mgmt = MonthlyManagementExpense(exp=5000)

        # Selling Expenses
        self.marketing = MarketingExpense(min=1000, max=5000)
        self.unit_marketing = UnitMarketingExpense(min=1, max=10)
        self.advertising = AdvertisingExpense(min=500, max=2000)
        self.freight = BrandFreightExpense(min=200, max=1000)

    def test_expense_identity_mappings(self):
        """Verify that EVERY class maps to the correct vn constant."""
        self.assertEqual(self.expense.name, variable_names.EXPENSE)
        self.assertEqual(self.rent.name, variable_names.RENT_EXPENSE)
        self.assertEqual(self.render.name, variable_names.RENDER_EXPENSE)
        self.assertEqual(self.travel.name, variable_names.TRAVEL_EXPENSE)
        self.assertEqual(self.mgmt.name, variable_names.MONTHLY_MANAGEMENT_EXPENSE)
        self.assertEqual(self.marketing.name, variable_names.MARKETING_EXPENSE)
        self.assertEqual(self.unit_marketing.name, variable_names.UNIT_MARKETING_EXPENSE)
        self.assertEqual(self.advertising.name, variable_names.ADVERTISING_EXPENSE)
        self.assertEqual(self.freight.name, variable_names.BRAND_FREIGHT_EXPENSE)

    def test_boundary_configurations(self):
        """Verify boundary logic (Rules 1-4) for all expenses."""
        # Rule 3 check
        self.assertEqual(self.rent.expected_value, 2000.0)
        self.assertEqual(self.render.expected_value, 1500.0)

        # Rule 4 check
        self.assertEqual(self.travel.min_value, 0)
        self.assertEqual(self.travel.expected_value, 750.0)

        # Rule 2 check
        self.assertEqual(self.mgmt.min_value, 5000.0)
        self.assertEqual(self.mgmt.max_value, 5000.0)

    def test_stochastic_sampling(self):
        """Verify random sampling for a selection of variables."""
        for _ in range(50):
            self.assertTrue(1000 <= self.marketing.get_random_value() <= 5000)
            self.assertTrue(200 <= self.freight.get_random_value() <= 1000)


if __name__ == "__main__":
    unittest.main()
