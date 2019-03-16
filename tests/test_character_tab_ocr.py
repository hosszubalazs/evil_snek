import cv2
import numpy
from evil_snek import evil_ocr, devil_vision
from tests import TEST_DATA_PATH


def test_ocr_xp_0():
    img = cv2.imread(TEST_DATA_PATH+'character_screen.png')
    xp_picture = devil_vision.crop_xp(img)
    xp_value = evil_ocr.read_single_int(xp_picture)
    assert xp_value == 73623
