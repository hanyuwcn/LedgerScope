from src.config import ERROR_VARIABLE_NOT_SETUP_WITH_MESSAGE
from src.utils import log


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


def check_variables_for_function(provided_variables: dict,
                                 required_variables: list = None, optional_variables: list = None) -> None:
    """
    Defensively validates that a context dictionary contains all necessary variables
    before executing mathematical or logic calculations.

    If required variables are missing, it logs an error and halts execution by raising
    a KeyError. If optional variables are missing, it logs an informational tracking statement
    but allows execution to proceed uninterrupted.

    Args:
        provided_variables (dict): The active context runtime dictionary holding system
            variables and configurations.
        required_variables (list, optional): Factors strictly mandatory for the mathematical
            integrity of a function. Defaults to None (treated safely as an empty list).
        optional_variables (list, optional): Nice-to-have factors that don't halt calculation
            if missing. Defaults to None (treated safely as an empty list).

    Raises:
        KeyError: If any strings specified inside `required_variables` are absent from
            the keys of `provided_variables`.
    """
    # Defensive normalization to eliminate mutable default argument side-effects
    req_vars = required_variables if required_variables is not None else []
    opt_vars = optional_variables if optional_variables is not None else []

    missing_necessary = get_missing_elements(provided_variables, req_vars)
    if missing_necessary:
        log.error(ERROR_VARIABLE_NOT_SETUP_WITH_MESSAGE.format(msg=str(missing_necessary)))
        raise KeyError

    missing_optional = get_missing_elements(provided_variables, opt_vars)
    if missing_optional:
        log.info(ERROR_VARIABLE_NOT_SETUP_WITH_MESSAGE.format(msg=str(missing_optional)))
