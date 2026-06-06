import unittest

from src.utils.formatting import list_to_element_string, fmt
from src.config import variable_names
from src.config.formatting import VARIABLE_FORMATTING_MAP


class TestFormattingUtils(unittest.TestCase):

    # =====================================================================
    # FMT (NUMBER FORMATTER) TESTS
    # =====================================================================

    def test_fmt_default_behavior(self):
        """Verify that basic integers and floats round to 0 decimal places with commas."""
        self.assertEqual(fmt(1234567), "1,234,567")
        self.assertEqual(fmt(1234.56), "1,235")

    def test_fmt_with_custom_decimals(self):
        """Verify that precision scales exactly to the custom 'd' argument."""
        self.assertEqual(fmt(1234.5678, d=2), "1,234.57")
        self.assertEqual(fmt(1234, d=2), "1,234.00")

    def test_fmt_with_currency_sign(self):
        """Verify that currency symbols are properly prefixed to formatted outputs."""
        self.assertEqual(fmt(1234567, d=0, s="¥"), "¥1,234,567")
        self.assertEqual(fmt(1234.56, d=2, s="$"), "$1,234.56")

    def test_fmt_percentage_mode(self):
        """Verify that numbers are scaled by 100, comma separated, and append a '%' sign."""
        # 0.0525 * 100 = 5.25%
        self.assertEqual(fmt(0.0525, d=2, p=True), "5.25%")
        # 1234.56 * 100 = 123,456.0%
        self.assertEqual(fmt(1234.56, d=1, p=True), "123,456.0%")

    def test_fmt_percentage_with_currency(self):
        """Verify that both currency symbols and scaled percentages render together gracefully."""
        # e.g., Margin rates in absolute currency performance notation
        self.assertEqual(fmt(0.085, d=1, s="¥", p=True), "¥8.5%")

    def test_fmt_string_and_invalid_fallbacks(self):
        """Verify that invalid inputs or text tags fail silently and return clean text strings."""
        self.assertEqual(fmt("N/A"), "N/A")
        self.assertEqual(fmt(None), "None")
        self.assertEqual(fmt("1234.56", d=2), "1,234.56")  # Valid numeric strings parse correctly

    # =====================================================================
    # VARIABLE FORMATTING CONFIGURATION MAP TESTS
    # =====================================================================

    def test_new_advertising_and_funnel_variable_formatting(self):
        """Verify new Google Search pipeline variables map to their designated precision rules and origin flags."""
        # CONVERSION_RATE_GOOGLE_SEARCH -> d=2, p=True (e.g., 0.04256 -> 4.26%)
        cvr_lambda = VARIABLE_FORMATTING_MAP[variable_names.CONVERSION_RATE_GOOGLE_SEARCH]
        self.assertEqual(cvr_lambda(0.04256), "4.26%")

        # CPC_GOOGLE_SEARCH -> d=1, s='$' (e.g., 2.54 -> $2.5)
        cpc_lambda = VARIABLE_FORMATTING_MAP[variable_names.CPC_GOOGLE_SEARCH]
        self.assertEqual(cpc_lambda(2.54), "$2.5")

        # ALLOCATION_GOOGLE_SEARCH -> d=0, p=True (e.g., 0.60 -> 60%)
        alloc_lambda = VARIABLE_FORMATTING_MAP[variable_names.ALLOCATION_GOOGLE_SEARCH]
        self.assertEqual(alloc_lambda(0.60), "60%")

        # CPL_GOOGLE_SEARCH -> d=1, s='$' (Conceptual dollar tag indicator verification)
        cpl_lambda = VARIABLE_FORMATTING_MAP[variable_names.CPL_GOOGLE_SEARCH]
        self.assertEqual(cpl_lambda(104.166), "$104.2")

        # CLOSE_RATE -> d=2, p=True (e.g., 0.125 -> 12.50%)
        close_lambda = VARIABLE_FORMATTING_MAP[variable_names.CLOSE_RATE]
        self.assertEqual(close_lambda(0.125), "12.50%")

    def test_new_performance_metrics_variable_formatting(self):
        """Verify that performance tracking metrics retain clear fractional precision and percentage marks."""
        # ROI -> d=2, p=True (e.g., 0.4567 -> 45.67%)
        roi_lambda = VARIABLE_FORMATTING_MAP[variable_names.ROI]
        self.assertEqual(roi_lambda(0.4567), "45.67%")

        # ROAS -> d=2, p=True (e.g., 3.75 -> 375.00%)
        roas_lambda = VARIABLE_FORMATTING_MAP[variable_names.ROAS]
        self.assertEqual(roas_lambda(3.75), "375.0%")

    # =====================================================================
    # LIST TO ELEMENT STRING TESTS
    # =====================================================================

    def test_list_to_element_string_with_multiple_elements(self):
        """Verify that multiple strings are joined with a space following each comma separator."""
        elements = ["COST_CPA", "FINANCE_TAX_RATE", "DEAL_ORDERS"]
        result = list_to_element_string(elements)
        self.assertEqual(result, "COST_CPA, FINANCE_TAX_RATE, DEAL_ORDERS")

    def test_list_to_element_string_with_single_element(self):
        """Verify that a list with one item returns just that item string without trailing commas."""
        elements = ["EXPENSE_MONTHLY_RENT"]
        result = list_to_element_string(elements)
        self.assertEqual(result, "EXPENSE_MONTHLY_RENT")

    def test_list_to_element_string_with_empty_list(self):
        """Verify that an empty input list returns a pristine empty string instantly."""
        self.assertEqual(list_to_element_string([]), "")


if __name__ == "__main__":
    unittest.main()
