def numeric_to_percentage(number: float, decimal: int = 1) -> str:
    """
    Formats a raw floating-point scalar value into a validated percentage string.

    Example:
        >>> numeric_to_percentage(0.045, decimal=1)
        '4.5%'
        >>> numeric_to_percentage(0.0456, decimal=2)
        '4.56%'

    Args:
        number (float): The raw fraction or scalar value to be converted (e.g., 0.125).
        decimal (int, optional): The precision metric defining how many trailing digits
            to preserve past the decimal point. Defaults to 1.

    Returns:
        str: A clean string representation of the value post-conversion, trailing with '%'.
    """
    return f"{number:.{decimal}%}"
