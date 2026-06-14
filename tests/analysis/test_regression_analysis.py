import unittest

from src.analysis import stochastic_bivariate_simulation
from src.config import variable_names
from src.core import Variable
from src.models import NetIncomeModel, MarketPriceModel
from src.variables import PriceToEarningsRatio


def _create_var(min_v, exp_v, max_v):
    return Variable(min=min_v, exp=exp_v, max=max_v)


class TestBivariateRegressionIntegration(unittest.TestCase):

    def setUp(self):
        """Build fiscal pipeline for OLS regression simulation."""
        self.pipeline = [NetIncomeModel(), MarketPriceModel()]

        # Scenario: Revenue drives MarketPrice (Bivariate X, Y)
        self.variables = {
            variable_names.REVENUE: _create_var(80000.0, 100000.0, 120000.0),
            variable_names.COST: _create_var(30000.0, 40000.0, 50000.0),
            variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
        }

    # -----------------------------------------------------------------
    # 1. ACCURACY: REGRESSION METRICS
    # -----------------------------------------------------------------

    def test_stochastic_bivariate_simulation_produces_valid_ols_metrics(self):
        """Verify the OLS result keys and distribution consistency."""
        x_dist, y_dist, stats = stochastic_bivariate_simulation(
            variables=self.variables,
            independent_target_x=variable_names.REVENUE,
            dependent_target_y=variable_names.MARKET_PRICE,
            shuffled_variables=[variable_names.REVENUE],
            model_pipeline=self.pipeline,
            sample_size=100
        )

        self.assertEqual(len(x_dist), 100)
        self.assertEqual(len(y_dist), 100)
        self.assertIn("slope", stats)
        self.assertIn("r_squared", stats)
        self.assertTrue(0 <= stats["r_squared"] <= 1.0)

    # -----------------------------------------------------------------
    # 2. RESILIENCE: GUARDRAILS & ERROR HANDLING
    # -----------------------------------------------------------------

    def test_stochastic_bivariate_simulation_aborts_on_missing_registry_variable(self):
        """Verify registry guardrail raises KeyError when required inputs (COST) are missing."""
        invalid_variables = {
            variable_names.REVENUE: self.variables[variable_names.REVENUE],
            variable_names.PE_RATIO: self.variables[variable_names.PE_RATIO]
        }

        with self.assertRaises(KeyError):
            stochastic_bivariate_simulation(
                variables=invalid_variables,
                independent_target_x=variable_names.REVENUE,
                dependent_target_y=variable_names.MARKET_PRICE,
                shuffled_variables=[variable_names.REVENUE],
                model_pipeline=self.pipeline
            )

    def test_stochastic_bivariate_simulation_aborts_on_invalid_pipeline_topology(self):
        """Verify topology guardrail raises KeyError when model order breaks dependency chain."""
        broken_pipeline = [MarketPriceModel(), NetIncomeModel()]

        with self.assertRaises(KeyError) as cm:
            stochastic_bivariate_simulation(
                variables=self.variables,
                independent_target_x=variable_names.REVENUE,
                dependent_target_y=variable_names.MARKET_PRICE,
                shuffled_variables=[variable_names.REVENUE],
                model_pipeline=broken_pipeline
            )
        self.assertIn("Pipeline Order Violation", str(cm.exception))

    def test_stochastic_bivariate_simulation_aborts_on_zero_variance(self):
        """Verify ValueError is raised if simulated variables lack statistical variance."""
        self.variables[variable_names.REVENUE] = _create_var(100000.0, 100000.0, 100000.0)

        with self.assertRaises(ValueError):
            stochastic_bivariate_simulation(
                variables=self.variables,
                independent_target_x=variable_names.REVENUE,
                dependent_target_y=variable_names.MARKET_PRICE,
                shuffled_variables=[variable_names.REVENUE],
                model_pipeline=self.pipeline
            )


if __name__ == "__main__":
    unittest.main()
