import pandas as pd
from IPython.display import HTML

from src.config import variable_names, plots


def get_break_even_dataframe(data_list, output_name):
    """
    Transforms a list of sensitivity dictionaries into a
    structured DataFrame using configured column constants.
    """
    processed_rows = []

    for item in data_list:
        # Row 1 (Visual): Impact Results (Outputs)
        processed_rows.append({
            plots.SENSITIVITY_VARIABLE: output_name,
            plots.BREAK_EVEN_COLUMN_NAME_BASE: item[variable_names.BREAK_EVEN_EXPECTED_RESULT],
            plots.BREAK_EVEN_COLUMN_NAME_THRESHOLD: item[variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT],
            plots.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN: None
        })

        # Row 2 (Visual): Input Values (VARIABLEs)
        processed_rows.append({
            plots.SENSITIVITY_VARIABLE: item[variable_names.BREAK_EVEN_VARIABLE_NAME],
            plots.BREAK_EVEN_COLUMN_NAME_BASE: item[variable_names.BREAK_EVEN_EXPECTED_VARIABLE_VALUE],
            plots.BREAK_EVEN_COLUMN_NAME_THRESHOLD: item[variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE],
            plots.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN: f"{item.get(variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE, 0.0):.1%}"
        })

    columns = [
        plots.SENSITIVITY_VARIABLE,
        plots.BREAK_EVEN_COLUMN_NAME_BASE,
        plots.BREAK_EVEN_COLUMN_NAME_THRESHOLD,
        plots.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN
    ]
    return pd.DataFrame(processed_rows, columns=columns)


def render_break_even_dashboard(data_list, output_name):
    html = f"""
            <style>
                .dash-table {{ border-collapse: collapse; font-family: 'Segoe UI', Tahoma, Geneva, sans-serif; width: 100%; margin: 15px 0; border: 1px solid #dee2e6; }}
                .dash-table th {{ background-color: #f1f3f5; color: #495057; padding: 12px; border-bottom: 2px solid #dee2e6; text-align: right; text-transform: uppercase; font-size: 0.85rem; }}
                .dash-table td {{ padding: 10px 15px; border-bottom: 1px solid #eee; text-align: right; font-variant-numeric: tabular-nums; }}

                .text-left {{ text-align: left !important; }}
                .sub-label {{ padding-left: 25px !important; color: #6c757d; font-style: italic; font-size: 0.9rem; }}

                /* Cell Styling */
                .val-exp {{ background-color: #4682B4; color: white; font-weight: bold; }}
                .val-thr {{ background-color: #CD5C5C; color: white; font-weight: bold; }}
                .res-exp {{ background-color: #e7f5ff; border-right: 1px solid #d0ebff; }}
                .res-thr {{ background-color: #fff5f5; border-right: 1px solid #ffe3e3; }}

                .margin-safe {{ background-color: #d4edda; color: #155724; font-weight: bold; }}
                .margin-warning {{ background-color: #F4D03F; color: #856404; font-weight: bold; }}
            </style>
            <table class="dash-table">
                <thead>
                    <tr>
                        <th class="text-left">{plots.SENSITIVITY_VARIABLE}</th>
                        <th>{plots.BREAK_EVEN_COLUMN_NAME_BASE}</th>
                        <th>{plots.BREAK_EVEN_COLUMN_NAME_THRESHOLD}</th>
                        <th>{plots.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN}</th>
                    </tr>
                </thead>
                <tbody>"""

    for item in data_list:
        margin_val = item.get(variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE, 0.0)
        margin_class = "margin-safe" if margin_val > 0 else "margin-warning"

        ## Row 1 (Visual): Impact Results (Outputs)
        html += f"""
                <tr>
                    <td class="text-left sub-label">{output_name}</td>
                    <td class="res-exp">${item[variable_names.BREAK_EVEN_EXPECTED_RESULT]:,.0f}</td>
                    <td class="res-thr">${item[variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT]:,.0f}</td>
                    <td style="border-bottom: 2px solid #dee2e6;">&nbsp;</td>
                </tr>"""

        ## Row 2 (Visual): Input Values (variables)
        html += f"""
                <tr>
                    <td class="text-left"><strong>{item[variable_names.BREAK_EVEN_VARIABLE_NAME]}</strong></td>
                    <td class="val-exp">{item[variable_names.BREAK_EVEN_EXPECTED_VARIABLE_VALUE]:,.2f}</td>
                    <td class="val-thr">{item[variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE]:,.2f}</td>
                    <td class="{margin_class}">{margin_val:.1%}</td>
                </tr>"""

    html += "</tbody></table>"
    return HTML(html)
