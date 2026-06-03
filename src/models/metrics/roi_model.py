from src.config import variable_names
from src.core.base_model import Model


def calculate_project_roi(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates Project Return on Investment (ROI) across all cash outlays.

    Mathematical Formula:
        ROI = NetIncome / (Cost + Expense + CapitalExpenditure)

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks
            for non-mandatory fields like EXPENSE and CAPITAL_EXPENDITURE.
        **kwargs: Arbitrary keyword arguments containing required calculation metrics:

            Mandatory Keys:
                NET_INCOME (float): Net operational profit after tax from NetIncomeModel.
                COST (float): Aggregated core operating costs.

            Optional Keys (Defaults to configuration maps if missing):
                EXPENSE (float): Duration-scaled operational expenses.
                CAPITAL_EXPENDITURE (float): Upfront asset capital investments.

    Returns:
        dict: A dictionary mapping the calculated ROI decimal directly to the registry.
            Example: {"ROI": 0.25} (representing a 25% return)
    """
    # Extract strictly required execution anchors
    net_income = kwargs[variable_names.NET_INCOME]
    cost = kwargs[variable_names.COST]

    # Resolve non-mandatory investment elements using runtime args, falling back to configuration defaults
    expense = kwargs.get(
        variable_names.EXPENSE,
        optional_variables.get(variable_names.EXPENSE, 0.0)
    )
    cap_ex = kwargs.get(
        variable_names.CAPITAL_EXPENDITURE,
        optional_variables.get(variable_names.CAPITAL_EXPENDITURE, 0.0)
    )

    total_denominational_investment = cost + expense + cap_ex

    # Protect engine against a zero-denominator division crash
    if total_denominational_investment == 0:
        return {variable_names.ROI: 0.0}

    calculated_roi = net_income / total_denominational_investment

    return {variable_names.ROI: calculated_roi}


class RoiModel(Model):
    """
    Pipeline calculation block evaluating overall project efficiency by scaling
    after-tax net income against cumulative cash outlays.

    In a Nutshell:
        Return on Investment (ROI) measures the efficiency and profitability of an investment.
        It shows exactly how much money a project makes relative to how much money was poured
        into it. For example, an ROI of 0.25 means that for every single dollar invested in the
        project, it hands back 25 cents in pure profit. It tells you if a project is a high-yield
        engine or a money pit.

    Description:
        The ROI Model offers a standardized framework for evaluating capital allocation efficiency
        across diverse corporate projects. By combining core costs, operational overhead (expenses),
        and long-term physical assets (CapEx) into a single unified denominational baseline, this model
        determines the true financial hurdle rate of an enterprise decision.

        Recognizing that different projects have distinct structures, this model handles operational
        overheads and asset investments flexibly. For streamlined projects or simple trading scenarios
        where indirect overheads and capital assets are non-existent, "expense" and "capital_expenditure"
        can be omitted entirely, automatically defaulting to 0.0 to prevent pipeline bottlenecks.

    Calculation Equation:
        roi = net_income / (cost + expense + capital_expenditure)

        Where:
        - "net_income" maps to NET_INCOME (Required)
        - "cost" maps to COST (Required)
        - "expense" maps to EXPENSE (Optional, Default: 0.0)
        - "capital_expenditure" maps to CAPITAL_EXPENDITURE (Optional, Default: 0.0)
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the RoiModel with standardized system boundaries and fallback maps.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Hooking functional engine transformations
        self._model_function = calculate_project_roi
        self._output_names = [variable_names.ROI]

        # Explicit tracking validation boundaries (anchoring core inputs)
        self._required_variables = [
            variable_names.NET_INCOME,
            variable_names.COST
        ]

        # Establishing safe pipeline fallbacks for streamlined project footprints
        self._optional_variables = {
            variable_names.EXPENSE: 0.0,
            variable_names.CAPITAL_EXPENDITURE: 0.0
        }
