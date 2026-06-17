import unittest

from src.config import variable_names
from src.engine import (
    evaluate_chained_models,
    evaluate_stochastic_iteration,
    evaluate_variable_scenario_sweep,
    evaluate_expected_scenario
)
from src.models import (UnitGrossProfitModel, CostOfGoodsSoldModel, TotalExpenseModel, UnitsSoldModel,
                        TotalSellingExpenseModel, AdvertisingExpenseModel)
from src.variables import (GoogleSearchConversionRate, GoogleSearchCostPerClick,
                           USDToRMB, UnitsPerOrder, UnitExwPrice, BrandFreightExpense, Orders,
                           MarketingExpense
                           )


class TestEvaluateChainedModelsPipeline(unittest.TestCase):
    """Execution engine unit tests verifying direct functional matrix mutations and state isolation."""

    def setUp(self):
        """Set up fresh, reusable model instances for clean pipeline configurations."""
        self.units_model = UnitsSoldModel()
        self.ugp_model = UnitGrossProfitModel()
        self.cogs_model = CostOfGoodsSoldModel()
        self.advertising_expense_model = AdvertisingExpenseModel()
        self.total_selling_expense_model = TotalSellingExpenseModel()
        self.total_expense_model = TotalExpenseModel()
        self.pipeline = [self.units_model,
                         self.cogs_model,
                         self.ugp_model,
                         self.advertising_expense_model,
                         self.total_selling_expense_model,
                         self.total_expense_model]

    # -----------------------------------------------------------------
    # 1. HAPPY PATH: MULTI-STAGE STEP CASCADING
    # -----------------------------------------------------------------

    def test_evaluate_chained_models_happy_path_cascades_state_perfectly(self):
        """Verify metrics accumulate chronologically across sequential model dependencies."""
        baseline_inputs = {
            variable_names.MARKETING_EXPENSE: 5000.0,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.10,  # 10% conversion rate
            variable_names.CPL_GOOGLE_SEARCH: 20.0,
            variable_names.USD_TO_RMB: 1.0,  # No conversion shift
            variable_names.UNITS_PER_ORDER: 2.0,  # 2 items per transaction
            variable_names.UNIT_EXW_PRICE: 15.0,  # $15 base purchase price
            variable_names.BRAND_FREIGHT_EXPENSE: 500.0,  # Operational shipping cost
            variable_names.ORDERS: 25.0  # Injected directly to drive downstream matrix matching
        }

        # Step-by-step mathematical trace:
        # 1. UnitsSoldModel:
        #    Units = 25.0 (Orders) * 2.0 (UnitsPerOrder) = 50.0
        # 2. CostOfGoodsSoldModel:
        #    COGS = 15.0 (UnitExwPrice) * 50.0 (Units) = 750.0
        # 3. AdvertisingExpenseModel:
        #    AdvertisingExpense = 5000.0 (MarketingExpense) * 1.0 = 5000.0
        # 4. TotalSellingExpenseModel:
        #    SellingExpense = 5000.0 (AdvertisingExpense) + 0.0 (FreightExpense) = 5000.0
        # 5. TotalExpenseModel:
        #    Expense = 5000.0 (SellingExpense) + 500.0 (ManagementExpense*) = 5500.0
        #    (*Assuming FreightExpense or other overhead inputs map here)
        final_state = evaluate_chained_models(baseline_inputs, [self.units_model,
                                                                self.cogs_model,
                                                                self.advertising_expense_model,
                                                                self.total_selling_expense_model,
                                                                self.total_expense_model])

        self.assertEqual(final_state[variable_names.COGS], 750.0)
        self.assertEqual(final_state[variable_names.EXPENSE], 5500.0)
        self.assertEqual(final_state[variable_names.ADVERTISING_EXPENSE], 5000.0)
        self.assertEqual(final_state[variable_names.UNIT_EXW_PRICE], 15.0)

    # -----------------------------------------------------------------
    # 2. IDEMPOTENCY & STATE ISOLATION (DEEP COPY GUARD)
    # -----------------------------------------------------------------

    def test_pipeline_execution_confines_mutations_and_does_not_pollute_input_state(self):
        """Verify baseline_inputs dictionary remains unmutated (isolated) after a pipeline run."""
        baseline_inputs = {
            variable_names.ADVERTISING_EXPENSE: 2000.0,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.05,
            variable_names.CPL_GOOGLE_SEARCH: 10.0,
            variable_names.UNITS_PER_ORDER: 1.0,
            variable_names.UNIT_EXW_PRICE: 10.0,
            variable_names.ORDERS: 10.0
        }

        original_keys = set(baseline_inputs.keys())
        evaluate_chained_models(baseline_inputs, [self.units_model, self.cogs_model])

        self.assertEqual(set(baseline_inputs.keys()), original_keys)
        self.assertNotIn(variable_names.COGS, baseline_inputs)

    # -----------------------------------------------------------------
    # 3. EDGE CASES: CORNER VARIABLES & VALIDATION FAILURES
    # -----------------------------------------------------------------

    def test_evaluate_chained_models_handles_empty_pipeline_safely(self):
        """Verify passing an empty sequence returns a clean copy of original input states."""
        baseline_inputs = {
            variable_names.ADVERTISING_EXPENSE: 1500.0,
            variable_names.UNIT_EXW_PRICE: 45.0
        }

        final_state = evaluate_chained_models(baseline_inputs, model_pipeline=[])

        self.assertEqual(final_state, baseline_inputs)
        self.assertIsNot(final_state, baseline_inputs)

    def test_pipeline_raises_key_error_and_halts_when_required_variable_is_missing(self):
        """Verify model validation fails fast if required pipeline dependencies are absent."""
        invalid_inputs = {
            variable_names.ADVERTISING_EXPENSE: 5000.0,
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: 0.10
        }

        with self.assertRaises(KeyError):
            evaluate_chained_models(invalid_inputs, [self.cogs_model])


