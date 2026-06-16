import unittest

from src.config import variable_names
from src.models import RevenueModel, TotalExpenseModel, OperatingIncomeModel
from src.utils.validation import (
    get_missing_elements,
    check_variables_for_function,
    check_model_pipeline_topology_order
)

ERROR_VARIABLE_NOT_SETUP_WITH_MESSAGE = "Variable(s) not setup: {msg}"


class TestValidationUtils(unittest.TestCase):

    def setUp(self):
        """
        Set up raw payload states and real production model instances
        to verify utility calculations and pipeline structural compliance.
        """
        self.mock_provided = {
            variable_names.COGS: 40000.0,
            variable_names.ORDERS: 100,
            variable_names.UNITS_PER_ORDER: 2,
            variable_names.UNIT_FOB_PRICE: 4500,
            variable_names.MONTHLY_MANAGEMENT_EXPENSE: 500.0
        }

        self.revenue_model = RevenueModel()
        self.operating_income_model = OperatingIncomeModel()
        self.expense_model = TotalExpenseModel()

    # =====================================================================
    # EDGE CASES: GET MISSING ELEMENTS
    # =====================================================================

    def test_get_missing_elements_handles_empty_requirements(self):
        """Verify that passing an empty list of requirements safely returns an empty list."""
        self.assertEqual(get_missing_elements(self.mock_provided, []), [])

    def test_get_missing_elements_isolates_and_sorts_omitted_keys(self):
        """Verify element set subtractions correctly isolate and sort missing dictionary keys."""
        required = [variable_names.ORDERS, variable_names.REVENUE, variable_names.TAX_RATE]
        missing = get_missing_elements(self.mock_provided, required)
        # Expected sorted: REVENUE, TAX_RATE
        self.assertEqual(missing, sorted([variable_names.REVENUE, variable_names.TAX_RATE]))

    # =====================================================================
    # EDGE CASES: CHECK VARIABLES FOR FUNCTION
    # =====================================================================

    def test_check_variables_success_path_returns_true(self):
        """Verify validation passes when all required items exist."""
        required = [variable_names.ORDERS, variable_names.UNIT_FOB_PRICE]
        self.assertTrue(check_variables_for_function(self.mock_provided, required_variables=required))

    def test_check_variables_missing_keys_raises_formatted_key_error(self):
        """Verify missing variables raise a correctly formatted, sorted error message."""
        required = ["MISSING_BETA", "MISSING_ALPHA"]
        expected_msg = ERROR_VARIABLE_NOT_SETUP_WITH_MESSAGE.format(msg="MISSING_ALPHA, MISSING_BETA")

        with self.assertRaises(KeyError) as context:
            check_variables_for_function(self.mock_provided, required_variables=required)
        self.assertEqual(context.exception.args[0], expected_msg)

    def test_check_variables_handles_none_inputs_safely(self):
        """Verify function returns True when required_variables is None (graceful exit)."""
        self.assertTrue(check_variables_for_function(self.mock_provided, required_variables=None))

    # =====================================================================
    # EDGE CASES: TOPOLOGY GUARDRAIL
    # =====================================================================

    def test_topology_order_passes_linear_cascade(self):
        """Verify a logically ordered dependency chain (Revenue -> Expense -> NetIncome) passes."""
        valid_pipeline = [self.revenue_model, self.expense_model, self.operating_income_model]
        self.assertTrue(check_model_pipeline_topology_order(valid_pipeline))

    def test_topology_order_catches_dependency_inversion(self):
        """Verify that a pipeline where a consumer precedes its provider raises a KeyError."""
        invalid_pipeline = [self.operating_income_model, self.revenue_model]

        # We must call the function inside the context manager
        with self.assertRaises(KeyError) as context:
            check_model_pipeline_topology_order(invalid_pipeline)

        # Now we assert that the error message contains the violation signature
        self.assertIn("Pipeline Order Violation", str(context.exception))

    def test_topology_order_catches_optional_dependency_violation(self):
        """Verify that placing a model needing an optional input before the model generating it fails."""
        # NetIncome needs EXPENSE (provided by TotalExpenseModel)
        invalid_pipeline = [self.operating_income_model, self.expense_model]
        with self.assertRaises(KeyError) as context:
            check_model_pipeline_topology_order(invalid_pipeline)
        self.assertIn("Pipeline Order Violation", str(context.exception))


if __name__ == "__main__":
    unittest.main()
