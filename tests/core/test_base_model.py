# tests/domain/test_base_model.py

import unittest

# Assuming standard package mapping layout based on your imports
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
            variable_names.ORDERS,
            variable_names.UNIT_FOB
        ]

        # Mapped to their default fallback values to support runtime lookups
        self._optional_variables = {
            variable_names.TAX_RATE: 0.2
        }

        # Enforcing single source of truth keys for computational outputs
        self._output_names = [
            variable_names.REVENUE,
            variable_names.PROFIT  # Using PROFIT to represent net returns here
        ]
        self._model_function = self._calculate_revenue

    def _calculate_revenue(self, optional_variables: dict, **kwargs) -> dict:
        """
        Dynamically extracts parameters via keyword arguments mapping directly
        to the global configuration variable names. Receives the base model's
        optional variable registry as its first parameter.
        """
        orders = kwargs[variable_names.ORDERS]
        unit_fob = kwargs[variable_names.UNIT_FOB]

        # Fallback dynamically to the passed dictionary default if omitted from inputs
        default_tax = optional_variables[variable_names.TAX_RATE]
        tax_rate = kwargs.get(variable_names.TAX_RATE, default_tax)

        raw_revenue = orders * unit_fob
        net_profit = raw_revenue * (1 - tax_rate)

        return {
            variable_names.REVENUE: raw_revenue,
            variable_names.PROFIT: net_profit
        }


