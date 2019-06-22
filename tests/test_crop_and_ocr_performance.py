import cv2
import numpy
import time
from tests import TEST_DATA_PATH

import devil_vision


test_chracter_sheet_0 = cv2.imread(
    TEST_DATA_PATH+'character_screen_1440_0.png')


def character_tab_test_helper(property_name: str, expected_value: int):
    prop = devil_vision.get_property_by_name(property_name)

    actual_value = devil_vision.get_property(
        test_chracter_sheet_0, prop)
    assert actual_value == expected_value


def test_crop_ocr_xp_1440_0_perf():
    start = time.time()
    for i in range(100):
        character_tab_test_helper("xp", 90910)
        character_tab_test_helper("nextlvl_xp", 108879)
        character_tab_test_helper("gold", 2587)
        character_tab_test_helper("hp", 83)
        character_tab_test_helper("hp_max", 102)
        character_tab_test_helper("mana", 19)
        character_tab_test_helper("mana_max", 19)
    testing_time_s = time.time() - start
    # Tested time is discovered based on actual performance
    # The goal is to keep it limited, maybe see improvements in the future
    reference_time_s = 0.7
    # A big margin is needed because the test is run in very different environemnts ( both locally and in the cloud)
    max_allowed_deviation_s = 0.2
    assert abs(reference_time_s - testing_time_s) < max_allowed_deviation_s
