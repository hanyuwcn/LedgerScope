import unittest
from unittest.mock import patch, MagicMock

import matplotlib.pyplot as plt
import numpy as np

# Target import rules
from src.visualization.histogram_distribution_view import generate_histogram_from_array


class TestHistogramDistributionViewEngine(unittest.TestCase):

    def setUp(self):
        """Set up standard execution constants and isolate dependencies via configuration patches."""
        # 1. Setup mock names to match config dependencies safely
        self.patch_plots = patch('src.visualization.histogram_distribution_view.plots')
        self.mock_plots = self.patch_plots.start()

        # Canvas structural and text configuration attributes
        self.mock_plots.FIGURE_SIZE = (10, 6)
        self.mock_plots.HISTOGRAM_BIN_FONT = {'bins': 10, 'alpha': 0.75}
        self.mock_plots.HISTOGRAM_VERTICAL_LINE_GOAL = "Goal: {goal}"
        self.mock_plots.HISTOGRAM_VERTICAL_LINE_MEAN = "Mean: {mean}"
        self.mock_plots.HISTOGRAM_TITLE_CONTEXT = "Distribution of {output}"
        self.mock_plots.HISTOGRAM_X_LABEL_CONTEXT = "{output}"
        self.mock_plots.HISTOGRAM_Y_LABEL_CONTEXT = "Probability Density"

        self.mock_plots.LINE_SETTING_BIGGER = {'color': 'black', 'linestyle': '-'}
        self.mock_plots.LINE_SETTING_SMALLER = {'color': 'blue', 'linestyle': '--'}
        self.mock_plots.HISTOGRAM_IN_GRAPH_TEXT_FONTS = {'fontsize': 10}
        self.mock_plots.HISTOGRAM_IN_LEGENDS_TEXT_FONTS = {'loc': 'upper right'}
        self.mock_plots.TITLE_FONT = {'fontsize': 14}
        self.mock_plots.X_AXIS_FONT = {'fontsize': 12}
        self.mock_plots.Y_AXIS_FONT = {'fontsize': 12}
        self.mock_plots.TICK_SIZE = 10
        self.mock_plots.X_AXIS_COLOR = '#333333'
        self.mock_plots.Y_AXIS_COLOR = '#333333'

        # 2. Patch underlying internal analytics utility methods
        self.patch_compute_stats = patch('src.visualization.histogram_distribution_view.compute_simulation_stats')
        self.patch_colors = patch('src.visualization.histogram_distribution_view.get_threshold_boundary_colors')
        self.patch_norm = patch('src.visualization.histogram_distribution_view.get_gradient_normalizer')
        self.patch_formatter = patch('src.visualization.histogram_distribution_view.get_formatter')
        self.patch_axis_fmt = patch('src.visualization.histogram_distribution_view.get_axis_formatters')
        self.patch_percentages = patch('src.visualization.histogram_distribution_view.compute_target_percentages')
        self.patch_cm = patch('src.visualization.histogram_distribution_view.cm')

        self.mock_compute_stats = self.patch_compute_stats.start()
        self.mock_colors = self.patch_colors.start()
        self.mock_norm = self.patch_norm.start()
        self.mock_formatter = self.patch_formatter.start()
        self.mock_axis_fmt = self.patch_axis_fmt.start()
        self.mock_percentages = self.patch_percentages.start()
        self.mock_cm = self.patch_cm.start()

        # 3. Inject standard safe return behaviors into mocks
        self.mock_colors.return_value = {"color_not_met": "red", "color_met": "green"}
        self.mock_norm.return_value = lambda v: 0.5
        self.mock_formatter.return_value = lambda v: f"${v:,.2f}"
        self.mock_axis_fmt.return_value = (MagicMock(), MagicMock())
        self.mock_percentages.return_value = (75.0, 25.0)
        self.mock_cm.viridis_r = lambda v: (0.1, 0.2, 0.3, 1.0)  # Mock color map return tuple

        # 4. Mock simulation input payload
        self.mock_simulations = [{'NetProfit': 100}, {'NetProfit': 200}]
        self.mock_stats_data = np.array([100.0, 120.0, 150.0, 180.0, 200.0])
        self.mock_compute_stats.return_value = {
            "data": self.mock_stats_data,
            "min": 100.0,
            "max": 200.0,
            "mean": 150.0
        }

    def tearDown(self):
        """Dismantle all isolation hooks and wipe the matplotlib active window registry clean."""
        self.patch_plots.stop()
        self.patch_compute_stats.stop()
        self.patch_colors.stop()
        self.patch_norm.stop()
        self.patch_formatter.stop()
        self.patch_axis_fmt.stop()
        self.patch_percentages.stop()
        self.patch_cm.stop()
        plt.close('all')

    # =========================================================================
    # MODULE STRUCTURAL TESTS: DATA DISTRIBUTIONS & PLOT CONTEXT
    # =========================================================================

    def test_generate_histogram_happy_path_no_goal(self):
        """Scenario 1: Confirm canvas initializes and renders baseline distribution assets with goal omitted."""
        fig = generate_histogram_from_array(self.mock_simulations, output_name="NetProfit", goal=None)

        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(len(fig.axes), 1)

        ax = fig.axes[0]
        # Check that title layout template bound the variables successfully
        self.assertEqual(ax.get_title(), "Distribution of NetProfit")

        # Verify safe numerical calculation bounds exist on the active axis layout limits
        xlim = ax.get_xlim()
        self.assertFalse(np.isnan(xlim).any())

    def test_generate_histogram_with_goal_bounds(self):
        """Scenario 2: Confirm split logic branch triggers line elements and text annotations."""
        fig = generate_histogram_from_array(self.mock_simulations, output_name="NetProfit", goal=140.0)

        self.assertIsInstance(fig, plt.Figure)
        ax = fig.axes[0]

        # Verify lines are present for both Mean and Goal anchors (at least 2 vertical lines drawn)
        lines = ax.get_lines()
        self.assertTrue(len(lines) >= 2)

        # Confirm target calculation utilities were invoked with the correct goal baseline
        self.mock_percentages.assert_called_once_with(self.mock_stats_data, 140.0)

    def test_generate_histogram_zero_variance_resilience(self):
        """Scenario 3: Verify math boundaries don't cascade crash when historical vectors are uniform."""
        # Force analytical inputs to look completely flat
        flat_data = np.array([50.0, 50.0, 50.0, 50.0])
        self.mock_compute_stats.return_value = {
            "data": flat_data,
            "min": 50.0,
            "max": 50.0,
            "mean": 50.0
        }

        fig = generate_histogram_from_array(self.mock_simulations, output_name="FlatRevenue", goal=None)
        self.assertIsInstance(fig, plt.Figure)

        ax = fig.axes[0]
        # Ensure axis ranges resolved safely to actual numerical coordinates instead of nan bounds
        xlim = ax.get_xlim()
        self.assertFalse(np.isnan(xlim).any())


if __name__ == '__main__':
    unittest.main()
