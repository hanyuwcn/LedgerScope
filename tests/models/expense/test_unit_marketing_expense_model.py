import unittest

from src.config import variable_names
from src.models import UnitMarketingExpenseModel


class TestUnitMarketingExpenseModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = UnitMarketingExpenseModel()

        # Verify output registry signature
        self.assertEqual(model.output_names, [variable_names.UNIT_MARKETING_EXPENSE])

        # Verify explicit required variable signature
        self.assertEqual(
            sorted(model.required_variables),
            sorted([variable_names.MARKETING_EXPENSE, variable_names.UNITS_SOLD])
        )

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_success_with_valid_parameters(self):
        """Verify UnitMarketingExpense calculation: MarketingExpense / UnitsSold."""
        # Math: 10000.0 / 500 = 20.0
        inputs = {
            variable_names.MARKETING_EXPENSE: 10000.0,
            variable_names.UNITS_SOLD: 500
        }
        model = UnitMarketingExpenseModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[variable_names.UNIT_MARKETING_EXPENSE], 20.0)
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_division_by_zero_safety(self):
        """Verify that zero sales volume returns 0.0 to prevent division errors."""
        inputs = {
            variable_names.MARKETING_EXPENSE: 10000.0,
            variable_names.UNITS_SOLD: 0
        }
        model = UnitMarketingExpenseModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[variable_names.UNIT_MARKETING_EXPENSE], 0.0)

    def test_check_variables_missing_required_raises_error(self):
        """Verify check_variables catches missing mandatory fields."""
        incomplete_inputs = {variable_names.MARKETING_EXPENSE: 5000.0}
        model = UnitMarketingExpenseModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation(self):
        """Verify dynamic updates to the UnitMarketingExpenseModel context."""
        model = UnitMarketingExpenseModel()
        model.update_input_variable(variable_names.MARKETING_EXPENSE, 2000.0)
        model.update_input_variable(variable_names.UNITS_SOLD, 100)

        # 2000 / 100 = 20.0
        result = model.evaluate()
        self.assertEqual(result[variable_names.UNIT_MARKETING_EXPENSE], 20.0)


if __name__ == "__main__":
    unittest.main()
