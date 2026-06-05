import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import UnitContributionMarginModel


class TestUnitContributionMarginModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = UnitContributionMarginModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.UNIT_CONTRIBUTION_MARGIN])

        # Verify explicit required variable signature bounds
        expected_requirements = [
            variable_names.PROFIT,
            variable_names.DEAL_ORDERS,
            variable_names.DEAL_ITEMS_PER_ORDER
        ]
        self.assertEqual(sorted(model.required_variables), sorted(expected_requirements))

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = UnitContributionMarginModel()
        fresh_inputs = {
            variable_names.PROFIT: 1000.0,
            variable_names.DEAL_ORDERS: 100,
            variable_names.DEAL_ITEMS_PER_ORDER: 2
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
        model = UnitContributionMarginModel()

        class DuckVariable:
            def __init__(self, name, val):
                self.name = name
                self.expected_value = val

        # Update Profit via object
        model.update_input_variable(DuckVariable(variable_names.PROFIT, 5000.0))
        self.assertEqual(model.input_variables[variable_names.PROFIT], 5000.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    def test_check_variables_success_with_all_metrics(self):
        """Verify check_variables clears execution cleanly when every metric constraint is met."""
        inputs = {
            variable_names.PROFIT: 2500.0,
            variable_names.DEAL_ORDERS: 50,
            variable_names.DEAL_ITEMS_PER_ORDER: 5
        }
        model = UnitContributionMarginModel(inputs)

        with patch('src.core.base_model.log') as mock_log:
            model.check_variables()
            mock_log.error.assert_not_called()

    def test_check_variables_missing_required_raises_key_error(self):
        """Verify check_variables logs errors and raises KeyError if a core driver is absent."""
        incomplete_inputs = {
            variable_names.PROFIT: 1000.0,
            variable_names.DEAL_ORDERS: 10
            # Missing DEAL_ITEMS_PER_ORDER
        }
        model = UnitContributionMarginModel(incomplete_inputs)

        with patch('src.core.base_model.log') as mock_log:
            with self.assertRaises(KeyError):
                model.check_variables()
            mock_log.error.assert_called_once()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & DIVISION DEFENSE PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify UCM calculation runs cleanly under standard parameters."""
        inputs = {
            variable_names.PROFIT: 2000.0,  # Total Profit
            variable_names.DEAL_ORDERS: 100,  # 100 Orders
            variable_names.DEAL_ITEMS_PER_ORDER: 4  # 4 Items each = 400 total units
        }
        model = UnitContributionMarginModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: 2000 / (100 * 4) = 5.0
        self.assertEqual(enriched_output[variable_names.UNIT_CONTRIBUTION_MARGIN], 5.0)

    def test_evaluate_zero_volume_handles_division_by_zero_safely(self):
        """Verify the engine falls back to 0.0 UCM when order volume or items-per-order is zero."""
        inputs = {
            variable_names.PROFIT: 500.0,
            variable_names.DEAL_ORDERS: 0,
            variable_names.DEAL_ITEMS_PER_ORDER: 2
        }
        model = UnitContributionMarginModel(inputs)
        enriched_output = model.evaluate()

        # Should return 0.0 rather than raising ZeroDivisionError
        self.assertEqual(enriched_output[variable_names.UNIT_CONTRIBUTION_MARGIN], 0.0)

    def test_evaluate_missing_required_variables_raises_key_error(self):
        """Verify omitting an operational driver variable triggers an immediate lookup error."""
        incomplete_inputs = {
            variable_names.PROFIT: 500.0
            # Missing orders and items per order!
        }
        model = UnitContributionMarginModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
