import random
from enum import Enum

import numpy as np

from src.config import error_messages, settings
from src.utils import log


class ValueType(Enum):
    """
    Specifies the analytical sampling target for variable evaluation boundaries.
    """
    MIN = "min"
    MAX = "max"
    EXPECTED = "expected"
    RANDOM = "random"


class Variable:
    """
    Primitive financial parameter object tracking boundaries, defaults, 
    and random sampling ranges for downstream sensitivity analysis.
    """

    def __init__(self, expected_value=None, min_value=None, max_value=None):
        """
        Initializes boundaries and default configurations. Note that 'MAX' and 'MIN' 
        define a testing threshold rather than structural math dependencies.

        Args:
            expected_value (float, optional): Operational default base state value.
            min_value (float, optional): Lower metric boundary marker.
            max_value (float, optional): Upper metric boundary marker.

        Raises:
            ValueError: If an illegal permutation of parameters is supplied.
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
            log.error(error_messages.ERROR_VARIABLE_CONSTRUCTION_ERROR)
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
        Locks down a variable, fixing all bounds directly to a static constant.
        """
        self._expected_value = value
        self._min = value
        self._max = value

    def get_random_value(self):
        """
        Randomly samples values from within the defined lower and upper bounds.
        """
        return self._get_random_value_with_digits(settings.DECIMAL_ROUNDING)

    def _get_random_value_with_digits(self, digit=2):
        random_value = random.uniform(self.min_value, self.max_value)
        return round(random_value, digit)

    def get_value(self, value_type=ValueType.EXPECTED):
        """
        Extracts a targeted data value slice based on a requested strategy state.
        """
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
                raise ValueError(error_messages.ERROR_VARIABLE_TYPE_NOT_SUPPORT)

    def get_range_values(self, num, digits=None):
        """
        Generates a lineary spaced numpy distribution array across boundaries.
        """
        if digits is None:
            digits = settings.DECIMAL_ROUNDING

        values = np.linspace(self._min, self._max, num=num)

        if digits == 0:
            rounded_values = np.round(values).astype(int)
        else:
            rounded_values = np.round(values, decimals=digits)

        return rounded_values
