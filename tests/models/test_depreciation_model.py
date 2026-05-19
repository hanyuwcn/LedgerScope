import unittest

from src.config import variable_names
from src.models import DepreciationModel


class TestDepreciationModel(unittest.TestCase):

    def test_initialization_with_zero_arguments(self):
        """Verify the model can be initialized cleanly without passing any arguments."""
        model = DepreciationModel()

        # Verify baseline properties are intact via inheritance
        self.assertEqual(model.input_variables, {})
        self.assertEqual(model.output_names, [variable_names.DEPRECIATION])

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
