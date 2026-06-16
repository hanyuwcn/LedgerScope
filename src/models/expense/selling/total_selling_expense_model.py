from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_total_selling_expense(variables: dict) -> dict:
    """
    Calculates the aggregated total selling expense for the operational period.

    Mathematical Formula:
        TotalSellingExpense = FreightExpense + MarketingExpense

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the aggregated selling expense directly to
            the central pipeline registry.
            Example: {"SELLING_EXPENSE": 5000.0}
    """
    # brand_freight_expense = variables.get(vn.BRAND_FREIGHT_EXPENSE, 0.0)
    # marketing_expense = variables.get(vn.MARKETING_EXPENSE, 0.0)
    brand_freight_expense = variables[vn.BRAND_FREIGHT_EXPENSE]
    marketing_expense = variables[vn.MARKETING_EXPENSE]

    calculated_total_selling_expense = brand_freight_expense + marketing_expense
    return {vn.SELLING_EXPENSE: calculated_total_selling_expense}


class TotalSellingExpenseModel(Model):
    """
    Pipeline calculation block responsible for aggregating variable logistics
    and marketing costs into a consolidated Selling Expense figure.

    Description:
        This model serves as a secondary aggregation layer, summing freight costs
        and marketing outlays. It provides the necessary inputs for higher-level
        expense modeling and profitability analysis.

    Calculation Equation:
        TotalSellingExpense = BrandFreightExpense + MarketingExpense

        Where:
        - "BrandFreightExpense" maps to vn.BRAND_FREIGHT_EXPENSE (Optional)
        - "MarketingExpense" maps to vn.MARKETING_EXPENSE (Optional)
        - "TotalSellingExpense" maps to vn.SELLING_EXPENSE
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the TotalSellingExpenseModel with optional parameter defaults.

        Args:
            input_variables (dict, optional): The active runtime configuration context.
        """
        super().__init__(input_variables)

        # Connect the calculation engine and primary output register
        self._model_function = calculate_total_selling_expense
        self._output_names = [vn.SELLING_EXPENSE]

        # Defining optional boundaries with default zero-values for stability
        self._optional_variables = {
            vn.BRAND_FREIGHT_EXPENSE: 0.0,
            vn.MARKETING_EXPENSE: 0.0,
        }
