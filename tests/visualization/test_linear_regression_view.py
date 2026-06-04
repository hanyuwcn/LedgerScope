import unittest
import matplotlib.pyplot as plt
from src.visualization.views.linear_regression_view import generate_linear_regression_from_lists


class TestLinearRegressionViewEngine(unittest.TestCase):

    def setUp(self):
        """Build standard telemetry arrays mimicking simulation vectors."""
        self.x_data = [10, 20, 30, 40, 50]
        self.y_data = [100, 150, 190, 260, 310]
        self.x_label = "MarketingSpend"
        self.y_label = "SalesRevenue"

    def test_generate_regression_plot_happy_path(self):
        """Scenario 1: Confirm chart generation compiles a valid figure with matching elements."""
        fig = generate_linear_regression_from_lists(
            self.x_data, self.y_data, self.x_label, self.y_label, x_benchmark=25, y_benchmark=200
        )

        self.assertIsInstance(fig, plt.Figure)
        self.assertTrue(len(fig.axes) > 0)

        ax = fig.axes[0]
        legend = ax.get_legend()
        self.assertIsNotNone(legend)

        # Trend line + 2 benchmark lines = 3 legends items expected
        self.assertEqual(len(legend.get_texts()), 3)
        plt.close(fig)

    def test_generate_regression_plot_no_benchmarks(self):
        """Scenario 2: Verify chart scales cleanly without crashing when benchmark markers are omitted."""
        fig = generate_linear_regression_from_lists(
            self.x_data, self.y_data, self.x_label, self.y_label, x_benchmark=None, y_benchmark=None
        )

        ax = fig.axes[0]
        legend = ax.get_legend()

        # Only trend line item should populate the legend card layout
        self.assertEqual(len(legend.get_texts()), 1)
        plt.close(fig)

    def test_generate_regression_plot_viewport_extension(self):
        """Scenario 3: Verify viewport limits stretch out safely when a benchmark sits far outside data pools."""
        # Benchmark far right of max value 50
        fig = generate_linear_regression_from_lists(
            self.x_data, self.y_data, self.x_label, self.y_label, x_benchmark=120, y_benchmark=None
        )

        ax = fig.axes[0]
        xlim_max = ax.get_xlim()[1]
        self.assertTrue(xlim_max > 120,
                        "Plotting viewport failed to extend outwards to capture out-of-bounds benchmark.")
        plt.close(fig)


if __name__ == '__main__':
    unittest.main()
