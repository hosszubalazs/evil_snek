import cv2
import numpy
from evil_snek import evil_ocr, devil_vision
from tests import TEST_DATA_PATH


# OCR troug image templateing --> https://www.pyimagesearch.com/2017/07/17/credit-card-ocr-with-opencv-and-python/
# However, as I’ve mentioned multiple times in these previous posts, Tesseract should not be considered a general,
# off-the-shelf solution for Optical Character Recognition capable of obtaining high accuracy.


# verify algorithm against clean data. What is the best possbile outcome with Exocet ??

# Csak a nagyon stabil adatot fogadjuk el.
# Counter vagy Gauge ?
# egyszerre milyen mertekben valtozhat?
# Dynamic cutting. Cut the whole possible text box -> Blob analysis -> cut tight -# text analysis.

# - Separate the tests based on resolution. Have the same cases in at least 2 resolutions. Understand the impact.
# - As a metadata analyze the length, validate
# - Train a dataset for Exocet

# - use object recognition for each character
# Accept tests with a certain success level, e.g. between 5% of expected
# - Break up the string to characters, and identify them one by one.
# Blob detecction ? cv2.dnn.blobFromImage

# Canny edge detection --> change to --> Holistically-Nested Edge Detection https://www.pyimagesearch.com/2019/03/04/holistically-nested-edge-detection-with-opencv-and-deep-learning/

def test_crop_ocr_xp_1440_0():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_1440_0.png')
    xp_picture = devil_vision.crop_xp(img)
    xp_value = devil_vision.analyze_number_from_image(xp_picture)
    assert xp_value == 90910

def test_crop_ocr_nextlvl_xp_1440_0():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_1440_0.png')
    nextlvl_xp_picture = devil_vision.crop_nextlvl_xp(img)
    nextlvl_xp_value = devil_vision.analyze_number_from_image(nextlvl_xp_picture)
    assert nextlvl_xp_value == 108879


def test_crop_ocr_gold_1440_0():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_1440_0.png')
    gold_picture = devil_vision.crop_gold(img)
    gold_value = devil_vision.analyze_number_from_image(gold_picture)
    assert gold_value == 2587


def test_crop_ocr_hp_1440_0():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_1440_0.png')
    hp_picture = devil_vision.crop_hp(img)
    hp_value = devil_vision.analyze_number_from_image(hp_picture)
    assert hp_value == 83


def test_crop_ocr_xp_1440_1():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_1440_1.png')
    xp_picture = devil_vision.crop_xp(img)
    xp_value = devil_vision.analyze_number_from_image(xp_picture)
    assert xp_value == 81769

def test_crop_ocr_nextlvl_xp_1440_1():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_1440_1.png')
    nextlvl_xp_picture = devil_vision.crop_nextlvl_xp(img)
    nextlvl_xp_value = devil_vision.analyze_number_from_image(nextlvl_xp_picture)
    assert nextlvl_xp_value == 83419


def test_crop_ocr_gold_1440_1():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_1440_1.png')
    gold_picture = devil_vision.crop_gold(img)
    gold_value = devil_vision.analyze_number_from_image(gold_picture)
    assert gold_value == 1835


def test_crop_ocr_hp_1440_1():
    img = cv2.imread(TEST_DATA_PATH+'character_screen_1440_1.png')
    hp_picture = devil_vision.crop_hp(img)
    hp_value = devil_vision.analyze_number_from_image(hp_picture)
    assert hp_value == 61
