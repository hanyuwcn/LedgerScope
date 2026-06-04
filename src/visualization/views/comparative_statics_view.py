import pandas as pd
from IPython.display import HTML

from src.config import variable_names
from src.config.formatting import VARIABLE_FORMATTING_MAP
from src.utils.formatting import fmt
from src.visualization.styles import comparative_statics_styles


def _get_formatter(var_name):
    """Retrieves the assigned lambda from the map, falling back to a safe layout."""
    return VARIABLE_FORMATTING_MAP.get(var_name, lambda v: fmt(v, d=2))


def get_comparative_statics_dataframe(data_list, output_name):
    """
    Transforms a list of comparative statics dictionaries into a
    structured DataFrame using configured column constants.
    """
    processed_rows = []

    for item in data_list:
        # Row 1: The Model Outputs (Results)
        processed_rows.append({
            comparative_statics_styles.SENSITIVITY_VARIABLE: output_name,
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MIN: item[
                variable_names.COMPARATIVE_STATICS_MIN_RESULT],
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_BASE: item[
                variable_names.COMPARATIVE_STATICS_EXPECTED_RESULT],
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MAX: item[
                variable_names.COMPARATIVE_STATICS_MAX_RESULT],
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY: None
        })

        # Row 2: The Input Factor Values
        processed_rows.append({
            comparative_statics_styles.SENSITIVITY_VARIABLE: item[variable_names.COMPARATIVE_STATICS_VARIABLE_NAME],
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MIN: item[
                variable_names.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE],
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_BASE: item[
                variable_names.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE],
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MAX: item[
                variable_names.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE],
            comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY: item[
                variable_names.COMPARATIVE_STATICS_ELASTICITY]
        })

    columns = [comparative_statics_styles.SENSITIVITY_VARIABLE,
               comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MIN,
               comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_BASE,
               comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MAX,
               comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY]
    return pd.DataFrame(processed_rows, columns=columns)


def render_comparative_statics_dashboard(data_list, output_name):
    """Generates an HTML matrix layout dashboard for comparative statics inside notebooks."""
    html = f"""
            {comparative_statics_styles.COMPARATIVE_STATICS_STYLE}
            <table class="cs-table">
                <thead>
                    <tr>
                        <th class="text-left">{comparative_statics_styles.SENSITIVITY_VARIABLE}</th>
                        <th>{comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MIN}</th>
                        <th>{comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_BASE}</th>
                        <th>{comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_MAX}</th>
                        <th>{comparative_statics_styles.COMPARATIVE_STATICS_COLUMN_NAME_ELASTICITY}</th>
                    </tr>
                </thead>
                <tbody>"""

    for item in data_list:
        try:
            elasticity_val = float(item.get(variable_names.COMPARATIVE_STATICS_ELASTICITY, 0.0))
        except (ValueError, TypeError):
            elasticity_val = 0.0

        if elasticity_val > 0:
            elasticity_class = "elasticity-positive"
            elasticity_str = f"{elasticity_val:+.2f}"
        elif elasticity_val < 0:
            elasticity_class = "elasticity-negative"
            elasticity_str = f"{elasticity_val:+.2f}"
        else:
            elasticity_class = ""
            elasticity_str = "0.00"

        var_name = item[variable_names.COMPARATIVE_STATICS_VARIABLE_NAME]

        # Resolve formatting rules dynamically from your configuration map
        output_formatter = _get_formatter(output_name)
        input_formatter = _get_formatter(var_name)

        # Apply formatting map rules effortlessly to results (outputs)
        min_res = output_formatter(item[variable_names.COMPARATIVE_STATICS_MIN_RESULT])
        base_res = output_formatter(item[variable_names.COMPARATIVE_STATICS_EXPECTED_RESULT])
        max_res = output_formatter(item[variable_names.COMPARATIVE_STATICS_MAX_RESULT])

        # Apply formatting map rules effortlessly to input variables
        min_val = input_formatter(item[variable_names.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE])
        base_val = input_formatter(item[variable_names.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE])
        max_val = input_formatter(item[variable_names.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE])

        html += f"""
                <tr class="row-output">
                    <td class="text-left sub-label">{output_name}</td>
                    <td class="res-dark-yellow">{min_res}</td>
                    <td class="res-light-blue">{base_res}</td>
                    <td class="res-dark-yellow">{max_res}</td>
                    <td style="border-bottom: 2px solid #dee2e6;">&nbsp;</td>
                </tr>
                <tr class="row-factor">
                    <td class="text-left"><strong>{var_name}</strong></td>
                    <td class="val-light-yellow">{min_val}</td>
                    <td class="val-heavy-blue">{base_val}</td>
                    <td class="val-light-yellow">{max_val}</td>
                    <td class="{elasticity_class}">{elasticity_str}</td>
                </tr>"""

    html += "</tbody></table>"
    return HTML(html)
