import unittest

import matplotlib.pyplot as plt

from src.visualization.views.linear_regression_view import generate_linear_regression_from_lists


class TestLinearRegressionViewEngine(unittest.TestCase):

    def setUp(self):
        """Standardize fixture using the core fiscal pipeline."""
        self.x_dist = [94223.7063, 83651.3576, 88117.9116, 89414.051, 114132.4516, 112890.3501, 88381.4365, 80572.3809,
                       91160.0967, 110766.8755, 99221.0998, 89850.2327, 99733.7687, 101218.1183, 101187.2687,
                       94022.9477, 103445.974, 101352.8869, 88002.434, 92501.2349]
        self.y_dist = [5205475.8048, 4190530.3296000003, 4619319.513600001, 4743748.896000001, 7116715.3536,
                       6997473.6096, 4644617.903999999, 3894948.5664000004, 4911369.2831999995, 6793620.0479999995,
                       5685225.5808, 4785622.339199999, 5734441.7952, 5876939.3568, 5873977.7952, 5186202.9792,
                       6090813.504000001, 5889877.1424, 4608233.663999999, 5040118.5504]

    # =========================================================================
    # MODULE STRUCTURAL TESTS: REGRESSION PLOT COMPILATION
    # =========================================================================

    def test_generate_regression_plot_happy_path(self):
        fig = generate_linear_regression_from_lists(
            self.x_dist, self.y_dist, "Rev", "Price",
            x_benchmark=100000.0, y_benchmark=5760000.0
        )
        self.assertIsInstance(fig, plt.Figure)
        plt.close(fig)

    def test_generate_regression_plot_no_benchmarks(self):
        fig = generate_linear_regression_from_lists(self.x_dist, self.y_dist, "Rev", "Price")
        ax = fig.axes[0]
        self.assertEqual(len(ax.get_legend().get_texts()), 1)
        plt.close(fig)

    def test_generate_regression_plot_viewport_extension(self):
        out_of_bounds = 200000.0
        fig = generate_linear_regression_from_lists(
            self.x_dist, self.y_dist, "Rev", "Price", x_benchmark=out_of_bounds
        )
        ax = fig.axes[0]
        self.assertTrue(ax.get_xlim()[1] >= out_of_bounds)
        plt.close(fig)

    def test_generate_regression_aggregated_mode(self):
        """Confirm aggregated mode returns None and draws to provided axes."""
        fig, ax = plt.subplots()
        result = generate_linear_regression_from_lists(
            self.x_dist, self.y_dist, "Rev", "Price", ax=ax
        )
        self.assertIsNone(result, "Function should return None when ax is provided.")
        # Verify ax contains plots (scatter + line)
        self.assertTrue(len(ax.lines) > 0 or len(ax.collections) > 0)
        plt.close(fig)

    def test_generate_regression_custom_title(self):
        """Confirm title argument is correctly applied to the axes."""
        custom_title = "Revenue Sensitivity Analysis"
        _, ax = plt.subplots()
        generate_linear_regression_from_lists(
            self.x_dist, self.y_dist, "Rev", "Price", ax=ax, title=custom_title
        )
        self.assertEqual(ax.get_title(), custom_title)
        plt.close()


if __name__ == '__main__':
    unittest.main()
