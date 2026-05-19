# src/ledgerscope/config/__init__.py

"""
LedgerScope Configuration Registry.

Exposes explicit localization parameters, error templates, and core variable keys 
governing pipeline calculations.
"""

from . import error_messages
from . import settings
from . import variable_names

__all__ = [
    "error_messages",
    "settings",
    "variable_names",
]
