import unittest
import numpy as np
import pandas as pd
from IPython.display import HTML

from src.config import variable_names
from src.visualization.styles import comparative_statics_styles
from src.visualization.views.comparative_statics_view import (
    get_comparative_statics_dataframe,
    render_comparative_statics_dashboard
)


class TestComparativeStaticsViewEngineComprehensive(unittest.TestCase):

    def setUp(self):
        """Map out target test schemas using true production dictionary configurations."""
        # Setup standard dataset capturing multiple elasticity behaviors (+ / -) using real configuration constants
        self.standard_comparative_statics_input = [
            {
                variable_names.COMPARATIVE_STATICS_VARIABLE_NAME: 'ConversionRate',
                variable_names.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE: 0.02,
                variable_names.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE: 0.03,
                variable_names.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE: 0.04,
                variable_names.COMPARATIVE_STATICS_MIN_RESULT: 80000.0,
                variable_names.COMPARATIVE_STATICS_EXPECTED_RESULT: 120000.0,
                variable_names.COMPARATIVE_STATICS_MAX_RESULT: 160000.0,
                variable_names.COMPARATIVE_STATICS_ELASTICITY: 1.25  # Positive elasticity path
            },
            {
                variable_names.COMPARATIVE_STATICS_VARIABLE_NAME: 'ChurnRate',
                variable_names.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE: 0.01,
                variable_names.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE: 0.02,
                variable_names.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE: 0.03,
                variable_names.COMPARATIVE_STATICS_MIN_RESULT: 140000.0,
                variable_names.COMPARATIVE_STATICS_EXPECTED_RESULT: 120000.0,
                variable_names.COMPARATIVE_STATICS_MAX_RESULT: 95000.0,
                variable_names.COMPARATIVE_STATICS_ELASTICITY: -0.45  # Negative elasticity path
            }
        ]

    # =========================================================================
    # 1. DATAFRAME GENERATION LOGIC
    # =========================================================================

    def test_get_comparative_statics_dataframe_happy_path(self):
        """Scenario 1: Confirm matrix array loops cleanly to yield nested row layouts."""
        df = get_comparative_statics_dataframe(self.standard_comparative_statics_input, output_name="Net Value")

        self.assertIsInstance(df, pd.DataFrame)
        # 2 input metrics * 2 structural rows per item (Output Row + Input Factor Row) = 4 rows total
        self.assertEqual(len(df), 4)

        # Confirm columns align directly to true architectural style variables
        expected_columns = [
            comparative_statics_styles.SENSITIVITY_VARIABLE,
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MIN,
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_BASE,
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MAX,
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY
        ]
        self.assertEqual(list(df.columns), expected_columns)

    def test_get_comparative_statics_dataframe_row_values(self):
        """Scenario 2: Verify specific structure blocks where Output rows suppress elasticity figures."""
        df = get_comparative_statics_dataframe(self.standard_comparative_statics_input, output_name="Net Value")

        elasticity_col = comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY

        # Row index 0 belongs to Output (Results) - verify it is a missing/None element
        # (Pandas turns None into a floating-point NaN or None depending on type tracking)
        self.assertTrue(pd.isna(df.iloc[0][elasticity_col]))

        # Row index 1 belongs to the Input factor (ConversionRate) - must match assigned metric value
        self.assertEqual(df.iloc[1][elasticity_col], 1.25)

    # =========================================================================
    # 2. HTML DASHBOARD RENDERING LOGIC
    # =========================================================================

    def test_render_comparative_statics_dashboard_html_compilation(self):
        """Scenario 3: Verify the table element compiles into display containers without structural crashes."""
        html_component = render_comparative_statics_dashboard(
            self.standard_comparative_statics_input, output_name="Gross Income"
        )

        self.assertIsInstance(html_component, HTML)

        raw_html = html_component._repr_html_()
        self.assertTrue(len(raw_html) > 0)

        # Confirm raw inputs and labels were injected cleanly into the markup data
        self.assertIn("Gross Income", raw_html)
        self.assertIn("ConversionRate", raw_html)
        self.assertIn("ChurnRate", raw_html)

    def test_render_comparative_statics_dashboard_elasticity_branching(self):
        """Scenario 4: Verify positive, negative, and safe non-float fallbacks handle class mappings."""
        edge_case_input = [
            {
                variable_names.COMPARATIVE_STATICS_VARIABLE_NAME: 'FixedOverhead',
                variable_names.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE: 100,
                variable_names.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE: 100,
                variable_names.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE: 100,
                variable_names.COMPARATIVE_STATICS_MIN_RESULT: 500,
                variable_names.COMPARATIVE_STATICS_EXPECTED_RESULT: 500,
                variable_names.COMPARATIVE_STATICS_MAX_RESULT: 500,
                variable_names.COMPARATIVE_STATICS_ELASTICITY: 'INVALID_STR_OR_NONE'  # String crash resilience test
            }
        ]

        raw_html_standard = render_comparative_statics_dashboard(
            self.standard_comparative_statics_input, output_name="Test"
        )._repr_html_()

        raw_html_edge = render_comparative_statics_dashboard(
            edge_case_input, output_name="Test"
        )._repr_html_()

        # Positive elasticity check
        self.assertIn("elasticity-positive", raw_html_standard)
        self.assertIn("+1.25", raw_html_standard)

        # Negative elasticity check
        self.assertIn("elasticity-negative", raw_html_standard)
        self.assertIn("-0.45", raw_html_standard)

        # Fallback string test - should be caught gracefully and formatted as structural 0.00 base line
        self.assertIn("0.00", raw_html_edge)


if __name__ == '__main__':
    unittest.main()