# =====================================================================
# COMPREHENSIVE ARCHITECTURAL VERIFICATION SUITE
# =====================================================================
class TestBaseModelArchitecture(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & INITIAL STATE TESTS
    # -----------------------------------------------------------------

    def test_model_initialization_defaults_to_empty_dictionary(self):
        """Verify that passing no inputs securely initializes input_variables to a clean dict."""
        model = MockRevenueModel()
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

    def test_model_initialization_with_none_safeguard(self):
        """Verify that explicitly passing None to the constructor forces an empty dictionary fallback."""
        model = MockRevenueModel(input_variables=None)
        self.assertEqual(model.input_variables, {})

    def test_model_initialization_retains_provided_dictionary(self):
        """Verify that initial input dictionaries are bound correctly to the internal state container."""
        initial_payload = {variable_names.ORDERS: 100}
        model = MockRevenueModel(input_variables=initial_payload)
        self.assertEqual(model.input_variables, initial_payload)
        self.assertEqual(model.input_variables[variable_names.ORDERS], 100)

    def test_output_names_getter(self):
        """Verify that output_names property correctly exposes the model's registered outputs."""
        model = MockRevenueModel()
        expected_outputs = [variable_names.REVENUE, variable_names.PROFIT]
        self.assertEqual(model.output_names, expected_outputs)

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables transitioned cleanly to a dictionary mapping."""
        model = MockRevenueModel()
        self.assertIsInstance(model._optional_variables, dict)
        self.assertEqual(model._optional_variables[variable_names.TAX_RATE], 0.2)

    def test_public_optional_variables_returns_list_keys(self):
        """Verify public contract exposes a flat list of keys preserving backward compatibility."""
        model = MockRevenueModel()
        expected_list = [variable_names.TAX_RATE]
        self.assertIsInstance(model.optional_variables, list)
        self.assertEqual(model.optional_variables, expected_list)

    # -----------------------------------------------------------------
    # 2. PROPERTY GETTER & SETTER TESTS (THE CURRENT CONTRACT)
    # -----------------------------------------------------------------

    def test_input_variables_getter_and_setter_happy_path(self):
        """Verify the property getter/setter can completely overwrite the state with a valid dictionary."""
        model = MockRevenueModel()
        fresh_state = {
            variable_names.ORDERS: 50,
            variable_names.UNIT_FOB: 20.0
        }

        # Trigger the setter
        model.input_variables = fresh_state

        # Trigger the getter and verify identity/content
        self.assertEqual(model.input_variables, fresh_state)
        self.assertIs(model.input_variables, fresh_state)

    def test_input_variables_setter_none_fallback(self):
        """Verify that setting input_variables property to None safely clears state to an empty dict."""
        initial_payload = {variable_names.ORDERS: 100}
        model = MockRevenueModel(input_variables=initial_payload)

        # Overwrite with None via setter
        model.input_variables = None

        # Verify defensive fallback kicked in
        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC INDIVIDUAL VARIABLE UPDATE TESTS
    # -----------------------------------------------------------------

    def test_update_input_variable_with_raw_string_key(self):
        """Verify updating with standard raw string keys maps inputs exactly."""
        model = MockRevenueModel()
        model.update_input_variable("CUSTOM_VARIABLE_KEY", 999.5)
        self.assertEqual(model.input_variables["CUSTOM_VARIABLE_KEY"], 999.5)

    def test_update_input_variable_with_duck_typed_name_and_expected_value(self):
        """Verify polymorphic update handles Domain Objects using 'name' and 'expected_value' properties."""
        model = MockRevenueModel()

        class MockPropertyVariable:
            def __init__(self):
                self.name = variable_names.ORDERS
                self.expected_value = 45

        model.update_input_variable(MockPropertyVariable())
        self.assertEqual(model.input_variables[variable_names.ORDERS], 45)

    def test_update_input_variable_with_duck_typed_getter_methods(self):
        """Verify polymorphic update handles Domain Objects using 'get_name()' and 'get_value()' methods."""
        model = MockRevenueModel()

        class MockMethodVariable:
            def get_name(self):
                return variable_names.UNIT_FOB

            def get_value(self):
                return 1500.0

        model.update_input_variable(MockMethodVariable())
        self.assertEqual(model.input_variables[variable_names.UNIT_FOB], 1500.0)

    # -----------------------------------------------------------------
    # 4. LIFECYCLE RUNTIME & VALIDATION TESTS
    # -----------------------------------------------------------------

    def test_evaluate_success_and_in_place_data_enrichment_merge(self):
        """Verify successful calculation execution and structural in-place state enrichment."""
        inputs = {
            variable_names.ORDERS: 20,
            variable_names.UNIT_FOB: 3000
        }
        model = MockRevenueModel(inputs)

        # Triggers evaluation using default fallback tax rate (0.2)
        enriched_output = model.evaluate()

        # 1. Verify original input values are perfectly retained
        self.assertEqual(enriched_output[variable_names.ORDERS], 20)
        self.assertEqual(enriched_output[variable_names.UNIT_FOB], 3000)

        # 2. Verify model calculation outputs are correctly appended
        self.assertEqual(enriched_output[variable_names.REVENUE], 60000)
        self.assertEqual(enriched_output[variable_names.PROFIT], 48000)

        # 3. Critical verification of In-Place Merge strategy: returned dict IS the active state container
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_missing_required_variables_halts_execution(self):
        """Verify that omitting a mandatory input parameter actively raises an unhandled KeyError."""
        incomplete_inputs = {
            variable_names.ORDERS: 20
        }  # Missing variable_names.UNIT_FOB string key identifier
        model = MockRevenueModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()

    def test_evaluate_accepts_optional_variables_safely(self):
        """Verify that passing an optional parameter bypasses default internal fallbacks cleanly."""
        custom_inputs = {
            variable_names.ORDERS: 10,
            variable_names.UNIT_FOB: 1000,
            variable_names.TAX_RATE: 0.10  # Explicit custom optional override
        }
        model = MockRevenueModel(custom_inputs)

        enriched_output = model.evaluate()

        # Revenue = 10 * 1000 = 10000. Profit = 10000 * (1 - 0.10) = 9000
        self.assertEqual(enriched_output[variable_names.REVENUE], 10000)
        self.assertEqual(enriched_output[variable_names.PROFIT], 9000)


if __name__ == "__main__":
    unittest.main()
