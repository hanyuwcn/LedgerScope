"""
break_even_view.py
Generates DataFrame models and renders high-fidelity sensitivity matrices using native Pandas Styling.
"""
import numpy as np
import pandas as pd

from src.config import variable_names
from src.config.formatting import VARIABLE_FORMATTING_MAP
from src.utils.formatting import fmt
from src.visualization.styles import break_even_styles


def _get_formatter(var_name):
    """Retrieves the assigned lambda from the map, falling back to a safe layout."""
    return VARIABLE_FORMATTING_MAP.get(var_name, lambda v: fmt(v, d=2))


def get_break_even_dataframe(data_list, output_name):
    """
    Transforms a list of sensitivity dictionaries into a
    structured DataFrame using configured column constants.
    """
    processed_rows = []

    for item in data_list:
        var_name = item[variable_names.BREAK_EVEN_VARIABLE_NAME]

        # Row 1 (Visual): Impact Results (Outputs)
        processed_rows.append({
            break_even_styles.SENSITIVITY_VARIABLE: output_name,
            break_even_styles.BREAK_EVEN_COLUMN_NAME_BASE: item[variable_names.BREAK_EVEN_EXPECTED_RESULT],
            break_even_styles.BREAK_EVEN_COLUMN_NAME_THRESHOLD: item[variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT],
            break_even_styles.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN: np.nan
        })

        # Row 2 (Visual): Input Values (Variables)
        processed_rows.append({
            break_even_styles.SENSITIVITY_VARIABLE: var_name,
            break_even_styles.BREAK_EVEN_COLUMN_NAME_BASE: item[variable_names.BREAK_EVEN_EXPECTED_VARIABLE_VALUE],
            break_even_styles.BREAK_EVEN_COLUMN_NAME_THRESHOLD: item[
                variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE],
            break_even_styles.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN: item.get(
                variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE, np.nan)
        })

    return pd.DataFrame(processed_rows)


def apply_variable_formatting(row):
    """Maps custom configurations to metrics columns with a robust safe fallback."""
    variable_name = row[break_even_styles.SENSITIVITY_VARIABLE]
    formatter = _get_formatter(variable_name)

    cols_to_format = [
        break_even_styles.BREAK_EVEN_COLUMN_NAME_BASE,
        break_even_styles.BREAK_EVEN_COLUMN_NAME_THRESHOLD,
    ]
    for col in cols_to_format:
        val = row[col]
        # Handle NaN values locally with an intentional dash token
        row[col] = formatter(val) if pd.notna(val) else "-"
    return row


def apply_safety_margin_formatting(row):
    """Transforms numeric safety margin variables into formatted percentage tokens."""
    safety_margin = row[break_even_styles.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN]

    # Catch raw NaN, missing, or structural output row tokens early here
    if pd.isna(safety_margin) or safety_margin == "":
        row[break_even_styles.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN] = ""
        return row

    try:
        numeric_safety_margin = float(safety_margin)
        row[break_even_styles.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN] = fmt(numeric_safety_margin, d=1, p=True)
    except (ValueError, TypeError):
        # Fall back to an empty string on invalid strings
        row[break_even_styles.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN] = ""

    return row


def render_break_even_dashboard(data_list, output_name):
    """
    Generates a native Pandas Styler dashboard utilizing table layouts and CSS definitions
    imported straight from break_even_styles.
    """
    # 1. Gather raw data structures from raw data list dictionaries
    raw_df = get_break_even_dataframe(data_list, output_name)

    # 2. Localized format sanitization sweeps without an external global fillna()
    formatted_df = raw_df.apply(apply_variable_formatting, axis=1)
    formatted_df = formatted_df.apply(apply_safety_margin_formatting, axis=1)

    # 3. Pipe directly to style engine components cleanly
    styled_pipeline = (
        formatted_df.style
        .apply(break_even_styles.generate_break_even_matrix_styles, data_list=data_list, axis=None)
        .set_table_styles(break_even_styles.get_table_layout_css())
        .hide(axis='index')
    )

    return styled_pipeline
