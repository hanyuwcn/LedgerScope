import unittest

from src.analysis.break_even_analysis import break_even_analysis
from src.config import variable_names, settings
from src.models import AdvertisingEfficiencyModel, CostOfGoodsSoldModel, TotalCostModel
from src.variables import (AdvertisingCost, ConversionRate, CostPerAcquisition,
                           USDToRMB, ItemsPerOrder, PurchasingPrice, Cost)


class TestBreakEvenAnalysis(unittest.TestCase):

    def setUp(self):
        """Build the raw business pipeline and baseline operational variables."""
        self.pipeline = [
            AdvertisingEfficiencyModel(),
            CostOfGoodsSoldModel(),
            TotalCostModel()
        ]

        # Force range subdivisions to a deterministic 3 steps for trace calculations:
        # [0.05, 0.10, 0.15]
        settings.NUMS_IN_RANGE = 3

        # Populate direct production variable configurations
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
    # 1. PRECISION VALIDATION: NATURAL CROSSOVER (POSITIVE IMPACT)
    # -----------------------------------------------------------------

    def test_break_even_precision_on_positive_impact_variable(self):
        """Verify natural break-even calculation for variables that scale metrics positively."""
        # Baseline State Metrics:
        #   Advertising = 5000.0, ConversionRate = 0.10
        #   Total Cost = 6250.0 (Expected Result)
        #
        # Isolated Search Range for ConversionRate (3 Steps): [0.05, 0.10, 0.15]
        #   Step 1 (0.05) -> Total Cost = 5875.0
        #   Step 2 (0.10) -> Total Cost = 6250.0
        #   Step 3 (0.15) -> Total Cost = 6625.0
        #
        # Set Target Goal = 6000.0 total cost buffer
        selected_variables = [variable_names.COST_CONVERSION_RATE]
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.COST,
            goal=6000.0
        )

        self.assertEqual(len(reports), 1)
        report = reports[0]

        self.assertEqual(report[variable_names.BREAK_EVEN_VARIABLE_NAME], variable_names.COST_CONVERSION_RATE)
        self.assertEqual(report["feasibility_status"], "CROSSOVER_FOUND")
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_EXPECTED_VARIABLE_VALUE], 0.10)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_EXPECTED_RESULT], 6250.0)

        # First step exceeding or meeting 6000.0 is Step 2 (0.10 -> 6250.0)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE], 0.10)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT], 6250.0)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE], 0.0)

    # -----------------------------------------------------------------
    # 2. PRECISION VALIDATION: UNREACHABLE DEFICIT MARGIN (< 0)
    # -----------------------------------------------------------------

    def test_break_even_handles_negative_margin_when_deficit_exists(self):
        """Verify safety margin drops below zero cleanly if expected performance baseline is in deficit."""
        # Set a target goal of 6500.0.
        # Range outputs: [5875.0, 6250.0, 6625.0]
        # Step 3 (0.15 -> 6625.0) hits this goal, but our expected baseline (0.10) is currently below it.
        selected_variables = [variable_names.COST_CONVERSION_RATE]
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.COST,
            goal=6500.0
        )

        report = reports[0]
        self.assertEqual(report["feasibility_status"], "CROSSOVER_FOUND")
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE], 0.15)

        # Unified Directional Safety Margin Formula Check:
        # 1 * (0.10 - 0.15) / 0.10 = -0.50 (-50% deficit runway)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE], -0.50)

    # -----------------------------------------------------------------
    # 3. CORNER CASE: ALL SIMULATED VALUES MEET GOAL
    # -----------------------------------------------------------------

    def test_boundary_handling_when_all_simulated_values_meet_goal(self):
        """Verify business rules cap metrics to the smallest surplus if goal is consistently met."""
        # Set a low benchmark target goal = 5000.0
        # All simulated range outputs [5875.0, 6250.0, 6625.0] sit cleanly above 5000.0.
        selected_variables = [variable_names.COST_CONVERSION_RATE]
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.COST,
            goal=5000.0
        )

        report = reports[0]
        self.assertEqual(report["feasibility_status"], "ALWAYS_FEASIBLE")

        # Business Rule Requirement: For increasing trends, pick index 0 (smallest absolute driver value)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE], 0.05)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT], 5875.0)

        # Safety Margin: (0.10 - 0.05) / 0.10 = 0.50 (+50% buffer)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE], 0.50)

    # -----------------------------------------------------------------
    # 4. CORNER CASE: NO SIMULATED VALUES MEET GOAL
    # -----------------------------------------------------------------

    def test_boundary_handling_when_no_simulated_values_meet_goal(self):
        """Verify business rules capture the closest maximum performance driver if goal is unreachable."""
        # Set a massive hurdle benchmark target goal = 9000.0
        # All simulated range outputs [5875.0, 6250.0, 6625.0] fail to reach 9000.0.
        selected_variables = [variable_names.COST_CONVERSION_RATE]
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.COST,
            goal=9000.0
        )

        report = reports[0]
        self.assertEqual(report["feasibility_status"], "UNREACHABLE")

        # Business Rule Requirement: Capture the maximum boundary driving the largest result closest to target
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE], 0.15)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT], 6625.0)

    # -----------------------------------------------------------------
    # 5. EDGE CASE: VALIDATION WRAPPERS AND EXCEPTIONS
    # -----------------------------------------------------------------

    def test_analysis_aborts_when_isolated_variable_is_missing_from_registry(self):
        """Verify exception flows bubble up immediately if an target evaluation key is missing."""
        with self.assertRaises(Exception):
            break_even_analysis(
                variables=self.variables,
                selected_variables=["NON_EXISTENT_OPERATIONAL_VARIABLE"],
                model_pipeline=self.pipeline,
                output_name=variable_names.COST
            )

    def test_analysis_aborts_when_pipeline_topological_sequence_breaks(self):
        """Verify topological sequence validation rules catch an un-ordered model flow sequence."""
        scrambled_pipeline = [
            TotalCostModel(),
            CostOfGoodsSoldModel(),
            AdvertisingEfficiencyModel()
        ]

        with self.assertRaises(Exception):
            break_even_analysis(
                variables=self.variables,
                selected_variables=[variable_names.COST_CONVERSION_RATE],
                model_pipeline=scrambled_pipeline,
                output_name=variable_names.COST
            )


if __name__ == "__main__":
    unittest.main()
