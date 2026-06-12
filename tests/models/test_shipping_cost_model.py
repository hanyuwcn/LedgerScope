import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import ShippingCostModel


class TestShippingCostModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = ShippingCostModel()

        self.assertEqual(model.output_names, [variable_names.SHIPPING_COST])
        self.assertEqual(
            set(model.required_variables),
            {variable_names.UNIT_RETAIL, variable_names.ORDERS, variable_names.UNITS_PER_ORDER}
        )

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables matches expected defaults."""
        model = ShippingCostModel()
        self.assertEqual(
            model._optional_variables,
            {
                variable_names.SHIPPING_RATE: 0.0,
                variable_names.USD_TO_RMB: 1.0
            }
        )

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify shipping cost calculation with explicit USD_TO_RMB conversion."""
        # Math: 100 * 7.2 * 0.1 * 10 * 2 = 1440.0
        inputs = {
            variable_names.UNIT_RETAIL: 100.0,
            variable_names.ORDERS: 10.0,
            variable_names.UNITS_PER_ORDER: 2.0,
            variable_names.SHIPPING_RATE: 0.1,
            variable_names.USD_TO_RMB: 7.2
        }
        model = ShippingCostModel(inputs)
        enriched_output = model.evaluate()

        self.assertAlmostEqual(enriched_output[variable_names.SHIPPING_COST], 1440.0, places=4)

    def test_evaluate_success_with_defaults(self):
        """Verify calculation falls back to default SHIPPNG_RATE (0.0) and USD_TO_RMB (1.0)."""
        # Math: 100 * 1.0 * 0.0 * 10 * 2 = 0.0
        inputs = {
            variable_names.UNIT_RETAIL: 100.0,
            variable_names.ORDERS: 10.0,
            variable_names.UNITS_PER_ORDER: 2.0
        }
        model = ShippingCostModel(inputs)
        enriched_output = model.evaluate()

        self.assertAlmostEqual(enriched_output[variable_names.SHIPPING_COST], 0.0, places=4)

    def test_check_variables_raises_error_on_missing_required(self):
        """Verify check_variables catches missing mandatory fields."""
        model = ShippingCostModel(input_variables={variable_names.UNIT_RETAIL: 10.0})

        # Should raise KeyError because ORDERS and UNITS_PER_ORDER are missing
        with self.assertRaises(KeyError):
            model.evaluate()

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation(self):
        """Verify dynamic updates to the ShippingCostModel context."""
        model = ShippingCostModel()
        model.update_input_variable(variable_names.UNIT_RETAIL, 50.0)
        model.update_input_variable(variable_names.ORDERS, 5.0)
        model.update_input_variable(variable_names.UNITS_PER_ORDER, 1.0)
        model.update_input_variable(variable_names.SHIPPING_RATE, 0.2)

        # 50 * 1.0 * 0.2 * 5 * 1 = 50.0
        result = model.evaluate()
        self.assertAlmostEqual(result[variable_names.SHIPPING_COST], 50.0, places=4)


if __name__ == "__main__":
    unittest.main()