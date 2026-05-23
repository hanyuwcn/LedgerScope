import unittest
from unittest.mock import patch

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Target import rules
from src.visualization.two_way_sensitivity_heatmap_view import generate_heatmap_from_df


class TestTwoWaySensitivityHeatmapViewEngine(unittest.TestCase):

    def setUp(self):
        """Set up standard execution layouts and isolate global style configuration modules."""
        # 1. Setup mock names to match global config modules safely
        self.patch_plots = patch('src.visualization.two_way_sensitivity_heatmap_view.plots')
        self.mock_plots = self.patch_plots.start()

        # Canvas layout structure configuration mappings
        self.mock_plots.HEATMAP_CONTEXT = 'notebook'
        self.mock_plots.FIGURE_SIZE = (8, 6)
        self.mock_plots.ROUNDING_FORMAT = '.2f'
        self.mock_plots.HEATMAP_COLORS = 'viridis'
        self.mock_plots.CBAR_SHRINK_RATIO = 0.8
        self.mock_plots.HEATMAP_TITLE = "Sensitivity of {output} by {factor_1} & {factor_2}"
        self.mock_plots.TITLE_FONT = {'fontsize': 14}
        self.mock_plots.X_AXIS_FONT = {'fontsize': 12}
        self.mock_plots.Y_AXIS_FONT = {'fontsize': 12}
        self.mock_plots.TICK_SIZE = 10
        self.mock_plots.X_AXIS_COLOR = '#222222'
        self.mock_plots.Y_AXIS_COLOR = '#222222'

        # 2. Setup structural baseline Matrix datasets (Happy Path)
        # 3x3 matrix representing cross-over metrics mapping
        self.matrix_data = [
            [100000, 110000, 120000],
            [130000, 140000, 150000],
            [160000, 170000, 180000]
        ]
        self.x_labels = [0.05, 0.10, 0.15]
        self.y_labels = [10, 20, 30]

        self.happy_path_df = pd.DataFrame(
            self.matrix_data,
            index=self.y_labels,
            columns=self.x_labels
        )
        self.happy_path_df.columns.name = "ConversionRate"
        self.happy_path_df.index.name = "TeamSize"

    def tearDown(self):
        """Dismantle visual container frameworks and clear out internal canvas registries."""
        self.patch_plots.stop()
        plt.close('all')

    # =========================================================================
    # MODULE STRUCTURAL TESTS: LAYOUT DATA INTEGRITY
    # =========================================================================

    def test_heatmap_happy_path_execution(self):
        """Scenario 1: Confirm matrix layout successfully transforms into visual heat maps with bound headers."""
        fig = generate_heatmap_from_df(self.happy_path_df, output_name="NetMargin")

        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(len(fig.axes), 2)  # 1 for heatmap content + 1 for colorbar axis scale

        ax = fig.axes[0]
        # Confirm that title formatting templates extracted coordinates smoothly
        self.assertEqual(ax.get_title(), "Sensitivity of NetMargin by ConversionRate & TeamSize")
        self.assertEqual(ax.get_xlabel(), "ConversionRate")
        self.assertEqual(ax.get_ylabel(), "TeamSize")

    def test_heatmap_axis_label_fallbacks(self):
        """Scenario 2: Validate fallback to hardcoded string values when schema name strings are completely blank."""
        anonymous_df = pd.DataFrame(self.matrix_data, index=self.y_labels, columns=self.x_labels)
        anonymous_df.columns.name = None
        anonymous_df.index.name = None

        fig = generate_heatmap_from_df(anonymous_df, output_name="EBITDA")

        self.assertIsInstance(fig, plt.Figure)
        ax = fig.axes[0]

        # Labels should pull straight from style dictionary fallbacks cleanly without crashing
        self.assertTrue(len(ax.get_xlabel()) > 0)
        self.assertTrue(len(ax.get_ylabel()) > 0)

    def test_heatmap_colorbar_alignment(self):
        """Scenario 3: Verify execution tree binds and builds color bar instances accurately."""
        fig = generate_heatmap_from_df(self.happy_path_df, output_name="GrossProfit")

        # Axis 1 represents the embedded color scale engine layout boundary
        cbar_ax = fig.axes[1]
        self.assertFalse(np.isnan(cbar_ax.get_ylim()).any())

    def test_heatmap_empty_dataframe_resilience(self):
        """Scenario 4: Confirm system safely passes zero-length matrix validations or layout exceptions."""
        empty_df = pd.DataFrame()
        empty_df.columns.name = "EmptyX"
        empty_df.index.name = "EmptyY"

        # Seaborn or Matplotlib will raise an error on zero data area rendering passes
        with self.assertRaises((ValueError, IndexError)):
            generate_heatmap_from_df(empty_df, output_name="CrashedOutput")


if __name__ == '__main__':
    unittest.main()
