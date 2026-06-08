import unittest
from unittest.mock import patch

from src.models import (
    PipelineComposer,
    AdvertisingEfficiencyGoogleSearchModel,
    CostOfGoodsSoldModel,
    TotalCostModel,
    RevenueModel,
    ProfitModel,
    FreeCashFlowModel,
    DepreciationModel,
    CapitalExpenditureModel
)

# 1. Define a completely stable, isolated mock dictionary for testing
MOCK_PIPELINE_CONFIGS = {
    "marketing_roi_analysis": [
        "advertising_efficiency_google_search",
        "cogs",
        "total_cost",
        "revenue",
        "profit"
    ]
}


# 2. Patch the configuration boundary at the class level so every test uses the mock
@patch("src.models.composer.model_composer.DYNAMIC_PIPELINE_CONFIGS", MOCK_PIPELINE_CONFIGS)
class TestPipelineComposerEngine(unittest.TestCase):

    # =========================================================================
    # COMPOSER ENGINE TESTS: THE THREE CORE ORCHESTRATION USE CASES
    # =========================================================================

    def test_case_a_baseline_standard_template(self):
        """Case A: Verify the standard blueprint resolves and instantiates natively."""
        base_pipeline = PipelineComposer.build_named_scenario("marketing_roi_analysis")

        # "marketing_roi_analysis" has exactly 5 base models in our mock config
        self.assertEqual(len(base_pipeline), 5)
        self.assertIsInstance(base_pipeline[0], AdvertisingEfficiencyGoogleSearchModel)
        self.assertIsInstance(base_pipeline[1], CostOfGoodsSoldModel)
        self.assertIsInstance(base_pipeline[2], TotalCostModel)
        self.assertIsInstance(base_pipeline[3], RevenueModel)
        self.assertIsInstance(base_pipeline[4], ProfitModel)

    def test_case_b_single_add_on_mixin(self):
        """Case B: Verify appending a single add-on class like FreeCashFlowModel on the fly."""
        marketing_fcf_pipeline = PipelineComposer.build_named_scenario(
            "marketing_roi_analysis",
            "free_cash_flow"
        )

        # Length expands to 6 with FreeCashFlowModel safely attached at the end
        self.assertEqual(len(marketing_fcf_pipeline), 6)
        self.assertIsInstance(marketing_fcf_pipeline[5], FreeCashFlowModel)

    def test_case_c_multiple_stacked_complex_mixins(self):
        """Case C: Verify stacking multiple deep modular components on the fly with deduplication guards."""
        advanced_pipeline = PipelineComposer.build_named_scenario(
            "marketing_roi_analysis",
            "free_cash_flow",
            "depreciation",
            "capital_expenditure",
            "profit"  # Duplicate guard check: 'profit' is already in our base template!
        )

        # Baseline (5) + FreeCashFlow (1) + Depreciation (1) + Capex (1) = 8 total.
        self.assertEqual(len(advanced_pipeline), 8)
        self.assertIsInstance(advanced_pipeline[5], FreeCashFlowModel)
        self.assertIsInstance(advanced_pipeline[6], DepreciationModel)
        self.assertIsInstance(advanced_pipeline[7], CapitalExpenditureModel)

    # =========================================================================
    # EDGE CASE & ERROR BOUNDARY VALIDATION
    # =========================================================================

    def test_build_pipeline_by_keys_raw_instantiation(self):
        """Verify explicit raw string key arrays convert cleanly to components."""
        target_keys = ["advertising_efficiency_google_search", "cogs"]
        pipeline = PipelineComposer.build_pipeline_by_keys(target_keys)

        self.assertEqual(len(pipeline), 2)
        self.assertIsInstance(pipeline[0], AdvertisingEfficiencyGoogleSearchModel)
        self.assertIsInstance(pipeline[1], CostOfGoodsSoldModel)

    def test_composer_invalid_registry_key_error(self):
        """Verify engine throws an explicit KeyError when an unregistered key is parsed."""
        with self.assertRaises(KeyError) as context:
            PipelineComposer.build_pipeline_by_keys(["invalid_ghost_model"])

        self.assertIn("not registered in MODEL_REGISTRY", str(context.exception))

    def test_composer_invalid_scenario_name_error(self):
        """Verify engine throws an explicit ValueError when an unknown scenario name is targeted."""
        with self.assertRaises(ValueError) as context:
            PipelineComposer.build_named_scenario("non_existent_scenario")

        self.assertIn("does not exist", str(context.exception))


if __name__ == '__main__':
    unittest.main()
