import cv2
from mss import mss
import numpy
import os
import time
import numpy

from imutils import contours
import imutils


def initialize_window_size(window_parameters):
    # FIXME the margins only work in 4:3 windowed mode
    side_margin = 1
    top_margin = 32
    bottom_margin = 1
    window_dimensions = {
        "top": window_parameters.top + top_margin,
        "left": window_parameters.left + side_margin,
        "width": window_parameters.right - window_parameters.left - 2*side_margin,
        "height": window_parameters.bottom - (window_parameters.top + top_margin) - bottom_margin
    }
    return window_dimensions


def create_folder(folder_path):
    try:
        os.mkdir(folder_path)
    except OSError:
        print("Creation of the directory %s failed" % folder_path)
    else:
        print("Successfully created the directory %s " % folder_path)


def take_screenshot(window_dimensions):
    with mss() as sct:
        screenshot = numpy.array(sct.grab(window_dimensions))
    return screenshot


def save_image(folder_path, filename, image):
    cv2.imwrite(
        r'{}\{}'.format(folder_path, filename), image)


def invert_image(image):
    return ~image


def threshold_chracter_text(image):
    # Removing background noise, defaulting it to black
    # Everything below minvalue goes to black, maxvalue is ignored
    ret, thresh1 = cv2.threshold(image, 150, 400, cv2.THRESH_TOZERO)
    # binarise the remaining
    ret, thresh2 = cv2.threshold(thresh1, 100, 255, cv2.THRESH_BINARY)

    return thresh2


def blur_test(image, kernel=3):
    return cv2.GaussianBlur(image, (kernel, kernel), 0)


def bw_and_normalize(image):
    grayed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    normalized = cv2.normalize(grayed, grayed, 0, 255, cv2.NORM_MINMAX)
    return normalized


def crop_and_grayfi_property(character_tab_screenshot, x_start_rel, x_size_rel, y_start_rel):
    height, width, channels = character_tab_screenshot.shape
    x_start_abs = int(x_start_rel * width)
    x_size_abs = int(x_size_rel * width)
    y_start_abs = int(y_start_rel * height)
    y_size_abs = int(30/1050 * height)
    cropped = character_tab_screenshot[y_start_abs:y_start_abs +
                                       y_size_abs, x_start_abs:x_start_abs+x_size_abs]

    thresholded = threshold_chracter_text(cropped)
    grayed = cv2.cvtColor(thresholded, cv2.COLOR_BGR2GRAY)

    return grayed


def crop_xp(character_tab_screenshot):
    x_start_rel = 470/1400
    x_size_rel = 190/1400
    y_start_rel = 125/1050
    return crop_and_grayfi_property(character_tab_screenshot, x_start_rel, x_size_rel, y_start_rel)


def crop_nextlvl_xp(character_tab_screenshot):
    height, width, channels = character_tab_screenshot.shape

    x_start = int(470/1400 * width)
    x_size = int(190/1400 * width)

    y_start = int(185/1050 * height)
    y_size = int(30/1050 * height)
    cropped = character_tab_screenshot[y_start:y_start +
                                       y_size, x_start:x_start+x_size]

    thresholded = threshold_chracter_text(cropped)
    grayed = cv2.cvtColor(thresholded, cv2.COLOR_BGR2GRAY)

    return grayed


def crop_gold(character_tab_screenshot):
    height, width, channels = character_tab_screenshot.shape

    x_start = int(470/1400 * width)
    x_size = int(190/1400 * width)

    y_start = int(295/1050 * height)
    y_size = int(30/1050 * height)
    cropped = character_tab_screenshot[y_start:y_start +
                                       y_size, x_start:x_start+x_size]
    thresholded = threshold_chracter_text(cropped)
    grayed = cv2.cvtColor(thresholded, cv2.COLOR_BGR2GRAY)

    return grayed


def crop_hp(character_tab_screenshot):
    height, width, channels = character_tab_screenshot.shape
    x_start = int(142/640 * width)
    x_size = int(35/640 * width)

    y_start = int(293/480 * height)
    y_size = int(30/1050 * height)
    cropped = character_tab_screenshot[y_start:y_start +
                                       y_size, x_start:x_start+x_size]

    # since the hp can have color
    normalized = bw_and_normalize(cropped)
    thresholded = threshold_chracter_text(normalized)

    return thresholded


def analyze_number_from_image(toread):
    magiced_number = 0

    tenyleg_ref = cv2.imread(
        "tests/test_data/exocet_heavy_digits_reference.PNG")
    tenyleg_ref = cv2.cvtColor(tenyleg_ref, cv2.COLOR_BGR2GRAY)

    # find contours in the OCR-A image (i.e,. the outlines of the digits)
    # sort them from left to right, and initialize a dictionary to map
    # digit name to the ROI
    toreadCnts = cv2.findContours(
        toread, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    toreadCnts = imutils.grab_contours(toreadCnts)
    toreadCnts = contours.sort_contours(toreadCnts, method="left-to-right")[0]

    alma = {1: "1", 2: "1", 3: "1", 14: "2", 15: "2", 30: "3", 31: "3", 45: "4", 46: "4", 47: "4", 62: "5", 63: "5", 78: "6",
            79: "6", 93: "7", 94: "7", 95: "7", 110: "8", 111: "8", 112: "8", 128: "9", 143: "0", 144: "0"}

    convert_this_str_to_int = ""
    # loop over the OCR-A reference contours
    for (i, c) in enumerate(toreadCnts):

        # compute the bounding box for the digit, extract it, and resize
        # it to a fixed size
        (x, y, w, h) = cv2.boundingRect(c)
        roi = toread[y:y + h, x:x + w]
        roi = invert_image(roi)
        moech = cv2.matchTemplate(tenyleg_ref, roi, cv2.TM_CCORR_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(moech)
        print("max_loc:{}", max_loc)
        convert_this_str_to_int += "{}".format(alma[max_loc[0]])

    return int(convert_this_str_to_int)


def opencv_fun(window_dimensions, temp_data_path):

    # Dummy initialization
    previous_frame = 0
    while 1:
        last_time = time.time()

        diablo_scrnsht = take_screenshot(window_dimensions)

        scrnsht_hsv = cv2.cvtColor(diablo_scrnsht, cv2.COLOR_BGR2HSV)
        canny_on_hue = cv2.Canny(scrnsht_hsv[:, :, 0], 100, 200)
        save_image(temp_data_path, "canny_on_hue.png", canny_on_hue)
        cv2.imshow('Canny on Hue channel', canny_on_hue)

        frame_difference = canny_on_hue - previous_frame
        time_diff = (time.time() - last_time)
        if time_diff > 0:
            fps = format(1 / time_diff, '.2f')
            # print("fps:", fps)
        cv2.putText(frame_difference, "FPS={}".format(fps),
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2)

        save_image(temp_data_path, "frame_difference.png", frame_difference)
        cv2.imshow('Difference between HSV frames', frame_difference)
        previous_frame = canny_on_hue

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
