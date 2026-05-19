import unittest

from src.config import variable_names
from src.models import ProfitModel


class TestProfitModel(unittest.TestCase):

    def test_evaluate_positive_net_profit(self):
        """Verify profit calculations match expected metrics in a standard profitable scenario."""
        inputs = {
            variable_names.REVENUE: 25000.0,
            variable_names.COST: 15000.0
        }
        model = ProfitModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 25000.0 - 15000.0 = 10000.0
        self.assertEqual(enriched_output[variable_names.PROFIT], 10000.0)
        self.assertEqual(enriched_output[variable_names.REVENUE], 25000.0)

    def test_evaluate_negative_net_profit_handling(self):
        """Verify the calculation functions flawlessly when expenses outpace top-line revenues (net loss)."""
        inputs = {
            variable_names.REVENUE: 5000.0,
            variable_names.COST: 8000.0
        }
        model = ProfitModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: 5000.0 - 8000.0 = -3000.0
        self.assertEqual(enriched_output[variable_names.PROFIT], -3000.0)

    def test_evaluate_missing_required_variables_throws_exception(self):
        """Verify that omitting a critical pipeline anchor like revenue blocks calculation runs."""
        incomplete_inputs = {
            variable_names.COST: 12000.0
            # Missing REVENUE!
        }
        model = ProfitModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
