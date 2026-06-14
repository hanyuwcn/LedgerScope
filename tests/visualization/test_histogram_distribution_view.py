import unittest

import matplotlib.pyplot as plt

from src.analysis import run_monte_carlo
from src.config import variable_names
from src.core import Variable
from src.models import NetIncomeModel, MarketPriceModel
from src.variables import PriceToEarningsRatio
from src.visualization.views.histogram_distribution_view import generate_histogram_from_array


class TestHistogramDistributionViewEngine(unittest.TestCase):

    def setUp(self):
        """Standardize fixture using the core fiscal pipeline."""
        self.pipeline = [NetIncomeModel(), MarketPriceModel()]

        self.variables = {
            variable_names.REVENUE: Variable(min=80000.0, exp=100000.0, max=120000.0),
            variable_names.COST: Variable(min=30000.0, exp=40000.0, max=50000.0),
            variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
        }

        # Generate production-ready simulation data
        self.simulation_data = run_monte_carlo(
            variables=self.variables,
            shuffled_inputs=[variable_names.REVENUE, variable_names.COST],
            model_pipeline=self.pipeline,
            tracked_outputs=[variable_names.MARKET_PRICE],
            iterations=100
        )

    # =========================================================================
    # MODULE STRUCTURAL TESTS: MATPLOTLIB CHART COMPILATION
    # =========================================================================

    def test_generate_histogram_happy_path_with_goal(self):
        """Confirm histogram renders with mean and goal reference lines."""
        fig = generate_histogram_from_array(
            self.simulation_data,
            variable_names.MARKET_PRICE,
            goal=5760000.0
        )

        self.assertIsInstance(fig, plt.Figure)
        ax = fig.axes[0]

        # Verify legend contains the expected reference lines
        legend = ax.get_legend()
        self.assertIsNotNone(legend)
        self.assertEqual(len(legend.get_texts()), 2)

        plt.close(fig)

    def test_generate_histogram_without_goal(self):
        """Confirm chart renders correctly with only the mean reference line."""
        fig = generate_histogram_from_array(
            self.simulation_data,
            variable_names.MARKET_PRICE,
            goal=None
        )

        ax = fig.axes[0]
        legend = ax.get_legend()
        self.assertEqual(len(legend.get_texts()), 1)

        plt.close(fig)

    def test_generate_histogram_zero_variance_resilience(self):
        """Confirm engine handles zero-variance outputs (forced inputs) gracefully."""
        # Force a deterministic state
        deterministic_data = [{variable_names.MARKET_PRICE: 5000000.0} for _ in range(10)]

        try:
            fig = generate_histogram_from_array(deterministic_data, variable_names.MARKET_PRICE, goal=5000000.0)
            plt.close(fig)
            success = True
        except Exception:
            success = False

        self.assertTrue(success, "Histogram engine crashed on zero-variance output.")


if __name__ == '__main__':
    unittest.main()
