import cv2
import numpy
from evil_snek import evil_ocr, devil_vision
from tests import TEST_DATA_PATH


def test_crop_ocr_xp_0():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_0.png')
    xp_picture = devil_vision.crop_xp(img)
    xp_value = evil_ocr.read_single_int(xp_picture)
    assert xp_value == 73623


def test_crop_ocr_gold_0():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_0.png')
    gold_picture = devil_vision.crop_gold(img)
    gold_value = evil_ocr.read_single_int(gold_picture)
    assert gold_value == 1646


def test_crop_ocr_xp_1():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_1.png')
    xp_picture = devil_vision.crop_xp(img)
    xp_value = evil_ocr.read_single_int(xp_picture)
    assert xp_value == 81769


def test_crop_ocr_gold_1():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_1.png')
    gold_picture = devil_vision.crop_gold(img)
    gold_value = evil_ocr.read_single_int(gold_picture)
    assert gold_value == 1835


def test_crop_ocr_xp_2():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_2.png')
    xp_picture = devil_vision.crop_xp(img)
    xp_value = evil_ocr.read_single_int(xp_picture)
    assert xp_value == 81769


def test_crop_ocr_gold_2():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_2.png')
    gold_picture = devil_vision.crop_gold(img)
    gold_value = evil_ocr.read_single_int(gold_picture)
    assert gold_value == 1835
