import pytesseract
import logging
import cv2


def read_single_int(image, psm=8):
    recognized_text = pytesseract.image_to_string(
        image, lang="digits_comma", config=" --psm {}".format(psm))
    # The trained data can contain ' . and , so were are tripping those off
    trimmed = recognized_text.strip('\'').strip('.').strip(',')

    # Default for 0
    value = 0
    # validate for int
    try:
        value = int(trimmed)
    except ValueError:
        logging.warning('Unsuccessful read_single_int')
        # BACKUP PLAN BOIS
        if(psm == 8):
            value = read_single_int(image, 10)

    return value
