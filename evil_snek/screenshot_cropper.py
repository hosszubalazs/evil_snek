import cv2
from mss import mss
import numpy
import time
import numpy
from imutils import contours
import imutils


def custom_cropper(character_tab_screenshot, x_start_rel: float, x_size_rel: float, y_start_rel: float):
    height = character_tab_screenshot.shape[0]
    width = character_tab_screenshot.shape[1]
    x_start_abs = int(x_start_rel * width)
    x_size_abs = int(x_size_rel * width)
    y_start_abs = int(y_start_rel * height)
    y_size_abs = int(30/1050 * height)
    return character_tab_screenshot[y_start_abs:y_start_abs +
                                    y_size_abs, x_start_abs:x_start_abs+x_size_abs]


def crop_belt(screenshot):
    width = screenshot.shape[1]
    height = screenshot.shape[0]

    # These are constants, we know the relative location
    x_start_rel = 450/1400
    x_size_rel = 500/1400
    y_start_rel = 780/1050
    y_size_rel = 62.5/1050

    # Based on the actual resolution now we know the pixel perfect coordinates we need
    x_start_abs = int(x_start_rel * width)
    x_size_abs = int(x_size_rel * width)
    y_start_abs = int(y_start_rel * height)
    y_size_abs = int(y_size_rel * height)

    return screenshot[y_start_abs:y_start_abs + y_size_abs, x_start_abs:x_start_abs+x_size_abs]
