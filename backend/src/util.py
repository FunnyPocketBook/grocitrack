import re
import deepl
from config import Config

config = Config()

translator = deepl.Translator(config.get("deepl")["api_key"])


def parse_quantity(quantity: str) -> tuple[float, str]:
    """Parses the quantity and unit from the quantity string.
    
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
    """Converts the string to a float.
    
    Args:
        string (str): The number string.

    Returns:
        float: The number as a float.
    """
    return float(string.replace(",", "."))


def translate(text: str, source_language: str="NL", target_language: str="EN-US") -> str:
    """Translates the text.
    
    Args:
        text (str): The text to translate.
        source_language (str): The source language.
        target_language (str): The target language.

    Returns:
        str: The translated text.
    """
    return deepl.translate_text(text, source_language, target_language).text