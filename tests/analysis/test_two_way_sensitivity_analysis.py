import unittest

import pandas as pd

from src.analysis import run_two_way_sensitivity_analysis
from src.config import variable_names
from src.models import AdvertisingEfficiencyModel, CostOfGoodsSoldModel, TotalCostModel
from src.variables import (AdvertisingCost, ConversionRate, CostPerAcquisition,
                           USDToRMB, ItemsPerOrder, PurchasingPrice, Cost)


class TestTwoWaySensitivityAnalysis(unittest.TestCase):

    def setUp(self):
        """Build the raw business pipeline and baseline operational variables."""
        self.pipeline = [
            AdvertisingEfficiencyModel(),
            CostOfGoodsSoldModel(),
            TotalCostModel()
        ]

        # Use your direct production classes populated with clean testing values
        self.variables = {
            variable_names.COST_ADVERTISING: AdvertisingCost(min_value=4000.0, max_value=6000.0),
            # X axis steps: [4000.0, 6000.0]
            variable_names.COST_CONVERSION_RATE: ConversionRate(min_value=0.05, max_value=0.15),
            # Y axis steps: [0.05, 0.15]
            variable_names.COST_CPA: CostPerAcquisition(expected_value=20.0),
            variable_names.FINANCE_USD_TO_RMB: USDToRMB(expected_value=1.0),
            variable_names.DEAL_ITEMS_PER_ORDER: ItemsPerOrder(min_value=2.0, max_value=2.0),
            variable_names.DEAL_PURCHASING_PRICE: PurchasingPrice(min_value=15.0, max_value=15.0),
            variable_names.COST_SHIPPING: Cost(expected_value=500.0)
        }

    # -----------------------------------------------------------------
    # 1. COMPREHENSIVE FULL-DATAFRAME VALIDATION
    # -----------------------------------------------------------------

    def test_sensitivity_matrix_matches_full_expected_financial_grid(self):
        """Verify the entire generated dataframe grid matches calculated financial outcomes."""

        # Execute a clean 2x2 grid search sweep
        df = run_two_way_sensitivity_analysis(
            variables=self.variables,
            param_x_name=variable_names.COST_ADVERTISING,
            param_y_name=variable_names.COST_CONVERSION_RATE,
            model_pipeline=self.pipeline,
            target_output_name=variable_names.COST,
            x_steps=2,
            y_steps=2,
            reverse_x=False,
            reverse_y=True  # Flips Y axis array to layout: [0.15, 0.05]
        )

        # --- Explicit Math Matrix Breakdown ---
        # Columns (X): [4000.0, 6000.0]
        # Rows (Y):    [0.15, 0.05] (flipped via reverse_y)
        #
        # Matrix Position 1 [Row: 0.15, Col: 4000.0]:
        #   Orders = (4000 * 0.15) / 20 = 30  -> COGS = 15 * 30 * 2 = 900  -> Cost = 900 + 4000 + 500 = 5400.0
        # Matrix Position 2 [Row: 0.15, Col: 6000.0]:
        #   Orders = (6000 * 0.15) / 20 = 45  -> COGS = 15 * 45 * 2 = 1350 -> Cost = 1350 + 6000 + 500 = 7850.0
        # Matrix Position 3 [Row: 0.05, Col: 4000.0]:
        #   Orders = (4000 * 0.05) / 20 = 10  -> COGS = 15 * 10 * 2 = 300  -> Cost = 300 + 4000 + 500 = 4800.0
        # Matrix Position 4 [Row: 0.05, Col: 6000.0]:
        #   Orders = (6000 * 0.05) / 20 = 15  -> COGS = 15 * 15 * 2 = 450  -> Cost = 450 + 6000 + 500 = 6950.0
        expected_data = {
            4000.0: {0.15: 5400.0, 0.05: 4800.0},
            6000.0: {0.15: 7850.0, 0.05: 6950.0}
        }
        expected_df = pd.DataFrame(expected_data)
        expected_df.index.name = variable_names.COST_CONVERSION_RATE
        expected_df.columns.name = variable_names.COST_ADVERTISING

        # Assert index metadata, column arrays, and full numeric cell values match perfectly
        pd.testing.assert_frame_equal(df, expected_df, check_dtype=False)

    # -----------------------------------------------------------------
    # 2. EDGE CASE: FIXED LABELS
    # -----------------------------------------------------------------

    def test_sensitivity_analysis_runs_cleanly_when_variable_range_is_fixed(self):
        """Verify the grid handles flat ranges without crashing out."""
        # Fix conversion rate strictly to a stagnant 10%
        self.variables[variable_names.COST_CONVERSION_RATE] = ConversionRate(min_value=0.10, max_value=0.10)

        df = run_two_way_sensitivity_analysis(
            variables=self.variables,
            param_x_name=variable_names.COST_ADVERTISING,
            param_y_name=variable_names.COST_CONVERSION_RATE,
            model_pipeline=self.pipeline,
            target_output_name=variable_names.COST,
            x_steps=2,
            y_steps=2,
            reverse_x=False,
            reverse_y=False
        )

        # Expected shape is 2x2, but every index label along the vertical axis is 0.10
        self.assertEqual(df.shape, (2, 2))
        self.assertEqual(list(df.index), [0.10, 0.10])

    # -----------------------------------------------------------------
    # 3. EDGE CASE: SELECTION HOOK FAILURES
    # -----------------------------------------------------------------

    def test_analysis_raises_exception_when_selected_variable_is_missing_from_dict(self):
        """Verify tracking exceptions bubble up instantly if an input variable key is completely missing."""
        with self.assertRaises(Exception):
            run_two_way_sensitivity_analysis(
                variables=self.variables,
                param_x_name="MISSING_TAX_VARIABLE_KEY",
                param_y_name=variable_names.COST_CONVERSION_RATE,
                model_pipeline=self.pipeline,
                target_output_name=variable_names.COST
            )

    # -----------------------------------------------------------------
    # 4. EDGE CASE: PIPELINE VALIDATION & ORDER FAILURES
    # -----------------------------------------------------------------

    def test_analysis_raises_exception_when_pipeline_sequence_order_fails(self):
        """Verify that a broken or out-of-order model pipeline immediately aborts execution."""
        # TotalCostModel depends on outputs generated by CostOfGoodsSoldModel.
        # Placing it first breaks the topological dependency flow.
        scrambled_pipeline = [
            TotalCostModel(),
            CostOfGoodsSoldModel(),
            AdvertisingEfficiencyModel()
        ]

        with self.assertRaises(Exception):
            run_two_way_sensitivity_analysis(
                variables=self.variables,
                param_x_name=variable_names.COST_ADVERTISING,
                param_y_name=variable_names.COST_CONVERSION_RATE,
                model_pipeline=scrambled_pipeline,
                target_output_name=variable_names.COST
            )


if __name__ == "__main__":
    unittest.main()
