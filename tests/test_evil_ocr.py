import cv2
import numpy
from evil_snek import evil_ocr as ocr
from PIL import Image

# plans:
# Input Chracter tab screen
# to assert : experience is correctly calculated
# d development ideas :  all fields will be necessary


def test_pytest_alive():
    assert 5 == 5


def test_pytest_alive():
    # cv2.imread('xp_captured.png',0)
    img = Image.open('tests/xp_captured.png')
    #img_new = Image.fromarray(img)
    result = ocr.read_single_int(img)
    print(result)
    assert result == 3447
