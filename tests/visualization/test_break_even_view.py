import unittest

import pandas as pd
from IPython.display import HTML

from src.config import variable_names, messages
from src.visualization.styles import break_even_styles
from src.visualization.views.break_even_view import get_break_even_dataframe, render_break_even_dashboard


class TestBreakEvenViewEngineComprehensive(unittest.TestCase):

    def setUp(self):
        """Map out target test schemas using true production dictionary configurations."""
        # Setup standard happy path dataset using real variable_name configuration constants
        self.standard_break_even_input = [
            {
                variable_names.BREAK_EVEN_VARIABLE_NAME: 'Orders',
                variable_names.BREAK_EVEN_FEASIBILITY_STATUS: messages.BREAK_EVEN_FEASIBILITY_ALWAYS_FEASIBLE,
                variable_names.BREAK_EVEN_EXPECTED_VARIABLE_VALUE: 25.0,
                variable_names.BREAK_EVEN_EXPECTED_RESULT: 1263823.52,
                variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE: 20.0,
                variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT: 1263823.52,
                variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE: 0.2
            },
            {
                variable_names.BREAK_EVEN_VARIABLE_NAME: 'SellingPrice',
                variable_names.BREAK_EVEN_FEASIBILITY_STATUS: messages.BREAK_EVEN_FEASIBILITY_STATUS_CROSSOVER,
                variable_names.BREAK_EVEN_EXPECTED_VARIABLE_VALUE: 4500.0,
                variable_names.BREAK_EVEN_EXPECTED_RESULT: 1263823.52,
                variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE: 3000.0,
                variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT: 813823.52,
                variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE: -0.15
            }
        ]

    # =========================================================================
    # 1. DATAFRAME GENERATION LOGIC
    # =========================================================================

    def test_get_break_even_dataframe_happy_path(self):
        """Scenario 1: Confirm array loop processing correctly appends alternating input/output rows."""
        df = get_break_even_dataframe(self.standard_break_even_input, output_name="Net Margin")

        self.assertIsInstance(df, pd.DataFrame)
        # Every element produces exactly 2 visual rows (1 Output Summary + 1 Input Metric)
        # 2 data objects * 2 rows = 4 rows total
        self.assertEqual(len(df), 4)

        # Verify columns match style configuration signatures precisely without mocks
        expected_columns = [
            break_even_styles.SENSITIVITY_VARIABLE,
            break_even_styles.BREAK_EVEN_COLUMN_NAME_BASE,
            break_even_styles.BREAK_EVEN_COLUMN_NAME_THRESHOLD,
            break_even_styles.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN
        ]
        self.assertEqual(list(df.columns), expected_columns)

    def test_get_break_even_dataframe_missing_margin_fallback(self):
        """Scenario 2: Validate fallback to N/A string when safety margin properties are missing."""
        stripped_input = [{
            variable_names.BREAK_EVEN_VARIABLE_NAME: 'CAC',
            variable_names.BREAK_EVEN_EXPECTED_VARIABLE_VALUE: 150.0,
            variable_names.BREAK_EVEN_EXPECTED_RESULT: 50000.0,
            variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE: 220.0,
            variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT: 50000.0
            # variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE key is deliberately omitted
        }]
        df = get_break_even_dataframe(stripped_input, output_name="Net Margin")

        # Index 0 is the metadata placeholder row ("-"). Index 1 is the metric tracking value row -> should show "N/A"
        margin_column_name = break_even_styles.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN
        self.assertEqual(df.iloc[1][margin_column_name], "N/A")

    # =========================================================================
    # 2. HTML DASHBOARD RENDERING LOGIC
    # =========================================================================

    def test_render_break_even_dashboard_html_compilation(self):
        """Scenario 3: Verify template formatter runs cleanly to generate executable HTML components."""
        html_component = render_break_even_dashboard(self.standard_break_even_input, output_name="EBITDA")

        # Verify output matches target display classes without checking layout frames
        self.assertIsInstance(html_component, HTML)

        # Extract underlying HTML string layout tracking signature
        raw_html = html_component._repr_html_()
        self.assertTrue(len(raw_html) > 0)

        # Ensure core matrix values compiled inside the table string cleanly
        self.assertIn("EBITDA", raw_html)
        self.assertIn("Orders", raw_html)
        self.assertIn("SellingPrice", raw_html)

    def test_render_break_even_dashboard_feasibility_branching_paths(self):
        """Scenario 4: Verify style pattern matching handles UNREACHABLE edge flags gracefully."""
        unreachable_input = [{
            variable_names.BREAK_EVEN_VARIABLE_NAME: 'ConversionRate',
            variable_names.BREAK_EVEN_FEASIBILITY_STATUS: messages.BREAK_EVEN_FEASIBILITY_UNREACHABLE,
            variable_names.BREAK_EVEN_EXPECTED_VARIABLE_VALUE: 0.01,
            variable_names.BREAK_EVEN_EXPECTED_RESULT: -12000.0,
            variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE: 0.99,
            variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT: -2000.0,
            variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE: -0.98
        }]

        html_component = render_break_even_dashboard(unreachable_input, output_name="Net Margin")
        raw_html = html_component._repr_html_()

        # Structural presence assertion—verifies compilation without locking onto styling frames
        self.assertTrue(len(raw_html) > 0)
        self.assertIn("ConversionRate", raw_html)


if __name__ == '__main__':
    unittest.main()
