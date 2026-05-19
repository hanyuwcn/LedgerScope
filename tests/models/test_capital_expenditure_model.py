import unittest

from src.config import variable_names
from src.models import CapitalExpenditureModel


class TestCapitalExpenditureModel(unittest.TestCase):

    def test_initialization_with_zero_arguments(self):
        """Verify the model can be initialized cleanly without passing any arguments."""
        model = CapitalExpenditureModel()

        # Verify baseline properties are intact via inheritance
        self.assertEqual(model.input_variables, {})
        self.assertEqual(model.output_names, [variable_names.CAPITAL_EXPENDITURE])

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
