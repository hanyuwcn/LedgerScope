import unittest

import numpy as np

from src.core import ValueType, Variable


# Create a concrete subclass to test the base Variable's structural mechanics
class DummyVariable(Variable):
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        super().__init__(expected_value, min_value, max_value)
        self._name = "Dummy"


class TestVariableMechanics(unittest.TestCase):

    # =====================================================================
    # INITIALIZATION RULE TESTS
    # =====================================================================

    def test_rule_1_full_window(self):
        """Rule 1: All three variables are provided."""
        var = DummyVariable(expected_value=10, min_value=5, max_value=20)
        self.assertEqual(var.min_value, 5)
        self.assertEqual(var.max_value, 20)
        self.assertEqual(var.expected_value, 10)

    def test_rule_2_static_constant(self):
        """Rule 2: Only expected value is provided."""
        var = DummyVariable(expected_value=15)
        self.assertEqual(var.min_value, 15)
        self.assertEqual(var.max_value, 15)
        self.assertEqual(var.expected_value, 15)

    def test_rule_3_range_bound(self):
        """Rule 3: Only max and min are provided (expected should be midpoint)."""
        var = DummyVariable(min_value=10, max_value=20)
        self.assertEqual(var.min_value, 10)
        self.assertEqual(var.max_value, 20)
        self.assertEqual(var.expected_value, 15.0)

    def test_rule_4_bounded_floor(self):
        """Rule 4: Only max is provided (min defaults to 0, expected is midpoint)."""
        var = DummyVariable(max_value=100)
        self.assertEqual(var.min_value, 0)
        self.assertEqual(var.max_value, 100)
        self.assertEqual(var.expected_value, 50.0)

    def test_rule_5_pure_placeholder(self):
        """Rule 5: No values are provided (everything defaults to None)."""
        var = DummyVariable()
        self.assertIsNone(var.min_value)
        self.assertIsNone(var.max_value)
        self.assertIsNone(var.expected_value)

    def test_invalid_combinations_raise_error(self):
        """Ensure invalid parameter sets throw the exact required construction error."""
        with self.assertRaises(ValueError) as context:
            DummyVariable(expected_value=10, min_value=5)

    # =====================================================================
    # VALUE RETRIEVAL & RANGE METHOD TESTS
    # =====================================================================

    def test_get_value_routing(self):
        """Verify that get_value accurately routes Enum variants to properties."""
        var = DummyVariable(expected_value=10, min_value=5, max_value=20)

        self.assertEqual(var.get_value(ValueType.EXPECTED), 10)
        self.assertEqual(var.get_value(ValueType.MIN), 5)
        self.assertEqual(var.get_value(ValueType.MAX), 20)

    def test_get_value_random(self):
        """Verify that ValueType.RANDOM respects boundaries and rounding constraints."""
        var = DummyVariable(expected_value=10, min_value=5, max_value=20)

        for _ in range(50):
            rand_val = var.get_value(ValueType.RANDOM)
            self.assertTrue(5 <= rand_val <= 20)
            # Verify that decimals do not exceed system rounding specs (e.g., 4)
            self.assertTrue(len(str(rand_val).split('.')[-1]) <= 4)

    def test_set_value_locks_variable(self):
        """Verify set_value flattens the variable boundaries to a single fixed point."""
        var = DummyVariable(expected_value=10, min_value=5, max_value=20)
        var.set_value(42)

        self.assertEqual(var.expected_value, 42)
        self.assertEqual(var.min_value, 42)
        self.assertEqual(var.max_value, 42)

    def test_get_range_values_generation(self):
        """Verify numpy range coordinates generate clean, linear partitions."""
        var = DummyVariable(min_value=0, max_value=10)
        steps = var.get_range_values(num=5, digits=1)

        expected_array = np.array([0.0, 2.5, 5.0, 7.5, 10.0])
        np.testing.assert_array_equal(steps, expected_array)


if __name__ == "__main__":
    unittest.main()
