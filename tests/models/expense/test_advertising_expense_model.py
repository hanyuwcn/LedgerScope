import unittest

from src.config import variable_names as vn
from src.models import AdvertisingExpenseModel


class TestAdvertisingExpenseModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds and output configurations."""
        model = AdvertisingExpenseModel()

        # Verify output registry
        self.assertEqual(model.output_names, [vn.ADVERTISING_EXPENSE])

        # Verify required variable mapping
        self.assertEqual(model.required_variables, [vn.MARKETING_EXPENSE])

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_success_with_marketing_expense(self):
        """Verify AdvertisingExpense equals MarketingExpense."""
        inputs = {vn.MARKETING_EXPENSE: 5000.0}
        model = AdvertisingExpenseModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[vn.ADVERTISING_EXPENSE], 5000.0)

    def test_evaluate_missing_required_variables_raises_key_error(self):
        """Verify that missing the mandatory marketing expense halts execution."""
        model = AdvertisingExpenseModel({})

        with self.assertRaises(KeyError):
            model.evaluate()

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation(self):
        """Verify dynamic updates to the model context."""
        model = AdvertisingExpenseModel()
        model.update_input_variable(vn.MARKETING_EXPENSE, 12000.0)

        result = model.evaluate()
        self.assertEqual(result[vn.ADVERTISING_EXPENSE], 12000.0)


if __name__ == "__main__":
    unittest.main()
