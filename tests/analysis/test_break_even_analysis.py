import unittest
from unittest.mock import MagicMock

from src.analysis.break_even_analysis import break_even_analysis
from src.config import variable_names, settings, messages
from src.models import DeductionRateModel, UnitFobModel
from src.variables import UnitRetail, DeductionRate, ShippingRate, TariffRate, ChannelMarkupRate, UnitFob


class TestBreakEvenAnalysisIntegration(unittest.TestCase):

    def setUp(self):
        """Build the raw business pipeline and baseline operational pricing variables."""
        # Realistic top-down cascade pricing models:
        # 1. DeductionRateModel outputs DEDUCTION_RATE by summing up shipping, tariff, and markup.
        # 2. UnitFobModel outputs UNIT_FOB = UNIT_RETAIL * (1 - DEDUCTION_RATE).
        self.pipeline = [
            DeductionRateModel(),
            UnitFobModel()
        ]

        # Force range subdivisions to a deterministic 3 steps for trace calculations
        self.old_nums_in_range = settings.NUMS_IN_RANGE
        settings.NUMS_IN_RANGE = 3

        # Populate direct production variable configurations based on your matrix specs
        self.variables = {
            variable_names.UNIT_RETAIL: UnitRetail(min=5000.0, exp=8000.0, max=12000.0),
            variable_names.SHIPPING_RATE: ShippingRate(min=0.04, exp=0.08, max=0.15),
            variable_names.TARIFF_RATE: TariffRate(min=0.15, exp=0.25, max=0.35),
            variable_names.CHANNEL_MARKUP_RATE: ChannelMarkupRate(min=0.15, exp=0.20, max=0.30),
            variable_names.DEDUCTION_RATE: DeductionRate(min=0.25, exp=0.42, max=0.62),
            variable_names.UNIT_FOB: UnitFob(min=3000.0, exp=4500.0, max=6000.0)
        }

        # Keeping a single MagicMock ONLY to force a clean, deterministic 3-step slice
        # on the evaluated target variable to keep math trackable without breaking its structure.
        # Range steps map to: [5000.0, 8000.0, 11000.0]
        self.variables[variable_names.UNIT_RETAIL].get_range_values = MagicMock(
            return_value=[5000.0, 8000.0, 11000.0]
        )

    def tearDown(self):
        """Restore global settings footprint."""
        settings.NUMS_IN_RANGE = self.old_nums_in_range

    # -----------------------------------------------------------------
    # 1. PRECISION VALIDATION: NATURAL CROSSOVER (POSITIVE IMPACT)
    # -----------------------------------------------------------------

    def test_break_even_precision_on_positive_impact_variable(self):
        """Verify natural break-even calculation for variables that scale metrics positively.

        Baseline State Metrics:
          Expected Rates: Shipping (0.08) + Tariff (0.25) + Markup (0.20) -> DeductionRate = 0.53
          Expected UnitFob (at Retail 8000) -> 8000 * (1 - 0.53) = 3760.0

        Sweep on UNIT_RETAIL steps: [5000.0, 8000.0, 11000.0]
          Step 1 (5000.0) -> UnitFob = 5000 * 0.47 = 2350.0
          Step 2 (8000.0) -> UnitFob = 8000 * 0.47 = 3760.0
          Step 3 (11000.0) -> UnitFob = 11000 * 0.47 = 5170.0

        Target Goal = 3500.0 UnitFob threshold value
        """
        selected_variables = [variable_names.UNIT_RETAIL]
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.UNIT_FOB,
            goal=3500.0
        )

        self.assertEqual(len(reports), 1)
        report = reports[0]

        self.assertEqual(report[variable_names.BREAK_EVEN_VARIABLE_NAME], variable_names.UNIT_RETAIL)
        self.assertEqual(report[variable_names.BREAK_EVEN_FEASIBILITY_STATUS],
                         messages.BREAK_EVEN_FEASIBILITY_STATUS_CROSSOVER)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_EXPECTED_VARIABLE_VALUE], 8000.0)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_EXPECTED_RESULT], 3760.0)

        # First step exceeding or meeting 3500.0 is Step 2 (8000.0 -> 3760.0)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE], 8000.0)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT], 3760.0)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE], 0.0)

    # -----------------------------------------------------------------
    # 2. PRECISION VALIDATION: DEFICIT MARGIN RUNWAY
    # -----------------------------------------------------------------

    def test_break_even_handles_negative_margin_when_deficit_exists(self):
        """Verify safety margin drops below zero cleanly if expected performance baseline is in deficit.

        Target Goal = 4000.0.
        Our expected outcome (3760.0) sits below the target hurdle.
        Step 3 (11000.0 -> 5170.0) breaks through the goal hurdle cleanly.
        """
        selected_variables = [variable_names.UNIT_RETAIL]
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.UNIT_FOB,
            goal=4000.0
        )

        report = reports[0]
        self.assertEqual(report[variable_names.BREAK_EVEN_FEASIBILITY_STATUS],
                         messages.BREAK_EVEN_FEASIBILITY_STATUS_CROSSOVER)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE], 11000.0)

        # Unified Directional Safety Margin Formula Check:
        # 1 * (Expected_Val - Threshold_Val) / Expected_Val -> (8000 - 11000) / 8000 = -0.375
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE], -0.375)

    # -----------------------------------------------------------------
    # 3. CORNER CASE: ALL SIMULATED VALUES MEET GOAL
    # -----------------------------------------------------------------

    def test_boundary_handling_when_all_simulated_values_meet_goal(self):
        """Verify business rules cap metrics to the smallest surplus if goal is consistently met.

        Set a low benchmark target goal = 1000.0.
        All simulated outcomes [2350.0, 3760.0, 5170.0] clear 1000.0 smoothly.
        """
        selected_variables = [variable_names.UNIT_RETAIL]
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.UNIT_FOB,
            goal=1000.0
        )

        report = reports[0]
        self.assertEqual(report[variable_names.BREAK_EVEN_FEASIBILITY_STATUS],
                         messages.BREAK_EVEN_FEASIBILITY_ALWAYS_FEASIBLE)

        # For positive trends, pick index 0 to calculate safety margin from minimum driving edge
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE], 5000.0)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT], 2350.0)

        # Safety Margin check: (8000 - 5000) / 8000 = 0.375 (+37.5% buffer)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE], 0.375)

    # -----------------------------------------------------------------
    # 4. CORNER CASE: NO SIMULATED VALUES MEET GOAL
    # -----------------------------------------------------------------

    def test_boundary_handling_when_no_simulated_values_meet_goal(self):
        """Verify business rules capture the closest maximum performance driver if goal is unreachable.

        Set an unreachable target goal = 20000.0.
        """
        selected_variables = [variable_names.UNIT_RETAIL]
        reports = break_even_analysis(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.UNIT_FOB,
            goal=20000.0
        )

        report = reports[0]
        self.assertEqual(report[variable_names.BREAK_EVEN_FEASIBILITY_STATUS],
                         messages.BREAK_EVEN_FEASIBILITY_UNREACHABLE)

        # Captures highest edge boundary that yields the value closest to the target
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE], 11000.0)
        self.assertAlmostEqual(report[variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT], 5170.0)

    # -----------------------------------------------------------------
    # 5. EDGE CASE: VALIDATION WRAPPERS AND TOPOLOGY EXCEPTIONS
    # -----------------------------------------------------------------

    def test_analysis_aborts_when_isolated_variable_is_missing_from_registry(self):
        """Verify exception flows bubble up immediately if a target evaluation key is missing."""
        with self.assertRaises(KeyError):
            break_even_analysis(
                variables=self.variables,
                selected_variables=["NON_EXISTENT_VALUATION_KEY"],
                model_pipeline=self.pipeline,
                output_name=variable_names.UNIT_FOB
            )

    def test_analysis_aborts_when_pipeline_topological_sequence_breaks(self):
        """Verify sequence validation rules abort when an execution block lacks a required upstream input."""

        # Create a pipeline missing the required upstream dependencies altogether,
        # which will cleanly throw a validation error during checking phases.
        class BrokenDummyModel(UnitFobModel):
            def __init__(self):
                super().__init__()
                # Explicitly demand an unresolvable required upstream variable
                self._required_variables = ["STRICTLY_MISSING_UPSTREAM_DEPENDENCY"]

        scrambled_pipeline = [BrokenDummyModel()]

        with self.assertRaises(KeyError):
            break_even_analysis(
                variables=self.variables,
                selected_variables=[variable_names.UNIT_RETAIL],
                model_pipeline=scrambled_pipeline,
                output_name=variable_names.UNIT_FOB
            )


if __name__ == "__main__":
    unittest.main()