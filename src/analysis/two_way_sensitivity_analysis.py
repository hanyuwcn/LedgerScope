import copy

import pandas as pd

from src.config import settings
from src.engine import evaluate_chained_models
from src.utils import check_model_pipeline_topology_order


def run_two_way_sensitivity_analysis(
        variables: dict,
        param_x_name: str,
        param_y_name: str,
        model_pipeline: list,
        target_output_name: str,
        x_steps: int = settings.NUMS_IN_RANGE,
        y_steps: int = settings.NUMS_IN_RANGE,
        reverse_x: bool = False,
        reverse_y: bool = True
) -> pd.DataFrame:
    """Executes a Two-Way Sensitivity Analysis across a grid matrix of two parameters.

    Iterates through all joint combinations of ranges generated for two specified
    independent input variables, executing the full model pipeline sequence for each
    coordinate to map out their co-dependent impact on a single targeted outcome metric.

    Args:
        variables (dict): A dictionary mapping domain variable names to their
            respective Variable objects or raw primitive numbers.
        param_x_name (str): The dictionary key name of the independent variable
            moving along the horizontal axis (DataFrame columns vector).
        param_y_name (str): The dictionary key name of the independent variable
            moving along the vertical axis (DataFrame index vector).
        model_pipeline (list): A ordered sequence of callable calculation models/modules
            used to cascade variables downstream.
        target_output_name (str): The specific dictionary key name of the final
            KPI output to capture and record in the resulting matrix cells.
        x_steps (int, optional): The number of value iterations to pick across
            the parameter X range. Defaults to `settings.NUMS_IN_RANGE`.
        y_steps (int, optional): The number of value iterations to pick across
            the parameter Y range. Defaults to `settings.NUMS_IN_RANGE`.
        reverse_x (bool, optional): Determines if the generated horizontal X-axis
            vector should have its sorting order flipped. Defaults to False.
        reverse_y (bool, optional): Determines if the generated vertical Y-axis
            vector should have its sorting order flipped. Defaults to True to place
            the lowest numerical values in the bottom-left corner of the grid matrix.

    Raises:
        ValueError: If `param_x_name` or `param_y_name` is detected inside the
            pipeline's downstream output state dictionary, indicating a failure
            of the independent variable condition requirement.
        KeyError: If the requested `target_output_name` cannot be resolved within
            the evaluated output dictionary returned by the execution pipeline.

    Returns:
        pd.DataFrame: A cross-tabulated matrix containing the evaluated calculations.
            The index matches raw floating-point Y parameters, columns match X parameters,
            and the respective name properties match their variable string fields.
    """

    # 1. Enforce Structural Input & Pipeline Guardrails    check_variables_for_function(variables, [param_x_name, param_y_name])
    check_model_pipeline_topology_order(model_pipeline)

    # Extract baseline primitive values seamlessly
    baseline_primitives = {
        name: var.get_value() if hasattr(var, "get_value") else var
        for name, var in variables.items()
    }

    # 2. Extract Range Arrays (Kept pure, un-rounded, and intact)
    x_values = variables[param_x_name].get_range_values(num=x_steps)
    y_values = variables[param_y_name].get_range_values(num=y_steps)

    if reverse_x:
        x_values = x_values[::-1]
    if reverse_y:
        y_values = y_values[::-1]

    # 3. Compute Grid Matrix Layout
    sensitivity_grid = []

    for y_val in y_values:
        row_results = []
        for x_val in x_values:
            # Deep-copy primitive baseline state to block multi-threading pointer collision leaks
            runtime_state = copy.deepcopy(baseline_primitives)

            # Inject current matrix coordinates explicitly
            runtime_state[param_x_name] = x_val
            runtime_state[param_y_name] = y_val

            # Execute calculations cascade
            evaluated_outputs = evaluate_chained_models(runtime_state, model_pipeline)

            if target_output_name not in evaluated_outputs:
                raise KeyError(
                    f"Target tracking variable '{target_output_name}' missing from calculation cascade. "
                    f"Available outputs: {list(evaluated_outputs.keys())}"
                )

            row_results.append(evaluated_outputs[target_output_name])
        sensitivity_grid.append(row_results)

    # 4. Wrap inside a structured, multi-index Dataframe matrix
    analysis_df = pd.DataFrame(
        data=sensitivity_grid,
        index=y_values,
        columns=x_values
    )
    analysis_df.index.name = param_y_name
    analysis_df.columns.name = param_x_name

    # matrix = [[int(ele) for ele in row] for row in sensitivity_grid]
    # print(matrix)

    return analysis_df
