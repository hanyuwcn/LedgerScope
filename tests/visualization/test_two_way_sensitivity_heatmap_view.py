import unittest

import matplotlib.pyplot as plt
import pandas as pd

from src.visualization.views.two_way_sensitivity_heatmap_view import generate_heatmap_from_df


class TestTwoWaySensitivityHeatmapViewEngine(unittest.TestCase):

    def setUp(self):
        # Using a minimal mock dataframe for faster structural testing
        self.sensitivity_df = pd.DataFrame(
            [[10, 20], [30, 40]],
            index=[1.0, 2.0],
            columns=[0.1, 0.2]
        )
        self.sensitivity_df.index.name = "Variable Y"
        self.sensitivity_df.columns.name = "Variable X"

    def test_generate_heatmap_standalone_mode(self):
        """Confirm standalone compilation returns a Figure."""
        fig = generate_heatmap_from_df(self.sensitivity_df, output_name="Valuation")
        self.assertIsInstance(fig, plt.Figure)
        plt.close(fig)

    def test_generate_heatmap_aggregated_mode(self):
        """Confirm aggregated mode returns None and draws to provided axes."""
        fig, ax = plt.subplots()
        # Mocking formatters to avoid dependency on global config in test
        result = generate_heatmap_from_df(
            self.sensitivity_df,
            output_name="Valuation",
            ax=ax
        )

        self.assertIsNone(result, "Function should return None when ax is provided.")
        # Verify ax now contains a collection (the heatmap image)
        self.assertTrue(len(ax.collections) > 0)
        plt.close(fig)

    def test_generate_heatmap_custom_title(self):
        """Confirm custom title is applied correctly."""
        custom_title = "Sensitivity Surface"
        fig, ax = plt.subplots()
        generate_heatmap_from_df(
            self.sensitivity_df,
            output_name="Valuation",
            ax=ax,
            title=custom_title
        )
        self.assertEqual(ax.get_title(), custom_title)
        plt.close(fig)

    def test_heatmap_empty_df_resilience(self):
        """Verify safety guard processes empty DataFrame gracefully."""
        empty_df = pd.DataFrame()
        fig = generate_heatmap_from_df(empty_df, output_name="Empty")
        self.assertIsInstance(fig, plt.Figure)
        plt.close(fig)


if __name__ == '__main__':
    unittest.main()
