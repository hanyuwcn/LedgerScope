import unittest

from src.analysis import stochastic_contribution_analysis
from src.config import variable_names
from src.models import AdvertisingEfficiencyModel, CostOfGoodsSoldModel, TotalCostModel
from src.variables import (AdvertisingCost, ConversionRate, CostPerAcquisition,
                           USDToRMB, ItemsPerOrder, PurchasingPrice, Cost)


class TestStochasticContributionAnalysis(unittest.TestCase):

    def setUp(self):
        """
        Build production pipeline environments and establish baseline variables.
        No mock objects or mock functions are used here.
        """
        self.pipeline = [
            AdvertisingEfficiencyModel(),
            CostOfGoodsSoldModel(),
            TotalCostModel()
        ]

        # Standard business context registry
        self.variables = {
            variable_names.COST_ADVERTISING: AdvertisingCost(min_value=4000.0, max_value=6000.0, expected_value=5000.0),
            variable_names.COST_CONVERSION_RATE: ConversionRate(min_value=0.05, max_value=0.15, expected_value=0.10),
            variable_names.COST_CPA: CostPerAcquisition(expected_value=20.0),
            variable_names.FINANCE_USD_TO_RMB: USDToRMB(expected_value=1.0),
            variable_names.DEAL_ITEMS_PER_ORDER: ItemsPerOrder(min_value=2.0, max_value=2.0),
            variable_names.DEAL_PURCHASING_PRICE: PurchasingPrice(min_value=15.0, max_value=15.0),
            variable_names.COST_SHIPPING: Cost(expected_value=500.0)
        }

    # -----------------------------------------------------------------
    # 1. ACCURACY OF DATA: EXACT MATHEMATICAL TRACING
    # -----------------------------------------------------------------

    def test_analysis_data_accuracy_with_fixed_inputs(self):
        """
        Verify the mathematical accuracy of the contribution averages.

        Trace Logic:
          If we pass an empty shuffled_inputs list, every variable stays fixed at its expected value.

          Inputs:
          - AdvertisingCost = 5000.0
          - Orders = (AdvertisingCost / CPA) * ConversionRate = (5000 / 20) * 0.10 = 25
          - COGS = Orders * ItemsPerOrder * PurchasingPrice = 25 * 2 * 15 = 750.0
          - ShippingCost = 500.0

          Therefore, regardless of sample_size, the mathematical mean for each
          component must match these exact static numbers.
        """
        breakdown_metrics = [
            variable_names.COST_ADVERTISING,
            variable_names.COST_COGS,
            variable_names.COST_SHIPPING
        ]

        mean_results = stochastic_contribution_analysis(
            variables=self.variables,
            breakdown_metrics=breakdown_metrics,
            model_pipeline=self.pipeline,
            shuffled_inputs=[],  # Kept fixed to isolate math baseline tracking
            sample_size=10
        )

        # Confirm structural keys match exactly
        self.assertEqual(set(mean_results.keys()), set(breakdown_metrics))

        # Assert exact absolute values are preserved via the arithmetic averaging logic
        self.assertAlmostEqual(mean_results[variable_names.COST_ADVERTISING], 5000.0, places=4)
        self.assertAlmostEqual(mean_results[variable_names.COST_COGS], 750.0, places=4)
        self.assertAlmostEqual(mean_results[variable_names.COST_SHIPPING], 500.0, places=4)

    def test_analysis_averaging_accuracy_with_shuffled_inputs(self):
        """
        Verify that the arithmetic mean accurately aggregates fluctuating data vectors.

        Trace Logic:
          When we shuffle 'AdvertisingCost' (min=4000, max=6000), the stochastic engine
          draws samples across this uniform range. For a sufficiently large sample size,
          the average absolute value must converge cleanly toward the expected value midpoint ($5000).
        """
        breakdown_metrics = [variable_names.COST_ADVERTISING]
        sample_size = 500

        mean_results = stochastic_contribution_analysis(
            variables=self.variables,
            breakdown_metrics=breakdown_metrics,
            model_pipeline=self.pipeline,
            shuffled_inputs=[variable_names.COST_ADVERTISING],
            sample_size=sample_size
        )

        # Verify mean convergence holds within a standard 1.5% margin of error
        self.assertAlmostEqual(mean_results[variable_names.COST_ADVERTISING], 5000.0, delta=75.0)

    # -----------------------------------------------------------------
    # 2. EDGE CASES: BOUNDARY LIMITS AND EXTREME PARAMETERS
    # -----------------------------------------------------------------

    def test_analysis_aborts_safely_on_invalid_sample_size(self):
        """
        Edge Case: Confirm that the module handles zero or negative sample sizes
        by throwing an exception rather than silently corrupting numbers.
        """
        breakdown_metrics = [variable_names.COST_ADVERTISING]

        # Since the code doesn't have an early guard check, it throws a ZeroDivisionError
        with self.assertRaises((ValueError, ZeroDivisionError)):
            stochastic_contribution_analysis(
                variables=self.variables,
                breakdown_metrics=breakdown_metrics,
                model_pipeline=self.pipeline,
                shuffled_inputs=[],
                sample_size=0
            )

    def test_analysis_with_empty_metrics_list_returns_blank_payload(self):
        """
        Edge Case: Confirm that an empty breakdown list smoothly runs the simulation
        and returns an empty dictionary output without unexpected structural failures.
        """
        mean_results = stochastic_contribution_analysis(
            variables=self.variables,
            breakdown_metrics=[],
            model_pipeline=self.pipeline,
            shuffled_inputs=[],
            sample_size=5
        )

        # Should cleanly return an empty dict: {}
        self.assertEqual(mean_results, {})


if __name__ == "__main__":
    unittest.main()
