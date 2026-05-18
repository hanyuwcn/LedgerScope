from src.config import ERROR_VARIABLE_NOT_SETUP_WITH_MESSAGE
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


def check_variables_for_function(provided_variables: dict, required_variables: list = None) -> None:
    """
    Defensively asserts that all mandatory variables are present in a context dictionary
    before allowing downstream logic execution to proceed.

    If any required keys are missing, this function constructs a clean, formatted error
    string containing the sorted missing elements and raises a KeyError back to the caller.
    This allows upper-level business logic to determine how to handle execution failure.

    Args:
        provided_variables (dict): The active runtime configuration dictionary containing
            available variables and context metrics.
        required_variables (list, optional): Strings representing keys that are strictly
            mandatory for a calculation. Defaults to None (treated safely as an empty list).

    Raises:
        KeyError: If one or more keys specified in `required_variables` are absent from
            the keys of `provided_variables`.
    """
    req_vars = required_variables if required_variables is not None else []

    missing = get_missing_elements(provided_variables, req_vars)
    if missing:
        raise KeyError(ERROR_VARIABLE_NOT_SETUP_WITH_MESSAGE.format(msg=list_to_element_string(missing)))
