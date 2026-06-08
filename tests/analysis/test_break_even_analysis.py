import unittest
from unittest.mock import MagicMock

from src.analysis.break_even_analysis import break_even_analysis
from src.config import variable_names, settings
from src.models import CostOfGoodsSoldModel, TotalCostModel
from src.variables import (
    AdvertisingCost, GoogleSearchConversionRate, GoogleSearchCostPerClick,
    USDToRMB, UnitsPerOrder, UnitExw, Cost
)


class TestBreakEvenAnalysis(unittest.TestCase):

    def setUp(self):
        """Build the raw business pipeline and baseline operational variables."""
        self.pipeline = [
            CostOfGoodsSoldModel(),
            TotalCostModel()
        ]

        # Force range subdivisions to a deterministic 3 steps for trace calculations:
        # [0.05, 0.10, 0.15]
        settings.NUMS_IN_RANGE = 3

        # Populate direct production variable configurations
        self.variables = {
            variable_names.ADVERTISING_COST: AdvertisingCost(min=4000.0, max=6000.0, exp=5000.0),
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: GoogleSearchConversionRate(min=0.05, max=0.15, exp=0.10),
            variable_names.CPL_GOOGLE_SEARCH: GoogleSearchCostPerClick(exp=20.0),
            variable_names.USD_TO_RMB: USDToRMB(exp=1.0),
            variable_names.UNITS_PER_ORDER: UnitsPerOrder(min=2.0, max=2.0),
            variable_names.UNIT_EXW: UnitExw(min=15.0, max=15.0),
            variable_names.SHIPPING_COST: Cost(exp=500.0),
            variable_names.ORDERS: Cost(exp=25.0)  # Standard runner baseline injection driving 25 units
        }

        # Mock the specific isolated variable's range loop method to return a predictable,
        # linear sequence matching the original test math parameters: [0.05, 0.10, 0.15]
        self.variables[variable_names.CONVERSION_RATE_GOOGLE_SEARCH].get_range_values = MagicMock(
            return_value=[0.05, 0.10, 0.15]
        )

    # -----------------------------------------------------------------
    # 1. PRECISION VALIDATION: NATURAL CROSSOVER (POSITIVE IMPACT)
    # -----------------------------------------------------------------

    def test_break_even_precision_on_positive_impact_variable(self):
        """Verify natural break-even calculation for variables that scale metrics positively."""
        # Baseline State Metrics:
        #   Orders = 25.0, UnitExw = 15.0, UnitsPerOrder = 2.0 -> COGS = 750.0
        #   AdvertisingCost = 5000.0, ShippingCost = 500.0
        #   Total Cost = 6250.0 (Expected Result)
        #
        # Isolated Search Range for CONVERSION_RATE_GOOGLE_SEARCH (3 Steps): [0.05, 0.10, 0.15]
        #   We modify the underlying Orders directly inside the test sweep matrix to trace values:
        #   Step 1 (0.05) -> Injected Orders baseline adjusts to 12.5 -> Cost = 5875.0
        #   Step 2 (0.10) -> Injected Orders baseline adjusts to 25.0 -> Cost = 6250.0
        #   Step 3 (0.15) -> Injected Orders baseline adjusts to 37.5 -> Cost = 6625.0
        #
        # Set Target Goal = 6000.0 total cost buffer

        # Dynamically patch variable mock references during evaluation sweep execution
        original_sweep = self.variables[variable_names.CONVERSION_RATE_GOOGLE_SEARCH].get_range_values

        selected_variables = [variable_names.CONVERSION_RATE_GOOGLE_SEARCH]
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.COST,
            goal=6000.0
        )

        self.assertEqual(len(reports), 1)
        report = reports[0]

        self.assertEqual(report[variable_names.BREAK_EVEN_VARIABLE_NAME], variable_names.CONVERSION_RATE_GOOGLE_SEARCH)
        self.assertEqual(report["FeasibilityStatus"], "CROSSOVER_FOUND")
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
        selected_variables = [variable_names.CONVERSION_RATE_GOOGLE_SEARCH]
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.COST,
            goal=6500.0
        )

        report = reports[0]
        self.assertEqual(report["FeasibilityStatus"], "CROSSOVER_FOUND")
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
        selected_variables = [variable_names.CONVERSION_RATE_GOOGLE_SEARCH]
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.COST,
            goal=5000.0
        )

        report = reports[0]
        self.assertEqual(report["FeasibilityStatus"], "ALWAYS_FEASIBLE")

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
        selected_variables = [variable_names.CONVERSION_RATE_GOOGLE_SEARCH]
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.COST,
            goal=9000.0
        )

        report = reports[0]
        self.assertEqual(report["FeasibilityStatus"], "UNREACHABLE")

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
            CostOfGoodsSoldModel()
        ]

        with self.assertRaises(Exception):
            break_even_analysis(
                variables=self.variables,
                selected_variables=[variable_names.CONVERSION_RATE_GOOGLE_SEARCH],
                model_pipeline=scrambled_pipeline,
                output_name=variable_names.COST
            )


if __name__ == "__main__":
    unittest.main()
