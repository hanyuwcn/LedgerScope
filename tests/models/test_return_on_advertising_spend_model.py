import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import ReturnOnAdvertisingSpendModel


class TestReturnOnAdvertisingSpendModelComprehensive(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_metadata_and_getters_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = ReturnOnAdvertisingSpendModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.ROAS])

        # Verify explicit required variable signature bounds for isolating ROAS
        self.assertEqual(
            model.required_variables,
            [
                variable_names.REVENUE,
                variable_names.COST_ADVERTISING
            ]
        )

        # Verify no optional parameters are registered for this model block
        self.assertEqual(model.optional_variables, [])

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_and_getter_happy_path(self):
        """Verify the property setter completely overwrites and binds the active state."""
        model = ReturnOnAdvertisingSpendModel()
        fresh_inputs = {
            variable_names.REVENUE: 12000.0,
            variable_names.COST_ADVERTISING: 3000.0
        }

        # Fire property setter
        model.input_variables = fresh_inputs

        # Verify getter returns the exact structural dictionary reference
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify that passing None to the property setter securely defaults to an empty dictionary."""
        initial_inputs = {variable_names.REVENUE: 5000.0}
        model = ReturnOnAdvertisingSpendModel(initial_inputs)

        # Overwrite context explicitly with None via property assign
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_update_input_variable_with_raw_string_key(self):
        """Verify individual metric updates when providing raw string identities and values."""
        model = ReturnOnAdvertisingSpendModel()
        model.update_input_variable(variable_names.REVENUE, 15000.0)
        self.assertEqual(model.input_variables[variable_names.REVENUE], 15000.0)

    def test_update_input_variable_with_duck_typed_properties(self):
        """Verify individual metric updates using domain variable Type A objects (.name, .expected_value)."""
        model = ReturnOnAdvertisingSpendModel()

        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.COST_ADVERTISING
                self.expected_value = 2500.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.COST_ADVERTISING], 2500.0)

    def test_update_input_variable_with_duck_typed_getters(self):
        """Verify individual metric updates using domain variable Type B objects (.get_name(), .get_value())."""
        model = ReturnOnAdvertisingSpendModel()

        class DuckTypeB:
            def get_name(self):
                return variable_names.REVENUE

            def get_value(self):
                return 9000.0

        model.update_input_variable(DuckTypeB())
        self.assertEqual(model.input_variables[variable_names.REVENUE], 9000.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_success_with_all_metrics(self, mock_log):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.REVENUE: 10000.0,
            variable_names.COST_ADVERTISING: 2000.0
        }
        model = ReturnOnAdvertisingSpendModel(inputs)

        # Should clear without raising exceptions or logging errors
        model.check_variables()
        mock_log.error.assert_not_called()
        mock_log.info.assert_not_called()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_required_logs_error_and_raises(self, mock_log):
        """Verify check_variables triggers error logs and raises a KeyError if a requirement is absent."""
        incomplete_inputs = {
            variable_names.REVENUE: 10000.0
            # Missing variable_names.COST_ADVERTISING!
        }
        model = ReturnOnAdvertisingSpendModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

        # Assert the internal framework captured the structural omission via error logger
        mock_log.error.assert_called_once()

    # -----------------------------------------------------------------
    # 5. RUNTIME MATHEMATICAL EVALUATIONS
    # -----------------------------------------------------------------

    def test_evaluate_success_calculation_correctness(self):
        """Verify formula execution evaluates standard metrics correctly with reasonable business data numbers."""
        # Setup using clear, realistic e-commerce parameters:
        # Spending $2,500 on ads to generate $10,000 in gross revenue (4.0x ROAS)
        inputs = {
            variable_names.REVENUE: 10000.0,
            variable_names.COST_ADVERTISING: 2500.0
        }
        model = ReturnOnAdvertisingSpendModel(inputs)
        enriched_output = model.evaluate()

        # Calculation Check: ROAS = 10000.0 / 2500.0 = 4.0
        self.assertEqual(enriched_output[variable_names.ROAS], 4.0)

        # Verify in-place structural validation rule
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_success_fractional_precision_calculation(self):
        """Verify math formula evaluation retains fractional tracking values precisely under uneven return bounds."""
        # Testing uneven values: $11,250 revenue generated from $3,000 ad spend (3.75x ROAS)
        inputs = {
            variable_names.REVENUE: 11250.0,
            variable_names.COST_ADVERTISING: 3000.0
        }
        model = ReturnOnAdvertisingSpendModel(inputs)
        enriched_output = model.evaluate()

        self.assertAlmostEqual(enriched_output[variable_names.ROAS], 3.75, places=4)


if __name__ == "__main__":
    unittest.main()
