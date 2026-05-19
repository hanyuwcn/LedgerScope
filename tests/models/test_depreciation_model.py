import unittest
from unittest.mock import patch

from src.config import variable_names
from src.models import DepreciationModel


class TestDepreciationModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. INITIALIZATION & METADATA GETTER PATHS
    # -----------------------------------------------------------------

    def test_initialization_with_zero_arguments(self):
        """Verify the model can be initialized cleanly without passing any arguments."""
        model = DepreciationModel()

        # Verify baseline properties are intact via inheritance
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)
        self.assertEqual(model.output_names, [variable_names.DEPRECIATION])

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = DepreciationModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.DEPRECIATION])

        # Verify explicit required and optional variable signature bounds
        self.assertEqual(model.required_variables, [])
        self.assertEqual(model.optional_variables, [])

    # -----------------------------------------------------------------
    # 2. STATE DICTIONARY GETTER & SETTER PROPERTIES
    # -----------------------------------------------------------------

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = DepreciationModel()
        fresh_inputs = {
            variable_names.COST_COGS: 3000.0,
            "ASSET_LIFETIME": 5
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {"ASSET_VALUATION": 15000.0}
        model = DepreciationModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    # -----------------------------------------------------------------
    # 3. INDIVIDUAL PARAMETER MUTATION (POLYMORPHIC CORES)
    # -----------------------------------------------------------------

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = DepreciationModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable("ASSET_VALUATION", 12000.0)
        self.assertEqual(model.input_variables["ASSET_VALUATION"], 12000.0)

        # Context B: Structural duck-typed object validation Type A (.name, .expected_value)
        class DuckTypeA:
            def __init__(self):
                self.name = "SALVAGE_VALUE"
                self.expected_value = 2000.0

        model.update_input_variable(DuckTypeA())
        self.assertEqual(model.input_variables["SALVAGE_VALUE"], 2000.0)

        # Context C: Structural duck-typed object validation Type B (.get_name(), .get_value())
        class DuckTypeB:
            def get_name(self):
                return "USEFUL_LIFE_YEARS"

            def get_value(self):
                return 10

        model.update_input_variable(DuckTypeB())
        self.assertEqual(model.input_variables["USEFUL_LIFE_YEARS"], 10)

    # -----------------------------------------------------------------
    # 4. EXPLICIT DEPENDENCY CHECKING MECHANISMS
    # -----------------------------------------------------------------

    @patch('src.core.base_model.log')
    def test_check_variables_success_with_arbitrary_context(self, mock_log):
        """Verify check_variables clears execution cleanly with any or zero variables present.

        Since DepreciationModel returns a static 0 value, it typically holds no hard process requirements.
        """
        arbitrary_context = {"SOME_UNRELATED_VARIABLE": 500}
        model = DepreciationModel(arbitrary_context)

        # Execution should complete smoothly without generating system alerts
        model.check_variables()
        mock_log.error.assert_not_called()
        mock_log.info.assert_not_called()

    # -----------------------------------------------------------------
    # 5. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_returns_static_zero_and_merges_state(self):
        """Verify evaluation works seamlessly and appends the static depreciation metric."""
        # Even if initialized with unexpected tracking data...
        arbitrary_context = {"SOME_UNRELATED_VARIABLE": 500}
        model = DepreciationModel(arbitrary_context)

        enriched_output = model.evaluate()

        # ...the model should preserve incoming states while injecting the depreciation zero
        self.assertEqual(enriched_output["SOME_UNRELATED_VARIABLE"], 500)
        self.assertEqual(enriched_output[variable_names.DEPRECIATION], 0)

        # Ensure the in-place reference match holds true
        self.assertIs(enriched_output, model.input_variables)


if __name__ == "__main__":
    unittest.main()
