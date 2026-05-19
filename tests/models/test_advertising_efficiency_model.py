import unittest

from src.config import variable_names
from src.models import AdvertisingEfficiencyModel


class TestAdvertisingEfficiencyModel(unittest.TestCase):

    def test_evaluate_success_with_all_parameters(self):
        """Verify order calculation with explicit currency exchange factors provided."""
        inputs = {
            variable_names.COST_ADVERTISING: 10000,  # $10,000 Ads Budget
            variable_names.COST_CONVERSION_RATE: 0.05,  # 5% Conversion Rate
            variable_names.COST_CPA: 20,  # $20 CPA
            variable_names.FINANCE_USD_TO_RMB: 7.0  # Currency factor multiplier
        }
        model = AdvertisingEfficiencyModel(inputs)
        enriched_output = model.evaluate()

        # Calculation: (10000 * 0.05) / (20 * 7.0) = 500 / 140 = 3.5714...
        expected_orders = (10000 * 0.05) / (20 * 7.0)
        self.assertAlmostEqual(enriched_output[variable_names.DEAL_ORDERS], expected_orders, places=4)

    def test_evaluate_success_with_omitted_optional_currency(self):
        """Verify calculation falls back safely when optional exchange rate is omitted."""
        inputs = {
            variable_names.COST_ADVERTISING: 5000,
            variable_names.COST_CONVERSION_RATE: 0.10,  # 10%
            variable_names.COST_CPA: 25
        }
        model = AdvertisingEfficiencyModel(inputs)
        enriched_output = model.evaluate()

        # Calculation falls back to usd_to_rmb = 1.0: (5000 * 0.10) / (25 * 1.0) = 500 / 25 = 20
        self.assertEqual(enriched_output[variable_names.DEAL_ORDERS], 20)

    def test_evaluate_missing_required_variables_raises_key_error(self):
        """Verify that omitting a mandatory variable like CPA stops execution."""
        incomplete_inputs = {
            variable_names.COST_ADVERTISING: 5000,
            variable_names.COST_CONVERSION_RATE: 0.10
            # Missing COST_CPA!
        }
        model = AdvertisingEfficiencyModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
