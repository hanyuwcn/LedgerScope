import unittest

from src.config import variable_names
from src.models import BrandFreightExpenseModel


class TestBrandFreightExpenseModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata and output configuration."""
        model = BrandFreightExpenseModel()

        # Verify output registry signature
        self.assertEqual(model.output_names, [variable_names.BRAND_FREIGHT_EXPENSE])

        # Verify no requirements are defined for this static model
        self.assertEqual(model.required_variables, [])

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS
    # -----------------------------------------------------------------

    def test_evaluate_returns_zero_constant(self):
        """Verify that the model consistently returns 0.0 regardless of inputs."""
        # Test with empty inputs
        model = BrandFreightExpenseModel()
        enriched_output = model.evaluate()
        self.assertEqual(enriched_output[variable_names.BRAND_FREIGHT_EXPENSE], 0.0)

        # Test with dummy inputs to ensure they are ignored
        model.input_variables = {variable_names.REVENUE: 100000.0}
        enriched_output = model.evaluate()
        self.assertEqual(enriched_output[variable_names.BRAND_FREIGHT_EXPENSE], 0.0)

    # -----------------------------------------------------------------
    # 3. POLYMORPHIC MUTATION
    # -----------------------------------------------------------------

    def test_parameter_mutation_no_effect(self):
        """Verify that injecting variables does not affect the output."""
        model = BrandFreightExpenseModel()
        model.update_input_variable(variable_names.REVENUE, 99999.0)

        result = model.evaluate()
        self.assertEqual(result[variable_names.BRAND_FREIGHT_EXPENSE], 0.0)


if __name__ == "__main__":
    unittest.main()
