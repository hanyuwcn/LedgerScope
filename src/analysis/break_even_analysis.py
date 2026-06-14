import numpy as np

from src.config import variable_names as vn, settings, messages
from src.engine import evaluate_variable_scenario_sweep, evaluate_expected_scenario
from src.utils import check_variables_for_function, check_model_pipeline_topology_order, log


def break_even_analysis(variables: dict, selected_variables: list, model_pipeline: list, output_name: str,
                        goal: float = 0.0) -> list[dict]:
    """
    Executes a multi-variable break-even analysis across a sequence of chained models.

    This function evaluates how changes to independent variables affect a targeted model output
    relative to a specific business benchmark (the goal). It repeats the analysis individually
    for each selected variable while keeping all other baseline parameters static.

    Args:
        variables (dict): The complete registry of project variables mapping names to their value objects.
        selected_variables (list): Explicit list of variable identifier strings to isolate and analyze.
        model_pipeline (list): Sequence of model execution steps passed into the evaluation engine.
        output_name (str): The specific dictionary key of the metric targeted for the goal (e.g., 'FCF').
        goal (float, optional): The target financial or operational benchmark. Defaults to 0.0.

    Returns:
        list[dict]: A list of clean, JSON-serializable dictionaries containing key metrics
                    and safety margins for each analyzed variable, structured for dashboard consumption.
    """
    check_variables_for_function(variables, selected_variables)
    check_model_pipeline_topology_order(model_pipeline)

    break_even_analysis_report = []
    for variable in selected_variables:
        try:
            variable_break_even_report = get_break_even_analysis_for_one_variable(
                variables, variable, model_pipeline, output_name, goal
            )
            break_even_analysis_report.append(variable_break_even_report)
        except ValueError:
            continue

    return break_even_analysis_report


