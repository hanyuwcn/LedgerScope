import unittest

import matplotlib.pyplot as plt
import pandas as pd

from src.analysis import run_two_way_sensitivity_analysis
from src.config import variable_names
from src.core import Variable
from src.models import NetIncomeModel, MarketPriceModel
from src.variables import PriceToEarningsRatio
from src.visualization.views.two_way_sensitivity_heatmap_view import generate_heatmap_from_df


class TestTwoWaySensitivityHeatmapViewEngine(unittest.TestCase):

    def setUp(self):
        """Standardize fixture using the core fiscal pipeline."""
        self.pipeline = [NetIncomeModel(), MarketPriceModel()]

        self.variables = {
            variable_names.REVENUE: Variable(min=80000.0, exp=100000.0, max=120000.0),
            variable_names.COST: Variable(min=30000.0, exp=40000.0, max=50000.0),
            variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
        }

        # Generate production-ready sensitivity matrix
        self.sensitivity_df = run_two_way_sensitivity_analysis(
            variables=self.variables,
            param_x_name=variable_names.REVENUE,
            param_y_name=variable_names.COST,
            model_pipeline=self.pipeline,
            target_output_name=variable_names.MARKET_PRICE,
            x_steps=3,
            y_steps=3
        )

    def test_generate_heatmap_happy_path(self):
        """Confirm heatmap generates correctly using real engine-derived fiscal data."""
        fig = generate_heatmap_from_df(self.sensitivity_df, output_name="Market Valuation")

        self.assertIsInstance(fig, plt.Figure)
        self.assertTrue(len(fig.axes) > 0)

        ax = fig.axes[0]

        # Verify labels match the fiscal variable configuration names
        self.assertEqual(ax.get_xlabel(), variable_names.REVENUE)
        self.assertEqual(ax.get_ylabel(), variable_names.COST)

        plt.close(fig)

    def test_heatmap_empty_df_resilience(self):
        """Verify safety guard: heatmaps should not crash on an empty DataFrame."""
        empty_df = pd.DataFrame()
        try:
            fig = generate_heatmap_from_df(empty_df, output_name="Empty")
            plt.close(fig)
            success = True
        except Exception:
            success = False

        self.assertTrue(success, "Heatmap engine crashed on empty DataFrame input.")


if __name__ == '__main__':
    unittest.main()
