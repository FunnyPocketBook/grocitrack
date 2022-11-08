import re

def parse_quantity(quantity: str) -> tuple[float, str]:
    """Parse the quantity and unit from the quantity string.
    
    Args:
        quantity (str): The quantity string.

    Returns:
        tuple[float, str]: The quantity and unit.
    """
    quantity = quantity.replace(",", ".")
    regex_result = re.match(r'(\d+.\d+)([a-zA-Z]+)', quantity)
    if quantity.isnumeric():
        return float(quantity), None
    elif regex_result:
        return float(regex_result.group(1)), regex_result.group(2)


def string_to_float(string: str) -> float:
    """Convert the string to a float.
    
    Args:
        string (str): The number string.

    Returns:
        float: The number as a float.
    """
    return float(string.replace(",", "."))