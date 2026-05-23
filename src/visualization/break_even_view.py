import pandas as pd
from IPython.display import HTML

from src.config import variable_names, plots
from src.config.formatting import VARIABLE_FORMATTING_MAP
from src.utils.formatting import fmt
from .break_even_styles import BREAK_EVEN_TABLE_STYLESHEET, BREAK_EVEN_DASHBOARD_TEMPLATE


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
        # Row 1 (Visual): Impact Results (Outputs)
        processed_rows.append({
            plots.SENSITIVITY_VARIABLE: f"└─ {output_name}",
            plots.BREAK_EVEN_COLUMN_NAME_BASE: item[variable_names.BREAK_EVEN_EXPECTED_RESULT],
            plots.BREAK_EVEN_COLUMN_NAME_THRESHOLD: item[variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT],
            plots.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN: "-"
        })

        # Safe extraction of safety margin percentage
        margin_raw = item.get(variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE)
        margin_str = f"{margin_raw:.1%}" if margin_raw is not None else "N/A"

        # Row 2 (Visual): Input Values (Variables)
        processed_rows.append({
            plots.SENSITIVITY_VARIABLE: item[variable_names.BREAK_EVEN_VARIABLE_NAME],
            plots.BREAK_EVEN_COLUMN_NAME_BASE: item[variable_names.BREAK_EVEN_EXPECTED_VARIABLE_VALUE],
            plots.BREAK_EVEN_COLUMN_NAME_THRESHOLD: item[variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE],
            plots.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN: margin_str
        })

    columns = [
        plots.SENSITIVITY_VARIABLE,
        plots.BREAK_EVEN_COLUMN_NAME_BASE,
        plots.BREAK_EVEN_COLUMN_NAME_THRESHOLD,
        plots.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN
    ]
    return pd.DataFrame(processed_rows, columns=columns)


def render_break_even_dashboard(data_list, output_name):
    """
    Generates a high-fidelity HTML component table with color-coded alerts
    mapped directly to centralized dictionary formatting configurations.
    """
    row_elements = []

    for item in data_list:
        feasibility = item.get("feasibility_status", "CROSSOVER_FOUND")
        margin_val = item.get(variable_names.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE, 0.0)

        # Assign explicit break-even contextual CSS hooks
        if feasibility == "ALWAYS_FEASIBLE":
            margin_class = "be-margin-safe"
            val_thr_class = "be-val-thr"
            res_thr_class = "be-res-thr"
        elif feasibility == "UNREACHABLE":
            margin_class = "be-margin-danger"
            val_thr_class = "be-val-thr-unreachable"
            res_thr_class = "be-res-thr-unreachable"
        elif feasibility == "CROSSOVER_FOUND":
            val_thr_class = "be-val-thr"
            res_thr_class = "be-res-thr"
            margin_class = "be-margin-caution" if margin_val >= 0 else "be-margin-warning"
        else:
            margin_class = "be-margin-warning"
            val_thr_class = "be-val-thr"
            res_thr_class = "be-res-thr"

        var_name = item[variable_names.BREAK_EVEN_VARIABLE_NAME]

        # Resolve format rules dynamically from your centralized dictionary map
        output_formatter = _get_formatter(output_name)
        input_formatter = _get_formatter(var_name)

        # Format variables & results seamlessly without checking types manually
        fmt_exp_res = output_formatter(item[variable_names.BREAK_EVEN_EXPECTED_RESULT])
        fmt_thr_res = output_formatter(item[variable_names.BREAK_EVEN_POINT_THRESHOLD_RESULT])

        fmt_exp_val = input_formatter(item[variable_names.BREAK_EVEN_EXPECTED_VARIABLE_VALUE])
        fmt_thr_val = input_formatter(item[variable_names.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE])

        # Compile Output Row (Results)
        row_elements.append(f"""
            <tr class="be-output-row">
                <td class="be-text-left be-sub-label">{output_name}</td>
                <td class="be-res-exp">{fmt_exp_res}</td>
                <td class="{res_thr_class}">{fmt_thr_res}</td>
                <td>&nbsp;</td>
            </tr>""")

        # Compile Input Row (Variables)
        row_elements.append(f"""
            <tr>
                <td class="be-text-left"><strong>{var_name}</strong></td>
                <td class="be-val-exp">{fmt_exp_val}</td>
                <td class="{val_thr_class}">{fmt_thr_val}</td>
                <td class="{margin_class}">{margin_val:.1%}</td>
            </tr>""")

    compiled_html = BREAK_EVEN_DASHBOARD_TEMPLATE.format(
        styles=BREAK_EVEN_TABLE_STYLESHEET,
        var_header=plots.SENSITIVITY_VARIABLE,
        base_header=plots.BREAK_EVEN_COLUMN_NAME_BASE,
        thr_header=plots.BREAK_EVEN_COLUMN_NAME_THRESHOLD,
        margin_header=plots.BREAK_EVEN_COLUMN_NAME_SAFETY_MARGIN,
        rows="".join(row_elements)
    )

    return HTML(compiled_html)
