import numpy as np
import pandas as pd

from src.config import variable_names
from src.config.formatting import VARIABLE_FORMATTING_MAP
from src.utils.formatting import fmt
from src.visualization.styles import comparative_statics_styles


def _get_formatter(var_name):
    """Retrieves the assigned lambda from the map, falling back to a safe layout."""
    return VARIABLE_FORMATTING_MAP.get(var_name, lambda v: fmt(v, d=2))


def get_comparative_statics_dataframe(data_list, output_name):
    """Transforms a list of comparative statics dictionaries into a structured DataFrame."""
    processed_rows = []
    for item in data_list:
        var_name = item[variable_names.COMPARATIVE_STATICS_VARIABLE_NAME]

        # Row 1: The Model Outputs (Results)
        processed_rows.append({
            comparative_statics_styles.SENSITIVITY_VARIABLE: output_name,
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MIN: item[
                variable_names.COMPARATIVE_STATICS_MIN_RESULT],
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_BASE: item[
                variable_names.COMPARATIVE_STATICS_EXPECTED_RESULT],
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MAX: item[
                variable_names.COMPARATIVE_STATICS_MAX_RESULT],
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY: np.nan
        })

        # Row 2: The Input Factor Values
        processed_rows.append({
            comparative_statics_styles.SENSITIVITY_VARIABLE: var_name,
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MIN: item[
                variable_names.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE],
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_BASE: item[
                variable_names.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE],
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MAX: item[
                variable_names.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE],
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY: item[
                variable_names.COMPARATIVE_STATICS_ELASTICITY]
        })
    return pd.DataFrame(processed_rows)


def apply_variable_formatting(row):
    variable_name = row[comparative_statics_styles.SENSITIVITY_VARIABLE]
    formatter = _get_formatter(variable_name)

    cols_to_format = [
        comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MIN,
        comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_BASE,
        comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MAX
    ]
    for col in cols_to_format:
        row[col] = formatter(row[col])
    return row


def apply_elasticity_formatting(row):
    """Transforms numeric elasticity variables into explicitly signed string tokens."""
    elasticity = row[comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY]

    # Fast exit for structural empty placeholders (like on Output rows)
    if elasticity == "" or pd.isna(elasticity):
        return row

    try:
        numeric_elasticity = float(elasticity)

        if numeric_elasticity > 0:
            row[comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY] = fmt(numeric_elasticity, s='+',
                                                                                             d=2)
        elif numeric_elasticity < 0:
            row[comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY] = fmt(numeric_elasticity, d=2)
        else:
            row[comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY] = "0.00"

    except (ValueError, TypeError):
        row[comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY] = ""

    return row


def render_comparative_statics_dashboard(data_list, output_name):
    """Renders directly inside notebooks/PyCharm using native Pandas Styling."""
    raw_df = get_comparative_statics_dataframe(data_list, output_name)

    # Resolve vectors needed for style calculation references
    row_vars = raw_df[comparative_statics_styles.SENSITIVITY_VARIABLE].values

    # Pre-format underlying raw elements exactly like your workable solution
    formatted_df = raw_df.fillna("")
    formatted_df = formatted_df.apply(apply_variable_formatting, axis=1)
    formatted_df = formatted_df.apply(apply_elasticity_formatting, axis=1)

    # Pipe directly to styles module components cleanly
    styled_pipeline = (
        formatted_df.style
        .apply(comparative_statics_styles.generate_matrix_cell_styles, row_vars=row_vars, output_name=output_name,
               axis=None)
        .set_table_styles(comparative_statics_styles.get_table_layout_css())
        .hide(axis='index')
    )

    return styled_pipeline
