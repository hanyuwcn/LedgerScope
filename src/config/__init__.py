# src/ledgerscope/config/__init__.py

"""
LedgerScope Configuration Registry.

Exposes explicit localization parameters, error templates, and core variable keys 
governing pipeline calculations.
"""

from . import messages
from . import settings
from . import variable_names
from .pipelines import DYNAMIC_PIPELINE_CONFIGS

__all__ = [
    "messages",
    "settings",
    "variable_names",
    "DYNAMIC_PIPELINE_CONFIGS",
]
