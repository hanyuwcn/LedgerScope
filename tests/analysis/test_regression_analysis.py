import unittest

from src.analysis import stochastic_bivariate_simulation
from src.config import variable_names
from src.models import AdvertisingEfficiencyGoogleSearchModel, CostOfGoodsSoldModel, TotalCostModel
from src.variables import (
    AdvertisingCost, GoogleSearchConversionRate, GoogleSearchCostPerClick,
    USDToRMB, UnitsPerOrder, UnitExw, Cost
)


class TestStochasticBivariateSimulation(unittest.TestCase):

    def setUp(self):
        """
        Build production pipeline environments and establish baseline variables.
        No mock objects or mock functions are used here.
        """
        self.pipeline = [
            AdvertisingEfficiencyGoogleSearchModel(),
            CostOfGoodsSoldModel(),
            TotalCostModel()
        ]

        # Standard business context registry
        self.variables = {
            variable_names.ADVERTISING_COST: AdvertisingCost(min=4000.0, max=6000.0, exp=5000.0),
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: GoogleSearchConversionRate(min=0.05, max=0.15, exp=0.10),
            variable_names.CPL_GOOGLE_SEARCH: GoogleSearchCostPerClick(exp=20.0),
            variable_names.USD_TO_RMB: USDToRMB(exp=1.0),
            variable_names.UNITS_PER_ORDER: UnitsPerOrder(min=2.0, max=2.0),
            variable_names.UNIT_EXW: UnitExw(min=15.0, max=15.0),
            variable_names.SHIPPING_COST: Cost(exp=500.0)
        }

    # -----------------------------------------------------------------
    # 1. ACCURACY OF DATA: EXACT MATHEMATICAL & SLOPE TRACING
    # -----------------------------------------------------------------

    def test_simulation_data_accuracy_and_perfect_linear_correlation(self):
        """
        Verify the mathematical accuracy of the simulated coordinate data streams.

        Trace Logic:
          If we only shuffle 'CONVERSION_RATE_GOOGLE_SEARCH', the relationship between
          CONVERSION_RATE_GOOGLE_SEARCH (X) and final Cost (Y) across our production formulas
          is purely linear.

          Equation: Cost = AdvertisingCost + (Orders * UnitsPerOrder * UnitExw) + Shipping
          Where:    Orders = (AdvertisingCost / CPA) * CONVERSION_RATE_GOOGLE_SEARCH

          Substituting variables yields:
          Cost = 5000 + ((5000 / 20) * X * 2 * 15) + 500
          Cost = 5500 + (250 * 30) * X
          Cost = 5500 + 7500 * X

          Therefore:
          - The R^2 metric must equal exactly 1.0 (perfect linear fit).
          - The calculated slope must equal exactly 7500.0.
          - The calculated intercept must equal exactly 5500.0.
        """
        sample_size = 20

        x_coords, y_coords, trend_metrics = stochastic_bivariate_simulation(
            variables=self.variables,
            independent_target_x=variable_names.CONVERSION_RATE_GOOGLE_SEARCH,
            dependent_target_y=variable_names.COST,
            shuffled_variables=[variable_names.CONVERSION_RATE_GOOGLE_SEARCH],
            model_pipeline=self.pipeline,
            sample_size=sample_size
        )

        # 1. Check array length consistency
        self.assertEqual(len(x_coords), sample_size)
        self.assertEqual(len(y_coords), sample_size)

        # 2. Assert exact coordinate verification (Point-by-Point mapping validation)
        for x_val, y_val in zip(x_coords, y_coords):
            expected_y = 5500.0 + (7500.0 * x_val)
            self.assertAlmostEqual(y_val, expected_y, places=4)

        # 3. Assert statistical analysis summaries match expected linear output properties
        self.assertAlmostEqual(trend_metrics["r_squared"], 1.0, places=5)
        self.assertAlmostEqual(trend_metrics["slope"], 7500.0, places=4)
        self.assertAlmostEqual(trend_metrics["intercept"], 5500.0, places=4)

    # -----------------------------------------------------------------
    # 2. EDGE CASES: EXTREME OR COLLAPSED SIMULATION LAYERS
    # -----------------------------------------------------------------

    def test_simulation_aborts_safely_on_zero_variance_independent_axis(self):
        """
        Edge Case: Verify that an exception is raised if the target X parameter
        has no variance (e.g., min == max), which makes calculating slope impossible.
        """
        # UNITS_PER_ORDER is structurally locked in setup (min=2.0, max=2.0, exp=2.0)
        # Shuffling it will yield zero data variance on the X-axis vector.
        with self.assertRaises(ValueError) as context:
            stochastic_bivariate_simulation(
                variables=self.variables,
                independent_target_x=variable_names.UNITS_PER_ORDER,
                dependent_target_y=variable_names.COST,
                shuffled_variables=[variable_names.UNITS_PER_ORDER],
                model_pipeline=self.pipeline,
                sample_size=10
            )

        self.assertIn("exhibit zero statistical variance", str(context.exception))

    def test_simulation_aborts_safely_when_no_variables_are_shuffled(self):
        """
        Edge Case: Verify that if the user passes an empty list of shuffled variables,
        every iteration remains stuck at its expected value baseline, triggering a
        variance validation failure.
        """
        with self.assertRaises(ValueError) as context:
            stochastic_bivariate_simulation(
                variables=self.variables,
                independent_target_x=variable_names.CONVERSION_RATE_GOOGLE_SEARCH,
                dependent_target_y=variable_names.COST,
                shuffled_variables=[],  # Dead engine state parameter
                model_pipeline=self.pipeline,
                sample_size=5
            )

        self.assertIn("exhibit zero statistical variance", str(context.exception))


if __name__ == "__main__":
    unittest.main()
