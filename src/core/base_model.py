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
        # Scenario A: A Domain Variable object instance was passed directly
        if hasattr(key_or_variable, "name") and hasattr(key_or_variable, "expected_value"):
            self._input_variables[key_or_variable.name] = key_or_variable.expected_value
        elif hasattr(key_or_variable, "get_name") and hasattr(key_or_variable, "get_value"):
            self._input_variables[key_or_variable.get_name()] = key_or_variable.get_value()
        # Scenario B: Standard raw string key and numeric value mapping
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
            log.error(e.args[0])
            raise

        # 2. Optional Validation Pass (Informational alert; calculation injects internal defaults)
        try:
            check_variables_for_function(self._input_variables, list(self._optional_variables.keys()))
        except KeyError as e:
            log.info(e.args[0])

    # def optional_variable_getter(self, variable_name):
    #     default_value = self.optional_variables[variable_name]
    #     return self._input_variables.get(variable_name, default_value)
    #
    # def required_variable_getter(self, variable_name):
    #     return self._input_variables[variable_name]

    def evaluate(self) -> dict:
        """
        Validates system dependencies and executes the subclass mathematical formula.

        Architectural Note: In-Place Merge Strategy vs. New Dictionary Creation
        ---------------------------------------------------------------------
        Calculated output variables are explicitly merged back into the existing input
        dictionary in-place rather than generating a brand new copy at each step. This
        design pattern is selected intentionally for two core reasons:

        1. Memory Optimization: It prevents the system from generating heavy memory overhead
           and garbage collection cycles during deep, multi-variable simulations.
        2. Seamless Model Chaining: It allows multiple sequential processing models (e.g.,
           Model A -> Model B -> Model C) to execute over a single, shared, cumulative state.
           Outputs from previous calculations automatically become available as valid inputs
           for downstream pipeline engines without writing manual aggregation logic.

        The registration defaults mapped within `self._optional_variables` are provided directly
        to the operational function implementation as its leading argument to resolve missing context.

        Risk Mitigation: Because this results in a mutable shared state across models, users
        should ensure that original raw inputs are duplicated via a copy/clone wrapper at the
        very beginning of an analysis workflow if the baseline state needs to remain uncorrupted.

        Returns:
            dict: The comprehensive shared context pool holding all consolidated inputs
                and newly updated computational outputs.
        """
        # Assert mathematical correctness checks before invoking execution thread
        self.check_variables()

        # Execute formula by unpacking our variables context directly into the target function
        result = self._model_function(self._optional_variables, **self._input_variables)

        # Enforce that the output is wrapped as a dict before performing merge
        if result and isinstance(result, dict):
            self._input_variables.update(result)

        return self._input_variables
