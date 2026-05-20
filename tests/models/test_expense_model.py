import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import ExpenseModel


class TestExpenseModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = ExpenseModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.EXPENSE])

        # Verify explicit required and optional variable signature bounds
        self.assertEqual(
            model.required_variables,
            []
        )
        self.assertEqual(
            model.optional_variables,
            [
                variable_names.EXPENSE_MONTHLY_RENT,
                variable_names.EXPENSE_RENDER_FEE,
                variable_names.EXPENSE_TRAVEL_FEE,
                variable_names.MONTHS
            ]
        )

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = ExpenseModel()
        fresh_inputs = {
            variable_names.MONTHS: 12,
            variable_names.EXPENSE_MONTHLY_RENT: 2000.0,
            variable_names.EXPENSE_RENDER_FEE: 500.0
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.MONTHS: 6}
        model = ExpenseModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = ExpenseModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable(variable_names.MONTHS, 24)
        self.assertEqual(model.input_variables[variable_names.MONTHS], 24)

        # Context B: Structural duck-typed object validation Type A (.name, .expected_value)
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.EXPENSE_MONTHLY_RENT
                self.expected_value = 1800.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.EXPENSE_MONTHLY_RENT], 1800.0)

        # Context C: Structural duck-typed object validation Type B (.get_name(), .get_value())
        class DuckTypeB:
            def get_name(self):
                return variable_names.EXPENSE_RENDER_FEE

            def get_value(self):
                return 350.0

        model.update_input_variable(DuckTypeB())
        self.assertEqual(model.input_variables[variable_names.EXPENSE_RENDER_FEE], 350.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_success_with_all_metrics(self, mock_log):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.MONTHS: 12,
            variable_names.EXPENSE_MONTHLY_RENT: 2000.0,
            variable_names.EXPENSE_RENDER_FEE: 500.0,
            variable_names.EXPENSE_TRAVEL_FEE: 300.0
        }
        model = ExpenseModel(inputs)

        # Should execute cleanly without throwing errors or recording telemetry failures
        model.check_variables()
        mock_log.error.assert_not_called()
        mock_log.info.assert_not_called()

    @patch('src.core.base_model.log')
    def test_check_variables_passes_perfectly_with_completely_empty_inputs(self, mock_log):
        """Verify check_variables logs informational alerts for optional parameters but executes without errors since nothing is mandatory."""
        model = ExpenseModel(input_variables={})

        # Because everything is optional, this must run cleanly without error
        model.check_variables()
        mock_log.error.assert_not_called()
        mock_log.info.assert_called()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_annual_expenses_with_full_parameters(self):
        """Verify standard 12-month annual cost scaling works perfectly when explicitly provided."""
        inputs = {
            variable_names.MONTHS: 12,
            variable_names.EXPENSE_MONTHLY_RENT: 2000.0,
            variable_names.EXPENSE_RENDER_FEE: 500.0,
            variable_names.EXPENSE_TRAVEL_FEE: 300.0
        }
        model = ExpenseModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: (2000 + 500 + 300) * 12 = 2800 * 12 = 33600.0
        self.assertEqual(enriched_output[variable_names.EXPENSE], 33600.0)

        # Ensure the in-place reference match holds true
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_uses_implicit_twelve_month_default_when_months_is_omitted(self):
        """Verify that omitting the MONTHS variable defaults implicitly to a 12-month scaling horizon."""
        inputs = {
            variable_names.EXPENSE_MONTHLY_RENT: 2000.0,
            variable_names.EXPENSE_RENDER_FEE: 500.0,
            variable_names.EXPENSE_TRAVEL_FEE: 300.0
        }
        model = ExpenseModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: (2000 + 500 + 300) * 12 [default] = 2800 * 12 = 33600.0
        self.assertEqual(enriched_output[variable_names.EXPENSE], 33600.0)

    def test_evaluate_quarterly_expenses_with_partial_inputs(self):
        """Verify that scaling adapts dynamically to a 3-month quarterly shift with omitted fields."""
        inputs = {
            variable_names.MONTHS: 3,
            variable_names.EXPENSE_MONTHLY_RENT: 1500.0
            # Render and Travel are omitted intentionally to act as zero-fallbacks
        }
        model = ExpenseModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: (1500 + 0 + 0) * 3 = 4500.0
        self.assertEqual(enriched_output[variable_names.EXPENSE], 4500.0)

    def test_evaluate_fallback_when_all_expenses_are_zeroed(self):
        """Verify model evaluates cleanly to zero if no operational costs are recorded."""
        inputs = {
            variable_names.MONTHS: 6
        }
        model = ExpenseModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: (0 + 0 + 0) * 6 = 0.0
        self.assertEqual(enriched_output[variable_names.EXPENSE], 0.0)


if __name__ == "__main__":
    unittest.main()
