import unittest

from src.config import variable_names
from src.models import CostOfGoodsSoldModel


class TestCostOfGoodsSoldModel(unittest.TestCase):

    def test_evaluate_success_with_valid_parameters(self):
        """Verify COGS calculation executes correctly and blends outputs into the runtime context."""
        inputs = {
            variable_names.DEAL_PURCHASING_PRICE: 15.0,  # $15 per item
            variable_names.DEAL_ORDERS: 100,  # 100 orders
            variable_names.DEAL_ITEMS_PER_ORDER: 2  # 2 items per order
        }
        model = CostOfGoodsSoldModel(inputs)
        enriched_output = model.evaluate()

        # Math check: 15.0 * 100 * 2 = 3000.0
        self.assertEqual(enriched_output[variable_names.COST_COGS], 3000.0)

        # Verify inputs are fully preserved along with the output
        self.assertEqual(enriched_output[variable_names.DEAL_ORDERS], 100)

    def test_evaluate_missing_required_variables_raises_key_error(self):
        """Verify that omitting raw parameters stops process execution immediately."""
        incomplete_inputs = {
            variable_names.DEAL_PURCHASING_PRICE: 15.0,
            variable_names.DEAL_ORDERS: 100
            # Missing DEAL_ITEMS_PER_ORDER!
        }
        model = CostOfGoodsSoldModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