class TestEvaluateVariableScenario(unittest.TestCase):
    """Baseline scenario runner validation targeting expected value snapshot execution."""

    def setUp(self):
        self.pipeline = [UnitsSoldModel(),
                         CostOfGoodsSoldModel(),
                         AdvertisingExpenseModel(),
                         TotalSellingExpenseModel(),
                         TotalExpenseModel()]

        self.variables = {
            variable_names.MARKETING_EXPENSE: MarketingExpense(exp=5000.0),
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: GoogleSearchConversionRate(exp=0.10),
            variable_names.CPL_GOOGLE_SEARCH: GoogleSearchCostPerClick(exp=20.0),
            variable_names.USD_TO_RMB: USDToRMB(exp=1.0),
            variable_names.UNITS_PER_ORDER: UnitsPerOrder(exp=2.0),
            variable_names.UNIT_EXW_PRICE: UnitExwPrice(exp=15.0),
            variable_names.BRAND_FREIGHT_EXPENSE: BrandFreightExpense(exp=500.0),
            variable_names.ORDERS: Orders(exp=25.0)
        }

    def test_evaluate_variable_scenario_extracts_and_runs_expected_values_perfectly(self):
        """Verify baseline values are extracted correctly from variable instances and cascade properly."""
        baseline_state = evaluate_expected_scenario(self.variables, self.pipeline)

        self.assertAlmostEqual(baseline_state[variable_names.COGS], 750.0)
        self.assertEqual(baseline_state[variable_names.EXPENSE], 5500.0)


