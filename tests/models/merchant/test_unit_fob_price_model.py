import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import UnitFobModel


class TestUnitFobModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = UnitFobModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.UNIT_FOB_PRICE])

        # Verify explicit required variable signature bounds (UnitRetail is mandatory)
        self.assertEqual(model.required_variables, [variable_names.UNIT_RETAIL_PRICE])

    def test_internal_optional_variables_is_dict(self):
        """Verify underlying storage for optional variables matches the dictionary mapping format."""
        model = UnitFobModel()
        self.assertIsInstance(model._optional_variables, dict)
        self.assertEqual(
            model._optional_variables,
            {
                variable_names.DEDUCTION_RATE: 0.0
            }
        )

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = UnitFobModel()
        fresh_inputs = {
            variable_names.UNIT_RETAIL_PRICE: 8000.0,
            variable_names.DEDUCTION_RATE: 0.25
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {variable_names.UNIT_RETAIL_PRICE: 5000.0}
        model = UnitFobModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = UnitFobModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable(variable_names.UNIT_RETAIL_PRICE, 10000.0)
        self.assertEqual(model.input_variables[variable_names.UNIT_RETAIL_PRICE], 10000.0)

        # Context B: Structural duck-typed object validation Type A (.name, .expected_value)
        class DuckTypeA:
            def __init__(self):
                self.name = variable_names.DEDUCTION_RATE
                self.expected_value = 0.42

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables[variable_names.DEDUCTION_RATE], 0.42)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    def test_check_variables_success_with_all_metrics(self):
        """Verify check_variables clears execution cleanly when metrics are provided."""
        inputs = {
            variable_names.UNIT_RETAIL_PRICE: 8000.0,
            variable_names.DEDUCTION_RATE: 0.30
        }
        model = UnitFobModel(inputs)

        with patch('src.core.base_model.log') as mock_log:
            model.check_variables()
            mock_log.error.assert_not_called()
            mock_log.info.assert_not_called()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_success_with_all_parameters(self):
        """Verify top-down port pricing calculation runs cleanly when parameters are explicit."""
        inputs = {
            variable_names.UNIT_RETAIL_PRICE: 10000.0,
            variable_names.DEDUCTION_RATE: 0.40
        }
        model = UnitFobModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: UnitFob = 10000.0 * (1.0 - 0.40) = 6000.0
        self.assertEqual(enriched_output[variable_names.UNIT_FOB_PRICE], 6000.0)
        self.assertIs(enriched_output, model.input_variables)

    def test_evaluate_success_with_omitted_values_fallback(self):
        """Verify pricing run-rate falls back to zero deduction leakage when omitted."""
        inputs = {
            variable_names.UNIT_RETAIL_PRICE: 7500.0
            # DeductionRate omitted intentionally (defaults to 0.0)
        }
        model = UnitFobModel(inputs)
        enriched_output = model.evaluate()

        # Math validation: UnitFob = 7500.0 * (1.0 - 0.0) = 7500.0
        self.assertEqual(enriched_output[variable_names.UNIT_FOB_PRICE], 7500.0)


if __name__ == "__main__":
    unittest.main()
