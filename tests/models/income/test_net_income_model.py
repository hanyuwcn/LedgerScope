import unittest
from unittest.mock import patch

from src.config import variable_names as vn
from src.models import NetIncomeModel


class TestNetIncomeModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = NetIncomeModel()

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [vn.NET_INCOME])

        # Verify required variable: now only OPERATING_INCOME
        self.assertEqual(model.required_variables, [vn.OPERATING_INCOME])

        # Verify optional variable: TAX_RATE
        self.assertEqual(model.optional_variables, [vn.TAX_RATE])

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_net_income_success(self):
        """Verify model computes Net Income: OperatingIncome * (1 - TaxRate)."""
        inputs = {
            vn.OPERATING_INCOME: 50000.0,
            vn.TAX_RATE: 0.20
        }
        model = NetIncomeModel(inputs)
        enriched_output = model.evaluate()

        # Math: 50000.0 * 0.8 = 40000.0
        self.assertEqual(enriched_output[vn.NET_INCOME], 40000.0)

    def test_evaluate_default_tax_rate(self):
        """Verify model defaults to 0.0 tax rate if not provided."""
        inputs = {
            vn.OPERATING_INCOME: 50000.0
        }
        model = NetIncomeModel(inputs)
        enriched_output = model.evaluate()

        # Math: 50000.0 * (1 - 0) = 50000.0
        self.assertEqual(enriched_output[vn.NET_INCOME], 50000.0)

    def test_missing_required_parameters_raises_key_error(self):
        """Verify that dropping a critical mandatory parameter halts execution."""
        model = NetIncomeModel({})  # Missing OPERATING_INCOME

        with self.assertRaises(KeyError):
            model.evaluate()

    # -----------------------------------------------------------------
    # 3. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_missing_required_logs_error(self, mock_log):
        """Verify check_variables logs errors and raises KeyError if OPERATING_INCOME is absent."""
        model = NetIncomeModel({})

        with self.assertRaises(KeyError):
            model.check_variables()

        mock_log.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
