import pytesseract


def read_single_number(image):
    return pytesseract.image_to_string(
        image, lang="digits_comma", config="--psm 8")
