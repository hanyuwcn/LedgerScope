import unittest

from src.config import variable_names as vn
from src.variables import SetupInvestment, PriceToEarningsRatio


class TestInvestmentVariables(unittest.TestCase):

    def setUp(self):
        """Initialize investment variables with defined operational boundaries."""
        # SetupInvestment: Testing within the 10k-30k range
        self.setup_inv = SetupInvestment(min=10000, exp=20000, max=30000)

        # PE Ratio: Testing standard valuation multiples
        self.pe_ratio = PriceToEarningsRatio(min=5.0, exp=10.0, max=15.0)

    # =====================================================================
    # IDENTITY & NAMING TESTS
    # =====================================================================

    def test_investment_identity_mappings(self):
        """Verify that classes map to the correct vn constant."""
        self.assertEqual(self.setup_inv.name, vn.SETUP_INVESTMENT)
        self.assertEqual(self.pe_ratio.name, vn.PE_RATIO)

    # =====================================================================
    # BOUNDARY CONFIGURATION TESTS
    # =====================================================================

    def test_setup_investment_range(self):
        """Verify SetupInvestment adheres to the defined startup cost window."""
        self.assertEqual(self.setup_inv.min_value, 10000)
        self.assertEqual(self.setup_inv.max_value, 30000)
        self.assertEqual(self.setup_inv.expected_value, 20000.0)

    def test_pe_ratio_range(self):
        """Verify PriceToEarningsRatio captures the expected market premium."""
        self.assertEqual(self.pe_ratio.min_value, 5.0)
        self.assertEqual(self.pe_ratio.max_value, 15.0)
        self.assertEqual(self.pe_ratio.expected_value, 10.0)

    # =====================================================================
    # BEHAVIORAL METHOD TESTS
    # =====================================================================

    def test_investment_stochastic_sampling(self):
        """Verify sampling remains within capital expenditure and valuation bounds."""
        for _ in range(50):
            rand_setup = self.setup_inv.get_random_value()
            rand_pe = self.pe_ratio.get_random_value()

            self.assertTrue(10000 <= rand_setup <= 30000)
            self.assertTrue(5.0 <= rand_pe <= 15.0)


if __name__ == "__main__":
    unittest.main()
