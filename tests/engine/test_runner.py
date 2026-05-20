import unittest

from src.config import variable_names
from src.engine import evaluate_chained_models, evaluate_stochastic_iteration, evaluate_variable_scenario_sweep, \
    evaluate_expected_scenario
from src.models import AdvertisingEfficiencyModel, CostOfGoodsSoldModel, TotalCostModel
from src.variables import (AdvertisingCost, ConversionRate, CostPerAcquisition,
                           USDToRMB, ItemsPerOrder, PurchasingPrice, Cost)


class TestEvaluateChainedModelsPipeline(unittest.TestCase):
    """Execution engine unit tests verifying direct functional matrix mutations and state isolation."""

    def setUp(self):
        """Set up fresh, reusable model instances for clean pipeline configurations."""
        self.ads_model = AdvertisingEfficiencyModel()
        self.cogs_model = CostOfGoodsSoldModel()
        self.cost_model = TotalCostModel()
        self.pipeline = [self.ads_model, self.cogs_model, self.cost_model]

    # -----------------------------------------------------------------
    # 1. HAPPY PATH: MULTI-STAGE STEP CASCADING
    # -----------------------------------------------------------------

    def test_evaluate_chained_models_happy_path_cascades_state_perfectly(self):
        """Verify metrics accumulate chronologically across sequential model dependencies."""
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
        #    Orders = (5000.0 * 0.10) / (20.0 * 1.0) = 25.0 Orders
        # 2. CostOfGoodsSoldModel:
        #    Cogs = 15.0 (PurchasingPrice) * 25.0 (Orders) * 2.0 (ItemsPerOrder) = 750.0
        # 3. TotalCostModel:
        #    Cost = 750.0 (Cogs) + 5000.0 (AdvertisingCost) + 500.0 (ShippingCost) = 6250.0

        final_state = evaluate_chained_models(baseline_inputs, self.pipeline)

        self.assertEqual(final_state[variable_names.DEAL_ORDERS], 25.0)
        self.assertEqual(final_state[variable_names.COST_COGS], 750.0)
        self.assertEqual(final_state[variable_names.COST], 6250.0)
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

        original_keys = set(baseline_inputs.keys())
        evaluate_chained_models(baseline_inputs, [self.ads_model, self.cogs_model])

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

        self.assertEqual(final_state, baseline_inputs)
        self.assertIsNot(final_state, baseline_inputs)

    def test_pipeline_raises_key_error_and_halts_when_required_variable_is_missing(self):
        """Verify model validation fails fast if required pipeline dependencies are absent."""
        invalid_inputs = {
            variable_names.COST_ADVERTISING: 5000.0,
            variable_names.COST_CONVERSION_RATE: 0.10
        }

        with self.assertRaises(KeyError):
            evaluate_chained_models(invalid_inputs, [self.ads_model, self.cogs_model])

    def test_downstream_failure_bubbles_up_if_upstream_fails_to_provide_outputs(self):
        """Verify downstream models fail predictably if upstream steps don't supply their requirements."""
        baseline_inputs = {
            variable_names.COST_ADVERTISING: 1000.0,
            variable_names.COST_CONVERSION_RATE: 0.05,
            variable_names.COST_CPA: 10.0,
            variable_names.DEAL_ITEMS_PER_ORDER: 3.0,
            variable_names.DEAL_PURCHASING_PRICE: 5.0
        }

        broken_pipeline = [self.ads_model, self.cost_model]

        with self.assertRaises(KeyError):
            evaluate_chained_models(baseline_inputs, broken_pipeline)


class TestEvaluateVariableScenario(unittest.TestCase):
    """Baseline scenario runner validation targeting expected value snapshot execution."""

    def setUp(self):
        """Establish baseline domain models and structured stateful Variable registries."""
        self.pipeline = [
            AdvertisingEfficiencyModel(),
            CostOfGoodsSoldModel(),
            TotalCostModel()
        ]

        self.variables = {
            variable_names.COST_ADVERTISING: AdvertisingCost(expected_value=5000.0),
            variable_names.COST_CONVERSION_RATE: ConversionRate(expected_value=0.10),
            variable_names.COST_CPA: CostPerAcquisition(expected_value=20.0),
            variable_names.FINANCE_USD_TO_RMB: USDToRMB(expected_value=1.0),
            variable_names.DEAL_ITEMS_PER_ORDER: ItemsPerOrder(expected_value=2.0),
            variable_names.DEAL_PURCHASING_PRICE: PurchasingPrice(expected_value=15.0),
            variable_names.COST_SHIPPING: Cost(expected_value=500.0)
        }

    def test_evaluate_variable_scenario_extracts_and_runs_expected_values_perfectly(self):
        """Verify baseline values are extracted correctly from variable instances and cascade properly."""
        # Expected Math Trace:
        # Orders = (5000 * 0.1) / 20 = 25
        # COGS = 15 * 25 * 2 = 750
        # Total Cost = 750 + 5000 + 500 = 6250
        baseline_state = evaluate_expected_scenario(self.variables, self.pipeline)

        self.assertAlmostEqual(baseline_state[variable_names.DEAL_ORDERS], 25.0)
        self.assertAlmostEqual(baseline_state[variable_names.COST], 6250.0)

        # Verify it didn't change the underlying stateful domain objects
        self.assertEqual(self.variables[variable_names.COST_ADVERTISING].get_value(), 5000.0)


