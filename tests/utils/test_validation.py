import unittest

from src.config import variable_names
from src.utils.validation import get_missing_elements, check_variables_for_function


class TestValidationUtils(unittest.TestCase):

    def setUp(self):
        """
        Set up a slice of an active context runtime dictionary 
        to test dictionary key compliance assertions.
        """
        self.mock_provided = {
            variable_names.DEAL_ORDERS: 100,
            variable_names.DEAL_SELLING_PRICE: 4500,
            variable_names.EXPENSE_MONTHLY_RENT: 2000
        }

    # =====================================================================
    # ELEMENT EXTRACTION TESTS
    # =====================================================================

    def test_get_missing_elements_handles_empty_requirements(self):
        """Verify that passing an empty list or None returns an empty list immediately."""
        self.assertEqual(get_missing_elements(self.mock_provided, []), [])

    def test_get_missing_elements_returns_sorted_omitted_keys(self):
        """Verify element set subtractions correctly isolate and sort missing keys."""
        required = [
            variable_names.DEAL_ORDERS,
            variable_names.DEAL_PURCHASING_PRICE,
            variable_names.FINANCE_TAX_RATE
        ]
        missing = get_missing_elements(self.mock_provided, required)

        # Elements must be isolated and strictly sorted alphabetically
        expected = sorted([variable_names.DEAL_PURCHASING_PRICE, variable_names.FINANCE_TAX_RATE])
        self.assertEqual(missing, expected)

    # =====================================================================
    # DEFENSIVE VARIABLE CHECKER TESTS
    # =====================================================================

    def test_check_variables_success_path(self):
        """Verify validation script passes quietly if all critical constraints are fulfilled."""
        required = [variable_names.DEAL_ORDERS, variable_names.EXPENSE_MONTHLY_RENT]
        optional = [variable_names.DEAL_SELLING_PRICE]

        try:
            check_variables_for_function(self.mock_provided, required, optional)
        except KeyError:
            self.fail("check_variables_for_function raised KeyError unexpectedly!")

    def test_check_variables_missing_critical_halts_execution(self):
        """Verify missing critical context keys triggers a crisp, intentional KeyError execution halt."""
        required = [variable_names.DEAL_ORDERS, "CRITICAL_MISSING_KEY"]

        with self.assertRaises(KeyError):
            check_variables_for_function(self.mock_provided, required_variables=required)

    def test_check_variables_handles_none_inputs_safely(self):
        """Verify mutable default normalization works perfectly when parameters are explicitly passed as None."""
        try:
            check_variables_for_function(self.mock_provided, required_variables=None, optional_variables=None)
        except Exception as exc:
            self.fail(f"check_variables_for_function crashed on None boundaries with error: {exc}")


if __name__ == "__main__":
    unittest.main()
