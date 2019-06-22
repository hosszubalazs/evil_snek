import cv2
import numpy

from tests import TEST_DATA_PATH
import devil_vision


test_chracter_sheet_0 = cv2.imread(
    TEST_DATA_PATH+'character_screen_1440_0.png')
test_chracter_sheet_1 = cv2.imread(
    TEST_DATA_PATH+'character_screen_1440_1.png')


def character_tab_test_helper(test_chracter_sheet, property_name: str, expected_value: int):
    prop = devil_vision.get_property_by_name(property_name)
    actual_value = devil_vision.get_property(
        test_chracter_sheet, prop)
    assert actual_value == expected_value


def test_crop_ocr_xp_1440_0():
    character_tab_test_helper(test_chracter_sheet_0, "xp", 90910)


def test_crop_ocr_nextlvl_xp_1440_0():
    character_tab_test_helper(
        test_chracter_sheet_0, "nextlvl_xp", 108879)


def test_crop_ocr_gold_1440_0():
    character_tab_test_helper(test_chracter_sheet_0, "gold", 2587)


def test_crop_ocr_hp_1440_0():
    character_tab_test_helper(test_chracter_sheet_0, "hp", 83)


def test_crop_ocr_hp_max_1440_0():
    character_tab_test_helper(test_chracter_sheet_0, "hp_max", 102)


def test_crop_ocr_mana_1440_0():
    character_tab_test_helper(test_chracter_sheet_0, "mana", 19)


def test_crop_ocr_mana_max_1440_0():
    character_tab_test_helper(test_chracter_sheet_0, "mana_max", 19)


def test_crop_ocr_xp_1440_1():
    character_tab_test_helper(test_chracter_sheet_1, "xp", 81769)


def test_crop_ocr_nextlvl_xp_1440_1():
    character_tab_test_helper(
        test_chracter_sheet_1, "nextlvl_xp", 83419)


def test_crop_ocr_gold_1440_1():
    character_tab_test_helper(test_chracter_sheet_1, "gold", 1835)


def test_crop_ocr_hp_1440_1():
    character_tab_test_helper(test_chracter_sheet_1, "hp", 61)


def test_crop_ocr_hp_max_1440_1():
    character_tab_test_helper(test_chracter_sheet_1, "hp_max", 100)


def test_crop_ocr_mana_1440_1():
    character_tab_test_helper(test_chracter_sheet_1, "mana", 18)


def test_crop_ocr_mana_max_1440_1():
    character_tab_test_helper(test_chracter_sheet_1, "mana_max", 18)
