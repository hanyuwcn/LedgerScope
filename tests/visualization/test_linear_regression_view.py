import unittest
from unittest.mock import patch

import matplotlib.pyplot as plt
import numpy as np

# Target import rules
from src.visualization.linear_regression_view import generate_linear_regression_from_lists


class TestLinearRegressionViewEngine(unittest.TestCase):

    def setUp(self):
        """Build isolation patches for shared configuration dependencies and setup test arrays."""
        # 1. Setup mock names to match global config modules safely
        self.patch_plots = patch('src.visualization.linear_regression_view.plots')
        self.mock_plots = self.patch_plots.start()

        # Mock out external configuration line properties used by optional benchmarks
        self.mock_plots.LINE_SETTING_BIGGER = {'color': 'grey', 'linestyle': '--'}
        self.mock_plots.LINE_SETTING_SMALLER = {'color': 'grey', 'linestyle': '-'}

        # 2. Setup baseline test vectors (Happy Path)
        self.standard_x = [10.0, 20.0, 30.0, 40.0, 50.0]
        self.standard_y = [100.0, 150.0, 190.0, 240.0, 310.0]

    def tearDown(self):
        """Dismantle active runtime isolation hooks and drop background matplotlib frames."""
        self.patch_plots.stop()
        plt.close('all')

    # =========================================================================
    # MODULE STRUCTURAL TESTS: EXECUTION & BOUNDARY SCENARIOS
    # =========================================================================

    def test_regression_happy_path_execution(self):
        """Scenario 1: Verify canvas renders fully with zero exceptions under typical data distributions."""
        fig = generate_linear_regression_from_lists(
            self.standard_x,
            self.standard_y,
            x_label="MarketingSpend",
            y_label="GrossRevenue",
            x_benchmark=30.0,
            y_benchmark=200.0
        )

        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(len(fig.axes), 1)

        ax = fig.axes[0]
        # Verify safe numerical layout coordinates exist on the active axis
        self.assertFalse(np.isnan(ax.get_xlim()).any())
        self.assertFalse(np.isnan(ax.get_ylim()).any())

    def test_regression_zero_variance_x_axis(self):
        """Scenario 2: Validate that scipy safely rejects zero-variance X inputs before linspace evaluation."""
        flat_x = [5.0, 5.0, 5.0, 5.0, 5.0]

        # Scipy's linregress strictly prohibits completely identical X values
        with self.assertRaises(ValueError) as context:
            generate_linear_regression_from_lists(
                flat_x,
                self.standard_y,
                x_label="FixedCost",
                y_label="NetProfit"
            )

        self.assertIn("Cannot calculate a linear regression if all x values are identical", str(context.exception))

    def test_regression_zero_variance_y_axis(self):
        """Scenario 3: Validate point size normalization normalization when the Y vector values are identical."""
        flat_y = [10.0, 10.0, 10.0, 10.0, 10.0]

        fig = generate_linear_regression_from_lists(
            self.standard_x,
            flat_y,
            x_label="ConversionRate",
            y_label="FixedKPI"
        )

        self.assertIsInstance(fig, plt.Figure)
        ax = fig.axes[0]

        # Verify that the canvas bounds are structured and stable
        ylim = ax.get_ylim()
        self.assertFalse(np.isnan(ylim).any())

    def test_regression_missing_benchmarks_pass(self):
        """Scenario 4: Verify engine processes safely when benchmark layers evaluate as None."""
        fig = generate_linear_regression_from_lists(
            self.standard_x,
            self.standard_y,
            x_label="Leads",
            y_label="DealsClosed",
            x_benchmark=None,
            y_benchmark=None
        )

        self.assertIsInstance(fig, plt.Figure)
        ax = fig.axes[0]

        # Verify that omission leaves only the core regression line (no benchmark axlines rendered)
        # 1 line = the regression trend line
        self.assertEqual(len(ax.get_lines()), 1)

    def test_regression_mismatched_vector_lengths(self):
        """Scenario 5: Check that mismatched dimensions crash cleanly at initialization inside scipy."""
        broken_x = [10.0, 20.0]

        # Scipy stats package expects matching lengths and will throw a ValueError
        with self.assertRaises(ValueError):
            generate_linear_regression_from_lists(
                broken_x,
                self.standard_y,
                x_label="BrokenX",
                y_label="TargetY"
            )


if __name__ == '__main__':
    unittest.main()
