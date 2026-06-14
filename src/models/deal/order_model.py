from src.config import variable_names as vn
from src.core.base_model import Model


def calculate_orders(variables: dict) -> dict:
    """
    Calculates total finalized sales transactions converted from acquired top-of-funnel leads.

    Mathematical Formula:
        Orders = Leads * CloseRate

    Args:
        variables (dict): Unified context containing all mandatory and
            optional variables, resolved by the Model base class.

    Returns:
        dict: A dictionary mapping the calculated order volume directly
            to the operational registry.
            Example: {"ORDERS": 64.8}
    """
    leads = variables[vn.LEADS]
    close_rate = variables[vn.CLOSE_RATE]

    calculated_orders = leads * close_rate

    return {vn.ORDERS: calculated_orders}


class OrderModel(Model):
    """
    Pipeline calculation block responsible for converting top-of-funnel prospect
    Leads into finalized transactional Orders.

    Description:
        This model serves as the connective tissue between marketing discovery and revenue
        realization within the business lifecycle pipeline. By taking the output of upstream
        lead generation layers and applying a sales closing percentage metric, it establishes
        the ultimate transaction volume driver used down-funnel for fulfillment cost calculations,
        gross revenue profiling, and inventory planning.

    Calculation Equation:
        Orders = Leads * CloseRate

        Where:
        - "Leads" maps to vn.LEADS
        - "CloseRate" maps to vn.CLOSE_RATE
    """

    def __init__(self, input_variables: dict = None):
        """
        Initializes the OrderModel with explicit parameter validation boundaries.

        Args:
            input_variables (dict, optional): The active runtime configuration context dictionary.
                If None, it defaults securely to an empty dictionary via the parent class.
        """
        super().__init__(input_variables)

        # Binding calculation identity and specifying the explicit output registry signature
        self._model_function = calculate_orders
        self._output_names = [vn.ORDERS]

        # Enforcing configuration dependency boundaries
        self._required_variables = [
            vn.LEADS,
            vn.CLOSE_RATE
        ]
