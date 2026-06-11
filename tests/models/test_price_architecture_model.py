import unittest

from src.config import variable_names
from src.models import PriceArchitectureModel


class TestPriceArchitectureModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify output footprint and required variable bounds."""
        model = PriceArchitectureModel()

        expected_outputs = [
            variable_names.COGS_PER_UNIT,
            variable_names.PROFIT_PER_UNIT,
            variable_names.SHIPPING_COST_PER_UNIT,
            variable_names.TARIFF_PER_UNIT,
            variable_names.RETAIL_MARGIN_PER_UNIT
        ]
        self.assertEqual(model.output_names, expected_outputs)

        expected_required = [
            variable_names.UNITS_PER_ORDER,
            variable_names.ORDERS,
            variable_names.COGS,
            variable_names.UNIT_RETAIL,
            variable_names.PROFIT
        ]
        self.assertEqual(model.required_variables, expected_required)

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_setter(self):
        """Verify the property setter correctly syncs the input state."""
        model = PriceArchitectureModel()
        fresh_inputs = {variable_names.UNIT_RETAIL: 1000.0, variable_names.ORDERS: 10}
        model.input_variables = fresh_inputs
        self.assertIs(model.input_variables, fresh_inputs)

    # -----------------------------------------------------------------
    # 3. RUNTIME CALCULATIONS & WATERFALL VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_waterfall_calculation(self):
        """Verify price decomposition logic with full parameters and currency conversion."""
        # Setup: 100 orders * 2 units = 200 total units
        # COGS (40000) / 200 = 200 COGS_PER_UNIT
        # Profit (10000) / 200 = 50 PROFIT_PER_UNIT
        # Shipping: 1000 * 0.05 * 7.0 (USD_TO_RMB) = 350
        # Tariff: 1000 * 0.10 * 7.0 = 700
        # Markup: 1000 * 0.15 * 7.0 = 1050

        inputs = {
            variable_names.UNITS_PER_ORDER: 2,
            variable_names.ORDERS: 100,
            variable_names.COGS: 40000.0,
            variable_names.UNIT_RETAIL: 1000.0,
            variable_names.PROFIT: 10000.0,
            variable_names.SHIPPING_RATE: 0.05,
            variable_names.TARIFF_RATE: 0.10,
            variable_names.CHANNEL_MARKUP_RATE: 0.15,
            variable_names.USD_TO_RMB: 7.0
        }

        model = PriceArchitectureModel(inputs)
        output = model.evaluate()

        self.assertAlmostEqual(output[variable_names.COGS_PER_UNIT], 200.0)
        self.assertAlmostEqual(output[variable_names.PROFIT_PER_UNIT], 50.0)
        self.assertAlmostEqual(output[variable_names.SHIPPING_COST_PER_UNIT], 350.0)
        self.assertAlmostEqual(output[variable_names.TARIFF_PER_UNIT], 700.0)
        self.assertAlmostEqual(output[variable_names.RETAIL_MARGIN_PER_UNIT], 1050.0)

    def test_evaluate_omitted_values_fallback(self):
        """Verify calculation defaults to 0.0 for friction rates if omitted."""
        inputs = {
            variable_names.UNITS_PER_ORDER: 1,
            variable_names.ORDERS: 1,
            variable_names.COGS: 100.0,
            variable_names.UNIT_RETAIL: 100.0,
            variable_names.PROFIT: 50.0
            # Rates omitted, should fallback to 0.0
        }

        model = PriceArchitectureModel(inputs)
        output = model.evaluate()

        self.assertEqual(output[variable_names.SHIPPING_COST_PER_UNIT], 0.0)
        self.assertEqual(output[variable_names.TARIFF_PER_UNIT], 0.0)
        self.assertEqual(output[variable_names.RETAIL_MARGIN_PER_UNIT], 0.0)


if __name__ == "__main__":
    unittest.main()
