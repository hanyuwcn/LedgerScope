import unittest

from src.config import variable_names as vn
from src.models import CurrencyExchangeModel


class TestCurrencyExchangeModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata and output register configuration."""
        model = CurrencyExchangeModel()

        expected_outputs = [
            vn.UNIT_RETAIL_PRICE_IN_RMB,
            vn.UNIT_FREIGHT_EXPENSE_IN_RMB,
            vn.UNIT_TARIFF_IN_RMB,
            vn.UNIT_RETAIL_MARGIN_IN_RMB,
            vn.UNIT_FOB_PRICE_IN_RMB,
        ]
        self.assertEqual(sorted(model.output_names), sorted(expected_outputs))
        self.assertEqual(model.required_variables, [vn.USD_TO_RMB])

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify that all inputs are correctly scaled by the exchange rate."""
        rate = 7.2
        inputs = {
            vn.USD_TO_RMB: rate,
            vn.UNIT_RETAIL_PRICE: 100.0,
            vn.UNIT_FREIGHT_EXPENSE: 10.0,
            vn.UNIT_TARIFF: 5.0,
            vn.UNIT_RETAIL_MARGIN: 20.0,
            vn.UNIT_FOB_PRICE: 50.0,
        }
        model = CurrencyExchangeModel(inputs)
        result = model.evaluate()

        self.assertEqual(result[vn.UNIT_RETAIL_PRICE_IN_RMB], 100.0 * rate)
        self.assertEqual(result[vn.UNIT_FREIGHT_EXPENSE_IN_RMB], 10.0 * rate)
        self.assertEqual(result[vn.UNIT_TARIFF_IN_RMB], 5.0 * rate)
        self.assertEqual(result[vn.UNIT_RETAIL_MARGIN_IN_RMB], 20.0 * rate)
        self.assertEqual(result[vn.UNIT_FOB_PRICE_IN_RMB], 50.0 * rate)

    def test_evaluate_defaults_to_zero_when_optional_missing(self):
        """Verify that missing optional attributes result in 0.0 conversion."""
        model = CurrencyExchangeModel({vn.USD_TO_RMB: 7.0})
        result = model.evaluate()

        self.assertEqual(result[vn.UNIT_RETAIL_PRICE_IN_RMB], 0.0)
        self.assertEqual(result[vn.UNIT_FREIGHT_EXPENSE_IN_RMB], 0.0)

    # -----------------------------------------------------------------
    # 3. EXPLICIT ERROR HANDLING
    # -----------------------------------------------------------------

    def test_check_variables_missing_required_rate_raises_error(self):
        """Verify check_variables catches missing exchange rate."""
        model = CurrencyExchangeModel({})
        with self.assertRaises(KeyError):
            model.check_variables()


if __name__ == "__main__":
    unittest.main()
