from src.config import variable_names as vn
from src.core import Auditor


def check_freight_expense(variables: dict) -> None:
    """
    Validates that freight costs are mutually exclusive between the Brand
    and the Merchant.

    Business Logic:
        Freight costs should either be borne by the Brand, the Merchant,
        or neither (if shipping is handled by a third party or N/A).
        It is logically inconsistent for both parties to report active
        freight costs for the same order/unit.

    Args:
        variables (dict): Context containing freight parameters.

    Raises:
        ValueError: If both merchant_freight_rate and brand_freight_expense
            are greater than zero.
    """
    merchant_freight_rate = variables[vn.MERCHANT_FREIGHT_RATE]
    brand_freight_expense = variables[vn.BRAND_FREIGHT_EXPENSE]

    # Mutually exclusive validation
    if merchant_freight_rate > 0 and brand_freight_expense > 0:
        raise ValueError(
            f"Freight cost conflict: Both merchant_freight_rate({merchant_freight_rate}) "
            f"and brand_freight_expense({brand_freight_expense}) are > 0. "
            "Freight responsibility must be exclusive."
        )


class FreightExpenseAuditor(Auditor):
    """
    Pipeline guardrail ensuring logical assignment of freight responsibility.

    Description:
        This auditor prevents data errors where freight costs are accidentally
        double-counted or assigned to both the Brand and the Merchant model
        simultaneously.

    Audit Logic:
        - Allows: (0, 0), (Rate, 0), or (0, Expense)
        - Disallows: (Rate, Expense) where both are > 0
    """

    def __init__(self, input_variables: dict = None):
        super().__init__(input_variables)
        self._model_function = check_freight_expense

        self._optional_variables = {
            vn.MERCHANT_FREIGHT_RATE: 0.0,
            vn.BRAND_FREIGHT_EXPENSE: 0.0,
        }
