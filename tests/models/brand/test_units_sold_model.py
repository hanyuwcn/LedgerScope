import unittest

from src.config import variable_names
from src.models import UnitsSoldModel


class TestUnitsSoldModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = UnitsSoldModel()

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.UNITS_SOLD])

        # Verify explicit required variable signature bounds
        self.assertEqual(
            set(model.required_variables),
            {variable_names.ORDERS, variable_names.UNITS_PER_ORDER}
        )
        self.assertEqual(model.optional_variables, [])

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_success_with_valid_parameters(self):
        """Verify UnitsSold calculation executes correctly (Orders * UnitsPerOrder)."""
        # Math: 50 * 3 = 150
        inputs = {
            variable_names.ORDERS: 50,
            variable_names.UNITS_PER_ORDER: 3
        }
        model = UnitsSoldModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[variable_names.UNITS_SOLD], 150)
        self.assertIs(enriched_output, model.input_variables)

    def test_check_variables_missing_required_raises_error(self):
        """Verify check_variables catches missing mandatory fields."""
        incomplete_inputs = {variable_names.ORDERS: 50}
        model = UnitsSoldModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation(self):
        """Verify dynamic updates to the UnitsSoldModel context."""
        model = UnitsSoldModel()
        model.update_input_variable(variable_names.ORDERS, 20)
        model.update_input_variable(variable_names.UNITS_PER_ORDER, 5)

        # 20 * 5 = 100
        result = model.evaluate()
        self.assertEqual(result[variable_names.UNITS_SOLD], 100)


if __name__ == "__main__":
    unittest.main()
