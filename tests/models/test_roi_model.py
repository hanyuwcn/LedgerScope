import unittest

from src.config import variable_names
from src.models import RoiModel


class TestRoiModel(unittest.TestCase):

    def test_evaluate_standard_positive_project_roi(self):
        """Verify ROI calculations yield standard positive fractional percentages."""
        inputs = {
            variable_names.NET_INCOME: 15000.0,
            variable_names.COST: 20000.0,
            variable_names.EXPENSE: 5000.0,
            variable_names.CAPITAL_EXPENDITURE: 5000.0
        }
        model = RoiModel(inputs)
        enriched_output = model.evaluate()

        # Denominator: 20000 + 5000 + 5000 = 30000.0 total outlay
        # ROI Math: 15000.0 / 30000.0 = 0.5 (50% ROI)
        self.assertEqual(enriched_output[variable_names.ROI], 0.5)

    def test_evaluate_negative_roi_from_net_loss(self):
        """Verify ROI correctly evaluates to a negative percentage when a net income loss is present."""
        inputs = {
            variable_names.NET_INCOME: -5000.0,
            variable_names.COST: 15000.0,
            variable_names.EXPENSE: 3000.0,
            variable_names.CAPITAL_EXPENDITURE: 2000.0
        }
        model = RoiModel(inputs)
        enriched_output = model.evaluate()

        # Denominator: 15000 + 3000 + 2000 = 20000.0 total outlay
        # ROI Math: -5000.0 / 20000.0 = -0.25 (-25% ROI)
        self.assertEqual(enriched_output[variable_names.ROI], -0.25)

    def test_division_by_zero_safety_catch(self):
        """Verify engine intercepts empty outlays and defaults to 0.0 instead of crashing."""
        edge_case_inputs = {
            variable_names.NET_INCOME: 1000.0,  # Arbitrary positive return data
            variable_names.COST: 0.0,
            variable_names.EXPENSE: 0.0,
            variable_names.CAPITAL_EXPENDITURE: 0.0
        }
        model = RoiModel(edge_case_inputs)
        enriched_output = model.evaluate()

        # System intercepts total_outlay == 0 and maps ROI cleanly to 0.0
        self.assertEqual(enriched_output[variable_names.ROI], 0.0)

    def test_missing_required_variables_halts_execution(self):
        """Verify that omitting an allocation layer parameter aborts execution processing."""
        incomplete_inputs = {
            variable_names.NET_INCOME: 15000.0,
            variable_names.COST: 20000.0,
            variable_names.EXPENSE: 5000.0
            # Missing CAPITAL_EXPENDITURE!
        }
        model = RoiModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.evaluate()


if __name__ == "__main__":
    unittest.main()
