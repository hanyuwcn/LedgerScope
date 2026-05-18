from src.config import MODEL_DEFAULT_OUTPUT_NAME
from src.utils import check_variables_for_function


class Model:
    def __init__(self):
        self._model_function = None
        self._output_name = MODEL_DEFAULT_OUTPUT_NAME

        ## Columns, model should apply the same object of _factors,
        ## so that each change to the factors can immediately effect on the model result
        self._columns = {}
        self._factors = {}

        ## To use for check variables
        self._required_factors = []
        self._required_columns = []

    def get_output_name(self):
        return self._output_name

    def set_columns(self, columns):
        self._columns = columns

    def get_columns(self):
        return self._columns

    def add_column(self, column):
        self._columns[column.get_name()] = column

    def set_factors(self, factors):
        """
        The most recommended way to generate model. Keep the model and every column applying the same factor object.
        ONLY set factor without evaluating columns.

        :param factors: to which the model and every column apply
        """
        self._factors = factors

    def apply_factors(self, factors):
        """
        Set up the factors and updating the corresponding columns.

        :param factors: to which the model and every column apply
        """
        self.set_factors(factors)
        self.evaluate_columns()

    def update_factors(self, factors):
        """
        Update the existing factors in the current model with the new factor dict, then reevaluate columns based on it
        Insert the new item if the key doesn't exist in the factors
        Update with the new value if the key exists in the factors

        :param factors: to be updated to the existing factors
        """
        for factor_name, factor_value in factors.items():
            self._factors[factor_name] = factor_value

        self.evaluate_columns()

    def get_factors(self):
        return self._factors

    def evaluate(self):
        ## Validate inputs (Letting KeyError bubble up naturally if mandatory columns are missing)
        self.check_variables()

        params = self.provide_params()
        return {self._output_name: self._model_function(**params)}

    def check_variables(self):
        check_variables_for_function(self._columns, self._required_columns)
        check_variables_for_function(self._factors, self._required_factors)

    def evaluate_columns(self):
        pass

    def provide_params(self):
        pass
