import unittest

from src.config import variable_names
from src.models import RevenueModel


class TestRevenueModel(unittest.TestCase):

    def test_evaluate_revenue_in_domestic_currency(self):
        """Verify baseline revenue calculations hold accurate when currency translations are omitted."""
        inputs = {
            variable_names.DEAL_SELLING_PRICE: 50.0,  # $50 per item
            variable_names.DEAL_ORDERS: 200,  # 200 orders
            variable_names.DEAL_ITEMS_PER_ORDER: 1.5  # 1.5 items average per order
        }
        model = RevenueModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 50.0 * 200 * 1.5 * 1.0 = 15000.0
        self.assertEqual(enriched_output[variable_names.REVENUE], 15000.0)
        self.assertEqual(enriched_output[variable_names.DEAL_SELLING_PRICE], 50.0)

    def test_evaluate_revenue_with_currency_translation_factor(self):
        """Verify international revenue scales reliably when an exchange rate multiplier is passed."""
        inputs = {
            variable_names.DEAL_SELLING_PRICE: 100.0,
            variable_names.DEAL_ORDERS: 10,
            variable_names.DEAL_ITEMS_PER_ORDER: 2,
            variable_names.FINANCE_USD_TO_RMB: 7.0
        }
        model = RevenueModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 100.0 * 10 * 2 * 7.0 = 2000 * 7.0 = 14000.0
        self.assertEqual(enriched_output[variable_names.REVENUE], 14000.0)

    def test_evaluate_missing_required_variables_throws_exception(self):
        """Verify that omitting a structural pillar like selling price triggers validation errors."""
        incomplete_inputs = {
            variable_names.DEAL_ORDERS: 10,
            variable_names.DEAL_ITEMS_PER_ORDER: 2
            # Missing DEAL_SELLING_PRICE!
        }
        model = RevenueModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
