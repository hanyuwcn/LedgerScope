import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import GrossProfitModel


class TestGrossProfitModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = GrossProfitModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.GROSS_PROFIT])

        # Verify explicit required variable signature bounds (now using COGS)
        self.assertEqual(
            model.required_variables,
            [
                variable_names.REVENUE,
                variable_names.COGS
            ]
        )
        self.assertEqual(model.optional_variables, [])

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = GrossProfitModel()
        fresh_inputs = {
            variable_names.REVENUE: 25000.0,
            variable_names.COGS: 15000.0
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.REVENUE: 10000.0}
        model = GrossProfitModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = GrossProfitModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable(variable_names.REVENUE, 35000.0)
        self.assertEqual(model.input_variables[variable_names.REVENUE], 35000.0)

        # Context B: Structural duck-typed object validation
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.COGS
                self.expected_value = 14000.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.COGS], 14000.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_success_with_all_metrics(self, mock_log):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.REVENUE: 25000.0,
            variable_names.COGS: 15000.0
        }
        model = GrossProfitModel(inputs)

        model.check_variables()
        mock_log.error.assert_not_called()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_required_logs_error_and_raises(self, mock_log):
        """Verify check_variables logs errors and safely raises a KeyError if a requirement is absent."""
        incomplete_inputs = {
            variable_names.COGS: 12000.0
            # Missing REVENUE!
        }
        model = GrossProfitModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

        mock_log.error.assert_called_once()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_positive_gross_profit(self):
        """Verify profit calculations match expected metrics in a standard profitable scenario."""
        inputs = {
            variable_names.REVENUE: 25000.0,
            variable_names.COGS: 15000.0
        }
        model = GrossProfitModel(inputs)
        enriched_output = model.evaluate()

        # Math: 25000.0 - 15000.0 = 10000.0
        self.assertEqual(enriched_output[variable_names.GROSS_PROFIT], 10000.0)
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_negative_gross_profit_handling(self):
        """Verify the calculation functions flawlessly when COGS outpaces revenues (net loss)."""
        inputs = {
            variable_names.REVENUE: 5000.0,
            variable_names.COGS: 8000.0
        }
        model = GrossProfitModel(inputs)
        enriched_output = model.evaluate()

        # Math: 5000.0 - 8000.0 = -3000.0
        self.assertEqual(enriched_output[variable_names.GROSS_PROFIT], -3000.0)


if __name__ == "__main__":
    unittest.main()
