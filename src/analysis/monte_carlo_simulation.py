from src.config import messages, variable_names
from src.core.base_variable import ValueType
from src.engine import evaluate_chained_models
from src.utils import check_variables_for_function, is_model_sequence_valid
from src.utils import log


def run_monte_carlo(
        variables: dict,
        shuffled_inputs: list,
        model_pipeline: list,
        tracked_outputs: list = None,
        iterations: int = 100
) -> list:
    """
    Executes a Monte Carlo simulation loop across a structured set of models, 
    sampling designated parameters and harvesting targeted execution metrics.

    Args:
        variables (dict): Map of string tokens to stateful Variable domain instances.
        shuffled_inputs (list): String keys identifying parameters targeted for random sampling.
        model_pipeline (list): Explicit, ordered sequence of Model classes to execute.
        tracked_outputs (list, optional): Subset of output keys to isolate in the history results. 
            Defaults to None (captures all system variables).
        iterations (int, optional): Total number of simulation execution loops. Defaults to 100.

    Returns:
        list[dict]: A list of flat dictionaries representing observed iteration data states.
    """
    # Guard 1: Verify our random target parameters actually exist in our pool
    check_variables_for_function(variables, shuffled_inputs)
    is_model_sequence_valid(model_pipeline)

    simulation_results = []
    log.info(messages.INFO_MONTE_CARLO_SIMULATION_START.format(iterations=iterations))

    for iteration_idx in range(1, iterations + 1):
        # 1. Evaluate a single randomized sample slice through the models
        calculated_state = _evaluate_single_iteration(variables, shuffled_inputs, model_pipeline)

        # 2. Performance Check: Validate target tracking columns exactly once on run 1
        if iteration_idx == 1 and tracked_outputs is not None:
            check_variables_for_function(calculated_state, tracked_outputs)

        # 3. Harvest and isolate our requested data slice
        if tracked_outputs is None:
            data_record = dict(calculated_state)
        else:
            data_record = {metric: calculated_state[metric] for metric in tracked_outputs}

        # Inject run telemetry metadata
        data_record[variable_names.SYSTEM_RUN_ID] = iteration_idx
        simulation_results.append(data_record)

    # log.info(messages.INFO_MONTE_CARLO_SIMULATION_FINISH.format(size=len(simulation_results)))
    return simulation_results


def _evaluate_single_iteration(variables: dict, shuffled_inputs: list, model_pipeline: list) -> dict:
    """
    Helper function to sample inputs and execute a single iteration of the engine.
    """
    sampled_inputs = {}

    for var_name, var_instance in variables.items():
        if not hasattr(var_instance, "get_value"):
            sampled_inputs[var_name] = var_instance
            continue

        # Choose sampling strategy based on parameter configuration flags
        if var_name in shuffled_inputs:
            sampled_inputs[var_name] = var_instance.get_value(ValueType.RANDOM)
        else:
            sampled_inputs[var_name] = var_instance.get_value(ValueType.EXPECTED)

    return evaluate_chained_models(runtime_state=sampled_inputs, model_pipeline=model_pipeline)
