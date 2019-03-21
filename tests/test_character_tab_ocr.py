import cv2
import numpy
from evil_snek import devil_vision
from tests import TEST_DATA_PATH


def character_tab_test_helper(file_name, property_name, expected_value):
    test_chracter_sheet = cv2.imread(TEST_DATA_PATH+file_name)
    cropped_image = 0
    # FIXME : this complicated if structure is really not nice. devil_vision should support more dynamic picture cutting.
    if property_name == "xp":
        cropped_image = devil_vision.crop_xp(test_chracter_sheet)
    elif property_name == "nextlvl_xp":
        cropped_image = devil_vision.crop_nextlvl_xp(test_chracter_sheet)
    elif property_name == "gold":
        cropped_image = devil_vision.crop_gold(test_chracter_sheet)
    elif property_name == "hp":
        cropped_image = devil_vision.crop_hp(test_chracter_sheet)
    elif property_name == "hp_max":
        cropped_image = devil_vision.crop_hp_max(test_chracter_sheet)
    elif property_name == "mana":
        cropped_image = devil_vision.crop_mana(test_chracter_sheet)
    elif property_name == "mana_max":
        cropped_image = devil_vision.crop_mana_max(test_chracter_sheet)

    actual_value = devil_vision.analyze_number_from_image(cropped_image)
    assert actual_value == expected_value


def test_crop_ocr_xp_1440_0():
    character_tab_test_helper('character_screen_1440_0.png', "xp", 90910)


def test_crop_ocr_nextlvl_xp_1440_0():
    character_tab_test_helper(
        'character_screen_1440_0.png', "nextlvl_xp", 108879)


def test_crop_ocr_gold_1440_0():
    character_tab_test_helper('character_screen_1440_0.png', "gold", 2587)


def test_crop_ocr_hp_1440_0():
    character_tab_test_helper('character_screen_1440_0.png', "hp", 83)


def test_crop_ocr_hp_max_1440_0():
    character_tab_test_helper('character_screen_1440_0.png', "hp_max", 102)


def test_crop_ocr_mana_1440_0():
    character_tab_test_helper('character_screen_1440_0.png', "mana", 19)


def test_crop_ocr_mana_max_1440_0():
    character_tab_test_helper('character_screen_1440_0.png', "mana_max", 19)


def test_crop_ocr_xp_1440_1():
    character_tab_test_helper('character_screen_1440_1.png', "xp", 81769)


def test_crop_ocr_nextlvl_xp_1440_1():
    character_tab_test_helper(
        'character_screen_1440_1.png', "nextlvl_xp", 83419)


def test_crop_ocr_gold_1440_1():
    character_tab_test_helper('character_screen_1440_1.png', "gold", 1835)


def test_crop_ocr_hp_1440_1():
    character_tab_test_helper('character_screen_1440_1.png', "hp", 61)


def test_crop_ocr_hp_max_1440_1():
    character_tab_test_helper('character_screen_1440_1.png', "hp_max", 100)


def test_crop_ocr_mana_1440_1():
    character_tab_test_helper('character_screen_1440_1.png', "mana", 18)


def test_crop_ocr_mana_max_1440_1():
    character_tab_test_helper('character_screen_1440_1.png', "mana_max", 18)
