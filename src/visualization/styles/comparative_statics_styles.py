"""
Design Token and Configuration Map for Comparative Statics Dashboard.
Houses naming constants and visual color tokens. All native HTML strings removed.
"""
import pandas as pd

from .common_styles import (
    COLOR_NAVY,
    WEB_COLOR_BORDER_LIGHT,
    WEB_COLOR_BORDER_ROW,
    WEB_COLOR_HEADER_BG,
    COLOR_WHITE,
    COLOR_HIGHLIGHT_EXP_VAL,
    COLOR_HIGHLIGHT_EXP_RES,
    COLOR_HIGHLIGHT_THR_VAL,
    COLOR_HIGHLIGHT_THR_RES,
    COLOR_HIGHLIGHT_THR_RES_TXT,
    COLOR_ALERT_SUCCESS_BG,
    COLOR_ALERT_SUCCESS_TXT,
    COLOR_ALERT_DANGER_BG,
    COLOR_ALERT_DANGER_TXT,

    get_base_table_layout_css
)

# ==========================================
# 1. Column Naming Schema
# ==========================================
SENSITIVITY_VARIABLE = "Sensitivity Variable"

COMPARATIVE_STATICS_COLUMN_NAME_MIN = 'Min State'
COMPARATIVE_STATICS_COLUMN_NAME_BASE = 'Base (Expected)'
COMPARATIVE_STATICS_COLUMN_NAME_MAX = 'Max State'
COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY = "Elasticity"

COMPARATIVE_STATICS_VARIABLE_NAME = "Variable Name"
COMPARATIVE_STATICS_ROW_TYPE = "Row Type"
COMPARATIVE_STATICS_ROW_TYPE_FACTOR = "Factor"
COMPARATIVE_STATICS_ROW_TYPE_OUTPUT = "Output"


def get_table_layout_css():
    """Fetches the unified global design system grid layout."""
    return get_base_table_layout_css(WEB_COLOR_HEADER_BG, COLOR_NAVY, WEB_COLOR_BORDER_LIGHT, WEB_COLOR_BORDER_ROW)


def generate_matrix_cell_styles(df_slice, row_vars, output_name):
    """Builds a cell-by-cell style configuration matrix using style sheet token metrics."""
    style_matrix = pd.DataFrame('', index=df_slice.index, columns=df_slice.columns)

    for idx in range(len(df_slice)):
        is_output = row_vars[idx] == output_name

        # Map colors from global style design file tokens natively
        background_color_min_max = COLOR_HIGHLIGHT_THR_RES if is_output else COLOR_HIGHLIGHT_THR_VAL
        background_color_base = COLOR_HIGHLIGHT_EXP_RES if is_output else COLOR_HIGHLIGHT_EXP_VAL

        text_color_min_max = COLOR_HIGHLIGHT_THR_RES_TXT
        text_color_base = COLOR_NAVY if is_output else COLOR_WHITE

        # Handle typography states
        style_matrix.iloc[
            idx, 0] = "text-align: left; font-weight: bold;" if not is_output else "text-align: left; font-style: italic;"
        style_matrix.iloc[
            idx, 1] = f"background-color: {background_color_min_max}; color: {text_color_min_max}; font-weight: bold;"
        style_matrix.iloc[
            idx, 2] = f"background-color: {background_color_base}; color: {text_color_base}; font-weight: bold;"
        style_matrix.iloc[
            idx, 3] = f"background-color: {background_color_min_max}; color: {text_color_min_max}; font-weight: bold;"

        # Handle conditional alerts matching string patterns
        if not is_output:
            elasticity = df_slice.iloc[idx, 4]
            if isinstance(elasticity, str):
                if elasticity.startswith('+'):
                    style_matrix.iloc[
                        idx, 4] = f"background-color: {COLOR_ALERT_SUCCESS_BG}; color: {COLOR_ALERT_SUCCESS_TXT}; font-weight: bold;"
                elif elasticity.startswith('-'):
                    style_matrix.iloc[
                        idx, 4] = f"background-color: {COLOR_ALERT_DANGER_BG}; color: {COLOR_ALERT_DANGER_TXT}; font-weight: bold;"

    return style_matrix
