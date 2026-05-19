import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import NetIncomeModel


class TestNetIncomeModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = NetIncomeModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.NET_INCOME])

        # Verify explicit required and optional variable signature bounds
        self.assertEqual(
            model.required_variables,
            [
                variable_names.REVENUE,
                variable_names.COST,
                variable_names.EXPENSE,
                variable_names.DEPRECIATION
            ]
        )
        self.assertEqual(
            model.optional_variables,
            [variable_names.FINANCE_TAX_RATE]
        )

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = NetIncomeModel()
        fresh_inputs = {
            variable_names.REVENUE: 50000.0,
            variable_names.COST: 20000.0,
            variable_names.EXPENSE: 5000.0,
            variable_names.DEPRECIATION: 1000.0
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.REVENUE: 40000.0}
        model = NetIncomeModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = NetIncomeModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable(variable_names.REVENUE, 75000.0)
        self.assertEqual(model.input_variables[variable_names.REVENUE], 75000.0)

        # Context B: Structural duck-typed object validation Type A (.name, .expected_value)
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.COST
                self.expected_value = 15000.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.COST], 15000.0)

        # Context C: Structural duck-typed object validation Type B (.get_name(), .get_value())
        class DuckTypeB:
            def get_name(self):
                return variable_names.EXPENSE

            def get_value(self):
                return 4500.0

        model.update_input_variable(DuckTypeB())
        self.assertEqual(model.input_variables[variable_names.EXPENSE], 4500.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_success_with_all_metrics(self, mock_log):
        """Verify check_variables clears execution cleanly when every metric constraint is fully met."""
        inputs = {
            variable_names.REVENUE: 40000.0,
            variable_names.COST: 15000.0,
            variable_names.EXPENSE: 5000.0,
            variable_names.DEPRECIATION: 1000.0,
            variable_names.FINANCE_TAX_RATE: 0.20
        }
        model = NetIncomeModel(inputs)

        # Should execute cleanly without throwing errors or recording telemetry failures
        model.check_variables()
        mock_log.error.assert_not_called()
        mock_log.info.assert_not_called()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_required_logs_error_and_raises(self, mock_log):
        """Verify check_variables logs errors and safely raises a KeyError if a requirement is absent."""
        incomplete_inputs = {
            variable_names.REVENUE: 40000.0,
            variable_names.COST: 15000.0
            # Missing required EXPENSE and DEPRECIATION!
        }
        model = NetIncomeModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

        # Confirm structural failure logs successfully generated
        mock_log.error.assert_called_once()

    @patch('src.core.base_model.log')
    def test_check_variables_missing_optional_logs_informational_alert(self, mock_log):
        """Verify check_variables logs an informational trace but passes when optional metrics are absent."""
        valid_inputs_no_optional = {
            variable_names.REVENUE: 40000.0,
            variable_names.COST: 15000.0,
            variable_names.EXPENSE: 5000.0,
            variable_names.DEPRECIATION: 1000.0
            # Missing optional variable_names.FINANCE_TAX_RATE!
        }
        model = NetIncomeModel(valid_inputs_no_optional)

        # Should log info but verify cleanly without process halt
        model.check_variables()
        mock_log.error.assert_not_called()
        mock_log.info.assert_called_once()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_net_income_pre_tax_defaults(self):
        """Verify calculation works cleanly when tax rate is completely omitted."""
        inputs = {
            variable_names.REVENUE: 40000.0,
            variable_names.COST: 15000.0,
            variable_names.EXPENSE: 5000.0,
            variable_names.DEPRECIATION: 1000.0
            # FINANCE_TAX_RATE is intentionally omitted to test 0.0 fallback
        }
        model = NetIncomeModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: (40000 - 15000 - 5000 - 1000) * (1 - 0.0) = 19000.0
        self.assertEqual(enriched_output[variable_names.NET_INCOME], 19000.0)

        # Ensure the in-place reference match holds true
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_net_income_with_active_taxation(self):
        """Verify after-tax corporate profit deduction structures compute accurately."""
        inputs = {
            variable_names.REVENUE: 100000.0,
            variable_names.COST: 40000.0,
            variable_names.EXPENSE: 10000.0,
            variable_names.DEPRECIATION: 5000.0,
            variable_names.FINANCE_TAX_RATE: 0.25  # 25% Tax Rate
        }
        model = NetIncomeModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: (100000 - 40000 - 10000 - 5000) = 45000.0 pre-tax
        # 45000.0 * (1 - 0.25) = 33750.0 after-tax
        self.assertEqual(enriched_output[variable_names.NET_INCOME], 33750.0)

    def test_evaluate_net_loss_scenario(self):
        """Verify math behaves appropriately when operational costs create a net fiscal loss."""
        inputs = {
            variable_names.REVENUE: 10000.0,
            variable_names.COST: 12000.0,
            variable_names.EXPENSE: 3000.0,
            variable_names.DEPRECIATION: 500.0,
            variable_names.FINANCE_TAX_RATE: 0.20
        }
        model = NetIncomeModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: (10000 - 12000 - 3000 - 500) = -5500.0 pre-tax
        # -5500.0 * (1 - 0.20) = -4400.0 net loss
        self.assertEqual(enriched_output[variable_names.NET_INCOME], -4400.0)

    def test_missing_required_parameters_raises_key_error(self):
        """Verify that dropping a critical parameter like Depreciation halts processing execution."""
        incomplete_inputs = {
            variable_names.REVENUE: 50000.0,
            variable_names.COST: 20000.0,
            variable_names.EXPENSE: 5000.0
            # Missing DEPRECIATION!
        }
        model = NetIncomeModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
