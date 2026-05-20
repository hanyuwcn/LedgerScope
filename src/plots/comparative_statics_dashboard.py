import pandas as pd
from IPython.display import HTML

from src.config import variable_names, plots


# from src.config import COMPARATIVE_STATICS_VARIABLE_NAME, \
#     COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE, COMPARATIVE_STATICS_EXPECTED_RESULT, \
#     COMPARATIVE_STATICS_MIN_VARIABLE_VALUE, COMPARATIVE_STATICS_MIN_RESULT, COMPARATIVE_STATICS_MAX_VARIABLE_VALUE, \
#     COMPARATIVE_STATICS_MAX_RESULT, COMPARATIVE_STATICS_ELASTICITY, COMPARATIVE_STATICS_COLUMN_NAME_MIN, \
#     COMPARATIVE_STATICS_COLUMN_NAME_BASE, \
#     COMPARATIVE_STATICS_COLUMN_NAME_MAX, SENSITIVITY_VARIABLE, COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY


def get_comparative_statics_dataframe(data_list, output_name):
    """
        Transforms a list of comparative statics dictionaries into a
        structured DataFrame using configured column constants.
        """
    processed_rows = []

    for item in data_list:
        # Row 1: The Model Outputs (Results)
        processed_rows.append({
            plots.SENSITIVITY_VARIABLE: output_name,
            plots.COMPARATIVE_STATICS_COLUMN_NAME_MIN: item[variable_names.COMPARATIVE_STATICS_MIN_RESULT],
            plots.COMPARATIVE_STATICS_COLUMN_NAME_BASE: item[variable_names.COMPARATIVE_STATICS_EXPECTED_RESULT],
            plots.COMPARATIVE_STATICS_COLUMN_NAME_MAX: item[variable_names.COMPARATIVE_STATICS_MAX_RESULT],
            variable_names.COMPARATIVE_STATICS_ELASTICITY: None
        })

        # Row 2: The Input Factor Values
        processed_rows.append({
            plots.SENSITIVITY_VARIABLE: item[variable_names.COMPARATIVE_STATICS_VARIABLE_NAME],
            plots.COMPARATIVE_STATICS_COLUMN_NAME_MIN: item[variable_names.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE],
            plots.COMPARATIVE_STATICS_COLUMN_NAME_BASE: item[
                variable_names.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE],
            plots.COMPARATIVE_STATICS_COLUMN_NAME_MAX: item[variable_names.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE],
            plots.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY: item[variable_names.COMPARATIVE_STATICS_ELASTICITY]
        })

    columns = [plots.SENSITIVITY_VARIABLE,
               plots.COMPARATIVE_STATICS_COLUMN_NAME_MIN,
               plots.COMPARATIVE_STATICS_COLUMN_NAME_BASE,
               plots.COMPARATIVE_STATICS_COLUMN_NAME_MAX,
               plots.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY]
    return pd.DataFrame(processed_rows, columns=columns)


def render_comparative_statics_dashboard(data_list, output_name):
    html = f"""
            <style>
                .cs-table {{ border-collapse: collapse; font-family: 'Segoe UI', Tahoma, Geneva, sans-serif; width: 100%; margin: 15px 0; border: 1px solid #dee2e6; }}
                .cs-table th {{ background-color: #f1f3f5; color: #495057; padding: 12px 15px; border-bottom: 2px solid #dee2e6; text-align: right; text-transform: uppercase; font-size: 0.85rem; }}
                .cs-table td {{ padding: 10px 15px; border-bottom: 1px solid #eee; text-align: right; font-variant-numeric: tabular-nums; }}

                .text-left {{ text-align: left !important; }}
                .sub-label {{ padding-left: 25px !important; color: #6c757d; font-style: italic; font-size: 0.9rem; }}

                /* Row Base Overrides */
                .row-factor {{ background-color: #f8f9fa; }}
                .row-output {{ background-color: #ffffff; }}

                /* Inverted Cell Styling Palette */
                .val-heavy-blue {{ background-color: #4682B4; color: white; font-weight: bold; }}
                .val-heavy-red {{ background-color: #CD5C5C; color: white; font-weight: bold; }}

                .res-light-blue {{ background-color: #e7f5ff; border: 1px solid #d0ebff; }}
                .res-light-red {{ background-color: #fff5f5; border: 1px solid #ffe3e3; }}

                .elasticity-positive {{ background-color: #d4edda; color: #155724; font-weight: bold; }}
                .elasticity-negative {{ background-color: #F4D03F; color: #856404; font-weight: bold; }}
            </style>
            <table class="cs-table">
                <thead>
                    <tr>
                        <th class="text-left">{plots.SENSITIVITY_VARIABLE}</th>
                        <th>{plots.COMPARATIVE_STATICS_COLUMN_NAME_MIN}</th>
                        <th>{plots.COMPARATIVE_STATICS_COLUMN_NAME_BASE}</th>
                        <th>{plots.COMPARATIVE_STATICS_COLUMN_NAME_MAX}</th>
                        <th>{plots.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY}</th>
                    </tr>
                </thead>
                <tbody>"""

    for item in data_list:
        elasticity_val = item.get(variable_names.COMPARATIVE_STATICS_ELASTICITY, 0.0)
        elasticity_class = "elasticity-positive" if elasticity_val >= 0 else "elasticity-negative"

        ## Row 1 (Visual): Impact Results (Outputs) -> Light Blue | White | Light Red
        html += f"""
                <tr class="row-output">
                    <td class="text-left sub-label">{output_name}</td>
                    <td class="res-light-blue">${item[variable_names.COMPARATIVE_STATICS_MIN_RESULT]:,.0f}</td>
                    <td>${item[variable_names.COMPARATIVE_STATICS_EXPECTED_RESULT]:,.0f}</td>
                    <td class="res-light-red">${item[variable_names.COMPARATIVE_STATICS_MAX_RESULT]:,.0f}</td>
                    <td style="border-bottom: 2px solid #dee2e6;">&nbsp;</td>
                </tr>"""

        ## Row 2 (Visual): Input Values (Factors) -> Heavy Blue | Grey | Heavy Red | Elasticity
        html += f"""
                <tr class="row-factor">
                    <td class="text-left"><strong>{item[variable_names.COMPARATIVE_STATICS_VARIABLE_NAME]}</strong></td>
                    <td class="val-heavy-blue">{item[variable_names.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE]:,.2f}</td>
                    <td>{item[variable_names.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE]:,.2f}</td>
                    <td class="val-heavy-red">{item[variable_names.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE]:,.2f}</td>
                    <td class="{elasticity_class}">{elasticity_val:+.2f}</td>
                </tr>"""

    html += "</tbody></table>"
    return HTML(html)