def get_break_even_analysis_for_one_variable(variables: dict, selected_variable: str, model_pipeline: list,
                                             output_name: str, goal: float = 0.0) -> dict:
    """
    Evaluates a single variable to locate its break-even point and calculate its safety margin headroom.

    The function generates an operational range for the isolated variable, evaluates the pipeline results,
    and handles boundary states based on business rules:
      - If the goal is always achieved, it flags the boundary driving the smallest surplus.
      - If the goal is never achieved, it flags the boundary driving the largest result (closest to target).
      - If a natural crossover exists, it executes an optimal binary search to pinpoint the threshold.

    Args:
        variables (dict): Registry of variable entities.
        selected_variable (str): Name of the variable currently being isolated.
        model_pipeline (list): Executable sequence of chained business models.
        output_name (str): Key of the isolated performance indicator tracked against the goal.
        goal (float, optional): Target baseline benchmark. Defaults to 0.0.

    Raises:
        ValueError: Emitted if changing the variable yields a non-monotonic result curve.

    Returns:
        dict: Sanitized payload metrics including baseline values, break-even thresholds,
              directional safety margins, and a discrete feasibility status code for UI routing.
    """
    # Initialize report map with baseline structural metadata
    variable_analysis_report = {
        vn.BREAK_EVEN_VARIABLE_NAME: selected_variable,
        vn.BREAK_EVEN_FEASIBILITY_STATUS: messages.BREAK_EVEN_FEASIBILITY_STATUS_CROSSOVER
    }

    # 1. Capture baseline model state and extract the expected outcome
    expected_variable_val = variables[selected_variable].expected_value

    variable_analysis_report[vn.BREAK_EVEN_EXPECTED_VARIABLE_VALUE] = expected_variable_val
    variable_analysis_report[vn.BREAK_EVEN_EXPECTED_RESULT] = \
        evaluate_expected_scenario(variables, model_pipeline)[output_name]

    # 2. Simulate range scenarios for the target variable
    variable_test_range = variables[selected_variable].get_range_values(num=settings.NUMS_IN_RANGE)
    variable_scenario_outcomes = evaluate_variable_scenario_sweep(variables, selected_variable, variable_test_range,
                                                                  model_pipeline)
    simulated_outcomes = [outcome[output_name] for outcome in variable_scenario_outcomes]

    try:
        impact_is_positive, impact_is_negative = determine_variable_impact_direction(simulated_outcomes)

        all_scenarios_meet_goal = np.all(np.array(simulated_outcomes) >= goal)
        no_scenarios_meet_goal = np.all(np.array(simulated_outcomes) < goal)

        # 3. Apply operational boundary rules
        if all_scenarios_meet_goal:
            variable_analysis_report[
                vn.BREAK_EVEN_FEASIBILITY_STATUS] = messages.BREAK_EVEN_FEASIBILITY_ALWAYS_FEASIBLE
            break_even_index = 0 if impact_is_positive else (len(simulated_outcomes) - 1)

        elif no_scenarios_meet_goal:
            variable_analysis_report[
                vn.BREAK_EVEN_FEASIBILITY_STATUS] = messages.BREAK_EVEN_FEASIBILITY_UNREACHABLE
            break_even_index = (len(simulated_outcomes) - 1) if impact_is_positive else 0

        else:
            # A natural crossover bounds exist; target precisely via binary search
            if impact_is_positive:
                break_even_index = find_first_index_above_target_increasing(simulated_outcomes, goal)
            else:
                break_even_index = find_last_index_above_target_decreasing(simulated_outcomes, goal)

        threshold_variable_val = variable_test_range[break_even_index]
        variable_analysis_report[vn.BREAK_EVEN_POINT_THRESHOLD_VARIABLE_VALUE] = threshold_variable_val
        variable_analysis_report[vn.BREAK_EVEN_POINT_THRESHOLD_RESULT] = simulated_outcomes[
            break_even_index]

        # 4. Unified Directional Safety Margin Calculation
        # Yields a positive margin if operating safely in surplus headroom, or a negative value if in deficit.
        if expected_variable_val != 0:
            directional_modifier = 1 if impact_is_positive else -1
            safety_margin = directional_modifier * (
                    expected_variable_val - threshold_variable_val) / expected_variable_val
            variable_analysis_report[vn.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE] = safety_margin
        else:
            variable_analysis_report[vn.BREAK_EVEN_SAFETY_MARGIN_PERCENTAGE] = 0.0

    except ValueError:
        log.info(messages.ERROR_VARIABLE_NOT_MONOTONIC_EFFECT.format(variable=selected_variable, result=output_name))
        raise
    finally:
        # Cast NumPy scalars to native Python types inline to secure structural JSON compliance
        return {k: (v.item() if isinstance(v, np.generic) else v) for k, v in variable_analysis_report.items()}


def determine_variable_impact_direction(outcomes: list[float]) -> tuple[bool, bool]:
    """
    Evaluates a sequence of outcomes to determine the direction of a variable's business impact.

    Args:
        outcomes (list[float]): Sequential performance indicators extracted from simulated ranges.

    Raises:
        ValueError: Raised if the trend fluctuations are non-monotonic, breaking search assertions.

    Returns:
        tuple[bool, bool]: Boolean flags mapping (impact_is_positive, impact_is_negative).
    """
    outcomes_array = np.array(outcomes)
    impact_is_positive = np.all(outcomes_array[:-1] <= outcomes_array[1:])
    impact_is_negative = np.all(outcomes_array[:-1] >= outcomes_array[1:])

    if not impact_is_positive and not impact_is_negative:
        raise ValueError
    return impact_is_positive, impact_is_negative


def find_first_index_above_target_increasing(array: list[float], target: float) -> int:
    """
    Locates the leftmost index where values stably cross or equal the target on an increasing curve.
    Uses binary search with an explicit two-element guard window.
    """
    left, right = 0, len(array) - 1
    while left + 1 < right:
        mid = (left + right) // 2
        if array[mid] >= target:
            right = mid
        else:
            left = mid
    return left if array[left] >= target else right


def find_last_index_above_target_decreasing(array: list[float], target: float) -> int:
    """
    Locates the rightmost index where values stably remain above or equal the target on a decreasing curve.
    Uses binary search with an explicit two-element guard window.
    """
    left, right = 0, len(array) - 1
    while left + 1 < right:
        mid = (left + right) // 2
        if array[mid] >= target:
            left = mid
        else:
            right = mid
    return right if array[right] >= target else left
