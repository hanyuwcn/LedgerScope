from src.config import messages
from src.utils import log
from src.utils.validation import check_variables_for_function


class Model:
    """
    Abstract base framework representing a modular financial or operational calculation block.

    Subclasses must define their core execution formula, operational bounds, and trackable 
    outputs while this core orchestrator guarantees parameter verification before calculations run.
    The internal model calculation function expects to receive the registry's default
    optional variables dictionary as its first positional parameter.
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the base Model framework with essential internal configuration state mappings.

        Args:
            input_variables (dict, optional): A dictionary mapping variable name strings to
                their corresponding numeric values (e.g., {"DEAL_ORDERS": 100}). If None,
                it defaults securely to an empty dictionary to prevent NoneType attribute errors.
        """
        # Configuration attributes defined explicitly by specific subclasses
        self._required_variables = []  # Mandatory variable names required to execute
        self._optional_variables = {}  # Optional variable names mapped to their default fallback values
        self._model_function = None  # The core executable calculation method/formula
        self._output_names = []  # List of string keys this specific model calculates

        # Initialize input container defensively to eliminate NoneType errors
        self._input_variables = input_variables if input_variables is not None else {}

    @property
    def required_variables(self) -> list:
        """
        Returns the list of mandatory variable names required to execute this model.

        Returns:
            list: A list of strings representing the required input keys.
        """
        return self._required_variables

    @property
    def optional_variables(self) -> list:
        """
        Returns the list of optional variable names that this model can evaluate.

        Returns:
            list: A list of strings representing the optional input keys derived from the default mapping.
        """
        return list(self._optional_variables.keys())

    @property
    def output_names(self) -> list:
        """
        Returns the list of specific variable names calculated by this model.

        Returns:
            list: A list of strings representing the output keys.
        """
        return self._output_names

    @property
    def input_variables(self) -> dict:
        """
        Returns the active operational context runtime dictionary.

        Returns:
            dict: The shared state pool containing active metrics and variables.
        """
        return self._input_variables

    @input_variables.setter
    def input_variables(self, input_variables: dict) -> None:
        """
        Overwrites or binds a fresh state execution map to the model context.

        Args:
            input_variables (dict): A fresh dictionary mapping variables to values.
                If None is passed, it falls back cleanly to an empty dictionary.
        """
        self._input_variables = input_variables if input_variables is not None else {}

    def update_input_variable(self, key_or_variable, value=None) -> None:
        """
        Updates an existing runtime variable or injects a completely new execution factor.

        Supports polymorphic signatures: accepts either an explicit Variable instance
        or standard raw key-value arguments.

        Args:
            key_or_variable (Union[str, object]): Either a raw string configuration key
                name (e.g., "COST_CPA") OR a domain Variable object instance that implements
                either the property layout or getter interface.
            value (Union[int, float], optional): The raw numeric value to map to the variable.
                This parameter is only evaluated if `key_or_variable` is provided as a raw string.
        """
        if hasattr(key_or_variable, "name") and hasattr(key_or_variable, "expected_value"):
            self._input_variables[key_or_variable.name] = key_or_variable.expected_value
        else:
            self._input_variables[str(key_or_variable)] = value

    def check_variables(self) -> None:
        """
        Defensively validates context dictionary states before executing formulas.

        Required variable omission throws a process-halting KeyError, whereas optional
        variable omission triggers an informational tracking statement allowing downstream
        defaults to kick in.
        """
        # 1. Critical Validation Pass (Strict execution stop)
        try:
            check_variables_for_function(self._input_variables, self._required_variables)
        except KeyError as e:
            # print(self.__class__.__name__)
            # log.error(e.args[0])
            log.error(messages.ERROR_VARIABLE_MISSING_FOR_MODEL.format(var_not_setup_message=e.args[0],
                                                                       model=self.__class__.__name__))
            raise

        # 2. Optional Validation Pass (Informational alert; calculation injects internal defaults)
        try:
            check_variables_for_function(self._input_variables, list(self._optional_variables.keys()))
        except KeyError as e:
            log.info(e.args[0])

    def _get_variable_value(self, name, is_optional=False):
        """
        Resolves a single variable value by checking the input context with fallback to defaults.

        Args:
            name (str): The identifier of the variable to retrieve.
            is_optional (bool): If True, falls back to `_optional_variables` if missing from input.
                                If False, expects the variable to exist in input (raises KeyError).
        """
        if is_optional:
            return self._input_variables.get(name, self._optional_variables.get(name))
        return self._input_variables[name]

    def prepare_calculation_context(self) -> dict:
        """
        Assembles a consolidated execution context for calculation functions.

        This method acts as the data-provider interface for the subclass's `_model_function`.
        It performs a deterministic merge of mandatory inputs (required variables) and
        operational defaults (optional variables) into a single flat dictionary,
        abstracting retrieval logic away from the mathematical formula.

        Returns:
            dict: A unified map of all variables required for the current execution cycle.
        """
        context = {
            variable_name: self._get_variable_value(variable_name, is_optional=False)
            for variable_name in self._required_variables
        }
        context.update({
            variable_name: self._get_variable_value(variable_name, is_optional=True)
            for variable_name in self._optional_variables.keys()
        })
        return context

    def evaluate(self) -> dict:
        """
        Validates dependencies and executes the subclass mathematical formula.

        Workflow:
        1. Validates input state via `check_variables()`.
        2. Prepares a unified variable context via `prepare_calculation_context()`.
        3. Invokes `_model_function` with the unified context dictionary.
        4. Merges resulting metrics back into the operational `input_variables` state.

        Returns:
            dict: The shared context pool containing updated computational outputs.
        """
        self.check_variables()

        # Execute formula with unified context
        result = self._model_function(self.prepare_calculation_context())

        if result and isinstance(result, dict):
            self._input_variables.update(result)

        return self._input_variables
