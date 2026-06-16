import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import CacModel


class TestCacModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = CacModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.CAC])

        # Verify explicit required variable signature bounds
        self.assertEqual(
            sorted(model.required_variables),
            sorted([variable_names.ADVERTISING_EXPENSE, variable_names.ORDERS])
        )

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables matches the empty dictionary default."""
        model = CacModel()
        self.assertIsInstance(model._optional_variables, dict)
        self.assertEqual(model._optional_variables, {})

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = CacModel()
        fresh_inputs = {
            variable_names.ADVERTISING_EXPENSE: 5000.0,
            variable_names.ORDERS: 250
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.ADVERTISING_EXPENSE: 3000.0}
        model = CacModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = CacModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable(variable_names.ADVERTISING_EXPENSE, 4500.0)
        self.assertEqual(model.input_variables[variable_names.ADVERTISING_EXPENSE], 4500.0)

        # Context B: Structural duck-typed object validation
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.ORDERS
                self.expected_value = 150

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.ORDERS], 150)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    def test_check_variables_success_with_all_metrics(self):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.ADVERTISING_EXPENSE: 2000.0,
            variable_names.ORDERS: 100
        }
        model = CacModel(inputs)

        with patch('src.core.base_model.log') as mock_log:
            model.check_variables()
            mock_log.error.assert_not_called()

    def test_check_variables_missing_required_logs_error_and_raises(self):
        """Verify check_variables logs errors and safely raises a KeyError if an essential anchor is absent."""
        incomplete_inputs = {
            variable_names.ADVERTISING_EXPENSE: 1500.0
            # Missing required variable_names.ORDERS!
        }
        model = CacModel(incomplete_inputs)

        with patch('src.core.base_model.log') as mock_log:
            with self.assertRaises(KeyError):
                model.check_variables()
            mock_log.error.assert_called_once()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & DIVISION DEFENSE PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify acquisition efficiency calculations run cleanly under standard parameters."""
        inputs = {
            variable_names.ADVERTISING_EXPENSE: 3000.0,
            variable_names.ORDERS: 150
        }
        model = CacModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: 3000.0 / 150 = 20.0
        self.assertEqual(enriched_output[variable_names.CAC], 20.0)
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_zero_orders_handles_division_by_zero_safely(self):
        """Verify the calculation engine falls back safely to 0.0 CAC when zero orders are logged."""
        inputs = {
            variable_names.ADVERTISING_EXPENSE: 1500.0,
            variable_names.ORDERS: 0
        }
        model = CacModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[variable_names.CAC], 0.0)

    def test_evaluate_missing_required_variables_raises_key_error(self):
        """Verify that omitting an operational driver variable triggers an immediate lookup error."""
        incomplete_inputs = {variable_names.ORDERS: 50}
        model = CacModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
