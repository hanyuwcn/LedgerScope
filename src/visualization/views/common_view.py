"""
common_view.py
Shared value formatters and row-wise DataFrame utilities for dashboard visualization modules.
"""
import pandas as pd

from src.config.formatting import VARIABLE_FORMATTING_MAP
from src.utils.formatting import fmt


def get_formatter(var_name):
    """Retrieves the assigned lambda from the map, falling back to a safe layout."""
    return VARIABLE_FORMATTING_MAP.get(var_name, lambda v: fmt(v, d=2))


def apply_custom_variable_formatting(row, variable_col, target_cols):
    """
    Iterates over a list of designated numeric columns in a row,
    applying the specific formatter configured for that variable.
    """
    variable_name = row[variable_col]
    formatter = get_formatter(variable_name)

    for col in target_cols:
        val = row[col]
        # Normalize missing or NaN elements gracefully to a dash token
        row[col] = formatter(val) if pd.notna(val) and val != "" else "-"
    return row
