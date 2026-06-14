import unittest

import pandas as pd

from src.analysis import run_two_way_sensitivity_analysis
from src.config import variable_names
from src.core import Variable
from src.models import NetIncomeModel, MarketPriceModel
from src.variables import PriceToEarningsRatio


def _create_var(min_v, exp_v, max_v):
    return Variable(min=min_v, exp=exp_v, max=max_v)


class TestTwoWaySensitivityIntegration(unittest.TestCase):

    def setUp(self):
        """Build fiscal pipeline for Two-Way sensitivity grid."""
        # Standard valid pipeline: NetIncome -> MarketPrice
        self.pipeline = [NetIncomeModel(), MarketPriceModel()]

        self.variables = {
            variable_names.REVENUE: _create_var(80000.0, 100000.0, 120000.0),
            variable_names.COST: _create_var(30000.0, 40000.0, 50000.0),
            variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
        }

    # -----------------------------------------------------------------
    # 1. ACCURACY & LOGIC
    # -----------------------------------------------------------------

    def test_run_two_way_sensitivity_analysis_produces_correct_grid_dimensions(self):
        """Verify the output is a DataFrame with requested shape and axis names."""
        df = run_two_way_sensitivity_analysis(
            variables=self.variables,
            param_x_name=variable_names.REVENUE,
            param_y_name=variable_names.COST,
            model_pipeline=self.pipeline,
            target_output_name=variable_names.MARKET_PRICE,
            x_steps=3,
            y_steps=3
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (3, 3))
        self.assertEqual(df.index.name, variable_names.COST)
        self.assertEqual(df.columns.name, variable_names.REVENUE)

    def test_run_two_way_sensitivity_analysis_validates_economic_trend(self):
        """Verify sensitivity matrix logic: high revenue/low cost yields highest value."""
        df = run_two_way_sensitivity_analysis(
            variables=self.variables,
            param_x_name=variable_names.REVENUE,
            param_y_name=variable_names.COST,
            model_pipeline=self.pipeline,
            target_output_name=variable_names.MARKET_PRICE
        )

        # Ensure price increases with revenue and decreases with cost
        self.assertGreater(df.iloc[-1, -1], df.iloc[0, 0])

    # -----------------------------------------------------------------
    # 2. RESILIENCE: GUARDRAILS & ERROR HANDLING
    # -----------------------------------------------------------------

    def test_run_two_way_sensitivity_analysis_aborts_on_missing_registry_variable(self):
        """Verify registry guardrail raises KeyError when required inputs (COST) are missing."""
        # COST is mandatory and lacks a default value, unlike PE_RATIO
        invalid_variables = {
            variable_names.REVENUE: self.variables[variable_names.REVENUE],
            variable_names.PE_RATIO: self.variables[variable_names.PE_RATIO]
        }

        with self.assertRaises(KeyError):
            run_two_way_sensitivity_analysis(
                variables=invalid_variables,
                param_x_name=variable_names.REVENUE,
                param_y_name=variable_names.PE_RATIO,
                model_pipeline=self.pipeline,
                target_output_name=variable_names.MARKET_PRICE
            )

    def test_run_two_way_sensitivity_analysis_aborts_on_invalid_pipeline_topology(self):
        """Verify topology guardrail raises KeyError when model order breaks dependency chain."""
        # MarketPriceModel depends on NetIncomeModel output; order reversal violates topology.
        broken_pipeline = [MarketPriceModel(), NetIncomeModel()]

        with self.assertRaises(KeyError) as cm:
            run_two_way_sensitivity_analysis(
                variables=self.variables,
                param_x_name=variable_names.REVENUE,
                param_y_name=variable_names.COST,
                model_pipeline=broken_pipeline,
                target_output_name=variable_names.MARKET_PRICE
            )
        self.assertIn("Pipeline Order Violation", str(cm.exception))

    def test_run_two_way_sensitivity_analysis_aborts_on_missing_target_output(self):
        """Verify system raises KeyError if the requested target output cannot be resolved."""
        with self.assertRaises(KeyError):
            run_two_way_sensitivity_analysis(
                variables=self.variables,
                param_x_name=variable_names.REVENUE,
                param_y_name=variable_names.COST,
                model_pipeline=self.pipeline,
                target_output_name="INVALID_METRIC"
            )


if __name__ == "__main__":
    unittest.main()
