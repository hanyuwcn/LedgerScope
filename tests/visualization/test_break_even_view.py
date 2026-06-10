import unittest

import pandas as pd
from pandas.io.formats.style import Styler

from src.analysis import break_even_analysis
from src.config import variable_names
from src.core import Variable
from src.models import NetIncomeModel, MarketPriceModel
from src.variables import Cost, PriceToEarningsRatio
from src.visualization.styles import break_even_styles
from src.visualization.views.break_even_view import get_break_even_dataframe, render_break_even_dashboard


class TestBreakEvenViewEngineComprehensive(unittest.TestCase):

    def setUp(self):
        """Standardize fixture using the core fiscal pipeline."""
        self.pipeline = [NetIncomeModel(), MarketPriceModel()]

        # Consistent fiscal scenario
        self.variables = {
            variable_names.REVENUE: Variable(min=80000.0, exp=100000.0, max=120000.0),
            variable_names.COST: Cost(min=30000.0, exp=40000.0, max=50000.0),
            variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
        }

        # Generate production-ready analysis output from the engine
        self.analysis_output = break_even_analysis(
            variables=self.variables,
            selected_variables=[variable_names.REVENUE, variable_names.COST],
            model_pipeline=self.pipeline,
            output_name=variable_names.MARKET_PRICE,
            goal=5000000.0
        )

    # =========================================================================
    # 1. DATAFRAME GENERATION LOGIC
    # =========================================================================

    def test_get_break_even_dataframe_happy_path(self):
        """Confirm the view engine correctly processes the engine's output."""
        df = get_break_even_dataframe(self.analysis_output, output_name="Market Valuation")

        self.assertIsInstance(df, pd.DataFrame)
        # 2 variables * 2 rows = 4 rows
        self.assertEqual(len(df), 4)

        expected_columns = [
            break_even_styles.SENSITIVITY_VARIABLE,
            break_even_styles.BREAK_EVEN_COLUMN_NAME_BASE,
            break_even_styles.BREAK_EVEN_COLUMN_NAME_THRESHOLD,
            break_even_styles.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN
        ]
        self.assertEqual(list(df.columns), expected_columns)

    # =========================================================================
    # 2. PANDAS STYLER RENDERING LOGIC
    # =========================================================================

    def test_render_break_even_dashboard_styler_compilation(self):
        """Verify the UI pipeline compiles the fiscal model output into a Styler."""
        styler_component = render_break_even_dashboard(self.analysis_output, output_name="Market Valuation")

        self.assertIsInstance(styler_component, Styler)

        raw_html = styler_component.to_html()
        self.assertTrue(len(raw_html) > 0)

        # Assert fiscal keys from our model pipeline are rendered
        self.assertIn(variable_names.REVENUE, raw_html)
        self.assertIn(variable_names.COST, raw_html)


if __name__ == '__main__':
    unittest.main()
