import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import RoiModel


class TestRoiModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = RoiModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.ROI])

        # Verify explicit required variable signature bounds
        expected_requirements = [
            variable_names.NET_INCOME,
            variable_names.SETUP_INVESTMENT
        ]
        self.assertEqual(sorted(model.required_variables), sorted(expected_requirements))

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = RoiModel()
        fresh_inputs = {
            variable_names.NET_INCOME: 5000.0,
            variable_names.SETUP_INVESTMENT: 10000.0
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_via_duck_typing(self):
        """Verify individual variable injection works via structural duck-typed objects."""
        model = RoiModel()

        class DuckVariable:
            def __init__(self, name, val):
                self.name = name
                self.expected_value = val

        # Update Setup Investment via duck-typed structural variable
        model.update_input_variable(DuckVariable(variable_names.SETUP_INVESTMENT, 15000.0))
        self.assertEqual(model.input_variables[variable_names.SETUP_INVESTMENT], 15000.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    def test_check_variables_success_with_all_metrics(self):
        """Verify check_variables clears execution cleanly when every metric constraint is met."""
        inputs = {
            variable_names.NET_INCOME: 3000.0,
            variable_names.SETUP_INVESTMENT: 6000.0
        }
        model = RoiModel(inputs)

        with patch('src.core.base_model.log') as mock_log:
            model.check_variables()
            mock_log.error.assert_not_called()

    def test_check_variables_missing_required_raises_key_error(self):
        """Verify check_variables logs errors and raises KeyError if a core driver is absent."""
        incomplete_inputs = {
            variable_names.NET_INCOME: 4000.0
            # Missing SETUP_INVESTMENT!
        }
        model = RoiModel(incomplete_inputs)

        with patch('src.core.base_model.log') as mock_log:
            with self.assertRaises(KeyError):
                model.check_variables()
            mock_log.error.assert_called_once()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & DIVISION DEFENSE PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify ROI calculation runs cleanly under standard parameter bounds."""
        inputs = {
            variable_names.NET_INCOME: 2500.0,
            variable_names.SETUP_INVESTMENT: 10000.0
        }
        model = RoiModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: 2500 / 10000 = 0.25 (25% return)
        self.assertEqual(enriched_output[variable_names.ROI], 0.25)

    def test_evaluate_zero_setup_investment_handles_division_by_zero_safely(self):
        """Verify the engine falls back to 0.0 ROI when setup investment is zero."""
        inputs = {
            variable_names.NET_INCOME: 5000.0,
            variable_names.SETUP_INVESTMENT: 0.0
        }
        model = RoiModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[variable_names.ROI], 0.0)


if __name__ == "__main__":
    unittest.main()
