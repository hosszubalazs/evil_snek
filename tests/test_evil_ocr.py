import cv2
import numpy
from evil_snek import evil_ocr as ocr

# plans:
# Input Chracter tab screen
# to assert : experience is correctly calculated
# d development ideas :  all fields will be necessary

def test_ocr_xp_0():
    img = cv2.imread('tests/xp_3447.png')
    result = ocr.read_single_int(img)
    assert result == 3447

def test_ocr_xp_1():
    img = cv2.imread('tests/xp_73623.png')
    result = ocr.read_single_int(img)
    assert result == 73623

def test_ocr_xp_2():
    img = cv2.imread('tests/xp_83419.png')
    result = ocr.read_single_int(img)
    assert result == 83419
