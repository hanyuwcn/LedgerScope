import math
import unittest

from src.core import Auditor


# =====================================================================
# CONCRETE MOCK IMPLEMENTATION
# =====================================================================
def mock_reconciliation_check(variables: dict) -> None:
    """
    Simulates a logic check: requires a 'TOTAL' to equal the sum of 'PART_A' and 'PART_B'.
    Now expects a unified 'variables' dictionary.
    """
    total = variables['TOTAL']
    part_a = variables['PART_A']
    part_b = variables['PART_B']

    if not math.isclose(total, part_a + part_b):
        raise ValueError("Audit Failed: Total does not equal sum of parts.")


class MockAuditor(Auditor):
    def __init__(self, input_variables=None):
        super().__init__(input_variables)
        self._model_function = mock_reconciliation_check
        self._required_variables = ['TOTAL', 'PART_A']
        self._optional_variables = {'PART_B': 0.0}

    def evaluate(self) -> dict:
        """
        Executes internal audit logic and validates pipeline integrity.
        """
        # Resolve all variables into a single, fully-hydrated context dictionary
        context = super().prepare_calculation_context()

        try:
            # Execute the auditor-specific reconciliation function
            self._model_function(context)
        except ValueError:
            # Propagate the audit failure up the pipeline
            raise

        # Return state to maintain pipeline continuity
        return self._input_variables


# =====================================================================
# AUDITOR ARCHITECTURAL VERIFICATION SUITE
# =====================================================================
class TestAuditorArchitecture(unittest.TestCase):

    def test_output_names_is_empty(self):
        """Verify Auditor contract: output_names must be empty."""
        auditor = MockAuditor()
        self.assertEqual(auditor.output_names, [])

    def test_evaluate_success_passes_silently(self):
        """Verify that a successful audit does not raise errors and returns input state."""
        inputs = {'TOTAL': 100.0, 'PART_A': 60.0, 'PART_B': 40.0}
        auditor = MockAuditor(inputs)

        # Should not raise
        result = auditor.evaluate()
        self.assertEqual(result, inputs)

    def test_evaluate_failure_raises_value_error(self):
        """Verify that invalid logic correctly raises a ValueError (Circuit Breaker)."""
        inputs = {'TOTAL': 100.0, 'PART_A': 10.0, 'PART_B': 10.0}  # Sum is 20, Total is 100
        auditor = MockAuditor(inputs)

        with self.assertRaises(ValueError):
            auditor.evaluate()

    def test_evaluate_uses_optional_default_if_omitted(self):
        """Verify that missing optional parameters fall back to registered defaults."""
        # 100 = 60 + default 40.0 (if default is 40) -> Let's test with default 0.0
        # 100 = 100 + 0.0
        inputs = {'TOTAL': 100.0, 'PART_A': 100.0}
        auditor = MockAuditor(inputs)

        # Should pass
        auditor.evaluate()

    def test_evaluate_missing_required_variable_halts(self):
        """Verify base Model logic still enforces required variables."""
        inputs = {'TOTAL': 100.0}  # Missing PART_A
        auditor = MockAuditor(inputs)

        with self.assertRaises(KeyError):
            auditor.evaluate()


if __name__ == "__main__":
    unittest.main()
