import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import OperatingIncomeModel


class TestOperatingIncomeModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = OperatingIncomeModel()

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.OPERATING_INCOME])

        # Verify required variables
        self.assertEqual(
            sorted(model.required_variables),
            sorted([variable_names.REVENUE, variable_names.COGS])
        )

        # Verify optional variable signature bounds
        self.assertEqual(
            sorted(model.optional_variables),
            sorted([variable_names.EXPENSE, variable_names.DEPRECIATION])
        )

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_operating_income_success(self):
        """Verify model computes Operating Income: Revenue - COGS - Expense - Depreciation."""
        inputs = {
            variable_names.REVENUE: 100000.0,
            variable_names.COGS: 40000.0,
            variable_names.EXPENSE: 10000.0,
            variable_names.DEPRECIATION: 5000.0
        }
        model = OperatingIncomeModel(inputs)
        enriched_output = model.evaluate()

        # Math: 100000 - 40000 - 10000 - 5000 = 45000.0
        self.assertEqual(enriched_output[variable_names.OPERATING_INCOME], 45000.0)

    def test_evaluate_lean_bootstrap_defaults(self):
        """Verify model safely computes income under zero-overhead defaults."""
        inputs = {
            variable_names.REVENUE: 30000.0,
            variable_names.COGS: 10000.0
        }
        model = OperatingIncomeModel(inputs)
        enriched_output = model.evaluate()

        # Math: 30000 - 10000 - 0 - 0 = 20000.0
        self.assertEqual(enriched_output[variable_names.OPERATING_INCOME], 20000.0)

    def test_missing_required_parameters_raises_key_error(self):
        """Verify that dropping a critical mandatory parameter like COGS halts execution."""
        incomplete_inputs = {
            variable_names.REVENUE: 50000.0,
            variable_names.EXPENSE: 5000.0
        }
        model = OperatingIncomeModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()

    # -----------------------------------------------------------------
    # 3. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_missing_required_logs_error_and_raises(self, mock_log):
        """Verify check_variables logs errors and safely raises a KeyError."""
        incomplete_inputs = {variable_names.REVENUE: 40000.0}
        model = OperatingIncomeModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

        mock_log.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
