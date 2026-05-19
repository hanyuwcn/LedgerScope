import unittest

from src.config import variable_names
from src.models import CapitalExpenditureModel


class TestCapitalExpenditureModel(unittest.TestCase):

    # -----------------------------------------------------------------
    # 1. GETTER, SETTER, & STATE MANIPULATION TESTS
    # -----------------------------------------------------------------

    def test_initialization_with_zero_arguments(self):
        """Verify the model can be initialized cleanly without passing any arguments."""
        model = CapitalExpenditureModel()

        # Verify baseline properties are intact via inheritance
        self.assertEqual(model.input_variables, {})
        self.assertEqual(model.output_names, [variable_names.CAPITAL_EXPENDITURE])

    def test_structural_getters_and_outputs_initialize_correctly(self):
        """Verify tracking metadata bounds, output configurations, and initial state mappings."""
        model = CapitalExpenditureModel()

        # Verify initial dictionary state is isolated and empty
        self.assertEqual(model.input_variables, {})
        self.assertIsInstance(model.input_variables, dict)

        # Verify exact registered calculation footprint signatures
        self.assertEqual(model.output_names, [variable_names.CAPITAL_EXPENDITURE])

        # Verify explicit required and optional variable signature bounds
        self.assertEqual(model.required_variables, [])
        self.assertEqual(model.optional_variables, [])

    def test_input_variables_property_setter_happy_path(self):
        """Verify the property setter completely updates the operational variable context."""
        model = CapitalExpenditureModel()
        fresh_inputs = {
            "PROJECT_PHASE": "ALPHA",
            "INITIAL_BUDGET": 50000
        }

        # Execute property assignment
        model.input_variables = fresh_inputs

        # Assert structural synchronization and address identity equality
        self.assertEqual(model.input_variables, fresh_inputs)
        self.assertIs(model.input_variables, fresh_inputs)

    def test_input_variables_property_setter_none_defensive_fallback(self):
        """Verify setting input_variables context to None resets state safely to an empty dictionary."""
        initial_inputs = {"ASSET_CLASS": "MACHINERY"}
        model = CapitalExpenditureModel(initial_inputs)

        # Set context strictly to None to test the defensive barrier
        model.input_variables = None

        self.assertEqual(model.input_variables, {})

    def test_individual_variable_update_and_polymorphic_duck_typing(self):
        """Verify individual variable injection works via standard keys and structural objects."""
        model = CapitalExpenditureModel()

        # Context A: Explicit string key variable modification
        model.update_input_variable("DEPRECIATION_METHOD", "STRAIGHT_LINE")
        self.assertEqual(model.input_variables["DEPRECIATION_METHOD"], "STRAIGHT_LINE")

        # Context B: Structural duck-typed getter object validation
        class MockVariableObject:
            def get_name(self):
                return "USEFUL_LIFE_YEARS"

            def get_value(self):
                return 5

        model.update_input_variable(MockVariableObject())
        self.assertEqual(model.input_variables["USEFUL_LIFE_YEARS"], 5)

    # -----------------------------------------------------------------
    # 2. RUNTIME CALCULATIONS & VALIDATION PASS TESTS
    # -----------------------------------------------------------------

    def test_evaluate_returns_static_zero_and_merges_state(self):
        """Verify evaluation works seamlessly and appends the static cap-ex metric."""
        # Isolate testing with dummy tracking data
        arbitrary_context = {"EXISTING_METRIC": 1200}
        model = CapitalExpenditureModel(arbitrary_context)

        enriched_output = model.evaluate()

        # Ensure the model preserves incoming states while injecting the cap-ex zero
        self.assertEqual(enriched_output["EXISTING_METRIC"], 1200)
        self.assertEqual(enriched_output[variable_names.CAPITAL_EXPENDITURE], 0)

        # Ensure the in-place reference match holds true
        self.assertIs(enriched_output, model.input_variables)


if __name__ == "__main__":
    unittest.main()