class TestEvaluateStochasticIteration(unittest.TestCase):
    """Stochastic engine orchestration validation targeting input split-sampling boundaries."""

    def setUp(self):
        """Establish baseline domain models and structured stateful Variable registries."""
        self.pipeline = [
            AdvertisingEfficiencyModel(),
            CostOfGoodsSoldModel(),
            TotalCostModel()
        ]

        # Injected production objects populated with predictable bounds
        self.variables = {
            variable_names.COST_ADVERTISING: AdvertisingCost(min_value=4000.0, max_value=6000.0, expected_value=5000.0),
            variable_names.COST_CONVERSION_RATE: ConversionRate(min_value=0.05, max_value=0.15, expected_value=0.10),
            variable_names.COST_CPA: CostPerAcquisition(expected_value=20.0),
            variable_names.FINANCE_USD_TO_RMB: USDToRMB(expected_value=1.0),
            variable_names.DEAL_ITEMS_PER_ORDER: ItemsPerOrder(min_value=2.0, max_value=2.0, expected_value=2.0),
            variable_names.DEAL_PURCHASING_PRICE: PurchasingPrice(min_value=15.0, max_value=15.0, expected_value=15.0),
            variable_names.COST_SHIPPING: Cost(expected_value=500.0)
        }

    # -----------------------------------------------------------------
    # 1. ACCURACY OF DATA: MATHEMATICAL PROFILING
    # -----------------------------------------------------------------

    def test_iteration_uses_expected_values_when_no_inputs_are_shuffled(self):
        """
        Verify mathematical accuracy when zero variables are targeted for shuffling.
        The resulting data slice must exactly match baseline operational equations.
        """
        calculated_state = evaluate_stochastic_iteration(
            variables=self.variables,
            shuffled_inputs=[],
            model_pipeline=self.pipeline
        )

        self.assertAlmostEqual(calculated_state[variable_names.DEAL_ORDERS], 25.0, places=4)
        self.assertAlmostEqual(calculated_state[variable_names.COST_COGS], 750.0, places=4)
        self.assertAlmostEqual(calculated_state[variable_names.COST], 6250.0, places=4)

    def test_iteration_randomizes_shuffled_inputs_while_pinning_unshuffled_baselines(self):
        """Verify split-sampling configuration mapping anchors deterministic lines correctly."""
        # Force conversion bounds to static limits to isolate changes strictly to Ad Cost mutations
        self.variables[variable_names.COST_CONVERSION_RATE] = ConversionRate(min_value=0.10, max_value=0.10,
                                                                             expected_value=0.10)

        calculated_state = evaluate_stochastic_iteration(
            variables=self.variables,
            shuffled_inputs=[variable_names.COST_ADVERTISING],
            model_pipeline=self.pipeline
        )

        sampled_ad_cost = calculated_state[variable_names.COST_ADVERTISING]
        self.assertTrue(4000.0 <= sampled_ad_cost <= 6000.0)

        # Cross-model validation tracking using the generated stochastically-sampled entry point
        expected_orders = sampled_ad_cost * 0.005
        expected_cogs = expected_orders * 30.0
        expected_cost = sampled_ad_cost + expected_cogs + 500.0

        self.assertAlmostEqual(calculated_state[variable_names.DEAL_ORDERS], expected_orders, places=4)
        self.assertAlmostEqual(calculated_state[variable_names.COST_COGS], expected_cogs, places=4)
        self.assertAlmostEqual(calculated_state[variable_names.COST], expected_cost, places=4)

    # -----------------------------------------------------------------
    # 2. EDGE CASES: INJECTED TYPES AND BOUNDARIES
    # -----------------------------------------------------------------

    def test_iteration_handles_primitive_inputs_gracefully(self):
        """Verify that raw numerical primitives passed inside variables bypass execution filters without error."""
        self.variables["RAW_TAX_RATE_INJECTION"] = 0.08
        self.variables["ENVIRONMENT_LABEL_STRING"] = "production-simulation-run"

        try:
            calculated_state = evaluate_stochastic_iteration(
                variables=self.variables,
                shuffled_inputs=[variable_names.COST_ADVERTISING],
                model_pipeline=self.pipeline
            )
            self.assertEqual(calculated_state["RAW_TAX_RATE_INJECTION"], 0.08)
            self.assertEqual(calculated_state["ENVIRONMENT_LABEL_STRING"], "production-simulation-run")
        except AttributeError as error:
            self.fail(f"evaluate_stochastic_iteration crashed on primitive handling: {error}")

    def test_iteration_surfaces_pipeline_exceptions_instantly(self):
        """Verify that structural calculation issues inside steps safely halt the execution context."""
        # Set CPA to zero to deliberately provoke an internal division error
        self.variables[variable_names.COST_CPA] = CostPerAcquisition(expected_value=0.0)

        with self.assertRaises(ZeroDivisionError):
            evaluate_stochastic_iteration(
                variables=self.variables,
                shuffled_inputs=[],
                model_pipeline=self.pipeline
            )


