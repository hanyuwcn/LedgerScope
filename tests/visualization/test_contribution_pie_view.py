import unittest

import matplotlib.pyplot as plt

from src.visualization.styles import contribution_pie_styles
from src.visualization.views.contribution_pie_view import generate_contribution_pie_chart


class TestContributionPieViewEngine(unittest.TestCase):

    def setUp(self):
        self.analysis_output = {'Revenue': 102875.4356, 'CostOfGoodSold': 40749.9030}

    # =========================================================================
    # MODULE STRUCTURAL TESTS: MATPLOTLIB CHART COMPILATION
    # =========================================================================

    def test_generate_contribution_pie_chart_standalone_mode(self):
        """Confirm standalone compilation returns a Figure."""
        fig = generate_contribution_pie_chart(self.analysis_output)
        self.assertIsInstance(fig, plt.Figure)

        # Verify default title is set
        ax = fig.axes[0]
        self.assertEqual(ax.get_title(), contribution_pie_styles.PIE_MAIN_TITLE)

        plt.close(fig)

    def test_generate_contribution_pie_chart_aggregated_mode(self):
        """Confirm aggregated mode returns None and draws to provided axes."""
        fig, ax = plt.subplots()
        result = generate_contribution_pie_chart(self.analysis_output, ax=ax)

        self.assertIsNone(result, "Function should return None when ax is provided.")

        # Verify legend existence on the provided axes
        legend = ax.get_legend()
        self.assertIsNotNone(legend)
        self.assertEqual(len(legend.get_texts()), len(self.analysis_output))

        plt.close(fig)

    def test_generate_contribution_pie_chart_custom_title(self):
        """Confirm title argument is correctly applied to the axes."""
        custom_title = "Fiscal Impact Breakdown"
        _, ax = plt.subplots()
        generate_contribution_pie_chart(self.analysis_output, ax=ax, title=custom_title)

        self.assertEqual(ax.get_title(), custom_title)
        plt.close()

    def test_generate_contribution_pie_chart_zero_sum_safety(self):
        """Confirm safety guard processes zero-sum datasets without crashing."""
        zero_sum = {'Revenue': 0.0, 'COGS': 0.0}
        try:
            fig = generate_contribution_pie_chart(zero_sum)
            plt.close(fig)
            success = True
        except Exception as e:
            print(f"Caught expected error: {e}")
            success = False
        self.assertTrue(success, "Engine crashed processing zero-sum absolute metrics.")


if __name__ == '__main__':
    unittest.main()
