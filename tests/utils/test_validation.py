import unittest

from src.config import variable_names
from src.utils.validation import get_missing_elements, check_variables_for_function

# Mocking your config error message setup locally for explicit string assertions
ERROR_VARIABLE_NOT_SETUP_WITH_MESSAGE = "Variable(s) not setup: {msg}"


class TestValidationUtils(unittest.TestCase):

    def setUp(self):
        """
        Set up a mock payload dictionary mimicking a partially 
        complete ledger state to test key validation compliance.
        """
        self.mock_provided = {
            variable_names.DEAL_ORDERS: 100,
            variable_names.DEAL_SELLING_PRICE: 4500,
            variable_names.EXPENSE_MONTHLY_RENT: 2000
        }

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

    def test_check_variables_success_path_silent(self):
        """Verify validation passes silently if all required context items are fully provided."""
        required = [variable_names.DEAL_ORDERS, variable_names.EXPENSE_MONTHLY_RENT]

        try:
            check_variables_for_function(self.mock_provided, required_variables=required)
        except KeyError:
            self.fail("check_variables_for_function raised KeyError unexpectedly when all keys were present!")

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

    def test_check_variables_handles_none_inputs_safely(self):
        """Verify default initialization mapping prevents crashes when required_variables is None."""
        try:
            check_variables_for_function(self.mock_provided, required_variables=None)
        except Exception as exc:
            self.fail(f"check_variables_for_function crashed when passed None with error: {exc}")


if __name__ == "__main__":
    unittest.main()
