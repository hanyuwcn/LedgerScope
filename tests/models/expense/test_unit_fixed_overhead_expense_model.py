import unittest

from src.config import variable_names
from src.models import UnitFixedOverheadExpenseModel


class TestUnitFixedOverheadExpenseModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = UnitFixedOverheadExpenseModel()

        # Verify output registry signature
        self.assertEqual(model.output_names, [variable_names.UNIT_FIXED_OVERHEAD_EXPENSE])

        # Verify explicit required variable signature
        self.assertEqual(
            sorted(model.required_variables),
            sorted([variable_names.MANAGEMENT_EXPENSE, variable_names.UNITS_SOLD])
        )

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_success_with_valid_parameters(self):
        """Verify UnitFixedOverheadExpense calculation: ManagementExpense / UnitsSold."""
        # Math: 5000.0 / 200 = 25.0
        inputs = {
            variable_names.MANAGEMENT_EXPENSE: 5000.0,
            variable_names.UNITS_SOLD: 200
        }
        model = UnitFixedOverheadExpenseModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[variable_names.UNIT_FIXED_OVERHEAD_EXPENSE], 25.0)
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_division_by_zero_safety(self):
        """Verify that zero sales volume returns 0.0 to prevent division errors."""
        inputs = {
            variable_names.MANAGEMENT_EXPENSE: 5000.0,
            variable_names.UNITS_SOLD: 0
        }
        model = UnitFixedOverheadExpenseModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[variable_names.UNIT_FIXED_OVERHEAD_EXPENSE], 0.0)

    def test_check_variables_missing_required_raises_error(self):
        """Verify check_variables catches missing mandatory fields."""
        incomplete_inputs = {variable_names.MANAGEMENT_EXPENSE: 5000.0}
        model = UnitFixedOverheadExpenseModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation(self):
        """Verify dynamic updates to the UnitFixedOverheadExpenseModel context."""
        model = UnitFixedOverheadExpenseModel()
        model.update_input_variable(variable_names.MANAGEMENT_EXPENSE, 10000.0)
        model.update_input_variable(variable_names.UNITS_SOLD, 50)

        # 10000 / 50 = 200.0
        result = model.evaluate()
        self.assertEqual(result[variable_names.UNIT_FIXED_OVERHEAD_EXPENSE], 200.0)


if __name__ == "__main__":
    unittest.main()
