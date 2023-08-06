from deep_translator import GoogleTranslator
import logging

logging.getLogger().setLevel(logging.INFO)

# Not including in testing, function currently used only for error handling. Used try except instead.
def is_ascii(text):
    """Determine wether text is in ascii format

    Args:
        text (str): String query

    Returns:
        bool: is ascii value
    """
    if isinstance(text, str):
        return text.isascii()
    logging.info(f"{text} is not a string")
    return False

def to_english(text):
    """Translate given text to english

    Args:
        text (str): String query

    Returns:
        str: Translated text
    """
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        logging.error(f"Error while translating: {e}")
        























