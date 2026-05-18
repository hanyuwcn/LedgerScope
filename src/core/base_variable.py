import random
from enum import Enum

import numpy as np

from src.config import ERROR_VARIABLE_CONSTRUCTION_ERROR, ERROR_VARIABLE_TYPE_NOT_SUPPORT, DECIMAL_ROUNDING
from src.utils import log


class ValueType(Enum):
    MIN = "min"
    MAX = "max"
    EXPECTED = "expected"
    RANDOM = "random"


class Variable:
    def __init__(self, expected_value=None, min_value=None, max_value=None):
        """
        Please note the "MAX" and "MIN" does not necessarily mean on which max or min final result will be depending;
        it only serves to give a range of such factor so that
        on which final result can be make sensitivity analysis.

        :param expected_value: default value of this factor, which shall fall into the given range.
        :param min_value, max_value: range of this factor
        """
        self._name = ""

        if min_value is not None and max_value is not None and expected_value is not None:
            # Rule 1: All three variables are provided
            self._min = min_value
            self._max = max_value
            self._expected_value = expected_value
        elif expected_value is not None and min_value is None and max_value is None:
            # Rule 2: Only expected value is provided
            self._min = expected_value
            self._max = expected_value
            self._expected_value = expected_value
        elif min_value is not None and max_value is not None and expected_value is None:
            # Rule 3: Only max and min are provided
            self._min = min_value
            self._max = max_value
            self._expected_value = (min_value + max_value) / 2
        elif max_value is not None and min_value is None and expected_value is None:
            # Rule 4: Only max is provided
            self._min = 0
            self._max = max_value
            self._expected_value = (self._min + self._max) / 2
        elif max_value is None and min_value is None and expected_value is None:
            # Rule 5: No values are provided
            self._min = None
            self._max = None
            self._expected_value = None
        else:
            log.error(ERROR_VARIABLE_CONSTRUCTION_ERROR)
            raise ValueError

    # -----------------------------------------------------------------
    # PROPERTY ANNOTATIONS (Clean Pythonic Getters)
    # -----------------------------------------------------------------
    @property
    def name(self) -> str:
        return self._name

    @property
    def expected_value(self):
        return self._expected_value

    @property
    def min_value(self):
        return self._min

    @property
    def max_value(self):
        return self._max

    # -----------------------------------------------------------------
    # CORE IMPLEMENTATION METRIC CALCULATORS
    # -----------------------------------------------------------------
    def set_value(self, value):
        """
        Set the expected value, min value and max value all to be the given value.
        Current variable becomes a fixed one
        """
        self._expected_value = value
        self._min = value
        self._max = value

    def get_random_value(self):
        return self._get_random_value_with_digits(DECIMAL_ROUNDING)

    def _get_random_value_with_digits(self, digit=2):
        # Cleaned up to use our property attributes internally
        random_value = random.uniform(self.min_value, self.max_value)
        return round(random_value, digit)

    def get_value(self, value_type=ValueType.EXPECTED):
        match value_type:
            case ValueType.EXPECTED:
                return self.expected_value
            case ValueType.MIN:
                return self.min_value
            case ValueType.MAX:
                return self.max_value
            case ValueType.RANDOM:
                return self.get_random_value()
            case _:
                raise ValueError(ERROR_VARIABLE_TYPE_NOT_SUPPORT)

    def get_range_values(self, num, digits=DECIMAL_ROUNDING):
        values = np.linspace(self._min, self._max, num=num)

        if digits == 0:
            rounded_values = np.round(values).astype(int)
        else:
            rounded_values = np.round(values, decimals=digits)

        return rounded_values
