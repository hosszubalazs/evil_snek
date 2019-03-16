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


def report_current_xp():

    time.sleep(3)
    temp_data_path = "temp_data"
    devil_vision.create_folder(temp_data_path)
    while 1:
        # 1. openCv -> Cut part of the image
        fake_ui.press_button(WHND, fake_ui.C_VK, fake_ui.C_SC)
        time.sleep(0.1)

        character_tab_screenshot = devil_vision.take_screenshot()
        time.sleep(0.1)

        fake_ui.press_button(WHND, fake_ui.C_VK, fake_ui.C_SC)

        devil_vision.save_image(
            temp_data_path, "character_screen_captured.png", character_tab_screenshot)

        #
        # XP
        #
        img_of_xp =devil_vision.crop_xp(character_tab_screenshot)
        devil_vision.save_image(temp_data_path, "xp_captured.png", img_of_xp)
        xp = evil_ocr.read_single_int(img_of_xp)
        print(time.time()) 
        print("xp=", xp)

        #
        # GOLD
        #
        img_of_gold =devil_vision.crop_gold(character_tab_screenshot)
        devil_vision.save_image(temp_data_path, "gold_captured.png", img_of_gold)
        gold = evil_ocr.read_single_int(img_of_gold)
        print("gold=", gold)

        with open('temp_data/xp_log.csv', 'a') as xp_csv:
            xp_csv.write('{},{}\n'.format(time.time(), xp))
        # Let's do periodic check on how the value is changing.
        time.sleep(3)


if __name__ == '__main__':
    if ctypes.sizeof(ctypes.c_voidp) == 8:
        sys.exit("64 bit Python detected, stopping. Please use a 32bit Python distribution, this is a requirement for win32 api.")

    WHND = fake_ui.initalize_window_handler()

    xp_thread = threading.Thread(target=report_current_xp)
    xp_thread.daemon = True
    xp_thread.start()

    devil_vision.opencv_fun()
