import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import MonthlyExpenseModel


class TestMonthlyExpenseModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = MonthlyExpenseModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.MONTHLY_EXPENSE])

        # Verify explicit required variable signature bounds (none required)
        self.assertEqual(model.required_variables, [])

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables matches the dictionary mapping format."""
        model = MonthlyExpenseModel()
        self.assertIsInstance(model._optional_variables, dict)
        self.assertEqual(
            model._optional_variables,
            {
                variable_names.RENT_EXPENSE: 0.0,
                variable_names.RENDER_EXPENSE: 0.0,
                variable_names.TRAVEL_EXPENSE: 0.0
            }
        )

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = MonthlyExpenseModel()
        fresh_inputs = {
            variable_names.RENT_EXPENSE: 2500.0,
            variable_names.RENDER_EXPENSE: 400.0,
            variable_names.TRAVEL_EXPENSE: 150.0
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.RENT_EXPENSE: 2000.0}
        model = MonthlyExpenseModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = MonthlyExpenseModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable(variable_names.RENT_EXPENSE, 3200.0)
        self.assertEqual(model.input_variables[variable_names.RENT_EXPENSE], 3200.0)

        # Context B: Structural duck-typed object validation Type A (.name, .expected_value)
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.TRAVEL_EXPENSE
                self.expected_value = 600.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.TRAVEL_EXPENSE], 600.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    def test_check_variables_success_with_all_metrics(self):
        """Verify check_variables clears execution cleanly when metrics are provided."""
        inputs = {
            variable_names.RENT_EXPENSE: 1500.0,
            variable_names.RENDER_EXPENSE: 200.0,
            variable_names.TRAVEL_EXPENSE: 300.0
        }
        model = MonthlyExpenseModel(inputs)

        with patch('src.core.base_model.log') as mock_log:
            model.check_variables()
            mock_log.error.assert_not_called()
            mock_log.info.assert_not_called()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify monthly aggregation runs cleanly when parameters are explicit."""
        inputs = {
            variable_names.RENT_EXPENSE: 3000.0,
            variable_names.RENDER_EXPENSE: 500.0,
            variable_names.TRAVEL_EXPENSE: 250.0
        }
        model = MonthlyExpenseModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: 3000.0 + 500.0 + 250.0 = 3750.0
        self.assertEqual(enriched_output[variable_names.MONTHLY_EXPENSE], 3750.0)
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_success_with_omitted_values_fallback(self):
        """Verify monthly run-rate falls back to zero when optional fields are omitted."""
        inputs = {
            variable_names.RENT_EXPENSE: 2000.0
            # Render and Travel omitted intentionally (defaults to 0.0)
        }
        model = MonthlyExpenseModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: 2000.0 + 0.0 + 0.0 = 2000.0
        self.assertEqual(enriched_output[variable_names.MONTHLY_EXPENSE], 2000.0)


if __name__ == "__main__":
    unittest.main()
