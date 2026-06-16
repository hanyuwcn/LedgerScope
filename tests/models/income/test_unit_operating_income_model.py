import unittest

from src.config import variable_names as vn
from src.models import UnitOperatingIncomeModel


class TestUnitOperatingIncomeModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify output register and required variable boundaries."""
        model = UnitOperatingIncomeModel()

        self.assertEqual(model.output_names, [vn.UNIT_OPERATING_INCOME])
        self.assertEqual(
            sorted(model.required_variables),
            sorted([vn.OPERATING_INCOME, vn.UNITS_SOLD])
        )

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_success_with_valid_parameters(self):
        """Verify OperatingIncome / UnitsSold calculation."""
        # Math: 50000.0 / 2500 = 20.0
        inputs = {
            vn.OPERATING_INCOME: 50000.0,
            vn.UNITS_SOLD: 2500
        }
        model = UnitOperatingIncomeModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[vn.UNIT_OPERATING_INCOME], 20.0)

    def test_evaluate_division_by_zero_safety(self):
        """Verify that zero sales volume returns 0.0."""
        inputs = {
            vn.OPERATING_INCOME: 50000.0,
            vn.UNITS_SOLD: 0
        }
        model = UnitOperatingIncomeModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[vn.UNIT_OPERATING_INCOME], 0.0)

    def test_check_variables_missing_required_raises_error(self):
        """Verify check_variables catches missing mandatory fields."""
        incomplete_inputs = {vn.OPERATING_INCOME: 50000.0}
        model = UnitOperatingIncomeModel(incomplete_inputs)

        with self.assertRaises(KeyError):
            model.check_variables()

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation(self):
        """Verify dynamic updates to the context."""
        model = UnitOperatingIncomeModel()
        model.update_input_variable(vn.OPERATING_INCOME, 10000.0)
        model.update_input_variable(vn.UNITS_SOLD, 1000)

        # 10000 / 1000 = 10.0
        result = model.evaluate()
        self.assertEqual(result[vn.UNIT_OPERATING_INCOME], 10.0)


if __name__ == "__main__":
    unittest.main()
