import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import CostOfGoodsSoldModel


class TestCostOfGoodsSoldModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = CostOfGoodsSoldModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.COST_COGS])

        # Verify explicit required and optional variable signature bounds
        self.assertEqual(
            model.required_variables,
            [
                variable_names.DEAL_PURCHASING_PRICE,
                variable_names.DEAL_ORDERS,
                variable_names.DEAL_ITEMS_PER_ORDER
            ]
        )
        self.assertEqual(model.optional_variables, [])

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = CostOfGoodsSoldModel()
        fresh_inputs = {
            variable_names.DEAL_PURCHASING_PRICE: 10.0,
            variable_names.DEAL_ORDERS: 50,
            variable_names.DEAL_ITEMS_PER_ORDER: 3
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.DEAL_ORDERS: 200}
        model = CostOfGoodsSoldModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = CostOfGoodsSoldModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable(variable_names.DEAL_ORDERS, 150)
        self.assertEqual(model.input_variables[variable_names.DEAL_ORDERS], 150)

        # Context B: Structural duck-typed object validation Type A (.name, .expected_value)
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.DEAL_PURCHASING_PRICE
                self.expected_value = 12.5

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.DEAL_PURCHASING_PRICE], 12.5)

        # Context C: Structural duck-typed object validation Type B (.get_name(), .get_value())
        class DuckTypeB:
            def get_name(self):
                return variable_names.DEAL_ITEMS_PER_ORDER

            def get_value(self):
                return 4

        model.update_input_variable(DuckTypeB())
        self.assertEqual(model.input_variables[variable_names.DEAL_ITEMS_PER_ORDER], 4)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_success_with_all_metrics(self, mock_log):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.DEAL_PURCHASING_PRICE: 15.0,
            variable_names.DEAL_ORDERS: 100,
            variable_names.DEAL_ITEMS_PER_ORDER: 2
        }
        model = CostOfGoodsSoldModel(inputs)

        # Should execute cleanly without throwing errors or recording telemetry failures
        model.check_variables()
        mock_log.error.assert_not_called()
        mock_log.info.assert_not_called()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_required_logs_error_and_raises(self, mock_log):
        """Verify check_variables logs errors and safely raises a KeyError if a requirement is absent."""
        incomplete_inputs = {
            variable_names.DEAL_PURCHASING_PRICE: 15.0,
            variable_names.DEAL_ORDERS: 100
            # Missing required variable_names.DEAL_ITEMS_PER_ORDER!
        }
        model = CostOfGoodsSoldModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

        # Confirm structural failure logs successfully generated
        mock_log.error.assert_called_once()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_optional_logs_informational_alert(self, mock_log):
        """Verify check_variables logs an informational trace but passes when optional metrics are absent.

        Note: If this model has no optional variables, it defaults to checking required parameters
        and testing the happy path validation mechanics under the logging infrastructure.
        """
        inputs = {
            variable_names.DEAL_PURCHASING_PRICE: 15.0,
            variable_names.DEAL_ORDERS: 100,
            variable_names.DEAL_ITEMS_PER_ORDER: 2
        }
        model = CostOfGoodsSoldModel(inputs)
        model.check_variables()
        mock_log.error.assert_not_called()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_valid_parameters(self):
        """Verify COGS calculation executes correctly and blends outputs into the runtime context."""
        inputs = {
            variable_names.DEAL_PURCHASING_PRICE: 15.0,  # $15 per item
            variable_names.DEAL_ORDERS: 100,  # 100 orders
            variable_names.DEAL_ITEMS_PER_ORDER: 2  # 2 items per order
        }
        model = CostOfGoodsSoldModel(inputs)
        enriched_output = model.evaluate()

        # Math check: 15.0 * 100 * 2 = 3000.0
        self.assertEqual(enriched_output[variable_names.COST_COGS], 3000.0)

        # Verify inputs are fully preserved along with the output
        self.assertEqual(enriched_output[variable_names.DEAL_ORDERS], 100)

        # Ensure the in-place reference match holds true
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_missing_required_variables_raises_key_error(self):
        """Verify that omitting raw parameters stops process execution immediately."""
        incomplete_inputs = {
            variable_names.DEAL_PURCHASING_PRICE: 15.0,
            variable_names.DEAL_ORDERS: 100
            # Missing DEAL_ITEMS_PER_ORDER!
        }
        model = CostOfGoodsSoldModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