class TestEvaluateVariableScenarioSweep(unittest.TestCase):
    """Scenario sweep engine orchestration validation targeting ceteris paribus execution constraints."""

    def setUp(self):
        """Establish baseline domain models and structured stateful Variable registries."""
        self.pipeline = [
            AdvertisingEfficiencyModel(),
            CostOfGoodsSoldModel(),
            TotalCostModel()
        ]

        # Injected production objects populated with predictable bounds
        self.variables = {
            variable_names.COST_ADVERTISING: AdvertisingCost(min_value=4000.0, max_value=6000.0, expected_value=5000.0),
            variable_names.COST_CONVERSION_RATE: ConversionRate(min_value=0.05, max_value=0.15, expected_value=0.10),
            variable_names.COST_CPA: CostPerAcquisition(expected_value=20.0),
            variable_names.FINANCE_USD_TO_RMB: USDToRMB(expected_value=1.0),
            variable_names.DEAL_ITEMS_PER_ORDER: ItemsPerOrder(min_value=2.0, max_value=2.0, expected_value=2.0),
            variable_names.DEAL_PURCHASING_PRICE: PurchasingPrice(min_value=15.0, max_value=15.0, expected_value=15.0),
            variable_names.COST_SHIPPING: Cost(expected_value=500.0)
        }

    # -----------------------------------------------------------------
    # 1. ACCURACY OF DATA: MATHEMATICAL PROFILING
    # -----------------------------------------------------------------

    def test_sweep_calculates_mathematical_scenarios_accurately_across_list_bounds(self):
        """
        Verify mathematical accuracy over explicit list boundary conditions (e.g. Comparative Statics).
        Every other variable must remain pinned at its expected value.
        """
        # Testing explicit boundaries: Min (4000.0), Expected (5000.0), Max (6000.0)
        target_bounds = [4000.0, 5000.0, 6000.0]

        results = evaluate_variable_scenario_sweep(
            variables=self.variables,
            selected_variable=variable_names.COST_ADVERTISING,
            target_values=target_bounds,
            model_pipeline=self.pipeline
        )

        self.assertEqual(len(results), 3)

        # Mathematical Trace for Step 0 (Advertising Cost = 4000.0):
        # 1. Orders = (4000.0 * 0.10) / (20.0 * 1.0) = 20.0 Orders
        # 2. Cogs = 15.0 * 20.0 * 2.0 = 600.0
        # 3. Cost = 600.0 + 4000.0 + 500.0 = 5100.0
        self.assertAlmostEqual(results[0][variable_names.COST_ADVERTISING], 4000.0)
        self.assertAlmostEqual(results[0][variable_names.DEAL_ORDERS], 20.0)
        self.assertAlmostEqual(results[0][variable_names.COST], 5100.0)

        # Mathematical Trace for Step 1 (Advertising Cost = 5000.0 - Baseline Match):
        # 1. Orders = (5000.0 * 0.10) / (20.0 * 1.0) = 25.0 Orders
        # 2. Cogs = 15.0 * 25.0 * 2.0 = 750.0
        # 3. Cost = 750.0 + 5000.0 + 500.0 = 6250.0
        self.assertAlmostEqual(results[1][variable_names.COST_ADVERTISING], 5000.0)
        self.assertAlmostEqual(results[1][variable_names.DEAL_ORDERS], 25.0)
        self.assertAlmostEqual(results[1][variable_names.COST], 6250.0)

        # Mathematical Trace for Step 2 (Advertising Cost = 6000.0):
        # 1. Orders = (6000.0 * 0.10) / (20.0 * 1.0) = 30.0 Orders
        # 2. Cogs = 15.0 * 30.0 * 2.0 = 900.0
        # 3. Cost = 900.0 + 6000.0 + 500.0 = 7400.0
        self.assertAlmostEqual(results[2][variable_names.COST_ADVERTISING], 6000.0)
        self.assertAlmostEqual(results[2][variable_names.DEAL_ORDERS], 30.0)
        self.assertAlmostEqual(results[2][variable_names.COST], 7400.0)

        # Strict Ceteris Paribus Validation: Verify unselected variables never wavered from expected values
        for scenario in results:
            self.assertEqual(scenario[variable_names.COST_CONVERSION_RATE], 0.10)
            self.assertEqual(scenario[variable_names.COST_CPA], 20.0)
            self.assertEqual(scenario[variable_names.DEAL_PURCHASING_PRICE], 15.0)

    def test_sweep_handles_numpy_array_ranges_perfectly(self):
        """Verify the sweep execution accepts structural sequence types like numpy arrays (Break-Even ranges)."""
        import numpy as np

        # Simulating a typical break-even linearly spaced test matrix array
        target_array = np.linspace(0.05, 0.15, num=5)

        results = evaluate_variable_scenario_sweep(
            variables=self.variables,
            selected_variable=variable_names.COST_CONVERSION_RATE,
            target_values=target_array,
            model_pipeline=self.pipeline
        )

        self.assertEqual(len(results), 5)
        self.assertAlmostEqual(results[0][variable_names.COST_CONVERSION_RATE], 0.05)
        self.assertAlmostEqual(results[4][variable_names.COST_CONVERSION_RATE], 0.15)

        # Verify Ad Cost was locked at its expected 5000.0 state across the entire array matrix
        for scenario in results:
            self.assertEqual(scenario[variable_names.COST_ADVERTISING], 5000.0)

    # -----------------------------------------------------------------
    # 2. IDEMPOTENCY & STATE ISOLATION (SHALLOW COPY GUARD)
    # -----------------------------------------------------------------

    def test_sweep_preserves_original_variables_registry_unmutated(self):
        """Verify executing a scenario matrix sweep does not alter or pollute the input variables dictionary state."""
        original_keys = set(self.variables.keys())
        original_ad_cost = self.variables[variable_names.COST_ADVERTISING].get_value()

        _ = evaluate_variable_scenario_sweep(
            variables=self.variables,
            selected_variable=variable_names.COST_ADVERTISING,
            target_values=[1000.0, 9000.0],
            model_pipeline=self.pipeline
        )

        # Check for absolute state isolation
        self.assertEqual(set(self.variables.keys()), original_keys)
        self.assertEqual(self.variables[variable_names.COST_ADVERTISING].get_value(), original_ad_cost)

    # -----------------------------------------------------------------
    # 3. EDGE CASES: INJECTED TYPES AND BOUNDARIES
    # -----------------------------------------------------------------

    def test_sweep_handles_empty_target_values_sequence_safely(self):
        """Verify that passing an empty list sequence returns an empty list of outcomes without breaking."""
        results = evaluate_variable_scenario_sweep(
            variables=self.variables,
            selected_variable=variable_names.COST_ADVERTISING,
            target_values=[],
            model_pipeline=self.pipeline
        )
        self.assertEqual(results, [])

    def test_sweep_bubbles_up_pipeline_errors_instantly(self):
        """Verify structural execution faults (e.g. mathematical division rules) halt execution processing."""
        # Forcing a 0.0 value into an array to provoke an underlying model error (Division by zero CPA)
        self.variables[variable_names.COST_CPA] = CostPerAcquisition(expected_value=0.0)

        with self.assertRaises(ZeroDivisionError):
            evaluate_variable_scenario_sweep(
                variables=self.variables,
                selected_variable=variable_names.COST_ADVERTISING,
                target_values=[5000.0],
                model_pipeline=self.pipeline
            )


if __name__ == "__main__":
    unittest.main()
