import pytesseract
import logging


def read_single_int(image):
    recognized_text = pytesseract.image_to_string(
        image, lang="digits_comma", config=" --psm 8")
    # trim the single quotes from the two sides
    trimmed = recognized_text.strip('\'')
    # Default for 0
    value = 0
    # validate for int
    try:
        value = int(trimmed)
    except ValueError:
        logging.warning('Unsuccessful read_single_int')

    return value
