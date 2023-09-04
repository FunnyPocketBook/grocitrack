import re
import deepl
from config import Config

config = Config()

translator = deepl.Translator(config.get("deepl", "api_key"))

def string_to_float(string: str) -> float:
    """Converts the string to a float.
    
    Args:
        string (str): The number string.

    Returns:
        float: The number as a float.
    """
    if string is None:
        return None
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
    translated_text = translator.translate_text(text, source_lang=source_language, target_lang=target_language).text
    return translated_text
