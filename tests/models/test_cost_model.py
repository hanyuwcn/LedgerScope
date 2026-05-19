import unittest

from src.config import variable_names
from src.models import TotalCostModel


class TestTotalCostModel(unittest.TestCase):

    def test_evaluate_success_with_all_parameters(self):
        """Verify cost aggregation runs cleanly when optional shipping costs are explicit."""
        inputs = {
            variable_names.COST_COGS: 4500.0,
            variable_names.COST_ADVERTISING: 2000.0,
            variable_names.COST_SHIPPING: 350.0
        }
        model = TotalCostModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: 4500 + 2000 + 350 = 6850.0
        self.assertEqual(enriched_output[variable_names.COST], 6850.0)

        # Verify context integrity remains uncorrupted
        self.assertEqual(enriched_output[variable_names.COST_COGS], 4500.0)

    def test_evaluate_success_with_omitted_shipping_fallback(self):
        """Verify cost aggregation falls back to zero when shipping costs are omitted."""
        inputs = {
            variable_names.COST_COGS: 5000.0,
            variable_names.COST_ADVERTISING: 1500.0
            # Shipping omitted intentionally
        }
        model = TotalCostModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: 5000 + 1500 + 0 = 6500.0
        self.assertEqual(enriched_output[variable_names.COST], 6500.0)

    def test_evaluate_missing_required_variables_raises_key_error(self):
        """Verify omitting an operational pillar like COGS immediately aborts execution."""
        incomplete_inputs = {
            variable_names.COST_ADVERTISING: 1500.0
            # Missing COST_COGS!
        }
        model = TotalCostModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
