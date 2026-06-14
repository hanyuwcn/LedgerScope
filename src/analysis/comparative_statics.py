import numpy as np

from src.config import variable_names as vn
from src.engine import evaluate_variable_scenario_sweep
from src.utils import check_variables_for_function, check_model_pipeline_topology_order


def comparative_statics(
        variables: dict,
        selected_variables: list[str],
        model_pipeline: list,
        output_name: str
) -> list[dict]:
    """
    Executes a comprehensive sensitivity sweep across multiple targeted operational
    variables to evaluate their isolated impact on a designated model performance metric.

    This routine functions as the master orchestration layer, validating structural setup
    constraints, looping over each requested parameter, and aggregating individual
    sensitivity profiles into a unified analytical summary report.

    Args:
        variables (dict): The complete registry of active project variables, mapping string
            identifiers to variable instance objects (which expose boundary retrieval methods).
        selected_variables (list[str]): Explicit subset of variable identifier keys targeted
            for isolation and sensitivity charting.
        model_pipeline (list): Ordered sequence of structural domain models passed into
            the centralized execution engine.
        output_name (str): The explicit key signature of the target evaluation metric being
            monitored inside the output payload dictionary (e.g., 'Total Cost').

    Raises:
        ValueError: If any target tracking variable key is missing from the global operational registry.
        TypeError: If the chronological ordering or validation sequence of the model pipeline is violated.

    Returns:
        list[dict]: A list of aggregated sensitivity records, where each record contains the complete boundary
            outcomes, step evaluations, and calculated elasticity coefficient for a single variable.
    """
    check_variables_for_function(variables, selected_variables)
    check_model_pipeline_topology_order(model_pipeline)

    comparative_statics_report = []
    for variable_key in selected_variables:
        variable_report = get_comparative_statics_for_one_variable(
            variables=variables,
            selected_variable=variable_key,
            model_pipeline=model_pipeline,
            output_name=output_name
        )
        comparative_statics_report.append(variable_report)

    return comparative_statics_report


def get_comparative_statics_for_one_variable(
        variables: dict,
        selected_variable: str,
        model_pipeline: list,
        output_name: str
) -> dict:
    """
    Isolates a single independent variable and profiles its mathematical impact on a
    dependent metric by running scenarios across its minimum, expected, and maximum boundaries.

    While evaluating the target parameter, all other concurrent ledger variables are locked firmly
    at their baseline `expected_value` states to maintain strict ceteris paribus (all else being equal)
    analytical isolation.

    Args:
        variables (dict): The complete global variable dictionary framework.
        selected_variable (str): The specific identifier key of the single variable being investigated.
        model_pipeline (list): The sequence of pipeline execution blocks used to calculate outcomes.
        output_name (str): The targeted outcome metric key extracted from the resulting calculation matrix.

    Returns:
        dict: A sanitized, JSON-compliant sensitivity dataset containing the boundary matrix inputs,
            their corresponding downstream evaluations, and the localized operational elasticity metric.
    """
    single_variable_analysis_report = {vn.COMPARATIVE_STATICS_VARIABLE_NAME: selected_variable}

    # Extract baseline dictionary and pull specific range benchmarks under ceteris paribus constraints
    variable_instance = variables[selected_variable]

    independent_variable_steps = [
        variable_instance.min_value,
        variable_instance.expected_value,
        variable_instance.max_value
    ]

    # Dynamically inject boundary modifications while holding other factors static
    variable_scenario_outcomes = evaluate_variable_scenario_sweep(variables, selected_variable,
                                                                  independent_variable_steps, model_pipeline)
    dependent_scenario_outcomes = [outcome[output_name] for outcome in variable_scenario_outcomes]

    # Record independent range inputs
    single_variable_analysis_report[vn.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE] = independent_variable_steps[
        0]
    single_variable_analysis_report[vn.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE] = \
        independent_variable_steps[1]
    single_variable_analysis_report[vn.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE] = independent_variable_steps[
        2]

    # Record dependent model outcomes
    single_variable_analysis_report[vn.COMPARATIVE_STATICS_MIN_RESULT] = dependent_scenario_outcomes[0]
    single_variable_analysis_report[vn.COMPARATIVE_STATICS_EXPECTED_RESULT] = dependent_scenario_outcomes[1]
    single_variable_analysis_report[vn.COMPARATIVE_STATICS_MAX_RESULT] = dependent_scenario_outcomes[2]

    # Calculate elasticity utilizing structural parameter lookups
    single_variable_analysis_report[vn.COMPARATIVE_STATICS_ELASTICITY] = compute_elasticity(
        **single_variable_analysis_report)

    # Sanitize payload from NumPy data structures to native Python primitives for secure JSON transmission
    return {
        key: (val.item() if isinstance(val, np.generic) else val)
        for key, val in single_variable_analysis_report.items()
    }


