import unittest

from src.config import variable_names
from src.models import AdvertisingEfficiencyModel, CostOfGoodsSoldModel, TotalCostModel
from src.utils.validation import (
    get_missing_elements,
    check_variables_for_function,
    check_model_pipeline_topology_order
)

# Mocking your config error message setup locally for explicit string assertions
ERROR_VARIABLE_NOT_SETUP_WITH_MESSAGE = "Variable(s) not setup: {msg}"


class TestValidationUtils(unittest.TestCase):

    def setUp(self):
        """
        Set up raw payload states and real production model instances 
        to verify utility calculations and pipeline structural compliance.
        """
        # Baseline dictionary context for basic element checking
        self.mock_provided = {
            variable_names.DEAL_ORDERS: 100,
            variable_names.DEAL_SELLING_PRICE: 4500,
            variable_names.EXPENSE_MONTHLY_RENT: 2000
        }

        # Real model instances for pipeline structural verification
        self.advertising_model = AdvertisingEfficiencyModel()
        self.cogs_model = CostOfGoodsSoldModel()
        self.total_cost_model = TotalCostModel()

    # =====================================================================
    # GET MISSING ELEMENTS TESTS
    # =====================================================================

    def test_get_missing_elements_handles_empty_requirements(self):
        """Verify that passing an empty list of requirements safely returns an empty list."""
        self.assertEqual(get_missing_elements(self.mock_provided, []), [])

    def test_get_missing_elements_isolates_and_sorts_omitted_keys(self):
        """Verify element set subtractions correctly isolate and sort missing dictionary keys."""
        required = [
            variable_names.DEAL_ORDERS,
            variable_names.DEAL_PURCHASING_PRICE,
            variable_names.FINANCE_TAX_RATE
        ]
        missing = get_missing_elements(self.mock_provided, required)

        # Output must be isolated and strictly sorted alphabetically
        expected = sorted([variable_names.DEAL_PURCHASING_PRICE, variable_names.FINANCE_TAX_RATE])
        self.assertEqual(missing, expected)

    # =====================================================================
    # CHECK VARIABLES FOR FUNCTION TESTS
    # =====================================================================

    def test_check_variables_success_path_returns_true(self):
        """Verify validation passes and returns True if all required context items are fully provided."""
        required = [variable_names.DEAL_ORDERS, variable_names.EXPENSE_MONTHLY_RENT]

        result = check_variables_for_function(self.mock_provided, required_variables=required)
        self.assertTrue(result, "check_variables_for_function should return True on a successful validation pass.")

    def test_check_variables_missing_keys_raises_formatted_key_error(self):
        """
        Verify missing variables raise a KeyError containing the beautifully formatted,
        comma-separated list of sorted missing elements.
        """
        required = [
            variable_names.DEAL_ORDERS,
            "MISSING_BETA_KEY",
            "MISSING_ALPHA_KEY"
        ]

        # Expected dynamic message snippet: 'MISSING_ALPHA_KEY, MISSING_BETA_KEY' (alphabetically sorted)
        expected_msg = ERROR_VARIABLE_NOT_SETUP_WITH_MESSAGE.format(
            msg="MISSING_ALPHA_KEY, MISSING_BETA_KEY"
        )

        with self.assertRaises(KeyError) as context:
            check_variables_for_function(self.mock_provided, required_variables=required)

        # KeyErrors store their string representation slightly unique, let's look at the argument
        self.assertEqual(context.exception.args[0], expected_msg)

    def test_check_variables_handles_none_inputs_safely_and_returns_true(self):
        """Verify default initialization mapping prevents crashes and returns True when required_variables is None."""
        result = check_variables_for_function(self.mock_provided, required_variables=None)
        self.assertTrue(result, "check_variables_for_function should return True when required_variables is None.")

    # =====================================================================
    # CHECK MODEL PIPELINE TOPOLOGY ORDER TESTS (UPFRONT PIPELINE GUARDRAIL)
    # =====================================================================

    def test_check_model_pipeline_topology_order_passes_perfect_linear_cascade(self):
        """Verify that a perfectly ordered data-cascading pipeline passes validation cleanly."""
        valid_pipeline = [
            self.advertising_model,
            self.cogs_model,
            self.total_cost_model
        ]
        self.assertTrue(check_model_pipeline_topology_order(valid_pipeline))

    def test_check_model_pipeline_topology_order_catches_complete_reverse_inversion(self):
        """Verify that a backwards pipeline throws a descriptive KeyError instantly."""
        reversed_pipeline = [
            self.total_cost_model,
            self.cogs_model,
            self.advertising_model
        ]

        expected_error_msg = (
            f"Pipeline Order Violation: '{variable_names.COST_COGS}' is generated as an output by 'CostOfGoodsSoldModel', "
            f"but it was already consumed as a required input upstream by 'TotalCostModel'."
        )

        with self.assertRaises(KeyError) as context:
            check_model_pipeline_topology_order(reversed_pipeline)

        self.assertIn(expected_error_msg, str(context.exception))

    def test_check_model_pipeline_topology_order_catches_partial_misplacement(self):
        """Verify that even a small structural step inversion triggers an engineering alert."""
        misplaced_pipeline = [
            self.cogs_model,
            self.advertising_model,
            self.total_cost_model
        ]

        expected_error_msg = (
            f"Pipeline Order Violation: '{variable_names.DEAL_ORDERS}' is generated as an output by 'AdvertisingEfficiencyModel', "
            f"but it was already consumed as a required input upstream by 'CostOfGoodsSoldModel'."
        )

        with self.assertRaises(KeyError) as context:
            check_model_pipeline_topology_order(misplaced_pipeline)

        self.assertIn(expected_error_msg, str(context.exception))


if __name__ == "__main__":
    unittest.main()
