import unittest

from src.config import variable_names
from src.models import UnitGrossProfitModel


class TestUnitGrossProfitModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = UnitGrossProfitModel()

        # Verify output registry signature
        self.assertEqual(model.output_names, [variable_names.UNIT_GROSS_PROFIT])

        # Verify explicit required variable signature
        self.assertEqual(
            set(model.required_variables),
            {variable_names.GROSS_PROFIT, variable_names.UNITS_SOLD}
        )

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_success_with_valid_parameters(self):
        """Verify UnitGrossProfit calculation: Profit / UnitsSold."""
        # Math: 10000.0 / 200 = 50.0
        inputs = {
            variable_names.GROSS_PROFIT: 10000.0,
            variable_names.UNITS_SOLD: 200
        }
        model = UnitGrossProfitModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[variable_names.UNIT_GROSS_PROFIT], 50.0)
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_division_by_zero_safety(self):
        """Verify that zero sales volume returns 0.0 profit to prevent crashes."""
        inputs = {
            variable_names.GROSS_PROFIT: 10000.0,
            variable_names.UNITS_SOLD: 0
        }
        model = UnitGrossProfitModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[variable_names.UNIT_GROSS_PROFIT], 0.0)

    def test_check_variables_missing_required_raises_error(self):
        """Verify check_variables catches missing mandatory fields."""
        incomplete_inputs = {variable_names.GROSS_PROFIT: 10000.0}
        model = UnitGrossProfitModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation(self):
        """Verify dynamic updates to the UnitGrossProfitModel context."""
        model = UnitGrossProfitModel()
        model.update_input_variable(variable_names.GROSS_PROFIT, 5000.0)
        model.update_input_variable(variable_names.UNITS_SOLD, 50)

        # 5000 / 50 = 100.0
        result = model.evaluate()
        self.assertEqual(result[variable_names.UNIT_GROSS_PROFIT], 100.0)


if __name__ == "__main__":
    unittest.main()
