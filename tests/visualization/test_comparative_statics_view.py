import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from IPython.display import HTML

# Target import rules
from src.visualization.comparative_statics_view import (
    get_comparative_statics_dataframe,
    render_comparative_statics_dashboard
)


class TestComparativeStaticsViewEngine(unittest.TestCase):

    def setUp(self):
        """Build isolation patches for configurations and map out target test schemas."""
        # 1. Setup mock column/plot name mappings safely
        self.patch_plots = patch('src.visualization.comparative_statics_view.plots')
        self.mock_plots = self.patch_plots.start()

        self.mock_plots.SENSITIVITY_VARIABLE = "Metric/Variable"
        self.mock_plots.COMPARATIVE_STATICS_COLUMN_NAME_MIN = "Min Scenario"
        self.mock_plots.COMPARATIVE_STATICS_COLUMN_NAME_BASE = "Baseline Scenario"
        self.mock_plots.COMPARATIVE_STATICS_COLUMN_NAME_MAX = "Max Scenario"
        self.mock_plots.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY = "Sensitivity Elasticity"

        # Patch variable mapping keys to decouple from real data models
        self.patch_cs_vars = patch('src.visualization.comparative_statics_view.variable_names')
        self.mock_cs_vars = self.patch_cs_vars.start()

        self.mock_cs_vars.COMPARATIVE_STATICS_MIN_RESULT = 'MinResult'
        self.mock_cs_vars.COMPARATIVE_STATICS_EXPECTED_RESULT = 'ExpectedResult'
        self.mock_cs_vars.COMPARATIVE_STATICS_MAX_RESULT = 'MaxResult'
        self.mock_cs_vars.COMPARATIVE_STATICS_VARIABLE_NAME = 'VariableName'
        self.mock_cs_vars.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE = 'MinVariableValue'
        self.mock_cs_vars.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE = 'ExpectedVariableValue'
        self.mock_cs_vars.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE = 'MaxVariableValue'
        self.mock_cs_vars.COMPARATIVE_STATICS_ELASTICITY = 'Elasticity'

        # 2. Setup a standard dataset capturing multiple elasticity behaviors (+ / -)
        self.standard_comparative_statics_input = [
            {
                'VariableName': 'ConversionRate',
                'MinVariableValue': 0.02,
                'ExpectedVariableValue': 0.03,
                'MaxVariableValue': 0.04,
                'MinResult': 80000.0,
                'ExpectedResult': 120000.0,
                'MaxResult': 160000.0,
                'Elasticity': 1.25  # Positive elasticity path
            },
            {
                'VariableName': 'ChurnRate',
                'MinVariableValue': 0.01,
                'ExpectedVariableValue': 0.02,
                'MaxVariableValue': 0.03,
                'MinResult': 140000.0,
                'ExpectedResult': 120000.0,
                'MaxResult': 95000.0,
                'Elasticity': -0.45  # Negative elasticity path
            }
        ]

    def tearDown(self):
        """Dismantle background isolation wrappers safely."""
        self.patch_plots.stop()
        self.patch_cs_vars.stop()

    # =========================================================================
    # MODULE STRUCTURAL TESTS: DATAFRAME GENERATION
    # =========================================================================

    def test_get_comparative_statics_dataframe_happy_path(self):
        """Scenario 1: Confirm matrix array loops cleanly to yield nested row layouts."""
        df = get_comparative_statics_dataframe(self.standard_comparative_statics_input, output_name="Net Value")

        self.assertIsInstance(df, pd.DataFrame)
        # 2 input metrics * 2 structural rows per item (Output Row + Input Factor Row) = 4 rows total
        self.assertEqual(len(df), 4)

        # Confirm columns align directly to mocked configurations
        expected_columns = [
            self.mock_plots.SENSITIVITY_VARIABLE,
            self.mock_plots.COMPARATIVE_STATICS_COLUMN_NAME_MIN,
            self.mock_plots.COMPARATIVE_STATICS_COLUMN_NAME_BASE,
            self.mock_plots.COMPARATIVE_STATICS_COLUMN_NAME_MAX,
            self.mock_plots.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY
        ]
        self.assertEqual(list(df.columns), expected_columns)

    def test_get_comparative_statics_dataframe_row_values(self):
        """Scenario 2: Verify specific structure blocks where Output rows suppress elasticity figures."""
        df = get_comparative_statics_dataframe(self.standard_comparative_statics_input, output_name="Net Value")

        elasticity_col = self.mock_plots.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY

        # Row index 0 belongs to Output (Results) - verify it is a NaN/missing float value
        self.assertTrue(np.isnan(df.iloc[0][elasticity_col]))

        # Row index 1 belongs to the Input factor (ConversionRate) - must match assigned metric value
        self.assertEqual(df.iloc[1][elasticity_col], 1.25)

    # =========================================================================
    # MODULE STRUCTURAL TESTS: HTML DASHBOARD RENDERING
    # =========================================================================

    def test_render_comparative_statics_dashboard_html_compilation(self):
        """Scenario 3: Verify the core table element compiles cleanly into notebook display containers."""
        html_component = render_comparative_statics_dashboard(
            self.standard_comparative_statics_input, output_name="Gross Income"
        )

        self.assertIsInstance(html_component, HTML)

        raw_html = html_component._repr_html_()
        self.assertTrue(len(raw_html) > 0)

        # Structural asset markers
        self.assertIn("Gross Income", raw_html)
        self.assertIn("ConversionRate", raw_html)
        self.assertIn("ChurnRate", raw_html)

    def test_render_comparative_statics_dashboard_elasticity_branching(self):
        """Scenario 4: Verify positive, negative, and safe non-float types trigger correct CSS classes."""
        edge_case_input = [
            {
                'VariableName': 'FixedOverhead',
                'MinVariableValue': 100, 'ExpectedVariableValue': 100, 'MaxVariableValue': 100,
                'MinResult': 500, 'ExpectedResult': 500, 'MaxResult': 500,
                'Elasticity': 'INVALID_STR_OR_NONE'  # String format crash resilience test
            }
        ]

        # Process standard input to verify class rendering matches conditional constraints
        raw_html_standard = render_comparative_statics_dashboard(
            self.standard_comparative_statics_input, output_name="Test"
        )._repr_html_()

        raw_html_edge = render_comparative_statics_dashboard(
            edge_case_input, output_name="Test"
        )._repr_html_()

        # Positive elasticity should inject + indicator sign along with appropriate class hooks
        self.assertIn("elasticity-positive", raw_html_standard)
        self.assertIn("+1.25", raw_html_standard)

        # Negative elasticity should inject appropriate negative class hooks
        self.assertIn("elasticity-negative", raw_html_standard)
        self.assertIn("-0.45", raw_html_standard)

        # Malformed or string non-numeric metrics shouldn't crash; should fallback to 0.00 base style
        self.assertIn("0.00", raw_html_edge)


if __name__ == '__main__':
    unittest.main()
