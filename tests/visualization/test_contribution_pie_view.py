import unittest
import matplotlib.pyplot as plt

from src.visualization.styles import contribution_pie_styles
from src.visualization.views.contribution_pie_view import generate_contribution_pie_chart


class TestContributionPieViewEngine(unittest.TestCase):

    def setUp(self):
        """Build standard mock datasets capturing varied financial simulation outputs."""
        self.standard_contributions = {
            'AdvertisingCost': 5000.0,
            'SellingPrice': 15000.0,
            'PurchasingPrice': 2500.0
        }

        self.zero_sum_contributions = {
            'FixedOverhead': 0.0,
            'CAC': 0.0
        }

    # =========================================================================
    # MODULE STRUCTURAL TESTS: MATPLOTLIB CHART COMPILATION
    # =========================================================================

    def test_generate_contribution_pie_chart_happy_path(self):
        """Scenario 1: Confirm chart generation compiles a valid figure with correct labels and elements."""
        fig = generate_contribution_pie_chart(self.standard_contributions)

        # Verify object integrity
        self.assertIsInstance(fig, plt.Figure)
        self.assertTrue(len(fig.axes) > 0)

        ax = fig.axes[0]

        # Verify the title text is correctly set from styles config signature
        self.assertEqual(ax.get_title(), contribution_pie_styles.PIE_MAIN_TITLE)

        # Ensure legend items match dictionary size exactly
        legend = ax.get_legend()
        self.assertIsNotNone(legend)
        self.assertEqual(len(legend.get_texts()), len(self.standard_contributions))

        # Close the active canvas layout tracker cleanly to manage runner memory footprint
        plt.close(fig)

    def test_generate_contribution_pie_chart_zero_sum_safety(self):
        """Scenario 2: Confirm safety guard processes an all-zero dataset without mathematical crashes."""
        # This test ensures division-by-zero math operations don't throw unexpected ZeroDivisionErrors
        try:
            fig = generate_contribution_pie_chart(self.zero_sum_contributions)
            closed_successfully = True
        except ZeroDivisionError:
            closed_successfully = False

        self.assertTrue(closed_successfully, "Engine crashed processing zero-sum absolute metrics.")

        # Verify it still builds a functional fallback chart structure
        ax = fig.axes[0]
        legend = ax.get_legend()
        self.assertEqual(len(legend.get_texts()), len(self.zero_sum_contributions))

        plt.close(fig)


if __name__ == '__main__':
    unittest.main()
