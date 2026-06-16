import unittest

from src.auditors import FreightExpenseAuditor
from src.config import variable_names as vn


class TestFreightExpenseAuditor(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. SUCCESS PATHS
    # -----------------------------------------------------------------

    def test_freight_valid_configuration_brand_pays(self):
        """Verify audit passes when only Brand pays freight."""
        inputs = {vn.MERCHANT_FREIGHT_RATE: 0.0, vn.BRAND_FREIGHT_EXPENSE: 10.0}
        auditor = FreightExpenseAuditor(inputs)
        auditor.evaluate()  # Should not raise

    def test_freight_valid_configuration_merchant_pays(self):
        """Verify audit passes when only Merchant pays freight."""
        inputs = {vn.MERCHANT_FREIGHT_RATE: 0.05, vn.BRAND_FREIGHT_EXPENSE: 0.0}
        auditor = FreightExpenseAuditor(inputs)
        auditor.evaluate()

    def test_freight_valid_configuration_none_pay(self):
        """Verify audit passes when freight is ignored (0, 0)."""
        inputs = {vn.MERCHANT_FREIGHT_RATE: 0.0, vn.BRAND_FREIGHT_EXPENSE: 0.0}
        auditor = FreightExpenseAuditor(inputs)
        auditor.evaluate()

    # -----------------------------------------------------------------
    # 2. FAILURE PATHS (CIRCUIT BREAKER)
    # -----------------------------------------------------------------

    def test_freight_conflict_raises_value_error(self):
        """Verify failure when both parties claim freight responsibility."""
        inputs = {
            vn.MERCHANT_FREIGHT_RATE: 0.1,
            vn.BRAND_FREIGHT_EXPENSE: 50.0
        }
        auditor = FreightExpenseAuditor(inputs)

        with self.assertRaises(ValueError) as context:
            auditor.evaluate()

        self.assertIn("Freight cost conflict", str(context.exception))


if __name__ == "__main__":
    unittest.main()
