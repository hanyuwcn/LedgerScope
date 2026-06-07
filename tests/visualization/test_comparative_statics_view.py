import unittest

import pandas as pd
from pandas.io.formats.style import Styler

from src.config import variable_names
from src.visualization.styles import comparative_statics_styles as cs_style
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
            cs_style.SENSITIVITY_VARIABLE,
            cs_style.COMPARATIVE_STATICS_COLUMN_NAME_MIN,
            cs_style.COMPARATIVE_STATICS_COLUMN_NAME_BASE,
            cs_style.COMPARATIVE_STATICS_COLUMN_NAME_MAX,
            cs_style.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY
        ]
        self.assertEqual(list(df.columns), expected_columns)

    def test_get_comparative_statics_dataframe_row_values(self):
        """Scenario 2: Verify specific structure blocks where Output rows suppress elasticity figures."""
        df = get_comparative_statics_dataframe(self.standard_comparative_statics_input, output_name="Net Value")

        elasticity_col = cs_style.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY

        # Row index 0 belongs to Output (Results) - verify it is an empty or missing element
        self.assertTrue(pd.isna(df.iloc[0][elasticity_col]))

        # Row index 1 belongs to the Input factor (ConversionRate) - must match assigned metric value
        self.assertEqual(df.iloc[1][elasticity_col], 1.25)

    # =========================================================================
    # 2. PANDAS STYLER DASHBOARD RENDERING LOGIC
    # =========================================================================

    def test_render_comparative_statics_dashboard_styler_compilation(self):
        """Scenario 3: Verify the dashboard compiles into a Pandas Styler object without structural crashes."""
        styler_component = render_comparative_statics_dashboard(
            self.standard_comparative_statics_input, output_name="Gross Income"
        )

        # Assert it returns the modern Styler pipeline instead of raw HTML class wrapper
        self.assertIsInstance(styler_component, Styler)

        # Render layout to raw markup validation string
        raw_html = styler_component.to_html()
        self.assertTrue(len(raw_html) > 0)

        # Confirm raw inputs and labels were processed cleanly into output structures
        self.assertIn("Gross Income", raw_html)
        self.assertIn("ConversionRate", raw_html)
        self.assertIn("ChurnRate", raw_html)

    def test_render_comparative_statics_dashboard_elasticity_branching(self):
        """Scenario 4: Verify positive, negative, and safe non-float fallbacks handle output string generation."""
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
        ).to_html()

        raw_html_edge = render_comparative_statics_dashboard(
            edge_case_input, output_name="Test"
        ).to_html()

        # Positive elasticity check - verifies custom layout token string format logic (+ sign)
        self.assertIn("+1.25", raw_html_standard)

        # Negative elasticity check - verifies regular negative sign persistence
        self.assertIn("-0.45", raw_html_standard)

        # Fallback string test - because we added type safeguards to `apply_elasticity_formatting`,
        # invalid values are bypassed and filled as blank strings via `fillna("")` without throwing an error.
        self.assertIn('FixedOverhead', raw_html_edge)


if __name__ == '__main__':
    unittest.main()
