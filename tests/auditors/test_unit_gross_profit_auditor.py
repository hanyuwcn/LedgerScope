import unittest

from src.auditors.unit_gross_profit_auditor import UnitGrossProfitAuditor
from src.config import variable_names as vn


class TestUnitGrossProfitAuditor(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. SUCCESS PATHS
    # -----------------------------------------------------------------

    def test_reconciliation_success_exact_match(self):
        """Verify audit passes when Gross Profit matches FOB - EXW."""
        inputs = {
            vn.UNIT_FOB_PRICE_IN_RMB: 250.0,
            vn.UNIT_EXW_PRICE: 200.0,
            vn.UNIT_GROSS_PROFIT: 50.0
        }
        auditor = UnitGrossProfitAuditor(inputs)
        auditor.evaluate()

    def test_reconciliation_success_within_tolerance(self):
        """Verify audit passes when values are within the threshold."""
        inputs = {
            vn.UNIT_FOB_PRICE_IN_RMB: 250.0005,
            vn.UNIT_EXW_PRICE: 200.0,
            vn.UNIT_GROSS_PROFIT: 50.0005
        }
        auditor = UnitGrossProfitAuditor(inputs)
        auditor.evaluate()

    # -----------------------------------------------------------------
    # 2. FAILURE PATHS (CIRCUIT BREAKER)
    # -----------------------------------------------------------------

    def test_reconciliation_failure_raises_value_error(self):
        """Verify failure when (FOB - EXW) != Gross Profit."""
        inputs = {
            vn.UNIT_FOB_PRICE_IN_RMB: 300.0,
            vn.UNIT_EXW_PRICE: 200.0,
            vn.UNIT_GROSS_PROFIT: 50.0  # Incorrect: should be 100.0
        }
        auditor = UnitGrossProfitAuditor(inputs)

        with self.assertRaises(ValueError) as context:
            auditor.evaluate()

        # Validate that the error message contains the mis-calculated components
        self.assertIn("Reconciliation error", str(context.exception))
        self.assertIn("!= unit_gross_profit(50.0)", str(context.exception))

    # -----------------------------------------------------------------
    # 3. EXPLICIT DEPENDENCY CHECKING
    # -----------------------------------------------------------------

    def test_missing_required_variables_halts_with_keyerror(self):
        """Verify that missing mandatory keys trigger KeyError."""
        incomplete_inputs = {
            vn.UNIT_FOB_PRICE_IN_RMB: 250.0
            # Missing EXW and Gross Profit
        }
        auditor = UnitGrossProfitAuditor(incomplete_inputs)

        with self.assertRaises(KeyError):
            auditor.evaluate()


if __name__ == "__main__":
    unittest.main()
