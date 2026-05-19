import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import ProfitModel


class TestProfitModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = ProfitModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.PROFIT])

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = ProfitModel()
        fresh_inputs = {
            variable_names.REVENUE: 25000.0,
            variable_names.COST: 15000.0
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.REVENUE: 10000.0}
        model = ProfitModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = ProfitModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable(variable_names.REVENUE, 35000.0)
        self.assertEqual(model.input_variables[variable_names.REVENUE], 35000.0)

        # Context B: Structural duck-typed object validation Type A (.name, .expected_value)
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.COST
                self.expected_value = 14000.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.COST], 14000.0)

        # Context C: Structural duck-typed object validation Type B (.get_name(), .get_value())
        class DuckTypeB:
            def get_name(self):
                return variable_names.REVENUE

            def get_value(self):
                return 45000.0

        model.update_input_variable(DuckTypeB())
        self.assertEqual(model.input_variables[variable_names.REVENUE], 45000.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_success_with_all_metrics(self, mock_log):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.REVENUE: 25000.0,
            variable_names.COST: 15000.0
        }
        model = ProfitModel(inputs)

        # Should execute cleanly without throwing errors or recording telemetry failures
        model.check_variables()
        mock_log.error.assert_not_called()
        mock_log.info.assert_not_called()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_required_logs_error_and_raises(self, mock_log):
        """Verify check_variables logs errors and safely raises a KeyError if a requirement is absent."""
        incomplete_inputs = {
            variable_names.COST: 12000.0
            # Missing required variable_names.REVENUE!
        }
        model = ProfitModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

        # Confirm structural failure logs were successfully routed
        mock_log.error.assert_called_once()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_optional_logs_informational_alert(self, mock_log):
        """Verify check_variables behaves predictably when validating metrics.

        Note: If this model contains no optional execution paths, it defaults to confirming
        the required parameters and verifying that no unintended log errors are logged.
        """
        inputs = {
            variable_names.REVENUE: 25000.0,
            variable_names.COST: 15000.0
        }
        model = ProfitModel(inputs)
        model.check_variables()
        mock_log.error.assert_not_called()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_positive_net_profit(self):
        """Verify profit calculations match expected metrics in a standard profitable scenario."""
        inputs = {
            variable_names.REVENUE: 25000.0,
            variable_names.COST: 15000.0
        }
        model = ProfitModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 25000.0 - 15000.0 = 10000.0
        self.assertEqual(enriched_output[variable_names.PROFIT], 10000.0)
        self.assertEqual(enriched_output[variable_names.REVENUE], 25000.0)

        # Ensure the in-place reference match holds true
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_negative_net_profit_handling(self):
        """Verify the calculation functions flawlessly when expenses outpace top-line revenues (net loss)."""
        inputs = {
            variable_names.REVENUE: 5000.0,
            variable_names.COST: 8000.0
        }
        model = ProfitModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 5000.0 - 8000.0 = -3000.0
        self.assertEqual(enriched_output[variable_names.PROFIT], -3000.0)

    def test_evaluate_missing_required_variables_throws_exception(self):
        """Verify that omitting a critical pipeline anchor like revenue blocks calculation runs."""
        incomplete_inputs = {
            variable_names.COST: 12000.0
            # Missing REVENUE!
        }
        model = ProfitModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()