from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_net_income(variables: dict) -> dict:
    """
    Calculates the Net Income After Tax for the execution context.

    Mathematical Formula:
        NetIncome = (Revenue - Cost - Expense - Depreciation) * (1 - TaxRate)

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the net income metric directly to
            its source-of-truth registry key.
            Example: {"NET_INCOME": 7600.0}
    """
    revenue = variables[vn.REVENUE]
    cost = variables[vn.COST]
    expense = variables[vn.EXPENSE]
    depreciation = variables[vn.DEPRECIATION]
    tax_rate = variables[vn.TAX_RATE]

    # Core corporate accounting math block
    pre_tax_income = revenue - cost - expense - depreciation
    calculated_net_income = pre_tax_income * (1.0 - tax_rate)

    return {vn.NET_INCOME: calculated_net_income}


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
        - "Revenue" maps to vn.REVENUE (Required)
        - "Cost" maps to vn.COST (Required)
        - "Expense" maps to vn.EXPENSE (Optional, Defaults to 0.0)
        - "Depreciation" maps to vn.DEPRECIATION (Optional, Defaults to 0.0)
        - "TaxRate" maps to vn.TAX_RATE (Optional, Defaults to 0.0)
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
        self._output_names = [vn.NET_INCOME]

        # Revenue and core cost remain mandatory data inputs for processing
        self._required_variables = [
            vn.REVENUE,
            vn.COST
        ]

        # Shifted structural tracking lists into explicit dictionary default fallbacks
        self._optional_variables = {
            vn.EXPENSE: 0.0,
            vn.DEPRECIATION: 0.0,
            vn.TAX_RATE: 0.0
        }
