from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_project_roi(variables: dict) -> dict:
    """
    Calculates the Project Return on Investment (ROI) relative to initial setup costs.

    Mathematical Formula:
        ROI = NetIncome / SetupCost

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the calculated ROI decimal directly to the registry.
            Returns {"ROI": 0.0} if setup_cost is zero to avoid division errors.
    """
    net_income = variables[vn.NET_INCOME]
    setup_cost = variables[vn.SETUP_COST]

    # Protect engine against a zero-denominator division crash
    if setup_cost == 0:
        return {vn.ROI: 0.0}

    calculated_roi = net_income / setup_cost

    return {vn.ROI: calculated_roi}


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
        ROI = NetIncome / SetupCost

        Where:
        - "NetIncome" maps to vn.NET_INCOME (Required)
        - "SetupCost" maps to vn.SETUP_COST (Required)
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
        self._output_names = [vn.ROI]

        # Explicit tracking validation boundaries (anchoring core inputs)
        self._required_variables = [
            vn.NET_INCOME,
            vn.SETUP_COST
        ]
