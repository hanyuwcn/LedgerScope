import numpy as np
import pandas as pd

from src.config import variable_names
from src.utils.formatting import fmt
from src.visualization.styles import break_even_styles
from src.visualization.views.common_view import apply_custom_variable_formatting


def get_break_even_dataframe(data_list, output_name):
    """Transforms a list of sensitivity dictionaries into a structured DataFrame."""
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
    """Proxies to the shared core utility with Break Even columns."""
    cols_to_format = [
        break_even_styles.BREAK_EVEN_COLUMN_NAME_BASE,
        break_even_styles.BREAK_EVEN_COLUMN_NAME_THRESHOLD,
    ]
    return apply_custom_variable_formatting(
        row,
        variable_col=break_even_styles.SENSITIVITY_VARIABLE,
        target_cols=cols_to_format
    )


def apply_safety_margin_formatting(row):
    """Transforms numeric safety margin variables into formatted percentage tokens."""
    safety_margin = row[break_even_styles.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN]

    if pd.isna(safety_margin) or safety_margin == "":
        row[break_even_styles.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN] = ""
        return row

    try:
        numeric_safety_margin = float(safety_margin)
        row[break_even_styles.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN] = fmt(numeric_safety_margin, d=1, p=True)
    except (ValueError, TypeError):
        row[break_even_styles.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN] = ""

    return row


def render_break_even_dashboard(data_list, output_name):
    """Generates a native Pandas Styler dashboard utilizing table layouts and shared view utilities."""
    raw_df = get_break_even_dataframe(data_list, output_name)

    formatted_df = raw_df.apply(apply_variable_formatting, axis=1)
    formatted_df = formatted_df.apply(apply_safety_margin_formatting, axis=1)

    styled_pipeline = (
        formatted_df.style
        .apply(break_even_styles.generate_break_even_matrix_styles, data_list=data_list, axis=None)
        .set_table_styles(break_even_styles.get_table_layout_css())
        .hide(axis='index')
    )
    return styled_pipeline
