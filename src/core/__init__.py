"""
LedgerScope Core Architecture Layer.

Provides the primitive abstract base classes, tracking contracts, 
and variable primitives powering the analytical runtime engine.
"""

from .base_model import Model
from .base_variable import Variable, ValueType

__all__ = [
    "Model",
    "Variable",
    "ValueType",
]
