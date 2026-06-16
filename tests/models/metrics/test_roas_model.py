import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import RoasModel


class TestRoasModelComprehensive(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_metadata_and_getters_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = RoasModel()

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
                variable_names.ADVERTISING_EXPENSE
            ]
        )

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_and_getter_happy_path(self):
        """Verify the property setter completely overwrites and binds the active state."""
        model = RoasModel()
        fresh_inputs = {
            variable_names.REVENUE: 12000.0,
            variable_names.ADVERTISING_EXPENSE: 3000.0
        }

        # Fire property setter
        model.input_variables = fresh_inputs

        # Verify getter returns the exact structural dictionary reference
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_update_input_variable_with_raw_string_key(self):
        """Verify individual metric updates when providing raw string identities and values."""
        model = RoasModel()
        model.update_input_variable(variable_names.REVENUE, 15000.0)
        self.assertEqual(model.input_variables[variable_names.REVENUE], 15000.0)

    def test_update_input_variable_with_duck_typed_properties(self):
        """Verify individual metric updates using domain variable Type A objects."""
        model = RoasModel()

        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.ADVERTISING_EXPENSE
                self.expected_value = 2500.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.ADVERTISING_EXPENSE], 2500.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_missing_required_logs_error_and_raises(self, mock_log):
        """Verify check_variables triggers error logs and raises a KeyError if a requirement is absent."""
        incomplete_inputs = {
            variable_names.REVENUE: 10000.0
            # Missing variable_names.ADVERTISING_EXPENSE!
        }
        model = RoasModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

        mock_log.error.assert_called_once()

    # -----------------------------------------------------------------
    # 5. RUNTIME MATHEMATICAL EVALUATIONS & PROTECTION
    # -----------------------------------------------------------------

    def test_evaluate_success_calculation_correctness(self):
        """Verify formula execution evaluates standard metrics correctly."""
        inputs = {
            variable_names.REVENUE: 10000.0,
            variable_names.ADVERTISING_EXPENSE: 2500.0
        }
        model = RoasModel(inputs)
        enriched_output = model.evaluate()
        self.assertEqual(enriched_output[variable_names.ROAS], 4.0)

    def test_evaluate_zero_advertising_expense_protection(self):
        """Verify that zero advertising expense returns 0.0 instead of raising a division error."""
        inputs = {
            variable_names.REVENUE: 10000.0,
            variable_names.ADVERTISING_EXPENSE: 0.0
        }
        model = RoasModel(inputs)

        # Verify defensive return value
        enriched_output = model.evaluate()
        self.assertEqual(enriched_output[variable_names.ROAS], 0.0)


if __name__ == "__main__":
    unittest.main()
