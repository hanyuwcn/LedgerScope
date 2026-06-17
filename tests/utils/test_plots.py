import unittest

import matplotlib.pyplot as plt

from src.utils import plot_multiple_views
from src.visualization import generate_histogram_from_array


class TestReportOrchestrator(unittest.TestCase):

    def setUp(self):
        self.simulation_data = [{'MarketPrice': 5108052}, {'MarketPrice': 5960690}]
        self.output_key = 'MarketPrice'

    def test_plot_multiple_views_structure(self):
        """Confirm the orchestrator creates the correct number of axes."""
        # Create a list of 2 recipes (histograms)
        plot_functions = [
            lambda ax: generate_histogram_from_array(self.simulation_data, self.output_key, ax=ax),
            lambda ax: generate_histogram_from_array(self.simulation_data, self.output_key, ax=ax)
        ]

        fig = plot_multiple_views(plot_functions)

        # Verify the figure exists and has exactly 2 subplots
        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(len(fig.axes), 2)

        plt.close(fig)

    def test_plot_multiple_views_single_plot(self):
        """Ensure it handles a single function without crashing."""
        plot_functions = [
            lambda ax: generate_histogram_from_array(self.simulation_data, self.output_key, ax=ax)
        ]

        fig = plot_multiple_views(plot_functions)
        self.assertEqual(len(fig.axes), 1)

        plt.close(fig)

    def test_plot_multiple_views_figsize_logic(self):
        """Verify the dynamic figsize calculation."""
        plot_functions = [lambda ax: ax.plot([1], [1])] * 3

        # Default behavior: (base_w * 3, base_h)
        fig = plot_multiple_views(plot_functions)
        w, h = fig.get_size_inches()

        # Using 15 (base_w) as per your histogram_distribution_styles
        self.assertAlmostEqual(w, 45.0)
        plt.close(fig)


if __name__ == '__main__':
    unittest.main()
