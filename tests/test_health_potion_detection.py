import cv2
import numpy
from evil_snek import devil_vision
from tests import TEST_DATA_PATH


def test_health_potion_detection_1440_0():
    expected = [0, 0, 0, 1, 1, 1, 2, 2]
    file_name = 'character_screen_1440_0.png'
    screenshot = cv2.imread(TEST_DATA_PATH+file_name)

    image_of_belt = devil_vision.crop_belt(screenshot)
    actual = devil_vision.get_health_in_belt(image_of_belt)

    assert actual == expected


def test_health_potion_detection_1440_1():
    expected = [1, 1, 1, 1, 1, 1, 2, 2]
    file_name = 'character_screen_1440_1.png'
    screenshot = cv2.imread(TEST_DATA_PATH+file_name)

    image_of_belt = devil_vision.crop_belt(screenshot)
    actual = devil_vision.get_health_in_belt(image_of_belt)

    assert actual == expected
