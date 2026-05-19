import unittest

from src.config import variable_names
from src.engine import evaluate_chained_models
from src.models import AdvertisingEfficiencyModel, CostOfGoodsSoldModel, TotalCostModel


class TestEvaluateChainedModelsPipeline(unittest.TestCase):

    def setUp(self):
        """Set up fresh, reusable model instances for clean pipeline configurations."""
        self.ads_model = AdvertisingEfficiencyModel()
        self.cogs_model = CostOfGoodsSoldModel()
        self.cost_model = TotalCostModel()

    # -----------------------------------------------------------------
    # 1. HAPPY PATH: MULTI-STAGE STEP CASCADING
    # -----------------------------------------------------------------

    def test_evaluate_chained_models_happy_path_cascades_state_perfectly(self):
        """Verify metrics accumulate chronologically across sequential model dependencies."""
        # Baseline primitives matching model calculations explicitly
        baseline_inputs = {
            variable_names.COST_ADVERTISING: 5000.0,
            variable_names.COST_CONVERSION_RATE: 0.10,  # 10% conversion rate
            variable_names.COST_CPA: 20.0,  # $20 per acquisition
            variable_names.FINANCE_USD_TO_RMB: 1.0,  # No conversion shift
            variable_names.DEAL_ITEMS_PER_ORDER: 2.0,  # 2 items per transaction
            variable_names.DEAL_PURCHASING_PRICE: 15.0,  # $15 base purchase price
            variable_names.COST_SHIPPING: 500.0  # Operational shipping cost
        }

        # Step-by-step mathematical trace:
        # 1. AdvertisingEfficiencyModel:
        #    Orders = (5000.0 * 0.10) / (20.0 * 1.0) = 500.0 / 20.0 = 25.0 Orders
        # 2. CostOfGoodsSoldModel:
        #    Cogs = 15.0 (PurchasingPrice) * 25.0 (Orders) * 2.0 (ItemsPerOrder) = 750.0
        # 3. TotalCostModel:
        #    Cost = 750.0 (Cogs) + 5000.0 (AdvertisingCost) + 500.0 (ShippingCost) = 6250.0

        pipeline = [self.ads_model, self.cogs_model, self.cost_model]

        # Execute the pipeline with raw numeric inputs directly
        final_state = evaluate_chained_models(baseline_inputs, pipeline)

        # Assert upstream calculations were injected perfectly into downstream layers
        self.assertEqual(final_state[variable_names.DEAL_ORDERS], 25.0)
        self.assertEqual(final_state[variable_names.COST_COGS], 750.0)
        self.assertEqual(final_state[variable_names.COST], 6250.0)

        # Verify baseline entries remain correctly preserved inside the dictionary matrix
        self.assertEqual(final_state[variable_names.COST_ADVERTISING], 5000.0)
        self.assertEqual(final_state[variable_names.DEAL_PURCHASING_PRICE], 15.0)

    # -----------------------------------------------------------------
    # 2. IDEMPOTENCY & STATE ISOLATION (SHALLOW COPY GUARD)
    # -----------------------------------------------------------------

    def test_pipeline_execution_confines_mutations_and_does_not_pollute_input_state(self):
        """Verify baseline_inputs dictionary remains unmutated (isolated) after a pipeline run."""
        baseline_inputs = {
            variable_names.COST_ADVERTISING: 2000.0,
            variable_names.COST_CONVERSION_RATE: 0.05,
            variable_names.COST_CPA: 10.0,
            variable_names.DEAL_ITEMS_PER_ORDER: 1.0,
            variable_names.DEAL_PURCHASING_PRICE: 10.0
        }

        # Capture reference snapshots of keys to check for mutations post-run
        original_keys = set(baseline_inputs.keys())
        pipeline = [self.ads_model, self.cogs_model]

        # Execute processing loop
        final_state = evaluate_chained_models(baseline_inputs, pipeline)

        # Verify output state grew with calculation results
        self.assertIn(variable_names.COST_COGS, final_state)

        # Hard check: Verify original input dictionary mapping matrix is completely untouched
        self.assertEqual(set(baseline_inputs.keys()), original_keys)
        self.assertNotIn(variable_names.COST_COGS, baseline_inputs)
        self.assertNotIn(variable_names.DEAL_ORDERS, baseline_inputs)

    # -----------------------------------------------------------------
    # 3. EDGE CASES: CORNER VARIABLES & VALIDATION FAILURES
    # -----------------------------------------------------------------

    def test_evaluate_chained_models_handles_empty_pipeline_safely(self):
        """Verify passing an empty sequence returns a clean copy of original input states."""
        baseline_inputs = {
            variable_names.COST_ADVERTISING: 1500.0,
            variable_names.DEAL_PURCHASING_PRICE: 45.0
        }

        final_state = evaluate_chained_models(baseline_inputs, model_pipeline=[])

        # Assert data content is completely identical but represents a unique dictionary object
        self.assertEqual(final_state, baseline_inputs)
        self.assertIsNot(final_state, baseline_inputs)

    def test_pipeline_raises_key_error_and_halts_when_required_variable_is_missing(self):
        """Verify model validation fails fast if required pipeline dependencies are absent."""
        # Missing required parameter: variable_names.COST_CPA
        invalid_inputs = {
            variable_names.COST_ADVERTISING: 5000.0,
            variable_names.COST_CONVERSION_RATE: 0.10
        }

        # The pipeline should immediately crash inside AdvertisingEfficiencyModel's .evaluate() step
        pipeline = [self.ads_model, self.cogs_model]

        with self.assertRaises(KeyError):
            evaluate_chained_models(invalid_inputs, pipeline)

    def test_downstream_failure_bubbles_up_if_upstream_fails_to_provide_outputs(self):
        """Verify downstream models fail predictably if upstream steps don't supply their requirements."""
        # Inputs contain raw variables for Ads and COGS, but missing things for downstream TotalCost
        baseline_inputs = {
            variable_names.COST_ADVERTISING: 1000.0,
            variable_names.COST_CONVERSION_RATE: 0.05,
            variable_names.COST_CPA: 10.0,
            variable_names.DEAL_ITEMS_PER_ORDER: 3.0,
            variable_names.DEAL_PURCHASING_PRICE: 5.0
            # Omitting variable_names.COST_COGS intentionally!
        }

        # If we skip running CostOfGoodsSoldModel, TotalCostModel will instantly blow up
        # because its mandatory required variable 'Cogs' was never injected.
        broken_pipeline = [self.ads_model, self.cost_model]

        with self.assertRaises(KeyError):
            evaluate_chained_models(baseline_inputs, broken_pipeline)


if __name__ == "__main__":
    unittest.main()