class TestEvaluateStochasticIteration(unittest.TestCase):
    """Stochastic engine orchestration validation targeting input split-sampling boundaries."""

    def setUp(self):
        self.pipeline = [UnitsSoldModel(),
                         CostOfGoodsSoldModel(),
                         AdvertisingExpenseModel(),
                         TotalSellingExpenseModel(),
                         TotalExpenseModel()]

        self.variables = {
            variable_names.MARKETING_EXPENSE: MarketingExpense(min=4000.0, max=6000.0, exp=5000.0),
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: GoogleSearchConversionRate(exp=0.10),
            variable_names.CPL_GOOGLE_SEARCH: GoogleSearchCostPerClick(exp=20.0),
            variable_names.USD_TO_RMB: USDToRMB(exp=1.0),
            variable_names.UNITS_PER_ORDER: UnitsPerOrder(exp=2.0),
            variable_names.UNIT_EXW_PRICE: UnitExwPrice(exp=15.0),
            variable_names.BRAND_FREIGHT_EXPENSE: BrandFreightExpense(exp=500.0),
            variable_names.ORDERS: Orders(exp=25.0)
        }

    def test_iteration_uses_expected_values_when_no_inputs_are_shuffled(self):
        """Verify mathematical accuracy when zero variables are targeted for shuffling."""
        calculated_state = evaluate_stochastic_iteration(
            variables=self.variables,
            shuffled_inputs=[],
            model_pipeline=self.pipeline
        )

        self.assertAlmostEqual(calculated_state[variable_names.COGS], 750.0, places=4)
        self.assertAlmostEqual(calculated_state[variable_names.EXPENSE], 5500.0, places=4)

    def test_iteration_defaults_to_expected_values_when_shuffled_inputs_is_omitted(self):
        """Verify fallback behavior matches the expected scenario when shuffled_inputs is completely omitted."""
        calculated_state = evaluate_stochastic_iteration(
            variables=self.variables,
            shuffled_inputs=None,
            model_pipeline=self.pipeline
        )

        self.assertAlmostEqual(calculated_state[variable_names.COGS], 750.0, places=4)
        self.assertAlmostEqual(calculated_state[variable_names.EXPENSE], 5500.0, places=4)

    def test_iteration_randomizes_shuffled_inputs_while_pinning_unshuffled_baselines(self):
        """Verify split-sampling configuration mapping anchors deterministic lines correctly."""
        calculated_state = evaluate_stochastic_iteration(
            variables=self.variables,
            shuffled_inputs=[variable_names.MARKETING_EXPENSE],
            model_pipeline=self.pipeline
        )

        sampled_ad_cost = calculated_state[variable_names.ADVERTISING_EXPENSE]
        self.assertTrue(4000.0 <= sampled_ad_cost <= 6000.0)
        self.assertAlmostEqual(calculated_state[variable_names.EXPENSE], sampled_ad_cost + 500.0, places=4)


class TestEvaluateVariableScenarioSweep(unittest.TestCase):
    """Scenario sweep engine orchestration validation targeting ceteris paribus execution constraints."""

    def setUp(self):
        self.pipeline = [UnitsSoldModel(),
                         CostOfGoodsSoldModel(),
                         AdvertisingExpenseModel(),
                         TotalSellingExpenseModel(),
                         TotalExpenseModel()]

        self.variables = {
            variable_names.MARKETING_EXPENSE: MarketingExpense(exp=5000.0),
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: GoogleSearchConversionRate(exp=0.10),
            variable_names.CPL_GOOGLE_SEARCH: GoogleSearchCostPerClick(exp=20.0),
            variable_names.USD_TO_RMB: USDToRMB(exp=1.0),
            variable_names.UNITS_PER_ORDER: UnitsPerOrder(exp=2.0),
            variable_names.UNIT_EXW_PRICE: UnitExwPrice(exp=15.0),
            variable_names.BRAND_FREIGHT_EXPENSE: BrandFreightExpense(exp=500.0),
            variable_names.ORDERS: Orders(exp=25.0)
        }

    def test_sweep_calculates_mathematical_scenarios_accurately_across_list_bounds(self):
        """Verify mathematical accuracy over explicit list boundary conditions."""
        target_bounds = [4000.0, 6000.0]

        results = evaluate_variable_scenario_sweep(
            variables=self.variables,
            selected_variable=variable_names.MARKETING_EXPENSE,
            target_values=target_bounds,
            model_pipeline=self.pipeline
        )

        self.assertEqual(len(results), 2)
        self.assertAlmostEqual(results[0][variable_names.EXPENSE], 4000.0 + 500.0)
        self.assertAlmostEqual(results[1][variable_names.EXPENSE], 6000.0 + 500.0)


if __name__ == "__main__":
    unittest.main()
