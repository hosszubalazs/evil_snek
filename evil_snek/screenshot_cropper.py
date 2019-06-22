import cv2
from mss import mss
import numpy
import time
import numpy
from imutils import contours
import imutils


def custom_cropper(character_tab_screenshot, x_start_rel, x_size_rel, y_start_rel):
    height = character_tab_screenshot.shape[0]
    width = character_tab_screenshot.shape[1]
    x_start_abs = int(x_start_rel * width)
    x_size_abs = int(x_size_rel * width)
    y_start_abs = int(y_start_rel * height)
    y_size_abs = int(30/1050 * height)
    return character_tab_screenshot[y_start_abs:y_start_abs +
                                    y_size_abs, x_start_abs:x_start_abs+x_size_abs]


def crop_xp(character_tab_screenshot):
    x_start = 470/1400
    x_size = 190/1400
    y_start = 125/1050

    return custom_cropper(character_tab_screenshot, x_start, x_size, y_start)


def crop_nextlvl_xp(character_tab_screenshot):
    x_start = 470/1400
    x_size = 190/1400
    y_start = 185/1050

    return custom_cropper(character_tab_screenshot, x_start, x_size, y_start)


def crop_gold(character_tab_screenshot):
    x_start = 470/1400
    x_size = 190/1400
    y_start = 295/1050

    return custom_cropper(character_tab_screenshot, x_start, x_size, y_start)


def crop_hp(character_tab_screenshot):
    x_start = 142/640
    x_size = 35/640
    y_start = 293/480

    # since the health and mana points can be colored, normalization will be needed before thresholding
    # this is solved by an extra helper function
    # cropped = crop_and_grayfi_property(
    #    character_tab_screenshot, x_start, x_size, y_start, bw_and_normalize)
    return custom_cropper(character_tab_screenshot, x_start, x_size, y_start)


def crop_hp_max(character_tab_screenshot):
    x_start = 205/1400
    x_size = 70/1400
    y_start = 293/480

    return custom_cropper(character_tab_screenshot, x_start, x_size, y_start)


def crop_mana(character_tab_screenshot):
    x_start = 142/640
    x_size = 35/640
    y_start = 700/1050

    return custom_cropper(character_tab_screenshot, x_start, x_size, y_start)


def crop_mana_max(character_tab_screenshot):
    x_start = 205/1400
    x_size = 70/1400
    y_start = 700/1050

    return custom_cropper(character_tab_screenshot, x_start, x_size, y_start)
