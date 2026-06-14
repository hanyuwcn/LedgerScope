import unittest

from src.analysis import comparative_statics
from src.config import variable_names
from src.core import Variable
from src.models import NetIncomeModel, MarketPriceModel
from src.variables import PriceToEarningsRatio


def _create_var(min_v, exp_v, max_v):
    return Variable(min=min_v, exp=exp_v, max=max_v)


class TestComparativeStaticsIntegration(unittest.TestCase):

    def setUp(self):
        """Build the high-level fiscal pipeline (Net Income -> Market Price)."""
        self.pipeline = [NetIncomeModel(), MarketPriceModel()]

        self.variables = {
            variable_names.REVENUE: _create_var(80000.0, 100000.0, 120000.0),
            variable_names.COST: _create_var(30000.0, 40000.0, 50000.0),
            variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
        }

    # -----------------------------------------------------------------
    # 1. ACCURACY: ELASTICITY LOGIC
    # -----------------------------------------------------------------

    def test_comparative_statics_calculates_correct_positive_elasticity(self):
        """Verify elasticity calculation for a direct scaling variable (Revenue)."""
        reports = comparative_statics(
            variables=self.variables,
            selected_variables=[variable_names.REVENUE],
            model_pipeline=self.pipeline,
            output_name=variable_names.MARKET_PRICE
        )

        # Expected Elasticity: 1.6667
        self.assertAlmostEqual(reports[0][variable_names.COMPARATIVE_STATICS_ELASTICITY], 1.6667, places=4)

    # -----------------------------------------------------------------
    # 2. RESILIENCE: GUARDRAILS & ERROR HANDLING
    # -----------------------------------------------------------------

    def test_comparative_statics_aborts_on_missing_registry_variable(self):
        """Verify registry guardrail raises KeyError when mandatory input (COST) is absent."""
        invalid_variables = {
            variable_names.REVENUE: self.variables[variable_names.REVENUE],
            variable_names.PE_RATIO: self.variables[variable_names.PE_RATIO]
        }
        with self.assertRaises(KeyError):
            comparative_statics(
                variables=invalid_variables,
                selected_variables=[variable_names.REVENUE],
                model_pipeline=self.pipeline,
                output_name=variable_names.MARKET_PRICE
            )

    def test_comparative_statics_aborts_on_invalid_pipeline_topology(self):
        """Verify topology guardrail raises KeyError when model order violates lineage."""
        broken_pipeline = [MarketPriceModel(), NetIncomeModel()]
        with self.assertRaises(KeyError) as cm:
            comparative_statics(
                variables=self.variables,
                selected_variables=[variable_names.REVENUE],
                model_pipeline=broken_pipeline,
                output_name=variable_names.MARKET_PRICE
            )
        self.assertIn("Pipeline Order Violation", str(cm.exception))

    # -----------------------------------------------------------------
    # 3. SAFETY INTERCEPTS: BOUNDARY CONDITIONS
    # -----------------------------------------------------------------

    def test_comparative_statics_returns_zero_on_flat_boundary(self):
        """Verify elasticity returns 0.0 when independent variable range is flat (delta=0)."""
        self.variables[variable_names.REVENUE] = Variable(min=100000.0, exp=100000.0, max=100000.0)

        reports = comparative_statics(
            variables=self.variables,
            selected_variables=[variable_names.REVENUE],
            model_pipeline=self.pipeline,
            output_name=variable_names.MARKET_PRICE
        )

        self.assertEqual(reports[0][variable_names.COMPARATIVE_STATICS_ELASTICITY], 0.0)

    def test_comparative_statics_returns_zero_on_zero_equilibrium(self):
        """Verify elasticity returns 0.0 when baseline result is at zero equilibrium."""
        self.variables[variable_names.COST] = _create_var(100000.0, 100000.0, 100000.0)

        reports = comparative_statics(
            variables=self.variables,
            selected_variables=[variable_names.REVENUE],
            model_pipeline=self.pipeline,
            output_name=variable_names.MARKET_PRICE
        )

        self.assertEqual(reports[0][variable_names.COMPARATIVE_STATICS_ELASTICITY], 0.0)


if __name__ == "__main__":
    unittest.main()
