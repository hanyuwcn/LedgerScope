import unittest

import matplotlib.pyplot as plt

from src.visualization.views.histogram_distribution_view import generate_histogram_from_array


class TestHistogramDistributionViewEngine(unittest.TestCase):

    def setUp(self):
        """Map out structured inputs mimicking active simulation array tracking logs."""
        self.output_key = "NetRevenue"
        self.standard_simulations = [
            {"NetRevenue": 10000.0}, {"NetRevenue": 12000.0},
            {"NetRevenue": 15000.0}, {"NetRevenue": 9000.0},
            {"NetRevenue": 11500.0}
        ]
        # Edge case: No data variance (all simulation outputs land on exact same value)
        self.flat_simulations = [
            {"NetRevenue": 5000.0}, {"NetRevenue": 5000.0}, {"NetRevenue": 5000.0}
        ]

    def test_generate_histogram_happy_path_with_goal(self):
        """Scenario 1: Verify canvas generation builds valid reference labels and annotations when a goal is set."""
        fig = generate_histogram_from_array(self.standard_simulations, self.output_key, goal=11000)

        self.assertIsInstance(fig, plt.Figure)
        self.assertTrue(len(fig.axes) > 0)

        ax = fig.axes[0]
        legend = ax.get_legend()
        self.assertIsNotNone(legend)

        # Expecting 2 lines in the legend layout: Benchmark Goal line and Simulations Mean line
        self.assertEqual(len(legend.get_texts()), 2)
        plt.close(fig)

    def test_generate_histogram_without_goal(self):
        """Scenario 2: Verify chart limits labels down to just the Mean reference line when goal is omitted."""
        fig = generate_histogram_from_array(self.standard_simulations, self.output_key, goal=None)

        ax = fig.axes[0]
        legend = ax.get_legend()

        # Without a threshold target, only the simulation mean metric should appear in the legend card
        self.assertEqual(len(legend.get_texts()), 1)
        plt.close(fig)

    def test_generate_histogram_zero_variance_resilience(self):
        """Scenario 3: Verify the system normalizes flat, zero-variance outputs without crashing."""
        try:
            fig = generate_histogram_from_array(self.flat_simulations, self.output_key, goal=5000)
            executed_safely = True
        except ValueError:
            executed_safely = False

        self.assertTrue(executed_safely, "Histogram engine crashed on zero-variance gradient inputs.")
        plt.close(fig)


if __name__ == '__main__':
    unittest.main()
