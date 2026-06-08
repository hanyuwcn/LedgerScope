import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import OrderModel


class TestOrderModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = OrderModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.ORDERS])

        # Verify explicit required variable signature bounds
        expected_requirements = [
            variable_names.LEADS,
            variable_names.CLOSE_RATE
        ]
        self.assertEqual(sorted(model.required_variables), sorted(expected_requirements))

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables matches the empty dictionary default."""
        model = OrderModel()
        self.assertIsInstance(model._optional_variables, dict)
        self.assertEqual(model._optional_variables, {})

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = OrderModel()
        fresh_inputs = {
            variable_names.LEADS: 500.0,
            variable_names.CLOSE_RATE: 0.15
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.LEADS: 150.0}
        model = OrderModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_via_duck_typing(self):
        """Verify individual variable injection works via structural duck-typed objects."""
        model = OrderModel()

        class DuckVariable:
            def __init__(self, name, val):
                self.name = name
                self.expected_value = val

        # Update Close Rate via duck-typed structural variable
        model.update_input_variable(DuckVariable(variable_names.CLOSE_RATE, 0.08))
        self.assertEqual(model.input_variables[variable_names.CLOSE_RATE], 0.08)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    def test_check_variables_success_with_all_metrics(self):
        """Verify check_variables clears execution cleanly when every metric constraint is met."""
        inputs = {
            variable_names.LEADS: 1200.0,
            variable_names.CLOSE_RATE: 0.05
        }
        model = OrderModel(inputs)

        with patch('src.core.base_model.log') as mock_log:
            model.check_variables()
            mock_log.error.assert_not_called()

    def test_check_variables_missing_required_raises_key_error(self):
        """Verify check_variables logs errors and raises KeyError if a core driver is absent."""
        incomplete_inputs = {
            variable_names.LEADS: 350.0
            # Missing CLOSE_RATE!
        }
        model = OrderModel(incomplete_inputs)

        with patch('src.core.base_model.log') as mock_log:
            with self.assertRaises(KeyError):
                model.check_variables()
            mock_log.error.assert_called_once()

    # -----------------------------------------------------------------
    # 5. RUNTIME MATHEMATICAL EVALUATIONS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify lead-to-order pipeline conversion runs cleanly under standard parameter bounds."""
        inputs = {
            variable_names.LEADS: 250.0,
            variable_names.CLOSE_RATE: 0.12
        }
        model = OrderModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: 250 * 0.12 = 30.0 Orders
        self.assertAlmostEqual(enriched_output[variable_names.ORDERS], 30.0, places=4)
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_handles_zero_leads_or_close_rate_safely(self):
        """Verify the math module evaluates correctly when baseline metrics drop to absolute zero."""
        inputs = {
            variable_names.LEADS: 0.0,
            variable_names.CLOSE_RATE: 0.20
        }
        model = OrderModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: 0 * 0.20 = 0.0 Orders
        self.assertEqual(enriched_output[variable_names.ORDERS], 0.0)

    def test_evaluate_missing_required_variables_raises_key_error(self):
        """Verify omitting an operational driver variable triggers an immediate lookup error."""
        incomplete_inputs = {
            variable_names.CLOSE_RATE: 0.10
            # Missing LEADS!
        }
        model = OrderModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
