import unittest

from src.config import variable_names
from src.models import ExpenseModel


class TestExpenseModel(unittest.TestCase):

    def test_evaluate_annual_expenses_with_full_parameters(self):
        """Verify standard 12-month annual cost scaling works perfectly."""
        inputs = {
            variable_names.MONTHS: 12,
            variable_names.EXPENSE_MONTHLY_RENT: 2000.0,
            variable_names.EXPENSE_RENDER_FEE: 500.0,
            variable_names.EXPENSE_TRAVEL_FEE: 300.0
        }
        model = ExpenseModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: (2000 + 500 + 300) * 12 = 2800 * 12 = 33600.0
        self.assertEqual(enriched_output[variable_names.EXPENSE], 33600.0)

    def test_evaluate_quarterly_expenses_with_partial_inputs(self):
        """Verify that scaling adapts dynamically to a 3-month quarterly shift with omitted fields."""
        inputs = {
            variable_names.MONTHS: 3,
            variable_names.EXPENSE_MONTHLY_RENT: 1500.0
            # Render and Travel are omitted intentionally to act as zero-fallbacks
        }
        model = ExpenseModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: (1500 + 0 + 0) * 3 = 4500.0
        self.assertEqual(enriched_output[variable_names.EXPENSE], 4500.0)

    def test_evaluate_fallback_when_all_expenses_are_zeroed(self):
        """Verify model evaluates cleanly to zero if no operational costs are recorded."""
        inputs = {
            variable_names.MONTHS: 6
        }
        model = ExpenseModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: (0 + 0 + 0) * 6 = 0.0
        self.assertEqual(enriched_output[variable_names.EXPENSE], 0.0)

    def test_evaluate_missing_months_timeline_anchor_raises_key_error(self):
        """Verify that omitting the required pipeline time horizon triggers standard validation warnings."""
        incomplete_inputs = {
            variable_names.EXPENSE_MONTHLY_RENT: 1500.0
            # Missing MONTHS constraint!
        }
        model = ExpenseModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
