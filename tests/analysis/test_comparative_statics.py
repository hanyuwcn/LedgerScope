import unittest

from src.analysis import comparative_statics
from src.config import variable_names
from src.models import DeductionRateModel, UnitFobModel
from src.variables import UnitRetail, DeductionRate, ShippingRate, TariffRate, ChannelMarkupRate, UnitFob


class TestComparativeStaticsIntegration(unittest.TestCase):

    def setUp(self):
        """Build the raw business pipeline and baseline operational variables for comparative testing."""
        # Pipeline mapping cascade:
        # 1. DeductionRateModel sums Shipping + Tariff + ChannelMarkup
        # 2. UnitFobModel calculates UnitRetail * (1 - DeductionRate)
        self.pipeline = [
            DeductionRateModel(),
            UnitFobModel()
        ]

        # Explicitly build inputs matching your fixed metrics profile ranges
        # Expected baseline combination: Retail = 8000, Total Deduction = 0.08 + 0.25 + 0.20 = 0.53
        # Expected UnitFob Result = 8000 * (1 - 0.53) = 3760.0
        self.variables = {
            variable_names.UNIT_RETAIL: UnitRetail(min=5000.0, exp=8000.0, max=11000.0),
            variable_names.SHIPPING_RATE: ShippingRate(min=0.08, exp=0.08, max=0.08),
            variable_names.TARIFF_RATE: TariffRate(min=0.25, exp=0.25, max=0.25),
            variable_names.CHANNEL_MARKUP_RATE: ChannelMarkupRate(min=0.20, exp=0.20, max=0.20),
            variable_names.DEDUCTION_RATE: DeductionRate(min=0.25, exp=0.42, max=0.62),
            variable_names.UNIT_FOB: UnitFob(min=3000.0, exp=4500.0, max=6000.0)
        }

    # -----------------------------------------------------------------
    # 1. ACCURACYS: POSITIVE ELASTICITY CHECK (DIRECT SCALING)
    # -----------------------------------------------------------------

    def test_comparative_statics_positive_elasticity_calculation(self):
        """Verify elasticity calculation for a variable that has a direct positive impact on the output."""
        selected_variables = [variable_names.UNIT_RETAIL]

        reports = comparative_statics(
            variables=self.variables,
            selected_variables=selected_variables,
            model_pipeline=self.pipeline,
            output_name=variable_names.UNIT_FOB
        )

        self.assertEqual(len(reports), 1)
        report = reports[0]

        # Structural Assertions
        self.assertEqual(report[variable_names.COMPARATIVE_STATICS_VARIABLE_NAME], variable_names.UNIT_RETAIL)
        self.assertAlmostEqual(report[variable_names.COMPARATIVE_STATICS_MIN_RESULT], 5000.0 * 0.47)  # 2350.0
        self.assertAlmostEqual(report[variable_names.COMPARATIVE_STATICS_EXPECTED_RESULT], 8000.0 * 0.47)  # 3760.0
        self.assertAlmostEqual(report[variable_names.COMPARATIVE_STATICS_MAX_RESULT], 11000.0 * 0.47)  # 5170.0

        # Math Verification of Elasticity:
        # Slope = (5170 - 2350) / (11000 - 5000) = 2820 / 6000 = 0.47
        # Elasticity = 0.47 * (8000 / 3760) = 0.47 * 2.12765957 = 1.0 (Unit Elasticity)
        self.assertAlmostEqual(report[variable_names.COMPARATIVE_STATICS_ELASTICITY], 1.0, places=4)

    # -----------------------------------------------------------------
    # 2. ACCURACYS: NEGATIVE ELASTICITY CHECK (INVERSE SCALING)
    # -----------------------------------------------------------------

    def test_comparative_statics_negative_elasticity_calculation(self):
        """Verify elasticity calculation for a parameter that drives a negative impact on the output."""
        # Unfreeze TARIFF_RATE to check elasticity impacts of macro trade taxes
        self.variables[variable_names.TARIFF_RATE] = TariffRate(min=0.15, exp=0.25, max=0.35)

        # Baseline traces at expected (0.25): Total Deduction = 0.53 -> UnitFob = 3760.0
        # Step Min (0.15): Total Deduction = 0.43 -> UnitFob = 8000 * (1 - 0.43) = 4560.0
        # Step Max (0.35): Total Deduction = 0.63 -> UnitFob = 8000 * (1 - 0.63) = 2960.0

        reports = comparative_statics(
            variables=self.variables,
            selected_variables=[variable_names.TARIFF_RATE],
            model_pipeline=self.pipeline,
            output_name=variable_names.UNIT_FOB
        )

        report = reports[0]

        # Math Verification of Elasticity:
        # Delta Y = 2960.0 - 4560.0 = -1600.0
        # Delta X = 0.35 - 0.15 = 0.20
        # Slope = -1600.0 / 0.20 = -8000.0
        # Elasticity = -8000.0 * (0.25 / 3760.0) = -2000.0 / 3760.0 = -0.53191489
        self.assertAlmostEqual(report[variable_names.COMPARATIVE_STATICS_ELASTICITY], -0.5319, places=4)

    # -----------------------------------------------------------------
    # 3. EDGE CASES: EXPLICIT KEY ERROR TRACKING
    # -----------------------------------------------------------------

    def test_analysis_aborts_with_key_error_when_variable_is_missing(self):
        """Verify KeyError bubbles up if a target isolation key is missing from the registry context."""
        with self.assertRaises(KeyError):
            comparative_statics(
                variables=self.variables,
                selected_variables=["NON_EXISTENT_VALUATION_KEY"],
                model_pipeline=self.pipeline,
                output_name=variable_names.UNIT_FOB
            )

    def test_analysis_aborts_with_key_error_when_pipeline_dependencies_break(self):
        """Verify context evaluation crashes with a KeyError when a block lacks a required input variable."""

        class BrokenDummyModel(UnitFobModel):
            def __init__(self):
                super().__init__()
                self._required_variables = ["STRICTLY_MISSING_UPSTREAM_DEPENDENCY"]

        scrambled_pipeline = [BrokenDummyModel()]

        with self.assertRaises(KeyError):
            comparative_statics(
                variables=self.variables,
                selected_variables=[variable_names.UNIT_RETAIL],
                model_pipeline=scrambled_pipeline,
                output_name=variable_names.UNIT_FOB
            )


if __name__ == "__main__":
    unittest.main()