def compute_elasticity(**kwargs) -> float:
    """
    Measures the localized point responsiveness percentage of a dependent performance
    metric relative to an isolated percentage change in its driving independent variable.

    Mathematical Representation:
        $$\text{Elasticity} = \frac{\Delta Y / Y_{\text{expected}}}{\Delta X / X_{\text{expected}}} = \left(\frac{Y_{\text{max}} - Y_{\text{min}}}{X_{\text{max}} - X_{\text{min}}}\right) \times \left(\frac{X_{\text{expected}}}{Y_{\text{expected}}}\right)$$

    Economic Interpretation:
        *   An elasticity value where $|\epsilon| > 1.0$ implies high sensitivity (elasticity).
        *   An elasticity value where $|\epsilon| < 1.0$ denotes an insulated, less-sensitive structure (inelasticity).

    Safety Layer:
        Intercepts structural zero conditions directly. If the independent variable boundary range
        is flat ($\Delta X = 0$) or the baseline metric position operates at an equilibrium point of zero
        ($Y_{\text{expected}} = 0$), the execution returns `0.0` defensively to eliminate runtime arithmetic crashes.

    Args:
        **kwargs: Arbitrary keyword dictionary container which must hold the complete suite of
            six specific metric keys representing boundaries and baseline coordinates.

    Raises:
        KeyError: If any required analysis dictionary key is omitted from the input configuration.

    Returns:
        float: The final isolated elasticity ratio coefficient. Returns 0.0 under undefined zero boundaries.
    """
    check_variables_for_function(kwargs, [
        vn.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE,
        vn.COMPARATIVE_STATICS_EXPECTED_RESULT,
        vn.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE,
        vn.COMPARATIVE_STATICS_MIN_RESULT,
        vn.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE,
        vn.COMPARATIVE_STATICS_MAX_RESULT
    ])

    independent_expected = kwargs[vn.COMPARATIVE_STATICS_EXPECTED_VARIABLE_VALUE]
    dependent_expected = kwargs[vn.COMPARATIVE_STATICS_EXPECTED_RESULT]

    independent_min = kwargs[vn.COMPARATIVE_STATICS_MIN_VARIABLE_VALUE]
    dependent_min = kwargs[vn.COMPARATIVE_STATICS_MIN_RESULT]

    independent_max = kwargs[vn.COMPARATIVE_STATICS_MAX_VARIABLE_VALUE]
    dependent_max = kwargs[vn.COMPARATIVE_STATICS_MAX_RESULT]

    # Intercept condition 1: Flat boundary parameters across evaluation steps (zero parameter runway)
    delta_independent = independent_max - independent_min
    if delta_independent == 0.0:
        return 0.0

    # Intercept condition 2: Balanced net-zero baseline evaluation point (infinite percentage surge)
    if dependent_expected == 0.0:
        return 0.0

    # Execute traditional point-responsiveness derivative formulation
    marginal_slope = (dependent_max - dependent_min) / delta_independent
    elasticity_coefficient = marginal_slope * (independent_expected / dependent_expected)

    return float(elasticity_coefficient)
