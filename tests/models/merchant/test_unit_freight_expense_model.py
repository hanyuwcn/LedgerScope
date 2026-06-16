import unittest

from src.config import variable_names
from src.models import UnitMerchantFreightExpenseModel


class TestUnitMerchantFreightExpenseModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = UnitMerchantFreightExpenseModel()

        self.assertEqual(model.output_names, [variable_names.UNIT_MERCHANT_FREIGHT_EXPENSE])
        self.assertEqual(
            set(model.required_variables),
            {variable_names.UNIT_RETAIL_PRICE}
        )

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables matches expected defaults."""
        model = UnitMerchantFreightExpenseModel()
        self.assertEqual(
            model._optional_variables,
            {variable_names.MERCHANT_FREIGHT_RATE: 0.0}
        )

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify unit freight expense calculation."""
        # Math: 100.0 * 0.1 = 10.0
        inputs = {
            variable_names.UNIT_RETAIL_PRICE: 100.0,
            variable_names.MERCHANT_FREIGHT_RATE: 0.1
        }
        model = UnitMerchantFreightExpenseModel(inputs)
        enriched_output = model.evaluate()

        self.assertAlmostEqual(enriched_output[variable_names.UNIT_MERCHANT_FREIGHT_EXPENSE], 10.0, places=4)

    def test_evaluate_success_with_defaults(self):
        """Verify calculation falls back to default FREIGHT_RATE (0.0)."""
        # Math: 100.0 * 0.0 = 0.0
        inputs = {
            variable_names.UNIT_RETAIL_PRICE: 100.0
        }
        model = UnitMerchantFreightExpenseModel(inputs)
        enriched_output = model.evaluate()

        self.assertAlmostEqual(enriched_output[variable_names.UNIT_MERCHANT_FREIGHT_EXPENSE], 0.0, places=4)

    def test_check_variables_raises_error_on_missing_required(self):
        """Verify check_variables catches missing mandatory fields."""
        # UNIT_RETAIL_PRICE is required
        model = UnitMerchantFreightExpenseModel(input_variables={})

        with self.assertRaises(KeyError):
            model.evaluate()

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation(self):
        """Verify dynamic updates to the UnitMerchantFreightExpenseModel context."""
        model = UnitMerchantFreightExpenseModel()
        model.update_input_variable(variable_names.UNIT_RETAIL_PRICE, 200.0)
        model.update_input_variable(variable_names.MERCHANT_FREIGHT_RATE, 0.05)

        # 200.0 * 0.05 = 10.0
        result = model.evaluate()
        self.assertAlmostEqual(result[variable_names.UNIT_MERCHANT_FREIGHT_EXPENSE], 10.0, places=4)


if __name__ == "__main__":
    unittest.main()
