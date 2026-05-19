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

        # Verify explicit required and optional variable signature bounds
        self.assertEqual(
            model.required_variables,
            [
                variable_names.DEAL_SELLING_PRICE,
                variable_names.DEAL_ORDERS,
                variable_names.DEAL_ITEMS_PER_ORDER
            ]
        )
        self.assertEqual(
            model.optional_variables,
            [variable_names.FINANCE_USD_TO_RMB]
        )

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = RevenueModel()
        fresh_inputs = {
            variable_names.DEAL_SELLING_PRICE: 50.0,
            variable_names.DEAL_ORDERS: 200,
            variable_names.DEAL_ITEMS_PER_ORDER: 1.5
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.DEAL_ORDERS: 150}
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
        model.update_input_variable(variable_names.DEAL_ORDERS, 300)
        self.assertEqual(model.input_variables[variable_names.DEAL_ORDERS], 300)

        # Context B: Structural duck-typed object validation Type A (.name, .expected_value)
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.DEAL_SELLING_PRICE
                self.expected_value = 75.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.DEAL_SELLING_PRICE], 75.0)

        # Context C: Structural duck-typed object validation Type B (.get_name(), .get_value())
        class DuckTypeB:
            def get_name(self):
                return variable_names.FINANCE_USD_TO_RMB

            def get_value(self):
                return 7.2

        model.update_input_variable(DuckTypeB())
        self.assertEqual(model.input_variables[variable_names.FINANCE_USD_TO_RMB], 7.2)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_success_with_all_metrics(self, mock_log):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.DEAL_SELLING_PRICE: 50.0,
            variable_names.DEAL_ORDERS: 200,
            variable_names.DEAL_ITEMS_PER_ORDER: 1.5,
            variable_names.FINANCE_USD_TO_RMB: 7.0
        }
        model = RevenueModel(inputs)

        # Should execute cleanly without throwing errors or recording telemetry failures
        model.check_variables()
        mock_log.error.assert_not_called()
        mock_log.info.assert_not_called()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_required_logs_error_and_raises(self, mock_log):
        """Verify check_variables logs errors and safely raises a KeyError if a requirement is absent."""
        incomplete_inputs = {
            variable_names.DEAL_ORDERS: 200,
            variable_names.DEAL_ITEMS_PER_ORDER: 1.5
            # Missing required variable_names.DEAL_SELLING_PRICE!
        }
        model = RevenueModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

        # Confirm failure routing triggered the process logging system
        mock_log.error.assert_called_once()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_optional_logs_informational_alert(self, mock_log):
        """Verify check_variables logs an informational trace but passes when optional metrics are absent."""
        valid_inputs_no_optional = {
            variable_names.DEAL_SELLING_PRICE: 50.0,
            variable_names.DEAL_ORDERS: 200,
            variable_names.DEAL_ITEMS_PER_ORDER: 1.5
            # Missing optional variable_names.FINANCE_USD_TO_RMB!
        }
        model = RevenueModel(valid_inputs_no_optional)

        # Should log info but verify cleanly without process halt
        model.check_variables()
        mock_log.error.assert_not_called()
        mock_log.info.assert_called_once()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_revenue_in_domestic_currency(self):
        """Verify baseline revenue calculations hold accurate when currency translations are omitted."""
        inputs = {
            variable_names.DEAL_SELLING_PRICE: 50.0,  # $50 per item
            variable_names.DEAL_ORDERS: 200,  # 200 orders
            variable_names.DEAL_ITEMS_PER_ORDER: 1.5  # 1.5 items average per order
        }
        model = RevenueModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 50.0 * 200 * 1.5 * 1.0 = 15000.0
        self.assertEqual(enriched_output[variable_names.REVENUE], 15000.0)
        self.assertEqual(enriched_output[variable_names.DEAL_SELLING_PRICE], 50.0)

        # Ensure the in-place reference match holds true
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_revenue_with_currency_translation_factor(self):
        """Verify international revenue scales reliably when an exchange rate multiplier is passed."""
        inputs = {
            variable_names.DEAL_SELLING_PRICE: 100.0,
            variable_names.DEAL_ORDERS: 10,
            variable_names.DEAL_ITEMS_PER_ORDER: 2,
            variable_names.FINANCE_USD_TO_RMB: 7.0
        }
        model = RevenueModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 100.0 * 10 * 2 * 7.0 = 2000 * 7.0 = 14000.0
        self.assertEqual(enriched_output[variable_names.REVENUE], 14000.0)

    def test_evaluate_missing_required_variables_throws_exception(self):
        """Verify that omitting a structural pillar like selling price triggers validation errors."""
        incomplete_inputs = {
            variable_names.DEAL_ORDERS: 10,
            variable_names.DEAL_ITEMS_PER_ORDER: 2
            # Missing DEAL_SELLING_PRICE!
        }
        model = RevenueModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
