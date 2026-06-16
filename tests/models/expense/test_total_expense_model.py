import unittest

from src.config import variable_names as vn
from src.models import TotalExpenseModel


class TestTotalExpenseModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify output registry signature and optional variable bounds."""
        model = TotalExpenseModel()

        # Verify output registry signature
        self.assertEqual(model.output_names, [vn.EXPENSE])

        # Verify required_variables is now empty
        self.assertEqual(model.required_variables, [])

        # Verify optional_variables mapping
        self.assertEqual(
            model._optional_variables,
            {vn.MANAGEMENT_EXPENSE: 0.0, vn.SELLING_EXPENSE: 0.0}
        )

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify TotalExpense calculation: ManagementExpense + SellingExpense."""
        # Math: 15000.0 + 5000.0 = 20000.0
        inputs = {
            vn.MANAGEMENT_EXPENSE: 15000.0,
            vn.SELLING_EXPENSE: 5000.0
        }
        model = TotalExpenseModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[vn.EXPENSE], 20000.0)

    def test_evaluate_success_with_partial_parameters(self):
        """Verify fallback to default 0.0 for missing optional parameters."""
        inputs = {vn.MANAGEMENT_EXPENSE: 15000.0}
        model = TotalExpenseModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[vn.EXPENSE], 15000.0)

    def test_evaluate_success_with_no_parameters(self):
        """Verify result is 0.0 when no parameters are provided."""
        model = TotalExpenseModel({})
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[vn.EXPENSE], 0.0)

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation(self):
        """Verify dynamic updates to the TotalExpenseModel context."""
        model = TotalExpenseModel()
        model.update_input_variable(vn.MANAGEMENT_EXPENSE, 10000.0)
        model.update_input_variable(vn.SELLING_EXPENSE, 2000.0)

        # 10000 + 2000 = 12000.0
        result = model.evaluate()
        self.assertEqual(result[vn.EXPENSE], 12000.0)


if __name__ == "__main__":
    unittest.main()
