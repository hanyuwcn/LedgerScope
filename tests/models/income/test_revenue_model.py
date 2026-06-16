import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import RevenueModel


class TestRevenueModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = RevenueModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.REVENUE])

        # Verify explicit required variable signature bounds
        self.assertEqual(
            model.required_variables,
            [
                variable_names.UNIT_FOB_PRICE_IN_RMB,
                variable_names.UNITS_SOLD
            ]
        )

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables matches the dictionary mapping format."""
        model = RevenueModel()
        self.assertIsInstance(model._optional_variables, dict)
        self.assertEqual(
            model._optional_variables,
            {}
        )

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = RevenueModel()
        fresh_inputs = {
            variable_names.UNIT_FOB_PRICE_IN_RMB: 350.0,
            variable_names.UNITS_SOLD: 300
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.UNITS_SOLD: 150}
        model = RevenueModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = RevenueModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable(variable_names.UNITS_SOLD, 300)
        self.assertEqual(model.input_variables[variable_names.UNITS_SOLD], 300)

        # Context B: Structural duck-typed object validation
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.UNIT_FOB_PRICE_IN_RMB
                self.expected_value = 75.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.UNIT_FOB_PRICE_IN_RMB], 75.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_success_with_all_metrics(self, mock_log):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.UNIT_FOB_PRICE_IN_RMB: 350.0,
            variable_names.UNITS_SOLD: 300,
        }
        model = RevenueModel(inputs)

        model.check_variables()
        mock_log.error.assert_not_called()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_required_logs_error_and_raises(self, mock_log):
        """Verify check_variables logs errors and safely raises a KeyError if a requirement is absent."""
        incomplete_inputs = {
            variable_names.UNITS_SOLD: 300
            # Missing UNIT_FOB_PRICE_IN_RMB!
        }
        model = RevenueModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()
        mock_log.error.assert_called_once()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_revenue_in_domestic_currency(self):
        """Verify baseline revenue calculations hold accurate when currency translations are omitted."""
        inputs = {
            variable_names.UNIT_FOB_PRICE_IN_RMB: 350.0,
            variable_names.UNITS_SOLD: 300
        }
        model = RevenueModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 350.0 * 300 = 15000.0
        self.assertEqual(enriched_output[variable_names.REVENUE], 105000.0)
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_revenue_with_currency_translation_factor(self):
        """Verify international revenue scales reliably when an exchange rate multiplier is passed."""
        inputs = {
            variable_names.UNIT_FOB_PRICE_IN_RMB: 700.0,
            variable_names.UNITS_SOLD: 20,
        }
        model = RevenueModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 700.0 * 20 = 14000.0
        self.assertEqual(enriched_output[variable_names.REVENUE], 14000.0)


if __name__ == "__main__":
    unittest.main()
