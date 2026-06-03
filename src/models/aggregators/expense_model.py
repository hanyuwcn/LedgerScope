from src.config import variable_names
from src.core.base_model import Model


def calculate_total_expense(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates consolidated operational expenses scaled to a specific monthly horizon.

    Mathematical Formula:
        Expense = (MonthlyRent + MonthlyRenderFee + MonthlyTravelFee) * Months

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing mathematical tracking metrics:

            Optional Keys:
                MONTHS (int/float): The duration factor representing the fiscal timeline
                    horizon being evaluated (e.g., 3 for quarterly, 12 for annual).
                EXPENSE_MONTHLY_RENT (float): Monthly real estate lease fees.
                EXPENSE_RENDER_FEE (float): Monthly infrastructure/rendering overhead.
                EXPENSE_TRAVEL_FEE (float): Monthly team travel allowances.

    Returns:
        dict: A dictionary mapping the duration-scaled operating expenses directly to the source-of-truth registry.
            Example: {"Expense": 24000.0}
    """
    # Extract fallback parameter bounds directly out of the configuration registry map
    default_months = optional_variables[variable_names.MONTHS]
    default_rent = optional_variables[variable_names.EXPENSE_MONTHLY_RENT]
    default_render = optional_variables[variable_names.EXPENSE_RENDER_FEE]
    default_travel = optional_variables[variable_names.EXPENSE_TRAVEL_FEE]

    # Safely pull operational buckets, dropping back to default metrics if not considered for this analysis
    months = kwargs.get(variable_names.MONTHS, default_months)
    monthly_rent = kwargs.get(variable_names.EXPENSE_MONTHLY_RENT, default_rent)
    monthly_render_fee = kwargs.get(variable_names.EXPENSE_RENDER_FEE, default_render)
    monthly_travel_fee = kwargs.get(variable_names.EXPENSE_TRAVEL_FEE, default_travel)

    # Computes total sum scaled strictly to the requested time horizon
    calculated_expense = (monthly_rent + monthly_render_fee + monthly_travel_fee) * months

    return {variable_names.EXPENSE: calculated_expense}


class TotalExpenseModel(Model):
    """
    Pipeline calculation block responsible for aggregating individual fixed/variable
    operating expenses and scaling them across flexible calendar durations.

    Description:
        This model serves as a flexible operational expense calculator that unifies baseline
        real estate lease fees, structural infrastructure processing/rendering overhead, and corporate
        travel allocations. Once aggregated, the core operating footprint is multiplied across a
        dynamic time-horizon factor (months) to evaluate cumulative outlays over variable fiscal
        timelines (e.g., specific quarters or full operational years).

        Because all parameters default safely to baseline values (zero for financial costs and
        twelve for the monthly scale multiplier), the evaluation step remains isolated against missing
        inputs during early-stage scenario planning or baseline financial modeling.

    Calculation Equation:
        total expense = (rent + render fee + travel fee) * months

        Where:
        - "rent" maps to EXPENSE_MONTHLY_RENT
        - "render fee" maps to EXPENSE_RENDER_FEE
        - "travel fee" maps to EXPENSE_TRAVEL_FEE
        - "months" maps to MONTHS (Defaults to 12)
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the TotalExpenseModel with standardized analytical boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Hooking calculation interface logic to output registers
        self._model_function = calculate_total_expense
        self._output_names = [variable_names.EXPENSE]

        # All variables are now optional to support rapid, zero-overhead baseline testing
        self._required_variables = []

        # Migrated from structural list footprint to dynamic dictionary default mapping
        self._optional_variables = {
            variable_names.EXPENSE_MONTHLY_RENT: 0.0,
            variable_names.EXPENSE_RENDER_FEE: 0.0,
            variable_names.EXPENSE_TRAVEL_FEE: 0.0,
            variable_names.MONTHS: 12
        }
