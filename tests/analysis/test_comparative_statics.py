import unittest

from src.analysis.comparative_statics import comparative_statics, compute_elasticity
from src.config import variable_names
from src.models import AdvertisingEfficiencyModel, CostOfGoodsSoldModel, TotalCostModel
from src.variables import (AdvertisingCost, ConversionRate, CostPerAcquisition,
                           USDToRMB, ItemsPerOrder, PurchasingPrice, Cost)


class TestComparativeStaticsAnalysis(unittest.TestCase):

    def setUp(self):
        """Build the raw business pipeline and baseline operational variables."""
        self.pipeline = [
            AdvertisingEfficiencyModel(),
            CostOfGoodsSoldModel(),
            TotalCostModel()
        ]

        # Standard baseline values for trace checking logic
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
    # 1. PRECISION TRACKING: ELASTICITY METRIC SENSITIVITY VERIFICATION
    # -----------------------------------------------------------------

    def test_comparative_statics_precision_and_elasticity_metrics(self):
        """Verify the exact financial endpoints and mathematical calculations for elasticity."""
        # Baseline Math Mapping for Variable: ConversionRate
        #   Range limits defined: Min=0.05, Expected=0.10, Max=0.15
        #
        # Model Outcome Calculations Map:
        #   Min (0.05)      -> Total Cost = 5875.0
        #   Expected (0.10) -> Total Cost = 6250.0
        #   Max (0.15)      -> Total Cost = 6625.0
        #
        # Slope Calculation Step:
        #   Delta Y = 6625.0 - 5875.0 = 750.0
        #   Delta X = 0.15 - 0.05 = 0.10
        #   Slope = 750.0 / 0.10 = 7500.0
        #
        # Elasticity Formulation:
        #   Elasticity = Slope * (X_expected / Y_expected)
        #   Elasticity = 7500.0 * (0.10 / 6250.0) = 7500.0 * 0.000016 = 0.12

        selected_variables = [variable_names.COST_CONVERSION_RATE]
        reports = comparative_statics(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.COST
        )

        self.assertEqual(len(reports), 1)
        report = reports[0]

        # Validate structural payload metadata integration keys
        self.assertEqual(report[variable_names.COMPARATIVE_STATICS_VARIABLE_NAME], variable_names.COST_CONVERSION_RATE)
        self.assertAlmostEqual(report[variable_names.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE], 0.05)
        self.assertAlmostEqual(report[variable_names.COMPARATIVE_STATICS_MIN_RESULT], 5875.0)
        self.assertAlmostEqual(report[variable_names.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE], 0.10)
        self.assertAlmostEqual(report[variable_names.COMPARATIVE_STATICS_EXPECTED_RESULT], 6250.0)
        self.assertAlmostEqual(report[variable_names.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE], 0.15)
        self.assertAlmostEqual(report[variable_names.COMPARATIVE_STATICS_MAX_RESULT], 6625.0)

        # Precision trace validation assertion checking
        self.assertAlmostEqual(report[variable_names.COMPARATIVE_STATICS_ELASTICITY], 0.12)

    # -----------------------------------------------------------------
    # 2. CORNER CASE: INTERCEPTING ZERO DIVISION SCENARIOS
    # -----------------------------------------------------------------

    def test_compute_elasticity_safely_handles_zero_expected_result_baselines(self):
        """Verify that zeroed outcome baselines fall back cleanly instead of crashing."""
        kwargs = {
            variable_names.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE: 10.0,
            variable_names.COMPARATIVE_STATICS_MIN_RESULT: 100.0,
            variable_names.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE: 20.0,
            variable_names.COMPARATIVE_STATICS_EXPECTED_RESULT: 0.0,  # Zero base trigger
            variable_names.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE: 30.0,
            variable_names.COMPARATIVE_STATICS_MAX_RESULT: 200.0,
        }

        elasticity = compute_elasticity(**kwargs)
        self.assertEqual(elasticity, 0.0)

    def test_compute_elasticity_safely_handles_flat_variable_boundaries(self):
        """Verify that stagnant variable ranges catch zero delta structures cleanly."""
        kwargs = {
            variable_names.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE: 5.0,  # Flat limits matched
            variable_names.COMPARATIVE_STATICS_MIN_RESULT: 50.0,
            variable_names.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE: 5.0,
            variable_names.COMPARATIVE_STATICS_EXPECTED_RESULT: 50.0,
            variable_names.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE: 5.0,  # Flat limits matched
            variable_names.COMPARATIVE_STATICS_MAX_RESULT: 50.0,
        }

        elasticity = compute_elasticity(**kwargs)
        self.assertEqual(elasticity, 0.0)


if __name__ == "__main__":
    unittest.main()
