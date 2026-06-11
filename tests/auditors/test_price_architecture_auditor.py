import unittest

from src.auditors.price_architecture_auditor import PriceArchitectureAuditor
from src.config import variable_names


class TestPriceArchitectureAuditor(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. SUCCESS PATHS
    # -----------------------------------------------------------------

    def test_reconciliation_success_exact_match(self):
        """Verify audit passes when all components sum exactly to the totals."""
        inputs = {
            variable_names.COGS_PER_UNIT: 200.0,
            variable_names.PROFIT_PER_UNIT: 50.0,
            variable_names.UNIT_FOB: 250.0,
            variable_names.UNIT_RETAIL: 2000.0,
            variable_names.SHIPPING_COST_PER_UNIT: 350.0,
            variable_names.TARIFF_PER_UNIT: 700.0,
            variable_names.RETAIL_MARGIN_PER_UNIT: 700.0
        }
        auditor = PriceArchitectureAuditor(inputs)
        # Should execute without raising
        auditor.evaluate()

    def test_reconciliation_success_within_tolerance(self):
        """Verify audit passes when values are within the threshold."""
        inputs = {
            variable_names.COGS_PER_UNIT: 200.0005,
            variable_names.PROFIT_PER_UNIT: 50.0,
            variable_names.UNIT_FOB: 250.0,
            variable_names.UNIT_RETAIL: 250.0005,  # Sum of parts
            variable_names.SHIPPING_COST_PER_UNIT: 0.0,
            variable_names.TARIFF_PER_UNIT: 0.0,
            variable_names.RETAIL_MARGIN_PER_UNIT: 0.0
        }
        auditor = PriceArchitectureAuditor(inputs)
        auditor.evaluate()

    # -----------------------------------------------------------------
    # 2. FAILURE PATHS (CIRCUIT BREAKER)
    # -----------------------------------------------------------------

    def test_fob_reconciliation_failure_raises_value_error(self):
        """Verify failure when COGS + Profit != UnitFob."""
        inputs = {
            variable_names.COGS_PER_UNIT: 200.0,
            variable_names.PROFIT_PER_UNIT: 50.0,
            variable_names.UNIT_FOB: 999.0,  # Mismatch
            variable_names.UNIT_RETAIL: 1000.0
        }
        auditor = PriceArchitectureAuditor(inputs)
        with self.assertRaises(ValueError) as context:
            auditor.evaluate()

        expected_msg = "Reconciliation error: cog_per_unit(200.0) + profit_per_unit(50.0) != unit_fob(999.0)"
        self.assertEqual(str(context.exception), expected_msg)

    def test_retail_reconciliation_failure_raises_value_error(self):
        """Verify failure when components != UnitRetail."""
        inputs = {
            variable_names.COGS_PER_UNIT: 100.0,
            variable_names.PROFIT_PER_UNIT: 100.0,
            variable_names.UNIT_FOB: 200.0,
            variable_names.UNIT_RETAIL: 5000.0  # Mismatch
        }
        auditor = PriceArchitectureAuditor(inputs)
        with self.assertRaises(ValueError) as context:
            auditor.evaluate()

        expected_msg = ("Reconciliation error: unit_fob(200.0) + "
                        "shipping_cost_per_unit(0.0) + "
                        "tariff_per_unit(0.0) + "
                        "retail_margin_per_unit(0.0) != "
                        "unit_retail_price(5000.0)")

        self.assertEqual(str(context.exception), expected_msg)

    # -----------------------------------------------------------------
    # 3. EDGE CASES & OPTIONAL FALLBACKS
    # -----------------------------------------------------------------

    def test_omitted_optional_values_use_default_zero(self):
        """Verify that optional friction costs default to 0.0 if not provided."""
        # FOB: 200+50 = 250.
        # Retail: 250 + 0 + 0 + 0 = 250.
        inputs = {
            variable_names.COGS_PER_UNIT: 200.0,
            variable_names.PROFIT_PER_UNIT: 50.0,
            variable_names.UNIT_FOB: 250.0,
            variable_names.UNIT_RETAIL: 250.0
        }
        auditor = PriceArchitectureAuditor(inputs)
        auditor.evaluate()

    def test_optional_variable_override_failure(self):
        """Verify that providing specific optional values forces a new reconciliation check."""
        # 250 (FOB) + 10 (Shipping) = 260.
        # If we set RETAIL to 250, it should fail because 260 != 250.
        inputs = {
            variable_names.COGS_PER_UNIT: 200.0,
            variable_names.PROFIT_PER_UNIT: 50.0,
            variable_names.UNIT_FOB: 250.0,
            variable_names.UNIT_RETAIL: 250.0,
            variable_names.SHIPPING_COST_PER_UNIT: 10.0,  # Override default 0.0
            variable_names.TARIFF_PER_UNIT: 0.0,
            variable_names.RETAIL_MARGIN_PER_UNIT: 0.0
        }
        auditor = PriceArchitectureAuditor(inputs)

        # This should raise ValueError because 260 != 250
        with self.assertRaises(ValueError) as context:
            auditor.evaluate()

        expected_msg = ("Reconciliation error: unit_fob(250.0) + "
                        "shipping_cost_per_unit(10.0) + "
                        "tariff_per_unit(0.0) + "
                        "retail_margin_per_unit(0.0) != "
                        "unit_retail_price(250.0)")
        self.assertEqual(str(context.exception), expected_msg)

    def test_missing_required_variables_halts_with_keyerror(self):
        """Verify that missing mandatory keys triggers KeyError (via base class)."""
        inputs = {variable_names.COGS_PER_UNIT: 100.0}  # Missing mandatory keys
        auditor = PriceArchitectureAuditor(inputs)
        with self.assertRaises(KeyError):
            auditor.evaluate()


if __name__ == "__main__":
    unittest.main()
