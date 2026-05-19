import unittest

from src.config import variable_names
from src.models import FreeCashFlowModel


class TestFreeCashFlowModel(unittest.TestCase):

    def test_evaluate_standard_positive_free_cash_flow(self):
        """Verify cash flow reconciles correctly when net income and depreciation outpace CapEx."""
        inputs = {
            variable_names.NET_INCOME: 20000.0,
            variable_names.DEPRECIATION: 3000.0,
            variable_names.CAPITAL_EXPENDITURE: 5000.0
        }
        model = FreeCashFlowModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 20000.0 + 3000.0 - 5000.0 = 18000.0
        self.assertEqual(enriched_output[variable_names.FREE_CASH_FLOW], 18000.0)

    def test_evaluate_negative_cash_flow_due_to_heavy_capex(self):
        """Verify cash flow turns negative when asset investment eclipses immediate operational cash."""
        inputs = {
            variable_names.NET_INCOME: 15000.0,
            variable_names.DEPRECIATION: 2000.0,
            variable_names.CAPITAL_EXPENDITURE: 25000.0  # Large asset acquisition
        }
        model = FreeCashFlowModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 15000.0 + 2000.0 - 25000.0 = -8000.0
        self.assertEqual(enriched_output[variable_names.FREE_CASH_FLOW], -8000.0)

    def test_missing_required_variables_halts_execution(self):
        """Verify that omitting an structural asset variable triggers an engine error block."""
        incomplete_inputs = {
            variable_names.NET_INCOME: 15000.0,
            variable_names.DEPRECIATION: 2000.0
            # Missing CAPITAL_EXPENDITURE!
        }
        model = FreeCashFlowModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
