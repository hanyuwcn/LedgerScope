from src.config import variable_names
from src.core.base_model import Model


def calculate_net_income(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates the Net Income After Tax for the execution context.

    Mathematical Formula:
        NetIncome = (Revenue - Cost - Expense - Depreciation) * (1 - TaxRate)

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing operational mathematical metrics:

            Mandatory Keys:
                REVENUE (float): Gross top-line operational revenue.
                COST (float): Aggregated core operating costs (e.g., COGS and direct marketing outlays).

            Optional Keys (Pulled with fallbacks from configuration map):
                EXPENSE (float): Duration-scaled operational expenses (OPEX).
                DEPRECIATION (float): Non-cash fixed asset depreciation allocations.
                TAX_RATE (float): Corporate tax liability rate multiplier.

    Returns:
        dict: A dictionary mapping the net income metric directly to its source-of-truth registry key.
            Example: {"NetIncome": 7600.0}
    """
    # Extract structural required fields (will throw KeyError if missing, as intended)
    revenue = kwargs[variable_names.REVENUE]
    cost = kwargs[variable_names.COST]

    # Pull baseline configuration defaults for optional metrics
    default_expense = optional_variables[variable_names.EXPENSE]
    default_depreciation = optional_variables[variable_names.DEPRECIATION]
    default_tax_rate = optional_variables[variable_names.TAX_RATE]

    # Resolve runtime execution values against their safe fallbacks
    expense = kwargs.get(variable_names.EXPENSE, default_expense)
    depreciation = kwargs.get(variable_names.DEPRECIATION, default_depreciation)
    tax_rate = kwargs.get(variable_names.TAX_RATE, default_tax_rate)

    # Core corporate accounting math block
    pre_tax_income = revenue - cost - expense - depreciation
    calculated_net_income = pre_tax_income * (1.0 - tax_rate)

    return {variable_names.NET_INCOME: calculated_net_income}


class NetIncomeModel(Model):
    """
    Pipeline calculation block responsible for evaluating corporate net profitability
    by accounting for operating outlays, infrastructure overhead, and statutory tax obligations.

    Description:
        Net Income (also referred to as net profit, or the bottom line) represents the definitive
        measure of a business unit's financial health during an operational cycle. This model
        deducts primary cost of goods sold (COGS), direct marketing budgets, duration-scaled operating
        expenses (OpEx), and non-cash asset depreciation adjustments from gross top-line revenue.

        The resulting pre-tax figure is then compressed by the corporate tax rate multiplier to yield
        true after-tax profitability. By treating operational expenses, depreciation allocations,
        and tax exposure as optional fields defaulting to 0.0, this module easily accommodates
        lean pre-tax scenarios, zero-overhead bootstrap forecasts, or early-stage exploratory modeling.

    Calculation Equation:
        NetIncome = (Revenue - Cost - Expense - Depreciation) * (1.0 - TaxRate)

        Where:
        - "Revenue" maps to variable_names.REVENUE (Required)
        - "Cost" maps to variable_names.COST (Required)
        - "Expense" maps to variable_names.EXPENSE (Optional, Defaults to 0.0)
        - "Depreciation" maps to variable_names.DEPRECIATION (Optional, Defaults to 0.0)
        - "TaxRate" maps to variable_names.TAX_RATE (Optional, Defaults to 0.0)
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the NetIncomeModel with standardized operational accounting boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Connect the calculation engine and primary output register
        self._model_function = calculate_net_income
        self._output_names = [variable_names.NET_INCOME]

        # Revenue and core cost remain mandatory data inputs for processing
        self._required_variables = [
            variable_names.REVENUE,
            variable_names.COST
        ]

        # Shifted structural tracking lists into explicit dictionary default fallbacks
        self._optional_variables = {
            variable_names.EXPENSE: 0.0,
            variable_names.DEPRECIATION: 0.0,
            variable_names.TAX_RATE: 0.0
        }
