import unittest

from src.config import variable_names
from src.models import UnitTariffModel


class TestUnitTariffModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds and output configurations."""
        model = UnitTariffModel()

        # Verify output registry signature
        self.assertEqual(model.output_names, [variable_names.UNIT_TARIFF])

        # Verify explicit required variable signature
        self.assertEqual(
            sorted(model.required_variables),
            sorted([variable_names.UNIT_RETAIL_PRICE, variable_names.TARIFF_RATE])
        )

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_success_with_valid_parameters(self):
        """Verify UnitTariff calculation: UnitRetailPrice * TariffRate."""
        # Math: 200.0 * 0.10 = 20.0
        inputs = {
            variable_names.UNIT_RETAIL_PRICE: 200.0,
            variable_names.TARIFF_RATE: 0.10
        }
        model = UnitTariffModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[variable_names.UNIT_TARIFF], 20.0)
        self.assertIs(enriched_output, model.input_variables)

    def test_check_variables_missing_required_raises_error(self):
        """Verify check_variables catches missing mandatory fields."""
        incomplete_inputs = {variable_names.UNIT_RETAIL_PRICE: 200.0}
        model = UnitTariffModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation(self):
        """Verify dynamic updates to the UnitTariffModel context."""
        model = UnitTariffModel()
        model.update_input_variable(variable_names.UNIT_RETAIL_PRICE, 500.0)
        model.update_input_variable(variable_names.TARIFF_RATE, 0.05)

        # 500.0 * 0.05 = 25.0
        result = model.evaluate()
        self.assertEqual(result[variable_names.UNIT_TARIFF], 25.0)


if __name__ == "__main__":
    unittest.main()
