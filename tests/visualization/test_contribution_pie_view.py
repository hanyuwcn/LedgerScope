import unittest

import matplotlib.pyplot as plt

from src.analysis import stochastic_contribution_analysis
from src.config import variable_names
from src.core import Variable
from src.models import NetIncomeModel, MarketPriceModel, OperatingIncomeModel
from src.variables import PriceToEarningsRatio
from src.visualization.styles import contribution_pie_styles
from src.visualization.views.contribution_pie_view import generate_contribution_pie_chart


class TestContributionPieViewEngine(unittest.TestCase):

    def setUp(self):
        """Standardize fixture using the core fiscal pipeline."""
        self.pipeline = [OperatingIncomeModel(), NetIncomeModel(), MarketPriceModel()]

        self.variables = {
            variable_names.REVENUE: Variable(min=80000.0, exp=100000.0, max=120000.0),
            variable_names.COGS: Variable(min=30000.0, exp=40000.0, max=50000.0),
            variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
        }

        # Generate production-ready contribution output
        self.analysis_output = stochastic_contribution_analysis(
            variables=self.variables,
            breakdown_metrics=[variable_names.REVENUE, variable_names.COGS],
            model_pipeline=self.pipeline,
            shuffled_inputs=[variable_names.REVENUE, variable_names.COGS],
            sample_size=50
        )

    # =========================================================================
    # MODULE STRUCTURAL TESTS: MATPLOTLIB CHART COMPILATION
    # =========================================================================

    def test_generate_contribution_pie_chart_happy_path(self):
        """Confirm chart generation compiles using engine-derived data."""
        fig = generate_contribution_pie_chart(self.analysis_output)

        self.assertIsInstance(fig, plt.Figure)
        ax = fig.axes[0]

        # Verify title and legend reflect the fiscal pipeline inputs
        self.assertEqual(ax.get_title(), contribution_pie_styles.PIE_MAIN_TITLE)

        legend = ax.get_legend()
        self.assertIsNotNone(legend)
        self.assertEqual(len(legend.get_texts()), len(self.analysis_output))

        plt.close(fig)

    def test_generate_contribution_pie_chart_zero_sum_safety(self):
        """Confirm safety guard processes zero-sum datasets without crashing."""
        zero_sum = {variable_names.REVENUE: 0.0, variable_names.COGS: 0.0}

        try:
            fig = generate_contribution_pie_chart(zero_sum)
            plt.close(fig)
            success = True
        except Exception:
            success = False

        self.assertTrue(success, "Engine crashed processing zero-sum absolute metrics.")


if __name__ == '__main__':
    unittest.main()
