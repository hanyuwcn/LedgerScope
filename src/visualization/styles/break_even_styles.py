"""
break_even_styles.py
Dedicated design system and HTML components for Break-Even / Sensitivity tables.
"""

import pandas as pd

from src.config import variable_names, messages
from .common import (
    COLOR_NAVY,
    WEB_COLOR_BORDER_LIGHT,
    WEB_COLOR_BORDER_ROW,
    WEB_COLOR_HEADER_BG,
    WEB_COLOR_SUB_LABEL,
    COLOR_HIGHLIGHT_EXP_VAL,
    COLOR_HIGHLIGHT_EXP_RES,
    COLOR_HIGHLIGHT_EXP_BORDER,
    COLOR_HIGHLIGHT_THR_VAL,
    COLOR_HIGHLIGHT_THR_RES,
    COLOR_HIGHLIGHT_THR_TXT,
    COLOR_HIGHLIGHT_THR_RES_TXT,
    COLOR_ALERT_SUCCESS_BG,
    COLOR_ALERT_SUCCESS_TXT,
    COLOR_ALERT_DANGER_BG,
    COLOR_ALERT_DANGER_TXT
)

SENSITIVITY_VARIABLE = "Sensitivity Variable"

BREAK_EVEN_COLUMN_NAME_BASE = 'Base (Expected)'
BREAK_EVEN_COLUMN_NAME_THRESHOLD = 'BE (Threshold)'
BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN = 'Safety Margin %'


def get_table_layout_css():
    """Generates the static layout structure dictionary configurations for Pandas Styler."""
    return [
        {'selector': '', 'props': [('border-collapse', 'collapse'), ('width', '100%'), ('margin', '15px 0'),
                                   ('border', f'1px solid {WEB_COLOR_BORDER_LIGHT}')]},
        {'selector': 'th',
         'props': [('background-color', WEB_COLOR_HEADER_BG), ('color', COLOR_NAVY), ('padding', '12px'),
                   ('border-bottom', f'2px solid {WEB_COLOR_BORDER_LIGHT}'), ('text-align', 'right !important'),
                   ('text-transform', 'uppercase'), ('font-size', '0.85rem')]},
        {'selector': 'td', 'props': [('padding', '10px 15px'), ('border-bottom', f'1px solid {WEB_COLOR_BORDER_ROW}'),
                                     ('text-align', 'right'), ('font-variant-numeric', 'tabular-nums')]},
        {'selector': 'th.col0', 'props': [('text-align', 'right !important')]}
    ]


def generate_break_even_matrix_styles(df_slice, data_list):
    """
    Builds a cell-by-cell layout matrix string array targeting background colors,
    text weights, padding offsets, and specialized conditional safety margin flags.
    """
    # 1. Rebuild the row classes metadata context internally
    row_classes = []
    for item in data_list:
        feasibility = item.get(variable_names.BREAK_EVEN_FEASIBILITY_STATUS,
                               messages.BREAK_EVEN_FEASIBILITY_STATUS_CROSSOVER)
        margin_val = item.get(variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE, 0.0)

        match feasibility:
            case messages.BREAK_EVEN_FEASIBILITY_ALWAYS_FEASIBLE:
                margin_class = "be-margin-safe"
                val_thr_class = "be-val-thr"
                res_thr_class = "be-res-thr"
            case messages.BREAK_EVEN_FEASIBILITY_UNREACHABLE:
                margin_class = "be-margin-danger"
                val_thr_class = "be-val-thr-unreachable"
                res_thr_class = "be-res-thr-unreachable"
            case messages.BREAK_EVEN_FEASIBILITY_STATUS_CROSSOVER:
                val_thr_class = "be-val-thr"
                res_thr_class = "be-res-thr"
                margin_class = "be-margin-caution" if margin_val >= 0 else "be-margin-warning"
            case _:
                margin_class = "be-margin-warning"
                val_thr_class = "be-val-thr"
                res_thr_class = "be-res-thr"

        row_classes.append((res_thr_class, val_thr_class, margin_class))

    # 2. Render style mapping matrix properties row-by-row
    style_matrix = pd.DataFrame('', index=df_slice.index, columns=df_slice.columns)

    for i in range(len(df_slice)):
        pair_idx = i // 2
        is_output_row = (i % 2 == 0)
        res_thr_class, val_thr_class, margin_class = row_classes[pair_idx]

        if is_output_row:
            style_matrix.iloc[
                i, 0] = f"text-align: right !important; padding-left: 25px !important; color: {WEB_COLOR_SUB_LABEL}; font-style: italic; font-size: 0.9rem; border-bottom: 2px solid {WEB_COLOR_BORDER_LIGHT} !important;"
            style_matrix.iloc[
                i, 1] = f"background-color: {COLOR_HIGHLIGHT_EXP_RES}; color: {COLOR_NAVY}; font-weight: bold; border-right: 1px solid {COLOR_HIGHLIGHT_EXP_BORDER}; border-bottom: 2px solid {WEB_COLOR_BORDER_LIGHT} !important;"

            c_bg = COLOR_HIGHLIGHT_THR_RES
            c_txt = COLOR_HIGHLIGHT_THR_RES_TXT
            style_matrix.iloc[
                i, 2] = f"background-color: {c_bg}; color: {c_txt}; font-weight: bold; border-right: 1px solid {c_bg}; border-bottom: 2px solid {WEB_COLOR_BORDER_LIGHT} !important;"
            style_matrix.iloc[i, 3] = f"border-bottom: 2px solid {WEB_COLOR_BORDER_LIGHT} !important;"
        else:
            style_matrix.iloc[i, 0] = "text-align: right !important; font-weight: bold;"
            style_matrix.iloc[i, 1] = f"background-color: {COLOR_HIGHLIGHT_EXP_VAL}; color: white; font-weight: bold;"

            if val_thr_class == "be-val-thr-unreachable":
                style_matrix.iloc[
                    i, 2] = "background-color: #d99b00; color: #261b00; font-weight: bold; border-right: 1px solid #d99b00;"
            else:
                style_matrix.iloc[
                    i, 2] = f"background-color: {COLOR_HIGHLIGHT_THR_VAL}; color: {COLOR_HIGHLIGHT_THR_TXT}; font-weight: bold;"

            if margin_class == "be-margin-safe":
                style_matrix.iloc[i, 3] = "background-color: #2e7d32; color: #ffffff; font-weight: bold;"
            elif margin_class == "be-margin-caution":
                style_matrix.iloc[
                    i, 3] = f"background-color: {COLOR_ALERT_SUCCESS_BG}; color: {COLOR_ALERT_SUCCESS_TXT}; font-weight: bold;"
            elif margin_class == "be-margin-warning":
                style_matrix.iloc[
                    i, 3] = f"background-color: {COLOR_ALERT_DANGER_BG}; color: {COLOR_ALERT_DANGER_TXT}; font-weight: bold;"
            elif margin_class == "be-margin-danger":
                style_matrix.iloc[i, 3] = "background-color: #CD5C5C; color: white; font-weight: bold;"

    return style_matrix
