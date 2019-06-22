import cv2
from mss import mss
import numpy
import time
import numpy
from imutils import contours
import imutils
import screenshot_cropper

class Property:
    """
    FIXME a class might be too heavywieght for this data structure.
    Consider a named tuple: https://docs.python.org/3.7/library/collections.html#collections.namedtuple
    """
    def __init__(self, name: str, xstart: float, xsize: float, ystart: float, post_processor=0):
        self.name = name
        self.xstart = xstart
        self.xsize = xsize
        self.ystart = ystart
        self.post_processor = post_processor


Properties = Property("xp", 470/1400, 190/1400, 125/1050), \
             Property("nextlvl_xp", 470/1400, 190/1400, 185/1050), \
             Property("gold", 470/1400, 190/1400, 295/1050)


def get_property(screenshot, property_name: str):
    cropped_image, custom_processor = get_cropped_and_processed_property(
        screenshot, property_name)
    #cv2.imwrite("cropped.png", cropped_image)
    post_processed_image = post_process_property_screenshot(
        cropped_image, custom_processor)
    #cv2.imwrite("peepeed.png", post_processed_image)

    return analyze_number_from_image(post_processed_image)


def get_cropped_and_processed_property(screenshot, property_name: str):
    cropped_image = 0
    custom_post_processing = 0
    # FIXME : this complicated if structure is really not nice. devil_vision should support more dynamic picture cutting.
    if property_name == "xp":
        cropped_image = screenshot_cropper.crop_xp(screenshot)
    elif property_name == "nextlvl_xp":
        cropped_image = screenshot_cropper.crop_nextlvl_xp(screenshot)
    elif property_name == "gold":
        cropped_image = screenshot_cropper.crop_gold(screenshot)
    elif property_name == "hp":
        cropped_image = screenshot_cropper.crop_hp(screenshot)
        custom_post_processing = bw_and_normalize
    elif property_name == "hp_max":
        cropped_image = screenshot_cropper.crop_hp_max(screenshot)
    elif property_name == "mana":
        cropped_image = screenshot_cropper.crop_mana(screenshot)
        custom_post_processing = bw_and_normalize
    elif property_name == "mana_max":
        cropped_image = screenshot_cropper.crop_mana_max(screenshot)

    return cropped_image, custom_post_processing


def post_process_property_screenshot(property_screenshot, post_processing_func=0):
    final = 0

    # Some cases, like the health points which can be colored, require special processing.
    # This if makes that possible, while still providing a strong default flow.
    if post_processing_func != 0:
        final = post_processing_func(property_screenshot)
    else:
        thresholded = threshold_chracter_text(property_screenshot)
        final = cv2.cvtColor(thresholded, cv2.COLOR_BGR2GRAY)

    return final


def initialize_window_size(window_parameters):
    """ FIXME the margins only work in 4:3 windowed mode
    """
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


def bw_and_normalize(image):
    grayed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    normalized = cv2.normalize(grayed, grayed, 0, 255, cv2.NORM_MINMAX)
    return threshold_chracter_text(normalized)


def get_number_from_ocr_location(pixels_from_left: int) -> int:
    """
    Magic numbers are determined based on the test picture stored as reference.
    FIXME this implementation is very ugly, altough works.
    """
    if pixels_from_left < 10:
        return 1
    elif pixels_from_left < 27:
        return 2
    elif pixels_from_left < 40:
        return 3
    elif pixels_from_left < 60:
        return 4
    elif pixels_from_left < 75:
        return 5
    elif pixels_from_left < 90:
        return 6
    elif pixels_from_left < 110:
        return 7
    elif pixels_from_left < 125:
        return 8
    elif pixels_from_left < 140:
        return 9
    else:
        return 0


def analyze_number_from_image(image_to_analyse):
    """
    Solution heavily based on : https://www.pyimagesearch.com/2017/07/17/credit-card-ocr-with-opencv-and-python/
    """
    reference = cv2.imread("tests/test_data/exocet_heavy_digits_reference.PNG")
    reference = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)

    # find contours in the image (i.e,. the outlines of the digits)
    # sort them from left to right, and initialize a dictionary to map
    # digit name to the ROI
    numbers_contours = cv2.findContours(
        image_to_analyse, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    numbers_contours = imutils.grab_contours(numbers_contours)
    numbers_contours = contours.sort_contours(
        numbers_contours, method="left-to-right")[0]
    string_of_numbers = ""
    for (i, c) in enumerate(numbers_contours):

        # compute the bounding box for the digit, extract it, and resize
        (x, y, w, h) = cv2.boundingRect(c)
        roi = image_to_analyse[y:y + h, x:x + w]
        roi = invert_image(roi)
        match = cv2.matchTemplate(reference, roi, cv2.TM_CCORR_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
        pixel_distance_from_left = max_loc[0]

        string_of_numbers += "{}".format(
            get_number_from_ocr_location(pixel_distance_from_left))

    return int(string_of_numbers)


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

        fps = 0
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
