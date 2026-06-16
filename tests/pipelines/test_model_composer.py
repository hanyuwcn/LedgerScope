import unittest
from unittest.mock import patch

# Assuming Auditors are now available to test as well
from src.auditors import PriceArchitectureAuditor
from src.models import (
    AdvertisingEfficiencyGoogleSearchModel,
    GrossProfitModel,
    FreeCashFlowModel,
    DepreciationModel, CostOfGoodsSoldModel, RevenueModel
)
# Updated imports to reflect the new structure
from src.pipelines import PipelineComposer

# 1. Define a stable mock dictionary
MOCK_PIPELINE_CONFIGS = {
    "marketing_roi_analysis": [
        "advertising_efficiency_google_search",
        "cogs",
        "revenue",
        "gross_profit"
    ]
}


# 2. Patch the configuration boundary at the correct new location
@patch("src.pipelines.model_composer.DYNAMIC_PIPELINE_CONFIGS", MOCK_PIPELINE_CONFIGS)
class TestPipelineComposerEngine(unittest.TestCase):

    # =========================================================================
    # COMPOSER ENGINE TESTS
    # =========================================================================

    def test_case_a_baseline_standard_template(self):
        """Verify the standard blueprint resolves and instantiates natively."""
        base_pipeline = PipelineComposer.build_named_scenario("marketing_roi_analysis")

        self.assertEqual(len(base_pipeline), 4)
        self.assertIsInstance(base_pipeline[0], AdvertisingEfficiencyGoogleSearchModel)
        self.assertIsInstance(base_pipeline[3], GrossProfitModel)

    def test_case_b_single_add_on_mixin(self):
        """Verify appending a node (including auditors) on the fly."""
        # Mixing in an auditor to the model pipeline
        marketing_audit_pipeline = PipelineComposer.build_named_scenario(
            "marketing_roi_analysis",
            "price_architecture_auditor"
        )

        self.assertEqual(len(marketing_audit_pipeline), 5)
        self.assertIsInstance(marketing_audit_pipeline[4], PriceArchitectureAuditor)

    def test_case_c_multiple_stacked_complex_mixins(self):
        """Verify stacking components with deduplication guards."""
        advanced_pipeline = PipelineComposer.build_named_scenario(
            "marketing_roi_analysis",
            "free_cash_flow",
            "depreciation",
            "gross_profit"  # Duplicate guard check
        )

        # Baseline (4) + FreeCashFlow (1) + Depreciation (1) = 7 total
        self.assertEqual(len(advanced_pipeline), 6)
        self.assertIsInstance(advanced_pipeline[4], FreeCashFlowModel)
        self.assertIsInstance(advanced_pipeline[5], DepreciationModel)

    def test_case_d_merge_multiple_scenarios(self):
        """Verify that multiple scenarios can be merged with deduplication."""
        # Define a mock configuration with two distinct scenarios
        merged_mock_configs = {
            "scenario_a": ["advertising_efficiency_google_search", "cogs"],
            "scenario_b": ["cogs", "revenue"]  # Note: 'cogs' is a duplicate
        }

        # Patch the config to use our new multi-scenario mock
        with patch("src.pipelines.model_composer.DYNAMIC_PIPELINE_CONFIGS", merged_mock_configs):
            merged_pipeline = PipelineComposer.build_merged_scenarios(["scenario_a", "scenario_b"])

            # Expected: ['advertising_efficiency_google_search', 'cogs', 'total_cost']
            # Length should be 3, not 4 (due to deduplication)
            self.assertEqual(len(merged_pipeline), 3)
            self.assertIsInstance(merged_pipeline[0], AdvertisingEfficiencyGoogleSearchModel)
            self.assertIsInstance(merged_pipeline[1], CostOfGoodsSoldModel)
            self.assertIsInstance(merged_pipeline[2], RevenueModel)

    # =========================================================================
    # ERROR BOUNDARY VALIDATION
    # =========================================================================

    def test_composer_invalid_registry_key_error(self):
        """Verify engine throws an explicit KeyError when an unregistered key is parsed."""
        with self.assertRaises(KeyError) as context:
            PipelineComposer.build_pipeline_by_keys(["invalid_ghost_node"])

        self.assertIn("Key 'invalid_ghost_node' is not registered in MODEL_REGISTRY", str(context.exception))

    def test_composer_invalid_scenario_name_error(self):
        """Verify engine throws an explicit ValueError when an unknown scenario is targeted."""
        with self.assertRaises(ValueError) as context:
            PipelineComposer.build_named_scenario("non_existent_scenario")

        # This will tell you exactly what the error message was if it fails
        expected_msg = "Scenario 'non_existent_scenario' does not exist."
        self.assertEqual(str(context.exception), expected_msg)

    def test_merge_invalid_scenario_error(self):
        """Verify that merging an invalid scenario name raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            PipelineComposer.build_merged_scenarios(["ghost_scenario", "non_existent_scenario"])

        expected_msg = "Scenario 'ghost_scenario' does not exist."
        self.assertEqual(str(context.exception), expected_msg)


if __name__ == '__main__':
    unittest.main()
