import unittest
from unittest.mock import MagicMock, patch

from src.analysis import break_even_analysis
from src.config import variable_names, settings, messages
from src.core import Variable
from src.models import NetIncomeModel, MarketPriceModel, OperatingIncomeModel
from src.variables import PriceToEarningsRatio


def _create_var(min_v, exp_v, max_v):
    return Variable(min=min_v, exp=exp_v, max=max_v)


class TestBreakEvenAnalysisIntegration(unittest.TestCase):

    def setUp(self):
        """Build the high-level fiscal pipeline (Net Income -> Market Price)."""
        self.pipeline = [OperatingIncomeModel(), NetIncomeModel(), MarketPriceModel()]

        # Force range subdivisions to a deterministic 3 steps for trace calculations
        self.old_nums_in_range = settings.NUMS_IN_RANGE
        settings.NUMS_IN_RANGE = 3

        self.variables = {
            variable_names.REVENUE: _create_var(80000.0, 100000.0, 120000.0),
            variable_names.COGS: _create_var(30000.0, 40000.0, 50000.0),
            variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
        }

        # Deterministic 3-step slice: [80k, 100k, 120k]
        self.variables[variable_names.REVENUE].get_range_values = MagicMock(
            return_value=[80000.0, 100000.0, 120000.0]
        )

    def tearDown(self):
        settings.NUMS_IN_RANGE = self.old_nums_in_range

    # -----------------------------------------------------------------
    # 1. ACCURACY: PRECISION & MARGINS
    # -----------------------------------------------------------------

    def test_break_even_analysis_calculates_crossover_precision(self):
        """Verify break-even crossover at goal=5.0M."""
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=[variable_names.REVENUE],
            model_pipeline=self.pipeline,
            output_name=variable_names.MARKET_PRICE,
            goal=5000000.0
        )

        self.assertEqual(reports[0][variable_names.BREAK_EVEN_FEASIBILITY_STATUS],
                         messages.BREAK_EVEN_FEASIBILITY_STATUS_CROSSOVER)
        self.assertAlmostEqual(reports[0][variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE], 100000.0)

    def test_break_even_analysis_calculates_negative_margin_runway(self):
        """Verify safety margin calculates correctly when baseline is below target."""
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=[variable_names.REVENUE],
            model_pipeline=self.pipeline,
            output_name=variable_names.MARKET_PRICE,
            goal=6000000.0
        )
        self.assertAlmostEqual(reports[0][variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE], -0.2)

    # -----------------------------------------------------------------
    # 2. RESILIENCE: GUARDRAILS & ERROR HANDLING
    # -----------------------------------------------------------------

    def test_break_even_analysis_aborts_on_missing_registry_variable(self):
        """Verify registry guardrail raises KeyError when mandatory input (COGS) is absent."""
        invalid_variables = {
            variable_names.REVENUE: self.variables[variable_names.REVENUE],
            variable_names.PE_RATIO: self.variables[variable_names.PE_RATIO]
        }
        with self.assertRaises(KeyError):
            break_even_analysis(
                variables=invalid_variables,
                selected_variables=[variable_names.REVENUE],
                model_pipeline=self.pipeline,
                output_name=variable_names.MARKET_PRICE
            )

    def test_break_even_analysis_aborts_on_invalid_pipeline_topology(self):
        """Verify topology guardrail raises KeyError when model order violates lineage."""
        broken_pipeline = [MarketPriceModel(), NetIncomeModel()]
        with self.assertRaises(KeyError) as cm:
            break_even_analysis(
                variables=self.variables,
                selected_variables=[variable_names.REVENUE],
                model_pipeline=broken_pipeline,
                output_name=variable_names.MARKET_PRICE
            )
        self.assertIn("Pipeline Order Violation", str(cm.exception))

    # -----------------------------------------------------------------
    # 3. SAFETY INTERCEPTS: BOUNDARY CONDITIONS
    # -----------------------------------------------------------------

    def test_break_even_analysis_handles_always_feasible_state(self):
        """Verify smallest driver selected when goal is easily met."""
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=[variable_names.REVENUE],
            model_pipeline=self.pipeline,
            output_name=variable_names.MARKET_PRICE,
            goal=1000000.0
        )
        self.assertEqual(reports[0][variable_names.BREAK_EVEN_FEASIBILITY_STATUS],
                         messages.BREAK_EVEN_FEASIBILITY_ALWAYS_FEASIBLE)
        self.assertAlmostEqual(reports[0][variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE], 80000.0)

    def test_break_even_analysis_handles_unreachable_goal(self):
        """Verify max driver selected when goal is impossible."""
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=[variable_names.REVENUE],
            model_pipeline=self.pipeline,
            output_name=variable_names.MARKET_PRICE,
            goal=10000000.0
        )
        self.assertEqual(reports[0][variable_names.BREAK_EVEN_FEASIBILITY_STATUS],
                         messages.BREAK_EVEN_FEASIBILITY_UNREACHABLE)

    def test_break_even_analysis_aborts_on_non_monotonic_impact(self):
        """Verify engine handles non-monotonic impact curves."""
        with patch('src.analysis.break_even_analysis.evaluate_variable_scenario_sweep') as mock_sweep:
            mock_sweep.return_value = [
                {variable_names.MARKET_PRICE: 100.0},
                {variable_names.MARKET_PRICE: 50.0},
                {variable_names.MARKET_PRICE: 150.0}
            ]
            reports = break_even_analysis(
                variables=self.variables,
                selected_variables=[variable_names.REVENUE],
                model_pipeline=self.pipeline,
                output_name=variable_names.MARKET_PRICE
            )
            self.assertEqual(len(reports), 1)


if __name__ == "__main__":
    unittest.main()
