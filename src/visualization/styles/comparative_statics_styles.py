"""
CSS Layout Configuration for Comparative Statics Dashboard.
Following the project's isolated view styling pattern.
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
    COLOR_ALERT_DANGER_TXT,

)

SENSITIVITY_VARIABLE = "Sensitivity Variable"

COMPARATIVE_STATICS_COLUMN_NAME_MIN = 'Min State'
COMPARATIVE_STATICS_COLUMN_NAME_BASE = 'Base (Expected)'
COMPARATIVE_STATICS_COLUMN_NAME_MAX = 'Max State'
COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY = "Elasticity"

# High-fidelity component stylesheet reading from centralized tokens
COMPARATIVE_STATICS_STYLE = f"""
<style>
    .cs-table {{
        border-collapse: collapse;
        font-family: {WEB_FONT_FAMILY};
        width: 100%;
        margin: 15px 0;
        border: 1px solid {WEB_COLOR_BORDER_LIGHT};
    }}
    .cs-table th {{
        background-color: {WEB_COLOR_HEADER_BG};
        color: {COLOR_NAVY};
        padding: 12px 15px;
        border-bottom: 2px solid {WEB_COLOR_BORDER_LIGHT};
        text-align: right;
        text-transform: uppercase;
        font-size: 0.85rem;
    }}
    .cs-table td {{
        padding: 10px 15px;
        border-bottom: 1px solid {WEB_COLOR_BORDER_ROW};
        text-align: right;
        font-variant-numeric: tabular-nums;
    }}

    .text-left {{ text-align: left !important; }}
    .sub-label {{ padding-left: 25px !important; color: {WEB_COLOR_SUB_LABEL}; font-style: italic; font-size: 0.9rem; }}

    /* Row Base Overrides */
    .row-factor {{ background-color: #f8f9fa; }}
    .row-output {{ background-color: #ffffff; }}

    /* Color Configurations */
    .val-heavy-blue {{ background-color: {COLOR_HIGHLIGHT_EXP_VAL}; color: white; font-weight: bold; }}
    .res-light-blue {{ background-color: {COLOR_HIGHLIGHT_EXP_RES}; border-right: 1px solid {COLOR_HIGHLIGHT_EXP_BORDER}; font-weight: bold; }}

    .val-light-yellow {{ background-color: {COLOR_HIGHLIGHT_THR_VAL}; color: {COLOR_HIGHLIGHT_THR_TXT}; font-weight: bold; }}
    .res-dark-yellow {{ background-color: {COLOR_HIGHLIGHT_THR_RES}; color: {COLOR_HIGHLIGHT_THR_RES_TXT}; font-weight: bold; border-right: 1px solid {COLOR_HIGHLIGHT_THR_RES}; }}

    .elasticity-positive {{ background-color: {COLOR_ALERT_SUCCESS_BG}; color: {COLOR_ALERT_SUCCESS_TXT}; font-weight: bold; }}
    .elasticity-negative {{ background-color: {COLOR_ALERT_DANGER_BG}; color: {COLOR_ALERT_DANGER_TXT}; font-weight: bold; }}
</style>
"""

## TODO: apply this template for comparative statics, even better apply the `SHARED_DASHBOARD_HTML_TEMPLATE` from common
COMPARATIVE_STATICS_DASHBOARD_TEMPLATE = """
{styles}
<table class="cs-table">
    <thead>
        <tr>
            <th class="text-left">{var_header}</th>
            <th>{min_header}</th>
            <th>{base_header}</th>
            <th>{max_header}</th>
            <th>{elasticity_header}</th>
        </tr>
    </thead>
    <tbody>
        {rows}
    </tbody>
</table>
"""
