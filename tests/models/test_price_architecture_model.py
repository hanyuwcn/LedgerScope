import unittest

from src.config import variable_names as vn
from src.models import PriceArchitectureModel


class TestPriceArchitectureModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify output footprint and required variable bounds."""
        model = PriceArchitectureModel()

        expected_outputs = [
            vn.COST_PER_UNIT,
            vn.PROFIT_PER_UNIT,
            vn.SHIPPING_COST_PER_UNIT,
            vn.TARIFF_PER_UNIT,
            vn.RETAIL_MARGIN_PER_UNIT
        ]
        self.assertEqual(model.output_names, expected_outputs)

        expected_required = [
            vn.UNITS_PER_ORDER,
            vn.COST,
            vn.ORDERS,
            vn.UNIT_RETAIL,
            vn.PROFIT
        ]
        self.assertEqual(model.required_variables, expected_required)

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_setter(self):
        """Verify the property setter correctly syncs the input state."""
        model = PriceArchitectureModel()
        fresh_inputs = {vn.UNIT_RETAIL: 1000.0, vn.ORDERS: 10}
        model.input_variables = fresh_inputs
        self.assertIs(model.input_variables, fresh_inputs)

    # -----------------------------------------------------------------
    # 3. RUNTIME CALCULATIONS & WATERFALL VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_waterfall_calculation(self):
        """Verify price decomposition logic with updated COST and no currency scaling."""
        # Setup: 100 orders * 2 units = 200 total units
        # COST (40000) / 200 = 200 COST_PER_UNIT
        # Profit (10000) / 200 = 50 PROFIT_PER_UNIT
        # Shipping: 1000 * 0.05 = 50.0
        # Tariff: 1000 * 0.10 = 100.0
        # Markup: 1000 * 0.15 = 150.0

        inputs = {
            vn.UNITS_PER_ORDER: 2,
            vn.ORDERS: 100,
            vn.COST: 40000.0,
            vn.UNIT_RETAIL: 1000.0,
            vn.PROFIT: 10000.0,
            vn.SHIPPING_RATE: 0.05,
            vn.TARIFF_RATE: 0.10,
            vn.CHANNEL_MARKUP_RATE: 0.15
        }

        model = PriceArchitectureModel(inputs)
        output = model.evaluate()

        self.assertAlmostEqual(output[vn.COST_PER_UNIT], 200.0)
        self.assertAlmostEqual(output[vn.PROFIT_PER_UNIT], 50.0)
        self.assertAlmostEqual(output[vn.SHIPPING_COST_PER_UNIT], 50.0)
        self.assertAlmostEqual(output[vn.TARIFF_PER_UNIT], 100.0)
        self.assertAlmostEqual(output[vn.RETAIL_MARGIN_PER_UNIT], 150.0)

    def test_evaluate_omitted_values_fallback(self):
        """Verify calculation defaults to 0.0 for friction rates if omitted."""
        inputs = {
            vn.UNITS_PER_ORDER: 1,
            vn.ORDERS: 1,
            vn.COST: 100.0,
            vn.UNIT_RETAIL: 100.0,
            vn.PROFIT: 50.0
        }

        model = PriceArchitectureModel(inputs)
        output = model.evaluate()

        self.assertEqual(output[vn.SHIPPING_COST_PER_UNIT], 0.0)
        self.assertEqual(output[vn.TARIFF_PER_UNIT], 0.0)
        self.assertEqual(output[vn.RETAIL_MARGIN_PER_UNIT], 0.0)


if __name__ == "__main__":
    unittest.main()
