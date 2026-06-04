"""
break_even_styles.py
Dedicated design system and HTML components for Break-Even / Sensitivity tables.
"""

from .common import (
    COLOR_NAVY,
    WEB_FONT_FAMILY,
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

# High-fidelity dashboard component stylesheet isolated to break-even matrices
# Note: Double curly braces {{ }} preserve native CSS rules within the Python f-string
BREAK_EVEN_TABLE_STYLESHEET = f"""
<style>
    .be-dash-table {{ 
        border-collapse: collapse; 
        font-family: {WEB_FONT_FAMILY}; 
        width: 100%; 
        margin: 15px 0; 
        border: 1px solid {WEB_COLOR_BORDER_LIGHT}; 
    }}
    .be-dash-table th {{ 
        background-color: {WEB_COLOR_HEADER_BG}; 
        color: {COLOR_NAVY}; 
        padding: 12px; 
        border-bottom: 2px solid {WEB_COLOR_BORDER_LIGHT}; 
        text-align: right; 
        text-transform: uppercase; 
        font-size: 0.85rem; 
    }}
    .be-dash-table td {{ 
        padding: 10px 15px; 
        border-bottom: 1px solid {WEB_COLOR_BORDER_ROW}; 
        text-align: right; 
        font-variant-numeric: tabular-nums; 
    }}

    .be-text-left {{ text-align: left !important; }}
    .be-sub-label {{ padding-left: 25px !important; color: {WEB_COLOR_SUB_LABEL}; font-style: italic; font-size: 0.9rem; }}

    /* Row border normalization */
    .be-output-row td {{ border-bottom: 2px solid {WEB_COLOR_BORDER_LIGHT} !important; }}

    /* Data Cells Core Styling */
    .be-val-exp {{ background-color: {COLOR_HIGHLIGHT_EXP_VAL}; color: white; font-weight: bold; }}
    .be-res-exp {{ background-color: {COLOR_HIGHLIGHT_EXP_RES}; border-right: 1px solid {COLOR_HIGHLIGHT_EXP_BORDER}; }}

    /* Threshold Palette (Yellow Category) */
    .be-val-thr {{ background-color: {COLOR_HIGHLIGHT_THR_VAL}; color: {COLOR_HIGHLIGHT_THR_TXT}; font-weight: bold; }}
    .be-res-thr {{ background-color: {COLOR_HIGHLIGHT_THR_RES}; color: {COLOR_HIGHLIGHT_THR_RES_TXT}; font-weight: bold; border-right: 1px solid {COLOR_HIGHLIGHT_THR_RES}; }}

    /* Dynamic Darker Yellow for Unreachable Output State */
    .be-val-thr-unreachable {{ background-color: #d99b00; color: #261b00; font-weight: bold; border-right: 1px solid #d99b00; }}
    .be-res-thr-unreachable {{ background-color: {COLOR_HIGHLIGHT_THR_RES}; color: {COLOR_HIGHLIGHT_THR_RES_TXT}; font-weight: bold; border-right: 1px solid {COLOR_HIGHLIGHT_THR_RES}; }}

    /* Coordinated Feasibility Classes */
    .be-margin-safe {{ background-color: #2e7d32; color: #ffffff; font-weight: bold; }}
    .be-margin-caution {{ background-color: {COLOR_ALERT_SUCCESS_BG}; color: {COLOR_ALERT_SUCCESS_TXT}; font-weight: bold; }}
    .be-margin-warning {{ background-color: {COLOR_ALERT_DANGER_BG}; color: {COLOR_ALERT_DANGER_TXT}; font-weight: bold; }}
    .be-margin-danger {{ background-color: #CD5C5C; color: white; font-weight: bold; }}
</style>
"""

BREAK_EVEN_DASHBOARD_TEMPLATE = """
{styles}
<table class="be-dash-table">
    <thead>
        <tr>
            <th class="be-text-left">{var_header}</th>
            <th>{base_header}</th>
            <th>{thr_header}</th>
            <th>{margin_header}</th>
        </tr>
    </thead>
    <tbody>
        {rows}
    </tbody>
</table>
"""
