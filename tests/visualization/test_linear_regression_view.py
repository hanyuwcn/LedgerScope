import unittest

import matplotlib.pyplot as plt

from src.analysis import stochastic_bivariate_simulation
from src.config import variable_names
from src.core import Variable
from src.models import NetIncomeModel, MarketPriceModel
from src.variables import Cost, PriceToEarningsRatio
from src.visualization.views.linear_regression_view import generate_linear_regression_from_lists


class TestLinearRegressionViewEngine(unittest.TestCase):

    def setUp(self):
        """Standardize fixture using the core fiscal pipeline."""
        self.pipeline = [NetIncomeModel(), MarketPriceModel()]

        self.variables = {
            variable_names.REVENUE: Variable(min=80000.0, exp=100000.0, max=120000.0),
            variable_names.COST: Cost(min=30000.0, exp=40000.0, max=50000.0),
            variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
        }

        # Generate production-ready bivariate data
        self.x_dist, self.y_dist, _ = stochastic_bivariate_simulation(
            variables=self.variables,
            independent_target_x=variable_names.REVENUE,
            dependent_target_y=variable_names.MARKET_PRICE,
            shuffled_variables=[variable_names.REVENUE],
            model_pipeline=self.pipeline,
            sample_size=50
        )

    # =========================================================================
    # MODULE STRUCTURAL TESTS: REGRESSION PLOT COMPILATION
    # =========================================================================

    def test_generate_regression_plot_happy_path(self):
        """Confirm regression plot generates with trend line and benchmarks."""
        fig = generate_linear_regression_from_lists(
            self.x_dist,
            self.y_dist,
            variable_names.REVENUE,
            variable_names.MARKET_PRICE,
            x_benchmark=100000.0,
            y_benchmark=5760000.0
        )

        self.assertIsInstance(fig, plt.Figure)
        ax = fig.axes[0]

        legend = ax.get_legend()
        # Expecting Trend Line + 2 Benchmarks = 3 items
        self.assertIsNotNone(legend)
        self.assertEqual(len(legend.get_texts()), 3)

        plt.close(fig)

    def test_generate_regression_plot_no_benchmarks(self):
        """Verify view scales cleanly when benchmarks are omitted."""
        fig = generate_linear_regression_from_lists(
            self.x_dist,
            self.y_dist,
            variable_names.REVENUE,
            variable_names.MARKET_PRICE,
            x_benchmark=None,
            y_benchmark=None
        )

        ax = fig.axes[0]
        legend = ax.get_legend()
        self.assertEqual(len(legend.get_texts()), 1)

        plt.close(fig)

    def test_generate_regression_plot_viewport_extension(self):
        """Verify viewport auto-scales when benchmarks exist outside original data range."""
        out_of_bounds_x = 200000.0  # Well outside our 120k max
        fig = generate_linear_regression_from_lists(
            self.x_dist,
            self.y_dist,
            variable_names.REVENUE,
            variable_names.MARKET_PRICE,
            x_benchmark=out_of_bounds_x,
            y_benchmark=None
        )

        ax = fig.axes[0]
        xlim_max = ax.get_xlim()[1]
        self.assertTrue(xlim_max >= out_of_bounds_x, "Viewport failed to extend for benchmark.")
        plt.close(fig)


if __name__ == '__main__':
    unittest.main()
