import unittest

from src.config import variable_names
from src.models import TotalSellingExpenseModel


class TestTotalSellingExpenseModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata and optional variable configurations."""
        model = TotalSellingExpenseModel()

        # Verify output registry signature
        self.assertEqual(model.output_names, [variable_names.SELLING_EXPENSE])

        # Verify default values for optional variables
        self.assertEqual(model._optional_variables[variable_names.FREIGHT_EXPENSE], 0.0)
        self.assertEqual(model._optional_variables[variable_names.MARKETING_EXPENSE], 0.0)

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify summation: FreightExpense + MarketingExpense."""
        inputs = {
            variable_names.FREIGHT_EXPENSE: 500.0,
            variable_names.MARKETING_EXPENSE: 2500.0
        }
        model = TotalSellingExpenseModel(inputs)
        enriched_output = model.evaluate()

        self.assertEqual(enriched_output[variable_names.SELLING_EXPENSE], 3000.0)

    def test_evaluate_defaults_to_zero_when_inputs_missing(self):
        """Verify the model behaves safely with empty input context."""
        model = TotalSellingExpenseModel()
        enriched_output = model.evaluate()

        # Should aggregate defaults of 0.0 + 0.0
        self.assertEqual(enriched_output[variable_names.SELLING_EXPENSE], 0.0)

    def test_evaluate_partial_input_handling(self):
        """Verify model handles partial data by assuming zero for missing components."""
        inputs = {variable_names.MARKETING_EXPENSE: 1500.0}
        model = TotalSellingExpenseModel(inputs)
        enriched_output = model.evaluate()

        # 0.0 (default freight) + 1500.0 = 1500.0
        self.assertEqual(enriched_output[variable_names.SELLING_EXPENSE], 1500.0)

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation(self):
        """Verify dynamic updates to the TotalSellingExpenseModel context."""
        model = TotalSellingExpenseModel()
        model.update_input_variable(variable_names.FREIGHT_EXPENSE, 200.0)
        model.update_input_variable(variable_names.MARKETING_EXPENSE, 800.0)

        result = model.evaluate()
        self.assertEqual(result[variable_names.SELLING_EXPENSE], 1000.0)


if __name__ == "__main__":
    unittest.main()
