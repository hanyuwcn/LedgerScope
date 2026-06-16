import unittest

from src.config import variable_names
from src.models import UnitRetailMarginModel


class TestUnitRetailMarginModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = UnitRetailMarginModel()

        # Verify output registry signature
        self.assertEqual(model.output_names, [variable_names.UNIT_RETAIL_MARGIN])

        # Verify explicit required variable signature
        self.assertEqual(
            sorted(model.required_variables),
            sorted([variable_names.UNIT_RETAIL_PRICE, variable_names.CHANNEL_MARKUP_RATE])
        )

        # Verify no optional variables are registered
        self.assertEqual(model.optional_variables, [])

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_success_with_valid_parameters(self):
        """Verify UnitRetailMargin calculation: UnitRetailPrice * ChannelMarkupRate."""
        # Math: 100.0 * 0.25 = 25.0
        inputs = {
            variable_names.UNIT_RETAIL_PRICE: 100.0,
            variable_names.CHANNEL_MARKUP_RATE: 0.25
        }
        model = UnitRetailMarginModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[variable_names.UNIT_RETAIL_MARGIN], 25.0)
        self.assertIs(enriched_output, model.input_variables)

    def test_check_variables_missing_required_raises_error(self):
        """Verify check_variables catches missing mandatory fields."""
        incomplete_inputs = {variable_names.UNIT_RETAIL_PRICE: 100.0}
        model = UnitRetailMarginModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation(self):
        """Verify dynamic updates to the UnitRetailMarginModel context."""
        model = UnitRetailMarginModel()
        model.update_input_variable(variable_names.UNIT_RETAIL_PRICE, 200.0)
        model.update_input_variable(variable_names.CHANNEL_MARKUP_RATE, 0.30)

        # 200.0 * 0.30 = 60.0
        result = model.evaluate()
        self.assertEqual(result[variable_names.UNIT_RETAIL_MARGIN], 60.0)


if __name__ == "__main__":
    unittest.main()
