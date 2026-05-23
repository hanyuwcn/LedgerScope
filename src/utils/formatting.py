def fmt(val, d=0, s='', p=False):
    """Formats numeric inputs with dynamic precision, prefixes, and percentage scaling.

    Optimized for short-form brevity when mapping lambda lookup tables.

    Args:
        val (int | float | str): The numeric value or string to be formatted.
        d (int): Number of decimal digits to round and preserve. Defaults to 0.
        s (str): Prefix symbol, typically a currency mark like '$' or '¥'. Defaults to ''.
        p (bool): Percentage mode flag. If True, scales value by 100 and appends '%'. Defaults to False.

    Returns:
        str: The fully formatted output string, or raw fallback text if parsing fails.
    """
    try:
        num = float(val)
        if p:
            return f"{s}{num * 100:,.{d}f}%"
        return f"{s}{num:,.{d}f}"
    except (ValueError, TypeError):
        return str(val)


def list_to_element_string(elements: list) -> str:
    """
    Converts a list of strings into a single, comma-separated string representation.

    This presentation helper is primarily used to format lists of variable names or
    database keys into a clean, human-readable format for logs and error exceptions.

    Args:
        elements (list): A list of strings to be joined (e.g., ['Orders', 'TaxRate']).

    Returns:
        str: A single string containing all elements separated by a comma and a space
            (e.g., "Orders, TaxRate"). Returns an empty string if the input list is empty.
    """
    return ", ".join(elements)
