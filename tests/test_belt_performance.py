import cv2
import numpy
from evil_snek import devil_vision
from tests import TEST_DATA_PATH
import time


def test_health_potion_detection_1440_0():
    expected = [0, 0, 0, 1, 1, 1, 2, 2]
    file_name = 'character_screen_1440_0.png'
    screenshot = cv2.imread(TEST_DATA_PATH+file_name)
    start = time.time()
    for i in range(10000):
        actual = devil_vision.get_health_in_belt(screenshot)

        assert actual == expected
    testing_time_s = time.time() - start
    # Tested time is discovered based on actual performance
    # The goal is to keep it limited, maybe see improvements in the future
    reference_time_s = 1.3
    # A big margin is needed because the test is run in very different environemnts ( both locally and in the cloud)
    max_allowed_deviation_s = 0.2
    assert abs(reference_time_s - testing_time_s) < max_allowed_deviation_s
