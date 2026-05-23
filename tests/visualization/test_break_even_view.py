import unittest
from unittest.mock import patch

import pandas as pd
from IPython.display import HTML

# Target import rules
from src.visualization.break_even_view import get_break_even_dataframe, render_break_even_dashboard


class TestBreakEvenViewEngine(unittest.TestCase):

    def setUp(self):
        """Build isolation patches for configurations and map out target test schemas."""
        # 1. Setup mock names to match config dependencies safely
        self.patch_plots = patch('src.visualization.break_even_view.plots')
        self.mock_plots = self.patch_plots.start()

        # Stand-in string headers for the metrics layout matrix
        self.mock_plots.SENSITIVITY_VARIABLE = "Metric/Variable"
        self.mock_plots.BREAK_EVEN_COLUMN_NAME_BASE = "Baseline Value"
        self.mock_plots.BREAK_EVEN_COLUMN_NAME_THRESHOLD = "Crossover Point"
        self.mock_plots.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN = "Safety Runway"

        # Patch variable dictionary strings inside break_even views to decouple execution
        self.patch_be_vars = patch('src.visualization.break_even_view.variable_names')
        self.mock_be_vars = self.patch_be_vars.start()
        self.mock_be_vars.BREAK_EVEN_EXPECTED_RESULT = 'BreakEvenExpectedResult'
        self.mock_be_vars.BREAK_EVEN_POINT_THRESHOLD_RESULT = 'ThresholdResult'
        self.mock_be_vars.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE = 'SafetyMarginPercentage'
        self.mock_be_vars.BREAK_EVEN_VARIABLE_NAME = 'BreakEvenVariable'
        self.mock_be_vars.BREAK_EVEN_EXPECTED_VARIABLE_VALUE = 'BreakEvenExpectedVariableValue'
        self.mock_be_vars.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE = 'ThresholdVariableValue'

        # 2. Setup standard happy path dataset for execution runs
        self.standard_break_even_input = [
            {
                'BreakEvenVariable': 'Orders',
                'feasibility_status': 'ALWAYS_FEASIBLE',
                'BreakEvenExpectedVariableValue': 25.0,
                'BreakEvenExpectedResult': 1263823.52,
                'ThresholdVariableValue': 20.0,
                'ThresholdResult': 1263823.52,
                'SafetyMarginPercentage': 0.2
            },
            {
                'BreakEvenVariable': 'SellingPrice',
                'feasibility_status': 'CROSSOVER_FOUND',
                'BreakEvenExpectedVariableValue': 4500.0,
                'BreakEvenExpectedResult': 1263823.52,
                'ThresholdVariableValue': 3000.0,
                'ThresholdResult': 813823.52,
                'SafetyMarginPercentage': -0.15
            }
        ]

    def tearDown(self):
        """Dismantle background isolation wrappers safely."""
        self.patch_plots.stop()
        self.patch_be_vars.stop()

    # =========================================================================
    # MODULE STRUCTURAL TESTS: DATAFRAME GENERATION
    # =========================================================================

    def test_get_break_even_dataframe_happy_path(self):
        """Scenario 1: Confirm array loop processing correctly appends alternating input/output rows."""
        df = get_break_even_dataframe(self.standard_break_even_input, output_name="Net Margin")

        self.assertIsInstance(df, pd.DataFrame)
        # Every element produces exactly 2 visual rows (1 Output Summary + 1 Input Metric)
        # 2 elements * 2 rows = 4 rows total
        self.assertEqual(len(df), 4)

        # Verify columns line up with mock constants precisely
        expected_columns = [
            self.mock_plots.SENSITIVITY_VARIABLE,
            self.mock_plots.BREAK_EVEN_COLUMN_NAME_BASE,
            self.mock_plots.BREAK_EVEN_COLUMN_NAME_THRESHOLD,
            self.mock_plots.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN
        ]
        self.assertEqual(list(df.columns), expected_columns)

    def test_get_break_even_dataframe_missing_margin_fallback(self):
        """Scenario 2: Validate fallback to N/A string when safety margin properties are missing."""
        stripped_input = [{
            'BreakEvenVariable': 'CAC',
            'BreakEvenExpectedVariableValue': 150.0,
            'BreakEvenExpectedResult': 50000.0,
            'ThresholdVariableValue': 220.0,
            'ThresholdResult': 50000.0
            # 'SafetyMarginPercentage' key is deliberately omitted
        }]
        df = get_break_even_dataframe(stripped_input, output_name="Net Margin")

        # Index 0 is the output metadata row ("-"), Index 1 is the input row which should show "N/A"
        margin_column_name = self.mock_plots.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN
        self.assertEqual(df.iloc[1][margin_column_name], "N/A")

    # =========================================================================
    # MODULE STRUCTURAL TESTS: HTML DASHBOARD RENDERING
    # =========================================================================

    def test_render_break_even_dashboard_html_compilation(self):
        """Scenario 3: Verify template formatter runs cleanly to generate executable HTML objects."""
        html_component = render_break_even_dashboard(self.standard_break_even_input, output_name="EBITDA")

        self.assertIsInstance(html_component, HTML)

        # Extract underlying HTML raw string layout definition
        raw_html = html_component._repr_html_()
        self.assertTrue(len(raw_html) > 0)

        # Structural presence assertions instead of cosmetic validation
        self.assertIn("EBITDA", raw_html)
        self.assertIn("Orders", raw_html)
        self.assertIn("SellingPrice", raw_html)

    def test_render_break_even_dashboard_feasibility_branching_paths(self):
        """Scenario 4: Verify variable dictionary branch selection handles 'UNREACHABLE' edge flags safely."""
        unreachable_input = [{
            'BreakEvenVariable': 'ConversionRate',
            'feasibility_status': 'UNREACHABLE',
            'BreakEvenExpectedVariableValue': 0.01,
            'BreakEvenExpectedResult': -12000.0,
            'ThresholdVariableValue': 0.99,
            'ThresholdResult': -2000.0,
            'SafetyMarginPercentage': -0.98
        }]

        html_component = render_break_even_dashboard(unreachable_input, output_name="Net Margin")
        raw_html = html_component._repr_html_()

        # Ensure template engine mapped variables correctly into formatting strings
        self.assertTrue(len(raw_html) > 0)
        self.assertIn("ConversionRate", raw_html)


if __name__ == '__main__':
    unittest.main()
