# tests/test_core/test_base_model.py

import unittest

from src.config import variable_names
from src.core.base_model import Model


# =====================================================================
# CONCRETE MOCK IMPLEMENTATION UTILIZING CENTRAL REGISTRY CONSTANTS
# =====================================================================
class MockRevenueModel(Model):
    """
    Mock calculation processing logic referencing central configuration variables
    as a single source of truth instead of raw hardcoded strings.
    """

    def __init__(self, input_variables=None):
        super().__init__(input_variables)

        # Enforcing single source of truth keys for input parameter bounds
        self._required_variables = [
            variable_names.DEAL_ORDERS,
            variable_names.DEAL_SELLING_PRICE
        ]
        self._optional_variables = [
            variable_names.FINANCE_TAX_RATE
        ]

        # Enforcing single source of truth keys for computational outputs
        self._output_names = [
            variable_names.REVENUE,
            variable_names.PROFIT  # Using PROFIT to represent net returns here
        ]
        self._model_function = self._calculate_revenue

    def _calculate_revenue(self, **kwargs) -> dict:
        """
        Dynamically extracts parameters via keyword arguments mapping directly
        to the global configuration variable names.
        """
        # Safely extract values using the global constant registry variables
        orders = kwargs[variable_names.DEAL_ORDERS]
        selling_price = kwargs[variable_names.DEAL_SELLING_PRICE]

        # Fallback to an internal default metric if the optional tax parameter is omitted
        tax_rate = kwargs.get(variable_names.FINANCE_TAX_RATE, 0.2)

        raw_revenue = orders * selling_price
        net_profit = raw_revenue * (1 - tax_rate)

        # Build payload mapping directly back to central source-of-truth constants
        return {
            variable_names.REVENUE: raw_revenue,
            variable_names.PROFIT: net_profit
        }


# =====================================================================
# COMPREHENSIVE ARCHITECTURAL VERIFICATION SUITE
# =====================================================================
class TestBaseModelArchitecture(unittest.TestCase):

    def test_model_initialization_state_is_clean(self):
        """Verify basic property mapping and empty state containers initialize securely."""
        model = MockRevenueModel()
        self.assertEqual(model.input_variables, {})

        # Output list must match centralized registry rules exactly
        expected_outputs = [variable_names.REVENUE, variable_names.PROFIT]
        self.assertEqual(model.output_names, expected_outputs)

    def test_polymorphic_update_input_variable_mappings(self):
        """Verify update_input_variable accommodates both raw map entries and structured values."""
        model = MockRevenueModel()

        # Test updating with primitive key-value inputs mapped via central registry global variables
        model.update_input_variable(variable_names.DEAL_ORDERS, 10)
        self.assertEqual(model.input_variables[variable_names.DEAL_ORDERS], 10)

        # Test updating with a duck-typed structural variable object
        class MockVariable:
            def get_name(self):
                return variable_names.DEAL_SELLING_PRICE

            def get_value(self):
                return 5000

        model.update_input_variable(MockVariable())
        self.assertEqual(model.input_variables[variable_names.DEAL_SELLING_PRICE], 5000)

    def test_evaluate_success_and_in_place_data_enrichment_merge(self):
        """Verify evaluation executes correctly and merges outputs smoothly into the shared state map."""
        inputs = {
            variable_names.DEAL_ORDERS: 20,
            variable_names.DEAL_SELLING_PRICE: 3000
        }
        model = MockRevenueModel(inputs)

        # Execution path runs successfully using the default optional tax rate fallback (0.2)
        enriched_output = model.evaluate()

        # Verify in-place contextual merging matches configuration variable signatures perfectly
        self.assertEqual(enriched_output[variable_names.DEAL_ORDERS], 20)
        self.assertEqual(enriched_output[variable_names.REVENUE], 60000)
        self.assertEqual(enriched_output[variable_names.PROFIT], 48000)

        # Verify state identity holds true across execution environment context references
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_missing_required_variables_breaks_process(self):
        """Verify missing mandatory execution parameters explicitly triggers an unhandled KeyError."""
        incomplete_inputs = {
            variable_names.DEAL_ORDERS: 20
        }  # Missing variable_names.DEAL_SELLING_PRICE context
        model = MockRevenueModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
