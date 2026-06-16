import unittest

from src.auditors.deduction_auditor import DeductionAuditor
from src.config import variable_names as vn


class TestDeductionAuditor(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. SUCCESS PATHS
    # -----------------------------------------------------------------

    def test_reconciliation_success_all_components(self):
        """Verify audit passes when rates are valid and waterfall balances."""
        inputs = {
            vn.UNIT_FOB_PRICE: 100.0,
            vn.UNIT_RETAIL_PRICE: 200.0,
            vn.TARIFF_RATE: 0.1,
            vn.MERCHANT_FREIGHT_RATE: 0.1,
            vn.CHANNEL_MARKUP_RATE: 0.1,
            vn.UNIT_MERCHANT_FREIGHT_EXPENSE: 30.0,
            vn.UNIT_TARIFF: 30.0,
            vn.UNIT_RETAIL_MARGIN: 40.0
        }
        auditor = DeductionAuditor(inputs)
        auditor.evaluate()

    # -----------------------------------------------------------------
    # 2. FAILURE PATHS (CIRCUIT BREAKER)
    # -----------------------------------------------------------------

    def test_deduction_rate_upper_bound_failure(self):
        """Verify failure when sum of rates > 1.0."""
        inputs = {
            vn.UNIT_FOB_PRICE: 100.0,
            vn.UNIT_RETAIL_PRICE: 200.0,
            vn.TARIFF_RATE: 0.5,
            vn.MERCHANT_FREIGHT_RATE: 0.6,  # Total = 1.1
            vn.CHANNEL_MARKUP_RATE: 0.0
        }
        auditor = DeductionAuditor(inputs)
        with self.assertRaises(ValueError) as context:
            auditor.evaluate()
        self.assertIn("deduction_rate(1.1) > 1", str(context.exception))

    def test_price_reconciliation_failure(self):
        """Verify failure when waterfall sum != UnitRetailPrice."""
        inputs = {
            vn.UNIT_FOB_PRICE: 100.0,
            vn.UNIT_RETAIL_PRICE: 500.0,  # Wrong total
            vn.UNIT_MERCHANT_FREIGHT_EXPENSE: 10.0,
            vn.UNIT_TARIFF: 10.0,
            vn.UNIT_RETAIL_MARGIN: 10.0
        }
        auditor = DeductionAuditor(inputs)
        with self.assertRaises(ValueError) as context:
            auditor.evaluate()
        self.assertIn("Reconciliation error", str(context.exception))

    # -----------------------------------------------------------------
    # 3. DEPENDENCY CHECKING
    # -----------------------------------------------------------------

    def test_missing_required_variables_halts_with_keyerror(self):
        """Verify that missing mandatory keys trigger KeyError."""
        incomplete_inputs = {vn.UNIT_FOB_PRICE: 100.0}  # Missing Retail Price
        auditor = DeductionAuditor(incomplete_inputs)
        with self.assertRaises(KeyError):
            auditor.evaluate()


if __name__ == "__main__":
    unittest.main()
