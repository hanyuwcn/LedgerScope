import unittest

from src.analysis import run_monte_carlo
from src.config import variable_names
from src.models import AdvertisingEfficiencyGoogleSearchModel, CostOfGoodsSoldModel, TotalCostModel
from src.variables import (
    AdvertisingCost, GoogleSearchConversionRate, GoogleSearchCostPerClick,
    USDToRMB, UnitsPerOrder, UnitExw, Cost
)


class TestMonteCarloSimulation(unittest.TestCase):

    def setUp(self):
        """Build the raw business pipeline and baseline production domain variables."""
        self.pipeline = [
            AdvertisingEfficiencyGoogleSearchModel(),
            CostOfGoodsSoldModel(),
            TotalCostModel()
        ]

        # Use your direct production classes populated with clean testing values
        self.variables = {
            variable_names.ADVERTISING_COST: AdvertisingCost(min=4000.0, max=6000.0),
            variable_names.CONVERSION_RATE_GOOGLE_SEARCH: GoogleSearchConversionRate(min=0.05, max=0.15),
            variable_names.CPL_GOOGLE_SEARCH: GoogleSearchCostPerClick(exp=20.0),
            variable_names.USD_TO_RMB: USDToRMB(exp=1.0),
            variable_names.UNITS_PER_ORDER: UnitsPerOrder(min=2.0, max=2.0),
            variable_names.UNIT_EXW: UnitExw(min=15.0, max=15.0),
            variable_names.SHIPPING_COST: Cost(exp=500.0)
        }

    # -----------------------------------------------------------------
    # 1. COMPREHENSIVE LOOP OUTPUT VALIDATION
    # -----------------------------------------------------------------

    def test_monte_carlo_results_match_expected_financial_simulation_runs(self):
        """Verify the harvested iteration records accurately track calculated financial outcomes."""

        # Target X (Advertising Cost) for random sampling; keep Y (Conversion Rate) static/expected
        results = run_monte_carlo(
            variables=self.variables,
            shuffled_inputs=[variable_names.ADVERTISING_COST],
            model_pipeline=self.pipeline,
            tracked_outputs=[variable_names.COST],
            iterations=2
        )

        # Confirm the output contains the exact requested run count
        self.assertEqual(len(results), 2)

        # Verify the structure of the data dictionary fields
        for idx, iteration_record in enumerate(results, start=1):
            self.assertEqual(iteration_record[variable_names.SYSTEM_RUN_ID], idx)
            self.assertIn(variable_names.COST, iteration_record)
            # Verify it returns an expected numerical value type
            self.assertIsInstance(iteration_record[variable_names.COST], (int, float))

    # -----------------------------------------------------------------
    # 2. EDGE CASE: FIXED TRACKED COLUMNS
    # -----------------------------------------------------------------

    def test_monte_carlo_captures_all_system_variables_when_tracked_outputs_is_none(self):
        """Verify the loop defaults cleanly to harvesting all calculated state fields if un-isolated."""
        results = run_monte_carlo(
            variables=self.variables,
            shuffled_inputs=[],
            model_pipeline=self.pipeline,
            tracked_outputs=None,  # Captures full pipeline state map
            iterations=1
        )

        first_run = results[0]
        self.assertIn(variable_names.SYSTEM_RUN_ID, first_run)
        self.assertIn(variable_names.ORDERS, first_run)
        self.assertIn(variable_names.COGS, first_run)
        self.assertIn(variable_names.COST, first_run)

    # -----------------------------------------------------------------
    # 3. EDGE CASE: SELECTION HOOK FAILURES
    # -----------------------------------------------------------------

    def test_simulation_raises_exception_when_selected_shuffled_input_is_missing_from_dict(self):
        """Verify tracking exceptions bubble up instantly if a shuffle target parameter key is missing."""
        with self.assertRaises(Exception):
            run_monte_carlo(
                variables=self.variables,
                shuffled_inputs=["MISSING_SHUFFLE_KEY"],
                model_pipeline=self.pipeline,
                tracked_outputs=[variable_names.COST]
            )

    def test_simulation_raises_exception_on_first_run_if_tracked_output_cannot_be_resolved(self):
        """Verify tracking validations flag downstream outcome errors during iteration 1 profiling."""
        with self.assertRaises(Exception):
            run_monte_carlo(
                variables=self.variables,
                shuffled_inputs=[],
                model_pipeline=self.pipeline,
                tracked_outputs=["NON_EXISTENT_OUTPUT_METRIC"],
                iterations=1
            )

    # -----------------------------------------------------------------
    # 4. EDGE CASE: PIPELINE VALIDATION & ORDER FAILURES
    # -----------------------------------------------------------------

    def test_simulation_raises_exception_when_pipeline_sequence_order_fails(self):
        """Verify that a broken or out-of-order model pipeline immediately aborts execution."""
        # TotalCostModel depends on outputs generated by CostOfGoodsSoldModel.
        # Placing it first breaks the topological dependency flow.
        scrambled_pipeline = [
            TotalCostModel(),
            CostOfGoodsSoldModel(),
            AdvertisingEfficiencyGoogleSearchModel()
        ]

        with self.assertRaises(Exception):
            run_monte_carlo(
                variables=self.variables,
                shuffled_inputs=[variable_names.ADVERTISING_COST],
                model_pipeline=scrambled_pipeline,
                tracked_outputs=[variable_names.COST],
                iterations=1
            )


if __name__ == "__main__":
    unittest.main()
