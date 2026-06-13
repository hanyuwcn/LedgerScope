import unittest

from src.config import variable_names
from src.core.base_model import Model


# =====================================================================
# CONCRETE MOCK IMPLEMENTATION UTILIZING UNIFIED CONTEXT
# =====================================================================
class MockRevenueModel(Model):
    """
    Mock calculation processing logic utilizing the unified variable context
    provided by the base Model's prepare_calculation_context method.
    """

    def __init__(self, input_variables=None):
        super().__init__(input_variables)
        self._required_variables = [variable_names.ORDERS, variable_names.UNIT_FOB]
        self._optional_variables = {variable_names.TAX_RATE: 0.2}
        self._output_names = [variable_names.REVENUE, variable_names.PROFIT]
        self._model_function = self._calculate_revenue

    def _calculate_revenue(self, variables: dict) -> dict:
        """
        Receives a single unified variables dictionary.
        No kwargs or manual fallback management required here.
        """
        orders = variables[variable_names.ORDERS]
        unit_fob = variables[variable_names.UNIT_FOB]
        tax_rate = variables[variable_names.TAX_RATE]

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

    def test_prepare_calculation_context_merges_data_correctly(self):
        """Verify the new context preparation method correctly joins required and optional data."""
        inputs = {variable_names.ORDERS: 10, variable_names.UNIT_FOB: 100}
        model = MockRevenueModel(inputs)

        context = model.prepare_calculation_context()

        # Verify required and optional (defaulted) values exist
        self.assertEqual(context[variable_names.ORDERS], 10)
        self.assertEqual(context[variable_names.TAX_RATE], 0.2)

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
            @property
            def name(self) -> str:
                return variable_names.UNIT_FOB

            @property
            def expected_value(self):
                return 1500.0

        model.update_input_variable(MockMethodVariable())
        self.assertEqual(model.input_variables[variable_names.UNIT_FOB], 1500.0)

    # -----------------------------------------------------------------
    # 4. LIFECYCLE RUNTIME & VALIDATION TESTS
    # -----------------------------------------------------------------

    def test_evaluate_success_and_in_place_data_enrichment_merge(self):
        """Verify calculation execution using the unified variables context."""
        inputs = {variable_names.ORDERS: 20, variable_names.UNIT_FOB: 3000}
        model = MockRevenueModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[variable_names.REVENUE], 60000)
        self.assertEqual(enriched_output[variable_names.PROFIT], 48000)
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
        """Verify explicit optional overrides are respected via the unified context."""
        custom_inputs = {
            variable_names.ORDERS: 10,
            variable_names.UNIT_FOB: 1000,
            variable_names.TAX_RATE: 0.10
        }
        model = MockRevenueModel(custom_inputs)
        enriched_output = model.evaluate()

        # Profit = 10000 * (1 - 0.10) = 9000
        self.assertEqual(enriched_output[variable_names.PROFIT], 9000)


if __name__ == "__main__":
    unittest.main()
