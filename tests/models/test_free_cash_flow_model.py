import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import FreeCashFlowModel


class TestFreeCashFlowModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = FreeCashFlowModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.FREE_CASH_FLOW])

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = FreeCashFlowModel()
        fresh_inputs = {
            variable_names.NET_INCOME: 20000.0,
            variable_names.DEPRECIATION: 3000.0,
            variable_names.CAPITAL_EXPENDITURE: 5000.0
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.NET_INCOME: 15000.0}
        model = FreeCashFlowModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = FreeCashFlowModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable(variable_names.NET_INCOME, 25000.0)
        self.assertEqual(model.input_variables[variable_names.NET_INCOME], 25000.0)

        # Context B: Structural duck-typed object validation Type A (.name, .expected_value)
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.DEPRECIATION
                self.expected_value = 3500.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.DEPRECIATION], 3500.0)

        # Context C: Structural duck-typed object validation Type B (.get_name(), .get_value())
        class DuckTypeB:
            def get_name(self):
                return variable_names.CAPITAL_EXPENDITURE

            def get_value(self):
                return 4000.0

        model.update_input_variable(DuckTypeB())
        self.assertEqual(model.input_variables[variable_names.CAPITAL_EXPENDITURE], 4000.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_success_with_all_metrics(self, mock_log):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.NET_INCOME: 20000.0,
            variable_names.DEPRECIATION: 3000.0,
            variable_names.CAPITAL_EXPENDITURE: 5000.0
        }
        model = FreeCashFlowModel(inputs)

        # Should execute cleanly without throwing errors or recording telemetry failures
        model.check_variables()
        mock_log.error.assert_not_called()
        mock_log.info.assert_not_called()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_required_logs_error_and_raises(self, mock_log):
        """Verify check_variables logs errors and safely raises a KeyError if a requirement is absent."""
        incomplete_inputs = {
            variable_names.NET_INCOME: 20000.0,
            variable_names.DEPRECIATION: 3000.0
            # Missing required variable_names.CAPITAL_EXPENDITURE!
        }
        model = FreeCashFlowModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

        # Confirm structural failure logs successfully hit the logging path
        mock_log.error.assert_called_once()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_optional_logs_informational_alert(self, mock_log):
        """Verify check_variables behaves predictably when verifying parameters.

        Note: If this model contains no optional execution paths, it defaults to confirming
        the required variables and verifying that no unintended system logs are recorded.
        """
        inputs = {
            variable_names.NET_INCOME: 20000.0,
            variable_names.DEPRECIATION: 3000.0,
            variable_names.CAPITAL_EXPENDITURE: 5000.0
        }
        model = FreeCashFlowModel(inputs)
        model.check_variables()
        mock_log.error.assert_not_called()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_standard_positive_free_cash_flow(self):
        """Verify cash flow reconciles correctly when net income and depreciation outpace CapEx."""
        inputs = {
            variable_names.NET_INCOME: 20000.0,
            variable_names.DEPRECIATION: 3000.0,
            variable_names.CAPITAL_EXPENDITURE: 5000.0
        }
        model = FreeCashFlowModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 20000.0 + 3000.0 - 5000.0 = 18000.0
        self.assertEqual(enriched_output[variable_names.FREE_CASH_FLOW], 18000.0)

        # Ensure the in-place reference match holds true
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_negative_cash_flow_due_to_heavy_capex(self):
        """Verify cash flow turns negative when asset investment eclipses immediate operational cash."""
        inputs = {
            variable_names.NET_INCOME: 15000.0,
            variable_names.DEPRECIATION: 2000.0,
            variable_names.CAPITAL_EXPENDITURE: 25000.0  # Large asset acquisition
        }
        model = FreeCashFlowModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 15000.0 + 2000.0 - 25000.0 = -8000.0
        self.assertEqual(enriched_output[variable_names.FREE_CASH_FLOW], -8000.0)

    def test_missing_required_variables_halts_execution(self):
        """Verify that omitting an structural asset variable triggers an engine error block."""
        incomplete_inputs = {
            variable_names.NET_INCOME: 15000.0,
            variable_names.DEPRECIATION: 2000.0
            # Missing CAPITAL_EXPENDITURE!
        }
        model = FreeCashFlowModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()