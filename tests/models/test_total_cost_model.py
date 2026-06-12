import unittest

from src.config import variable_names
from src.models import TotalCostModel


class TestTotalCostModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify output footprint and required variables (COGS is mandatory)."""
        model = TotalCostModel()

        self.assertEqual(model.output_names, [variable_names.COST])
        self.assertEqual(model.required_variables, [variable_names.COGS])

    def test_internal_optional_variables_is_dict(self):
        """Verify setup_cost is removed and optional variables reflect OPEX only."""
        model = TotalCostModel()
        self.assertEqual(
            model._optional_variables,
            {
                variable_names.ADVERTISING_COST: 0.0,
                variable_names.SHIPPING_COST: 0.0
            }
        )

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify consolidated operational cost (COGS + ADS + SHIPPING)."""
        inputs = {
            variable_names.COGS: 5000.0,
            variable_names.ADVERTISING_COST: 1500.0,
            variable_names.SHIPPING_COST: 500.0
        }
        model = TotalCostModel(inputs)
        enriched_output = model.evaluate()

        # Math: 5000 + 1500 + 500 = 7000
        self.assertEqual(enriched_output[variable_names.COST], 7000.0)

    def test_evaluate_success_with_omitted_optional_values(self):
        """Verify that omitting optional ADS/SHIPPING costs defaults to 0.0 correctly."""
        inputs = {
            variable_names.COGS: 5000.0
            # ADVERTISING_COST and SHIPPING_COST omitted
        }
        model = TotalCostModel(inputs)
        enriched_output = model.evaluate()

        # Math: 5000 + 0 + 0 = 5000
        self.assertEqual(enriched_output[variable_names.COST], 5000.0)

    def test_check_variables_raises_error_on_missing_cogs(self):
        """Verify that the engine correctly mandates COGS as a required dependency."""
        model = TotalCostModel(input_variables={})

        with self.assertRaises(KeyError):
            model.evaluate()

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation(self):
        """Verify individual variable updates work post-initialization."""
        model = TotalCostModel({variable_names.COGS: 1000.0})
        model.update_input_variable(variable_names.ADVERTISING_COST, 200.0)

        result = model.evaluate()
        self.assertEqual(result[variable_names.COST], 1200.0)


if __name__ == "__main__":
    unittest.main()
