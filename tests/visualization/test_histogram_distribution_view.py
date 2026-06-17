import unittest

import matplotlib.pyplot as plt

from src.visualization import generate_histogram_from_array


class TestHistogramDistributionViewEngine(unittest.TestCase):

    def setUp(self):
        """Standardize fixture using the simplified market price dataset."""
        self.simulation_data = [
            {'MarketPrice': 5108052}, {'MarketPrice': 5960690}, {'MarketPrice': 6970990},
            {'MarketPrice': 4489177}, {'MarketPrice': 7062903}, {'MarketPrice': 5508399},
            {'MarketPrice': 3917523}, {'MarketPrice': 5689128}, {'MarketPrice': 5425780},
            {'MarketPrice': 4409374}
        ]
        # Use the string directly or constant if imported
        self.output_key = 'MarketPrice'

    def test_generate_histogram_title_application(self):
        """Confirm that the optional title argument is correctly applied to the axes."""
        custom_title = "Custom Market Price Projection"

        # Test with aggregated mode to verify title application on provided ax
        _, ax = plt.subplots()
        generate_histogram_from_array(
            self.simulation_data,
            self.output_key,
            title=custom_title,
            ax=ax
        )

        self.assertEqual(ax.get_title(), custom_title)
        plt.close()

    # =========================================================================
    # MODULE STRUCTURAL TESTS
    # =========================================================================

    def test_generate_histogram_standalone_mode(self):
        fig = generate_histogram_from_array(self.simulation_data, self.output_key, goal=5760000.0)
        self.assertIsInstance(fig, plt.Figure)
        plt.close(fig)

    def test_generate_histogram_aggregated_mode(self):
        fig, ax = plt.subplots()
        result = generate_histogram_from_array(self.simulation_data, self.output_key, goal=5760000.0, ax=ax)
        self.assertIsNone(result)
        legend = ax.get_legend()
        self.assertIsNotNone(legend)
        self.assertEqual(len(legend.get_texts()), 2)
        plt.close(fig)

    def test_generate_histogram_zero_variance_resilience(self):
        deterministic_data = [{self.output_key: 5000000.0} for _ in range(10)]
        fig = generate_histogram_from_array(deterministic_data, self.output_key)
        self.assertIsNotNone(fig)
        plt.close(fig)


if __name__ == '__main__':
    unittest.main()
