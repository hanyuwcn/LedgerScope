import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import AdvertisingEfficiencyModel


class TestAdvertisingEfficiencyModelComprehensive(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_metadata_and_getters_initialize_correctly(self):
        """Verify tracking constraints, output footprints, and default empty states."""
        model = AdvertisingEfficiencyModel()

        # Verify default constructor safety fallback
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify explicit subclass registration parameters
        self.assertEqual(model.output_names, [variable_names.DEAL_ORDERS])

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_and_getter_happy_path(self):
        """Verify the property setter completely overwrites and binds the active state."""
        model = AdvertisingEfficiencyModel()
        fresh_inputs = {
            variable_names.COST_ADVERTISING: 5000,
            variable_names.COST_CONVERSION_RATE: 0.08,
            variable_names.COST_CPA: 15
        }

        # Fire property setter
        model.input_variables = fresh_inputs

        # Verify getter returns the exact structural dictionary reference
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify that passing None to the property setter securely defaults to an empty dictionary."""
        initial_inputs = {variable_names.COST_ADVERTISING: 2500}
        model = AdvertisingEfficiencyModel(initial_inputs)

        # Overwrite context explicitly with None via property assign
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_update_input_variable_with_raw_string_key(self):
        """Verify individual metric updates when providing raw string identities and values."""
        model = AdvertisingEfficiencyModel()
        model.update_input_variable(variable_names.COST_ADVERTISING, 12000)
        self.assertEqual(model.input_variables[variable_names.COST_ADVERTISING], 12000)

    def test_update_input_variable_with_duck_typed_properties(self):
        """Verify individual metric updates using domain variable Type A objects (.name, .expected_value)."""
        model = AdvertisingEfficiencyModel()

        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.COST_CONVERSION_RATE
                self.expected_value = 0.06

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.COST_CONVERSION_RATE], 0.06)

    def test_update_input_variable_with_duck_typed_getters(self):
        """Verify individual metric updates using domain variable Type B objects (.get_name(), .get_value())."""
        model = AdvertisingEfficiencyModel()

        class DuckTypeB:
            def get_name(self):
                return variable_names.COST_CPA

            def get_value(self):
                return 22.5

        model.update_input_variable(DuckTypeB())
        self.assertEqual(model.input_variables[variable_names.COST_CPA], 22.5)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_success_with_all_metrics(self, mock_log):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.COST_ADVERTISING: 5000,
            variable_names.COST_CONVERSION_RATE: 0.05,
            variable_names.COST_CPA: 20,
            variable_names.FINANCE_USD_TO_RMB: 7.0
        }
        model = AdvertisingEfficiencyModel(inputs)

        # Should clear without raising exceptions or logging errors
        model.check_variables()
        mock_log.error.assert_not_called()
        mock_log.info.assert_not_called()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_required_logs_error_and_raises(self, mock_log):
        """Verify check_variables triggers process-halting error logs and raises a KeyError if a requirement is absent."""
        incomplete_inputs = {
            variable_names.COST_ADVERTISING: 5000,
            variable_names.COST_CONVERSION_RATE: 0.05
            # Missing variable_names.COST_CPA!
        }
        model = AdvertisingEfficiencyModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

        # Assert the internal framework captured the structural omission via error logger
        mock_log.error.assert_called_once()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_optional_logs_informational_alert(self, mock_log):
        """Verify check_variables registers an informational alert but lets processing pass if an optional is absent."""
        valid_inputs_no_optional = {
            variable_names.COST_ADVERTISING: 5000,
            variable_names.COST_CONVERSION_RATE: 0.05,
            variable_names.COST_CPA: 20
            # Missing optional variable_names.FINANCE_USD_TO_RMB!
        }
        model = AdvertisingEfficiencyModel(valid_inputs_no_optional)

        # Execution must pass seamlessly
        model.check_variables()

        # Verify tracking system noted the omission gracefully
        mock_log.error.assert_not_called()
        mock_log.info.assert_called_once()

    # -----------------------------------------------------------------
    # 5. RUNTIME MATHEMATICAL EVALUATIONS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify formula execution wraps currency exchange constraints perfectly when fully specified."""
        inputs = {
            variable_names.COST_ADVERTISING: 10000,
            variable_names.COST_CONVERSION_RATE: 0.05,
            variable_names.COST_CPA: 20,
            variable_names.FINANCE_USD_TO_RMB: 7.0
        }
        model = AdvertisingEfficiencyModel(inputs)
        enriched_output = model.evaluate()

        # Calculation Check: (10000 * 0.05) / (20 * 7.0) = 500 / 140 = 3.571428...
        expected_orders = (10000 * 0.05) / (20 * 7.0)
        self.assertAlmostEqual(enriched_output[variable_names.DEAL_ORDERS], expected_orders, places=4)

        # Verify in-place structural validation rule
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_success_with_omitted_optional_currency_fallback(self):
        """Verify formula execution drops securely back to standard 1.0 unit scalar if optional is absent."""
        inputs = {
            variable_names.COST_ADVERTISING: 5000,
            variable_names.COST_CONVERSION_RATE: 0.10,
            variable_names.COST_CPA: 25
        }
        model = AdvertisingEfficiencyModel(inputs)
        enriched_output = model.evaluate()

        # Calculation Check: (5000 * 0.10) / (25 * 1.0) = 500 / 25 = 20
        self.assertEqual(enriched_output[variable_names.DEAL_ORDERS], 20)


if __name__ == "__main__":
    unittest.main()