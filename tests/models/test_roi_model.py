import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import RoiModel


class TestRoiModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = RoiModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.ROI])

        # Verify explicit required variable signature bounds (now lean)
        self.assertEqual(
            model.required_variables,
            [
                variable_names.NET_INCOME,
                variable_names.COST
            ]
        )

        # Verify optional variable signature bounds capture all infrastructure overhead constants
        self.assertEqual(
            sorted(model.optional_variables),
            sorted([
                variable_names.EXPENSE,
                variable_names.CAPITAL_EXPENDITURE
            ])
        )

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables matches the dictionary footprint."""
        model = RoiModel()
        self.assertIsInstance(model._optional_variables, dict)
        self.assertEqual(
            model._optional_variables,
            {
                variable_names.EXPENSE: 0.0,
                variable_names.CAPITAL_EXPENDITURE: 0.0
            }
        )

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = RoiModel()
        fresh_inputs = {
            variable_names.NET_INCOME: 15000.0,
            variable_names.COST: 20000.0,
            variable_names.EXPENSE: 5000.0,
            variable_names.CAPITAL_EXPENDITURE: 5000.0
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.NET_INCOME: 5000.0}
        model = RoiModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = RoiModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable(variable_names.NET_INCOME, 25000.0)
        self.assertEqual(model.input_variables[variable_names.NET_INCOME], 25000.0)

        # Context B: Structural duck-typed object validation Type A (.name, .expected_value)
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.COST
                self.expected_value = 18000.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.COST], 18000.0)

        # Context C: Structural duck-typed object validation Type B (.get_name(), .get_value())
        class DuckTypeB:
            def get_name(self):
                return variable_names.CAPITAL_EXPENDITURE

            def get_value(self):
                return 6000.0

        model.update_input_variable(DuckTypeB())
        self.assertEqual(model.input_variables[variable_names.CAPITAL_EXPENDITURE], 6000.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_success_with_all_metrics(self, mock_log):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.NET_INCOME: 15000.0,
            variable_names.COST: 20000.0,
            variable_names.EXPENSE: 5000.0,
            variable_names.CAPITAL_EXPENDITURE: 5000.0
        }
        model = RoiModel(inputs)

        # Should execute cleanly without throwing errors or recording telemetry failures
        model.check_variables()
        mock_log.error.assert_not_called()
        mock_log.info.assert_not_called()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_required_logs_error_and_raises(self, mock_log):
        """Verify check_variables logs errors and safely raises a KeyError if a core requirement is absent."""
        incomplete_inputs = {
            variable_names.NET_INCOME: 15000.0
            # Missing strictly required variable_names.COST parameter anchor!
        }
        model = RoiModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

        # Confirm structural failure logs successfully hit the telemetry subsystem
        mock_log.error.assert_called_once()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_optional_logs_informational_alert(self, mock_log):
        """Verify check_variables logs informational trace logs when optional parameter layers are absent."""
        inputs = {
            variable_names.NET_INCOME: 15000.0,
            variable_names.COST: 20000.0
            # Optional keys (EXPENSE, CAPITAL_EXPENDITURE) are omitted entirely
        }
        model = RoiModel(inputs)
        model.check_variables()

        mock_log.error.assert_not_called()
        self.assertTrue(mock_log.info.called)

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_lean_project_roi_without_optional_parameters(self):
        """Verify calculation works cleanly under zero-overhead lean scenarios using system fallbacks."""
        inputs = {
            variable_names.NET_INCOME: 5000.0,
            variable_names.COST: 10000.0
            # EXPENSE and CAPITAL_EXPENDITURE omitted intentionally to default to 0.0
        }
        model = RoiModel(inputs)
        enriched_output = model.evaluate()

        # Denominator: 10000 + 0.0 + 0.0 = 10000.0 total outlay
        # ROI Math: 5000.0 / 10000.0 = 0.5 (50% ROI)
        self.assertEqual(enriched_output[variable_names.ROI], 0.5)

    def test_evaluate_standard_positive_project_roi(self):
        """Verify ROI calculations yield standard positive fractional percentages."""
        inputs = {
            variable_names.NET_INCOME: 15000.0,
            variable_names.COST: 20000.0,
            variable_names.EXPENSE: 5000.0,
            variable_names.CAPITAL_EXPENDITURE: 5000.0
        }
        model = RoiModel(inputs)
        enriched_output = model.evaluate()

        # Denominator: 20000 + 5000 + 5000 = 30000.0 total outlay
        # ROI Math: 15000.0 / 30000.0 = 0.5 (50% ROI)
        self.assertEqual(enriched_output[variable_names.ROI], 0.5)

        # Ensure the in-place reference match holds true
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_negative_roi_from_net_loss(self):
        """Verify ROI correctly evaluates to a negative percentage when a net income loss is present."""
        inputs = {
            variable_names.NET_INCOME: -5000.0,
            variable_names.COST: 15000.0,
            variable_names.EXPENSE: 3000.0,
            variable_names.CAPITAL_EXPENDITURE: 2000.0
        }
        model = RoiModel(inputs)
        enriched_output = model.evaluate()

        # Denominator: 15000 + 3000 + 2000 = 20000.0 total outlay
        # ROI Math: -5000.0 / 20000.0 = -0.25 (-25% ROI)
        self.assertEqual(enriched_output[variable_names.ROI], -0.25)

    def test_division_by_zero_safety_catch(self):
        """Verify engine intercepts empty outlays and defaults to 0.0 instead of crashing."""
        edge_case_inputs = {
            variable_names.NET_INCOME: 1000.0,
            variable_names.COST: 0.0,
            variable_names.EXPENSE: 0.0,
            variable_names.CAPITAL_EXPENDITURE: 0.0
        }
        model = RoiModel(edge_case_inputs)
        enriched_output = model.evaluate()

        # System intercepts total_outlay == 0 and maps ROI cleanly to 0.0
        self.assertEqual(enriched_output[variable_names.ROI], 0.0)

    def test_missing_required_variables_halts_execution(self):
        """Verify that omitting a critical core pipeline anchor like Cost halts evaluation runs."""
        incomplete_inputs = {
            variable_names.NET_INCOME: 15000.0,
            variable_names.EXPENSE: 5000.0
            # Missing strictly required COST input variable mapping!
        }
        model = RoiModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
