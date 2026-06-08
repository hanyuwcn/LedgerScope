import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import TotalExpenseModel


class TestTotalExpenseModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = TotalExpenseModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.EXPENSE])

        # Verify explicit required variable signature bounds
        self.assertEqual(
            model.required_variables,
            [variable_names.MONTHLY_EXPENSE]
        )

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables matches the dictionary mapping format."""
        model = TotalExpenseModel()
        self.assertIsInstance(model._optional_variables, dict)
        self.assertEqual(
            model._optional_variables,
            {
                variable_names.MONTHS: 12
            }
        )

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = TotalExpenseModel()
        fresh_inputs = {
            variable_names.MONTHLY_EXPENSE: 3500.0,
            variable_names.MONTHS: 6
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    def test_check_variables_missing_required_logs_error_and_raises(self):
        """Verify check_variables logs errors and safely raises a KeyError if MonthlyExpense is absent."""
        incomplete_inputs = {
            variable_names.MONTHS: 12
            # Missing required variable_names.MONTHLY_EXPENSE!
        }
        model = TotalExpenseModel(incomplete_inputs)

        with patch('src.core.base_model.log') as mock_log:
            with self.assertRaises(KeyError):
                model.check_variables()
            mock_log.error.assert_called_once()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify timeline horizon scaling runs cleanly when duration parameter is explicit."""
        inputs = {
            variable_names.MONTHLY_EXPENSE: 4000.0,
            variable_names.MONTHS: 3
        }
        model = TotalExpenseModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: 4000.0 * 3 = 12000.0 Total Expense
        self.assertEqual(enriched_output[variable_names.EXPENSE], 12000.0)
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_success_with_omitted_months_fallback(self):
        """Verify timeline horizon scaling falls back to default 12-month window when omitted."""
        inputs = {
            variable_names.MONTHLY_EXPENSE: 2500.0
            # Months omitted intentionally (defaults to 12)
        }
        model = TotalExpenseModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: 2500.0 * 12 = 30000.0 Total Expense
        self.assertEqual(enriched_output[variable_names.EXPENSE], 30000.0)

    def test_evaluate_missing_required_variables_raises_key_error(self):
        """Verify omitting the operational foundation base MonthlyExpense immediately aborts execution."""
        incomplete_inputs = {
            variable_names.MONTHS: 6
            # Missing MONTHLY_EXPENSE!
        }
        model = TotalExpenseModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
