from .base_model import Model


class Auditor(Model):
    """
    Abstract base framework for pipeline integrity verification.

    The Auditor acts as a specialized gating node within the computational pipeline.
    Unlike standard models that transform data, the Auditor performs validation
    checks against established fiscal constraints or business logic. If an audit
    fails, the execution thread is halted to prevent downstream models from
    processing corrupted or non-reconciled financial states.

    Architectural Roles:
        1. Integrity Gate: Monitors post-calculation outputs for mathematical
           consistency.
        2. Circuit Breaker: Raises exceptions to stop pipeline flow upon
           reconciliation failures.
        3. Transparency: Ensures that intermediate data states meet business
           requirements before entering deeper profit analysis.
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the Auditor framework.

        Args:
            input_variables (dict, optional): Contextual state pool for verification.
        """
        super().__init__(input_variables)

    @property
    def output_names(self) -> list:
        """
        Returns an empty list as Auditors do not generate new data outputs.

        Returns:
            list: Always returns an empty list to signify no state transformation.
        """
        return []

    def evaluate(self):
        """
        Executes internal audit logic and validates pipeline integrity.

        This method triggers the internal `_model_function` associated with the
        auditor. If the logic within that function detects an anomaly (e.g.,
        failing to reconcile price components), it must raise an exception.

        Returns:
            dict: The original input state if the audit passes, maintaining
                  seamless pipeline continuity.
        """
        self.check_variables()

        # Execute reconciliation check. Failure here propagates an exception,
        # effectively halting the pipeline's execution.
        self._model_function(self._optional_variables, **self._input_variables)

        return self._input_variables
