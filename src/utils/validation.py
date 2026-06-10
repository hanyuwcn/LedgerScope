from src.config import messages
from .formatting import list_to_element_string


def get_missing_elements(provided_factor_dict: dict, required_factors: list) -> list:
    """
    Identifies elements in a required list that are missing from a given dictionary's keys.

    Utilizes fast set subtraction to isolate missing keys, then sorts the results
    to ensure deterministic error outputs and log messages.

    Args:
        provided_factor_dict (dict): The active context runtime dictionary whose keys
            are checked for compliance.
        required_factors (list): A list of strings representing the keys absolutely
            required by a downstream calculation.

    Returns:
        list: A sorted list of strings representing the missing factors. Returns an
            empty list if all required factors are present or if required_factors is empty.
    """
    if not required_factors:
        return []
    missing = set(required_factors) - set(provided_factor_dict.keys())
    return sorted(list(missing))


def check_variables_for_function(provided_variables: dict, required_variables: list = None) -> bool:
    """
    Defensively asserts that all mandatory variables are present in a context dictionary
    before allowing downstream logic execution to proceed.

    If any required keys are missing, this function constructs a clean, formatted error
    string containing the sorted missing elements and raises a KeyError back to the caller.

    Args:
        provided_variables (dict): The active runtime configuration dictionary containing
            available variables and context metrics.
        required_variables (list, optional): Strings representing keys that are strictly
            mandatory for a calculation. Defaults to None.

    Raises:
        KeyError: If one or more keys specified in `required_variables` are absent from
            the keys of `provided_variables`.

    Returns:
        bool: True if all required variables are successfully verified and present.
    """
    req_vars = required_variables if required_variables is not None else []

    missing = get_missing_elements(provided_variables, req_vars)
    if missing:
        # Accessing the error template explicitly via the namespaced config file
        error_template = messages.ERROR_VARIABLE_NOT_SETUP_WITH_MESSAGE
        formatted_elements = list_to_element_string(missing)

        raise KeyError(error_template.format(msg=formatted_elements))

    return True


def check_model_pipeline_topology_order(models: list) -> bool:
    """
    Validates the structural sequence of a calculation pipeline to prevent point failures.

    This function scans a sequence of calculation blocks chronologically to ensure
    that data lineage remains intact. It catches 'Order of Operations' violations
    where a model down the line attempts to calculate and overwrite a variable that
    an earlier model already consumed as a raw, top-level baseline dependency.

    Args:
        models (list): An ordered sequence of model instances inheriting from the
            base Model class. Each instance must expose the `required_variables`
            and `output_names` list properties.

    Raises:
        KeyError: If a structural sequence violation is detected where a downstream
            model's output variable name is found within the accumulated set of
            required upstream inputs.

    Returns:
        bool: True if the pipeline sequence configuration is architecturally sound
            and ready for safe execution.
    """
    seen_inputs = set()
    input_consumers = {}  # Maps variable_name -> first_model_name_to_consume_it

    for model in models:
        model_name = model.__class__.__name__
        model_outputs = model.output_names
        model_inputs = set(model.required_variables) | set(model.optional_variables)

        # 1. Catch downstream models overwriting an upstream input dependency
        for output_name in model_outputs:
            if output_name in seen_inputs:
                raise KeyError(messages.ERROR_PIPELINE_TOPOLOGY_ORDER_VIOLATION.format(variable_name=output_name,
                                                                                       current_model=model_name,
                                                                                       earlier_model=input_consumers[
                                                                                           output_name]))

        # 2. Record inputs to track history for the next iteration step
        for input_name in model_inputs:
            seen_inputs.add(input_name)
            if input_name not in input_consumers:
                input_consumers[input_name] = model_name

    return True
