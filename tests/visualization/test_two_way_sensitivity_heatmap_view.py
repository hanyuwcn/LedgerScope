import unittest

import matplotlib.pyplot as plt
import pandas as pd

from src.visualization.views.two_way_sensitivity_heatmap_view import generate_heatmap_from_df


class TestTwoWaySensitivityHeatmapViewEngine(unittest.TestCase):

    def setUp(self):
        """Build standard mock DataFrames capturing varying pricing matrices."""
        # 3x3 mock sensitivity representation array grid
        matrix_data = [
            [10000.0, 12000.0, 14000.0],
            [11000.0, 13000.0, 15000.0],
            [12000.0, 14000.0, 16000.0]
        ]

        self.df = pd.DataFrame(
            matrix_data,
            index=[0.05, 0.10, 0.15],
            columns=[10, 20, 30]
        )
        self.df.columns.name = "ConversionRate"
        self.df.index.name = "FixedKPI"

        self.output_key = "NetProfit"

    def test_generate_heatmap_happy_path(self):
        """Scenario 1: Confirm heatmap generation builds valid figures and parses index strings accurately."""
        fig = generate_heatmap_from_df(self.df, output_name=self.output_key)

        self.assertIsInstance(fig, plt.Figure)
        self.assertTrue(len(fig.axes) > 0)

        ax = fig.axes[0]

        # Verify labels extract cleanly from axis configurations
        self.assertEqual(ax.get_xlabel(), "ConversionRate")
        self.assertEqual(ax.get_ylabel(), "FixedKPI")

        plt.close(fig)


if __name__ == '__main__':
    unittest.main()
