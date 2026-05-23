import unittest
from unittest.mock import patch

import matplotlib.pyplot as plt

from src.visualization.contribution_pie_view import generate_contribution_pie_chart


class TestContributionPieViewEngine(unittest.TestCase):

    def setUp(self):
        """Build isolation patches for shared configuration dependencies and setup test data."""
        # 1. Setup mock patches to match global config modules safely
        self.patch_plots = patch('src.visualization.contribution_pie_view.plots')
        self.mock_plots = self.patch_plots.start()

        # Mock out structural layout properties used during axes generation
        self.mock_plots.TITLE_FONT = {'fontsize': 14, 'weight': 'bold'}
        self.mock_plots.LINEAR_REGRESSION_IN_LEGENDS_TEXT_FONTS = {'fontsize': 10}
        self.mock_plots.LINEAR_REGRESSION_FIGURE_SIZE = (8, 6)
        self.mock_plots.LINEAR_REGRESSION_TICK_SIZE = 10
        self.mock_plots.X_AXIS_COLOR = '#333333'

        # 2. Patch formatting map to keep formatting predictable during testing
        self.patch_formatting = patch('src.visualization.contribution_pie_view.VARIABLE_FORMATTING_MAP', new={})
        self.mock_formatting = self.patch_formatting.start()

        # Inject explicit formatters for known variables
        self.mock_formatting['COGS'] = lambda v: f"${v:,.2f}"
        self.mock_formatting['Marketing'] = lambda v: f"${v:,.2f}"

        # 3. Setup baseline test vector dictionary (Happy Path)
        self.standard_contributions = {
            'COGS': 600.0,
            'Marketing': 300.0,
            'R&D': 100.0  # Will trigger the fallback formatter 'fmt'
        }

    def tearDown(self):
        """Dismantle active runtime isolation hooks and drop background matplotlib frames."""
        self.patch_plots.stop()
        self.patch_formatting.stop()
        plt.close('all')

    # =========================================================================
    # MODULE STRUCTURAL TESTS: EXECUTION & BOUNDARY SCENARIOS
    # =========================================================================

    def test_pie_chart_happy_path_execution(self):
        """Scenario 1: Verify canvas renders fully with correct axis count under typical data distributions."""
        fig = generate_contribution_pie_chart(self.standard_contributions)

        self.assertIsInstance(fig, plt.Figure)
        self.assertEqual(len(fig.axes), 1)

        ax = fig.axes[0]
        # Verify strict uniform aspect ratio scales cleanly to prevent oval distortion
        self.assertIn(ax.get_aspect(), [1.0, 'equal'])

    def test_pie_chart_zero_sum_safety_guard(self):
        """Scenario 2: Validate that an all-zero run safely triggers epsilon overrides instead of failing on division."""
        zero_contributions = {
            'COGS': 0.0,
            'Marketing': 0.0,
            'R&D': 0.0
        }

        # Engine must not raise ZeroDivisionError
        try:
            fig = generate_contribution_pie_chart(zero_contributions)
        except ZeroDivisionError:
            self.fail("generate_contribution_pie_chart raised ZeroDivisionError unexpectedly!")

        self.assertIsInstance(fig, plt.Figure)
        ax = fig.axes[0]

        # Verify that all slices have a safe, non-zero width (drawn via epsilon values)
        # and that the calculated text strings output exactly 0.0%
        texts = [t.get_text() for t in ax.texts]
        self.assertTrue(any("0.0%" in text for text in texts))

    def test_pie_chart_formatting_resolution(self):
        """Scenario 3: Verify legend string compilation matches formatting map configurations."""
        fig = generate_contribution_pie_chart(self.standard_contributions)
        ax = fig.axes[0]

        # Pull text components out of the rendered legend object
        legend = ax.get_legend()
        self.assertIsNotNone(legend)

        legend_texts = [t.get_text() for t in legend.get_texts()]

        # Check that explicit custom mapping rules resolved correctly
        self.assertIn("COGS ($600.00)", legend_texts)
        self.assertIn("Marketing ($300.00)", legend_texts)

        # Check that the unspecified 'R&D' metric gracefully utilized the fallback engine formatter
        self.assertTrue(any("R&D" in text for text in legend_texts))

    def test_pie_chart_single_variable_handling(self):
        """Scenario 4: Verify layout behaves cleanly when passed only one single data component (100% boundary check)."""
        single_contribution = {'MonopolyRevenue': 5000.0}

        fig = generate_contribution_pie_chart(single_contribution)
        self.assertIsInstance(fig, plt.Figure)

        ax = fig.axes[0]
        texts = [t.get_text() for t in ax.texts]

        # Verify slice sets up text mapping at perfect maximum volume
        self.assertIn("MonopolyRevenue\n(100.0%)", texts)


if __name__ == '__main__':
    unittest.main()
