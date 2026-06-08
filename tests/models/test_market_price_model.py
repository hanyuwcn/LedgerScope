import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import MarketPriceModel


class TestMarketPriceModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = MarketPriceModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.MARKET_PRICE])

        # Verify explicit required variable signature bounds (Net Income is mandatory)
        self.assertEqual(model.required_variables, [variable_names.NET_INCOME])

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables matches the dictionary mapping format."""
        model = MarketPriceModel()
        self.assertIsInstance(model._optional_variables, dict)

        # Verify default fallbacks: window scales to 1 month by default
        self.assertIn(variable_names.MONTHS, model._optional_variables)
        self.assertIn(variable_names.PE_RATIO, model._optional_variables)
        self.assertEqual(model._optional_variables[variable_names.MONTHS], 1)

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = MarketPriceModel()
        fresh_inputs = {
            variable_names.NET_INCOME: 50000.0,
            variable_names.PE_RATIO: 8.0,
            variable_names.MONTHS: 1
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.NET_INCOME: 40000.0}
        model = MarketPriceModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = MarketPriceModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable(variable_names.NET_INCOME, 120000.0)
        self.assertEqual(model.input_variables[variable_names.NET_INCOME], 120000.0)

        # Context B: Structural duck-typed object validation Type A (.name, .expected_value)
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.PE_RATIO
                self.expected_value = 10.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.PE_RATIO], 10.0)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    def test_check_variables_success_with_all_metrics(self):
        """Verify check_variables clears execution cleanly when metrics are provided."""
        inputs = {
            variable_names.NET_INCOME: 25000.0,
            variable_names.PE_RATIO: 5.0,
            variable_names.MONTHS: 3
        }
        model = MarketPriceModel(inputs)

        with patch('src.core.base_model.log') as mock_log:
            model.check_variables()
            mock_log.error.assert_not_called()
            mock_log.info.assert_not_called()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_monthly_income_and_expected_pe(self):
        """Verify valuation runs accurately on a 1-month window with the expected P/E multiplier."""
        # Scenario: $10,000 net income generated over a single month window using expected P/E = 8
        inputs = {
            variable_names.NET_INCOME: 10000.0,
            variable_names.PE_RATIO: 8.0,
            variable_names.MONTHS: 1
        }
        model = MarketPriceModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: ($10,000 * 12 * 8) / 1 = $960,000
        self.assertEqual(enriched_output[variable_names.MARKET_PRICE], 960000.0)
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_success_with_annualized_income_and_max_pe(self):
        """Verify valuation handles annual tracking windows seamlessly using maximum P/E limits."""
        # Scenario: $120,000 net income generated over a 12-month window using max P/E = 10
        inputs = {
            variable_names.NET_INCOME: 120000.0,
            variable_names.PE_RATIO: 10.0,
            variable_names.MONTHS: 12
        }
        model = MarketPriceModel(inputs)
        enriched_output = model.evaluate()

        # Math verification: ($120,000 * 12 * 10) / 12 = $1,200,000
        self.assertEqual(enriched_output[variable_names.MARKET_PRICE], 1200000.0)

    def test_evaluate_success_with_omitted_optional_values_fallback(self):
        """Verify valuation calculations securely fall back to default timeline environments."""
        # Scenario: Only net income provided. System assumes 1 month and parent settings PE.
        inputs = {
            variable_names.NET_INCOME: 5000.0
            # MONTHS and PE_RATIO omitted intentionally
        }
        model = MarketPriceModel(inputs)
        enriched_output = model.evaluate()

        # Pull core active default to guarantee accurate assertion comparison
        fallback_pe = model._optional_variables[variable_names.PE_RATIO]
        expected_market_price = (5000.0 * 12.0 * fallback_pe) / 1.0

        self.assertEqual(enriched_output[variable_names.MARKET_PRICE], expected_market_price)


if __name__ == "__main__":
    unittest.main()
