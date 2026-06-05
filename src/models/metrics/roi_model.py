from src.config import variable_names
from src.core.base_model import Model


def calculate_project_roi(optional_variables: dict, **kwargs) -> dict:
    """
    Calculates the Project Return on Investment (ROI) relative to initial setup costs.

    Mathematical Formula:
        ROI = NetIncome / SetupCost

    Description:
        This function evaluates the efficiency of the initial capital deployment. It
        measures how much net profit is generated for every dollar spent on the
        foundational setup of the business (e.g., registrations, website, equipment).

    Args:
        optional_variables (dict): Mapped configuration containing default parameter fallbacks.
        **kwargs: Arbitrary keyword arguments containing required calculation metrics:

            Mandatory Keys:
                NET_INCOME (float): The final net profit after all operational costs
                                   and taxes have been deducted.
                COST_SETUP (float): The initial foundational investment/startup cost.

    Returns:
        dict: A dictionary mapping the calculated ROI decimal directly to the registry.
            Example: {"ROI": 0.25} (representing a 25% return on initial setup)
            Returns {"ROI": 0.0} if setup_cost is zero to avoid division errors.
    """
    # Extract strictly required execution anchors
    net_income = kwargs[variable_names.NET_INCOME]
    setup_cost = kwargs[variable_names.COST_SETUP]

    # Protect engine against a zero-denominator division crash
    if setup_cost == 0:
        return {variable_names.ROI: 0.0}

    calculated_roi = net_income / setup_cost

    return {variable_names.ROI: calculated_roi}


class RoiModel(Model):
    """
    Pipeline calculation block evaluating capital allocation efficiency by scaling
    Net Income against the initial Setup Cost.

    Description:
        This model isolates the Return on Investment by treating foundational
        startup expenses (SetupCost) as the primary investment vehicle. While
        operating expenses like COGS and Advertising impact the 'Net Income'
        (the numerator), this specific ROI metric focuses on the yield generated
        specifically from the capital required to launch the project.

    Calculation Equation:
        ROI = net_income / setup_cost

        Where:
        - "net_income" maps to NET_INCOME (Required)
        - "setup_cost" maps to COST_SETUP (Required)
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the RoiModel with standardized system boundaries and required keys.

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
            variable_names.COST_SETUP
        ]