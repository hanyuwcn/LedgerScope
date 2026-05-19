import unittest

from src.config import variable_names
from src.models import NetIncomeModel


class TestNetIncomeModel(unittest.TestCase):

    def test_evaluate_net_income_pre_tax_defaults(self):
        """Verify calculation works cleanly when tax rate is completely omitted."""
        inputs = {
            variable_names.REVENUE: 40000.0,
            variable_names.COST: 15000.0,
            variable_names.EXPENSE: 5000.0,
            variable_names.DEPRECIATION: 1000.0
            # FINANCE_TAX_RATE is intentionally omitted to test 0.0 fallback
        }
        model = NetIncomeModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: (40000 - 15000 - 5000 - 1000) * (1 - 0.0) = 19000.0
        self.assertEqual(enriched_output[variable_names.NET_INCOME], 19000.0)

    def test_evaluate_net_income_with_active_taxation(self):
        """Verify after-tax corporate profit deduction structures compute accurately."""
        inputs = {
            variable_names.REVENUE: 100000.0,
            variable_names.COST: 40000.0,
            variable_names.EXPENSE: 10000.0,
            variable_names.DEPRECIATION: 5000.0,
            variable_names.FINANCE_TAX_RATE: 0.25  # 25% Tax Rate
        }
        model = NetIncomeModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: (100000 - 40000 - 10000 - 5000) = 45000.0 pre-tax
        # 45000.0 * (1 - 0.25) = 33750.0 after-tax
        self.assertEqual(enriched_output[variable_names.NET_INCOME], 33750.0)

    def test_evaluate_net_loss_scenario(self):
        """Verify math behaves appropriately when operational costs create a net fiscal loss."""
        inputs = {
            variable_names.REVENUE: 10000.0,
            variable_names.COST: 12000.0,
            variable_names.EXPENSE: 3000.0,
            variable_names.DEPRECIATION: 500.0,
            variable_names.FINANCE_TAX_RATE: 0.20
        }
        model = NetIncomeModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: (10000 - 12000 - 3000 - 500) = -5500.0 pre-tax
        # -5500.0 * (1 - 0.20) = -4400.0 net loss
        self.assertEqual(enriched_output[variable_names.NET_INCOME], -4400.0)

    def test_missing_required_parameters_raises_key_error(self):
        """Verify that dropping a critical parameter like Depreciation halts processing execution."""
        incomplete_inputs = {
            variable_names.REVENUE: 50000.0,
            variable_names.COST: 20000.0,
            variable_names.EXPENSE: 5000.0
            # Missing DEPRECIATION!
        }
        model = NetIncomeModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
