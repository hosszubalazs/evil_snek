"""Apply a bunch of OpenCV2 filters to the original Diablo 1 game, for fun and profit."""
import time

import sys
import threading

# Needed to check for proper 32bit Python distribution
import ctypes

import fake_ui
import evil_ocr
import devil_vision

# WIN32 Window Handler, not yet initialized
WHND = 0

# For debugging purposes we are creating throwaway screenshots when the app is runnig.
# Keep this path up-to-date with .gitignore.
TEMP_DATA_PATH = "temp_data"


def report_current_xp(diablo_window_dimensions):

    #time.sleep(3)
    devil_vision.create_folder(TEMP_DATA_PATH)
    while 1:
        # 1. openCv -> Cut part of the image
        fake_ui.press_button(WHND, fake_ui.C_VK, fake_ui.C_SC)
        time.sleep(0.1)

        character_tab_screenshot = devil_vision.take_screenshot(
            diablo_window_dimensions)
        time.sleep(0.1)

        fake_ui.press_button(WHND, fake_ui.C_VK, fake_ui.C_SC)

        devil_vision.save_image(
            TEMP_DATA_PATH, "character_screen_captured.png", character_tab_screenshot)

        #
        # XP
        #
        img_of_xp = devil_vision.crop_xp(character_tab_screenshot)
        devil_vision.save_image(TEMP_DATA_PATH, "xp_captured.png", img_of_xp)
        #xp = evil_ocr.read_single_int(img_of_xp)
        xp = devil_vision.analyze_number_from_image(img_of_xp)
        print(time.time())
        print("xp=", xp)

        #
        # GOLD
        #
        img_of_gold = devil_vision.crop_gold(character_tab_screenshot)
        devil_vision.save_image(
            TEMP_DATA_PATH, "gold_captured.png", img_of_gold)
        #gold = evil_ocr.read_single_int(img_of_gold)
        gold = devil_vision.analyze_number_from_image(img_of_gold)
        print("gold=", gold)

        #
        # HP
        #
        img_of_hp = devil_vision.crop_hp(character_tab_screenshot)
        devil_vision.save_image(
            TEMP_DATA_PATH, "hp_captured.png", img_of_hp)
        #hp = evil_ocr.read_single_int(img_of_hp)
        hp = devil_vision.analyze_number_from_image(img_of_hp)
        print("hp=", hp)

        with open(TEMP_DATA_PATH + '/xp_log.csv', 'a') as xp_csv:
            xp_csv.write('{},{}\n'.format(time.time(), xp))
        # Let's do periodic check on how the value is changing.
        time.sleep(3)


if __name__ == '__main__':
    if ctypes.sizeof(ctypes.c_voidp) == 8:
        sys.exit("64 bit Python detected, stopping. Please use a 32bit Python distribution, this is a requirement for win32 api.")

    WHND, rect = fake_ui.initalize_window_handler()
    diablo_window_dimensions = devil_vision.initialize_window_size(rect)

    xp_thread = threading.Thread(
        target=report_current_xp, args=(diablo_window_dimensions,))
    xp_thread.daemon = True
    xp_thread.start()

    devil_vision.opencv_fun(diablo_window_dimensions, TEMP_DATA_PATH)
