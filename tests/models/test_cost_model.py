import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import TotalCostModel


class TestTotalCostModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = TotalCostModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.COST])

        # Verify explicit required variable signature bounds
        self.assertEqual(
            model.required_variables,
            [variable_names.COST_COGS]
        )

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables matches the dictionary mapping format."""
        model = TotalCostModel()
        self.assertIsInstance(model._optional_variables, dict)
        self.assertEqual(
            model._optional_variables,
            {
                variable_names.COST_ADVERTISING: 0.0,
                variable_names.COST_SHIPPING: 0.0,
                variable_names.COST_SETUP: 0.0  # ADDED
            }
        )

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = TotalCostModel()
        fresh_inputs = {
            variable_names.COST_COGS: 3000.0,
            variable_names.COST_SETUP: 10000.0,  # ADDED
            variable_names.COST_ADVERTISING: 1200.0,
            variable_names.COST_SHIPPING: 150.0
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.COST_COGS: 4000.0}
        model = TotalCostModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = TotalCostModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable(variable_names.COST_COGS, 8500.0)
        self.assertEqual(model.input_variables[variable_names.COST_COGS], 8500.0)

        # Context B: Structural duck-typed object validation Type A (.name, .expected_value)
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.COST_SHIPPING
                self.expected_value = 250.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.COST_SHIPPING], 250.0)

        # Context C: Structural duck-typed object validation Type B (.get_name(), .get_value())
        class DuckTypeB:
            def get_name(self):
                return variable_names.COST_ADVERTISING

            def get_value(self):
                return 2500.0

        model.update_input_variable(DuckTypeB())
        self.assertEqual(model.input_variables[variable_names.COST_ADVERTISING], 2500.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    def test_check_variables_success_with_all_metrics(self):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.COST_COGS: 4000.0,
            variable_names.COST_SETUP: 10000.0,  # ADDED
            variable_names.COST_ADVERTISING: 1500.0,
            variable_names.COST_SHIPPING: 200.0
        }
        model = TotalCostModel(inputs)

        # Should execute cleanly without throwing errors or recording telemetry failures
        with patch('src.core.base_model.log') as mock_log:
            model.check_variables()
            mock_log.error.assert_not_called()
            mock_log.info.assert_not_called()

    def test_check_variables_missing_required_logs_error_and_raises(self):
        """Verify check_variables logs errors and safely raises a KeyError if a requirement is absent."""
        incomplete_inputs = {
            variable_names.COST_ADVERTISING: 1500.0
            # Missing required variable_names.COST_COGS!
        }
        model = TotalCostModel(incomplete_inputs)

        with patch('src.core.base_model.log') as mock_log:
            with self.assertRaises(KeyError):
                model.check_variables()
            # Confirm failure routing triggered the process logging system
            mock_log.error.assert_called_once()

    def test_check_variables_missing_optional_logs_informational_alert(self):
        """Verify check_variables logs an informational trace but passes when optional metrics are absent."""
        valid_inputs_no_optional = {
            variable_names.COST_COGS: 5000.0,
            variable_names.COST_SETUP: 10000.0,
            variable_names.COST_ADVERTISING: 1500.0
            # Missing optional variable_names.COST_SHIPPING!
        }
        model = TotalCostModel(valid_inputs_no_optional)

        # Should log info but verify cleanly without process halt
        with patch('src.core.base_model.log') as mock_log:
            model.check_variables()
            mock_log.error.assert_not_called()
            mock_log.info.assert_called_once()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify cost aggregation runs cleanly when optional parameters are explicit."""
        inputs = {
            variable_names.COST_COGS: 4500.0,
            variable_names.COST_SETUP: 10000.0,  # ADDED
            variable_names.COST_ADVERTISING: 2000.0,
            variable_names.COST_SHIPPING: 350.0
        }
        model = TotalCostModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: 10000 + 4500 + 2000 + 350 = 16850.0
        self.assertEqual(enriched_output[variable_names.COST], 16850.0)

        # Verify context integrity remains uncorrupted
        self.assertEqual(enriched_output[variable_names.COST_COGS], 4500.0)

        # Ensure the in-place reference match holds true
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_success_with_omitted_shipping_and_setup_fallback(self):
        """Verify cost aggregation falls back to zero when shipping or setup values are omitted."""
        inputs = {
            variable_names.COST_COGS: 5000.0,
            variable_names.COST_ADVERTISING: 1500.0
            # Shipping and Setup omitted intentionally (defaults to 0.0)
        }
        model = TotalCostModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: 0.0 + 5000 + 1500 + 0.0 = 6500.0
        self.assertEqual(enriched_output[variable_names.COST], 6500.0)

    def test_evaluate_missing_required_variables_raises_key_error(self):
        """Verify omitting an operational pillar like COGS immediately aborts execution."""
        incomplete_inputs = {
            variable_names.COST_ADVERTISING: 1500.0
            # Missing COST_COGS!
        }
        model = TotalCostModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()