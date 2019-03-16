import cv2
import numpy
from evil_snek import evil_ocr as ocr
from tests import TEST_DATA_PATH

# plans:
# Input Chracter tab screen
# to assert : experience is correctly calculated
# d development ideas :  all fields will be necessary

# All these tests might be deprecated, favouring the more complete workflows.


def test_ocr_xp_0():
    img = cv2.imread(TEST_DATA_PATH+'xp_3447.png')
    result = ocr.read_single_int(img)
    assert result == 3447


def test_ocr_xp_1():
    img = cv2.imread(TEST_DATA_PATH+'xp_73623.png')
    result = ocr.read_single_int(img)
    assert result == 73623
