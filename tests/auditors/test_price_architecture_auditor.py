import unittest

from src.auditors.price_architecture_auditor import PriceArchitectureAuditor
from src.config import variable_names as vn


class TestPriceArchitectureAuditor(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. SUCCESS PATHS
    # -----------------------------------------------------------------

    def test_reconciliation_success_exact_match(self):
        """Verify audit passes when all components sum exactly to the retail price."""
        inputs = {
            vn.UNIT_RETAIL_PRICE_IN_RMB: 1000.0,
            vn.UNIT_EXW_PRICE: 200.0,
            vn.UNIT_MARKETING_EXPENSE: 50.0,
            vn.UNIT_FIXED_OVERHEAD_EXPENSE: 50.0,
            vn.UNIT_OPERATING_INCOME: 300.0,
            vn.UNIT_FREIGHT_EXPENSE_IN_RMB: 100.0,
            vn.UNIT_TARIFF_IN_RMB: 100.0,
            vn.UNIT_RETAIL_MARGIN_IN_RMB: 200.0
        }
        auditor = PriceArchitectureAuditor(inputs)
        auditor.evaluate()

    def test_reconciliation_success_within_tolerance(self):
        """Verify audit passes when values are within the configured tolerance."""
        inputs = {
            vn.UNIT_RETAIL_PRICE_IN_RMB: 500.0005,
            vn.UNIT_EXW_PRICE: 200.0,
            vn.UNIT_OPERATING_INCOME: 300.0
        }
        auditor = PriceArchitectureAuditor(inputs)
        auditor.evaluate()

    # -----------------------------------------------------------------
    # 2. FAILURE PATHS (CIRCUIT BREAKER)
    # -----------------------------------------------------------------

    def test_reconciliation_failure_raises_value_error(self):
        """Verify failure when sum of components != UnitRetailPrice."""
        inputs = {
            vn.UNIT_RETAIL_PRICE_IN_RMB: 1000.0,
            vn.UNIT_EXW_PRICE: 100.0,
            vn.UNIT_OPERATING_INCOME: 100.0
        }
        auditor = PriceArchitectureAuditor(inputs)

        with self.assertRaises(ValueError) as context:
            auditor.evaluate()

        # Check that error message contains the mis-summed values
        self.assertIn("Reconciliation error", str(context.exception))
        self.assertIn("!= unit_retail_price(1000.0)", str(context.exception))

    # -----------------------------------------------------------------
    # 3. EDGE CASES & OPTIONAL FALLBACKS
    # -----------------------------------------------------------------

    def test_omitted_optional_values_use_default_zero(self):
        """Verify that optional expenses default to 0.0 if not provided."""
        # Sum = 200 (EXW) + 300 (Income) = 500
        inputs = {
            vn.UNIT_RETAIL_PRICE_IN_RMB: 500.0,
            vn.UNIT_EXW_PRICE: 200.0,
            vn.UNIT_OPERATING_INCOME: 300.0
        }
        auditor = PriceArchitectureAuditor(inputs)
        auditor.evaluate()

    def test_missing_required_variables_halts_with_keyerror(self):
        """Verify that missing mandatory keys trigger KeyError via base class."""
        inputs = {vn.UNIT_EXW_PRICE: 100.0}  # Missing Retail Price and Operating Income
        auditor = PriceArchitectureAuditor(inputs)
        with self.assertRaises(KeyError):
            auditor.evaluate()


if __name__ == "__main__":
    unittest.main()
