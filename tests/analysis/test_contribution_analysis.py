import unittest

from src.analysis import stochastic_contribution_analysis
from src.config import variable_names
from src.core import Variable
from src.models import NetIncomeModel, MarketPriceModel
from src.variables import Cost, PriceToEarningsRatio


def _create_var(min_v, exp_v, max_v):
    return Variable(min=min_v, exp=exp_v, max=max_v)


class TestStochasticContributionIntegration(unittest.TestCase):

    def setUp(self):
        """Build fiscal pipeline for Monte Carlo contribution simulation."""
        self.pipeline = [NetIncomeModel(), MarketPriceModel()]

        self.variables = {
            variable_names.REVENUE: _create_var(80000.0, 100000.0, 120000.0),
            variable_names.COST: Cost(min=30000.0, exp=40000.0, max=50000.0),
            variable_names.PE_RATIO: PriceToEarningsRatio(min=5.0, exp=8.0, max=10.0)
        }

    # -----------------------------------------------------------------
    # 1. ACCURACY: CONVERGENCE CHECK
    # -----------------------------------------------------------------

    def test_stochastic_contribution_analysis_averages_converge_on_expected_values(self):
        """Verify that averaged results align with baseline expected values."""
        breakdown = [variable_names.REVENUE, variable_names.COST]
        shuffled = [variable_names.REVENUE, variable_names.COST]

        results = stochastic_contribution_analysis(
            variables=self.variables,
            breakdown_metrics=breakdown,
            model_pipeline=self.pipeline,
            shuffled_inputs=shuffled,
            sample_size=100
        )

        self.assertAlmostEqual(results[variable_names.REVENUE], 100000.0, delta=5000)
        self.assertAlmostEqual(results[variable_names.COST], 40000.0, delta=2000)

    # -----------------------------------------------------------------
    # 2. RESILIENCE: GUARDRAILS & ERROR HANDLING
    # -----------------------------------------------------------------

    def test_stochastic_contribution_analysis_aborts_on_missing_registry_variable(self):
        """Verify registry guardrail raises KeyError when mandatory input (COST) is absent."""
        invalid_variables = {
            variable_names.REVENUE: self.variables[variable_names.REVENUE],
            variable_names.PE_RATIO: self.variables[variable_names.PE_RATIO]
        }
        with self.assertRaises(KeyError):
            stochastic_contribution_analysis(
                variables=invalid_variables,
                breakdown_metrics=[variable_names.REVENUE],
                model_pipeline=self.pipeline,
                shuffled_inputs=[variable_names.REVENUE]
            )

    def test_stochastic_contribution_analysis_aborts_on_invalid_pipeline_topology(self):
        """Verify topology guardrail raises KeyError when model order violates lineage."""
        broken_pipeline = [MarketPriceModel(), NetIncomeModel()]
        with self.assertRaises(KeyError) as cm:
            stochastic_contribution_analysis(
                variables=self.variables,
                breakdown_metrics=[variable_names.REVENUE],
                model_pipeline=broken_pipeline,
                shuffled_inputs=[variable_names.REVENUE]
            )
        self.assertIn("Pipeline Order Violation", str(cm.exception))

    def test_stochastic_contribution_analysis_aborts_on_missing_breakdown_metric(self):
        """Verify system raises KeyError if requested breakdown metric is unknown."""
        with self.assertRaises(KeyError):
            stochastic_contribution_analysis(
                variables=self.variables,
                breakdown_metrics=["NON_EXISTENT_METRIC"],
                model_pipeline=self.pipeline,
                shuffled_inputs=[variable_names.REVENUE]
            )

    def test_stochastic_contribution_analysis_aborts_on_missing_runtime_output(self):
        """Verify engine raises KeyError if runtime state fails to produce required breakdown metrics."""
        # 'NON_EXISTENT_METRIC' is not provided by the pipeline,
        # so check_variables_for_function will catch it on the first iteration.
        with self.assertRaises(KeyError):
            stochastic_contribution_analysis(
                variables=self.variables,
                breakdown_metrics=["NON_EXISTENT_METRIC"],
                model_pipeline=self.pipeline,
                shuffled_inputs=[variable_names.REVENUE],
                sample_size=10
            )


if __name__ == "__main__":
    unittest.main()
