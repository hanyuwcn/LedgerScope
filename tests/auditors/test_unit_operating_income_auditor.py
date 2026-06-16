import unittest

from src.auditors.unit_operating_income_auditor import UnitOperatingIncomeAuditor
from src.config import variable_names as vn


class TestUnitOperatingIncomeAuditor(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. SUCCESS PATHS
    # -----------------------------------------------------------------

    def test_reconciliation_success_with_defaults(self):
        """Verify audit passes when components sum to Operating Income, ignoring provided freight."""
        # Math: 250 (FOB) - 200 (EXW) - 0 (Marketing) - 0 (Fixed) = 50.0
        inputs = {
            vn.UNIT_OPERATING_INCOME: 50.0,
            vn.UNIT_FOB_PRICE: 250.0,
            vn.UNIT_EXW_PRICE: 200.0,
            vn.UNIT_MERCHANT_FREIGHT_EXPENSE_IN_RMB: 100.0  # Should be ignored (set to 0.0)
        }
        auditor = UnitOperatingIncomeAuditor(inputs)
        auditor.evaluate()

    def test_reconciliation_success_with_marketing_and_overhead(self):
        """Verify audit passes with optional marketing and overhead included."""
        # Math: 500 (FOB) - 200 (EXW) - 50 (Marketing) - 0 (Freight) - 50 (Fixed) = 200.0
        inputs = {
            vn.UNIT_OPERATING_INCOME: 200.0,
            vn.UNIT_FOB_PRICE: 500.0,
            vn.UNIT_EXW_PRICE: 200.0,
            vn.UNIT_MARKETING_EXPENSE: 50.0,
            vn.UNIT_FIXED_OVERHEAD_EXPENSE: 50.0,
            vn.UNIT_MERCHANT_FREIGHT_EXPENSE_IN_RMB: 999.0  # Should be ignored
        }
        auditor = UnitOperatingIncomeAuditor(inputs)
        auditor.evaluate()

    # -----------------------------------------------------------------
    # 2. FAILURE PATHS (CIRCUIT BREAKER)
    # -----------------------------------------------------------------

    def test_reconciliation_failure_raises_value_error(self):
        """Verify failure when Operating Income does not match calculation."""
        # Math: 250 - 200 = 50 (Expected). Provided: 40.0
        inputs = {
            vn.UNIT_OPERATING_INCOME: 40.0,
            vn.UNIT_FOB_PRICE: 250.0,
            vn.UNIT_EXW_PRICE: 200.0,
            vn.UNIT_MERCHANT_FREIGHT_EXPENSE_IN_RMB: 0.0
        }
        auditor = UnitOperatingIncomeAuditor(inputs)

        with self.assertRaises(ValueError) as context:
            auditor.evaluate()

        self.assertIn("!= unit_operating_income(40.0)", str(context.exception))

    # -----------------------------------------------------------------
    # 3. DEPENDENCY CHECKING
    # -----------------------------------------------------------------

    def test_missing_required_variables_halts_with_keyerror(self):
        """Verify that missing mandatory keys trigger KeyError."""
        incomplete_inputs = {
            vn.UNIT_OPERATING_INCOME: 50.0,
            vn.UNIT_FOB_PRICE: 250.0
            # Missing EXW and Freight
        }
        auditor = UnitOperatingIncomeAuditor(incomplete_inputs)

        with self.assertRaises(KeyError):
            auditor.evaluate()


if __name__ == "__main__":
    unittest.main()
