import unittest

import pandas as pd
from pandas.io.formats.style import Styler

from src.analysis import comparative_statics
from src.config import variable_names
from src.core import Variable
from src.models import NetIncomeModel, MarketPriceModel
from src.variables import Cost, PriceToEarningsRatio
from src.visualization.styles import comparative_statics_styles as cs_style
from src.visualization.views.comparative_statics_view import (
    get_comparative_statics_dataframe,
    render_comparative_statics_dashboard
)


class TestComparativeStaticsViewEngineComprehensive(unittest.TestCase):

    def setUp(self):
        """Standardize fixture using the core fiscal pipeline."""
        self.pipeline = [NetIncomeModel(), MarketPriceModel()]

        self.variables = {
            variable_names.REVENUE: Variable(min=80000.0, exp=100000.0, max=120000.0),
            variable_names.COST: Cost(min=30000.0, exp=40000.0, max=50000.0),
            variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
        }

        # Generate production-ready analysis output
        self.analysis_output = comparative_statics(
            variables=self.variables,
            selected_variables=[variable_names.REVENUE, variable_names.COST],
            model_pipeline=self.pipeline,
            output_name=variable_names.MARKET_PRICE
        )

    # =========================================================================
    # 1. DATAFRAME GENERATION LOGIC
    # =========================================================================

    def test_get_comparative_statics_dataframe_happy_path(self):
        """Confirm view engine processes analytical output into a nested matrix."""
        df = get_comparative_statics_dataframe(self.analysis_output, output_name="Market Valuation")

        self.assertIsInstance(df, pd.DataFrame)
        # 2 selected variables * 2 rows each = 4 total rows
        self.assertEqual(len(df), 4)

        expected_columns = [
            cs_style.SENSITIVITY_VARIABLE,
            cs_style.COMPARATIVE_STATICS_COLUMN_NAME_MIN,
            cs_style.COMPARATIVE_STATICS_COLUMN_NAME_BASE,
            cs_style.COMPARATIVE_STATICS_COLUMN_NAME_MAX,
            cs_style.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY
        ]
        self.assertEqual(list(df.columns), expected_columns)

    # =========================================================================
    # 2. PANDAS STYLER DASHBOARD RENDERING LOGIC
    # =========================================================================

    def test_render_comparative_statics_dashboard_styler_compilation(self):
        """Verify the UI pipeline compiles the fiscal model output into a Styler object."""
        styler_component = render_comparative_statics_dashboard(
            self.analysis_output, output_name="Market Valuation"
        )

        self.assertIsInstance(styler_component, Styler)

        raw_html = styler_component.to_html()
        self.assertTrue(len(raw_html) > 0)

        # Verify fiscal keys are present
        self.assertIn(variable_names.REVENUE, raw_html)
        self.assertIn(variable_names.COST, raw_html)


if __name__ == '__main__':
    unittest.main()
