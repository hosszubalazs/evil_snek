"""Apply a bunch of OpenCV2 filters to the original Diablo 1 game, for fun and profit."""
import time

import sys
import threading

# Needed to check for proper 32bit Python distribution
from ctypes import c_voidp, sizeof

from evil_snek import fake_ui
from evil_snek import devil_vision
import os

# WIN32 Window Handler, not yet initialized
WHND = 0

# For debugging purposes we are creating throwaway screenshots when the app is runnig.
# Keep this path up-to-date with .gitignore.
TEMP_DATA_PATH: str = "temp_data"
LOG_FILE_NAME = "character_log.csv"


def create_folder(folder_path: str) -> None:
    try:
        os.mkdir(folder_path)
    except OSError:
        print("Creation of the directory %s failed" % folder_path)
    else:
        print("Successfully created the directory %s " % folder_path)


def report_current_xp(diablo_window_dimensions):

    # time.sleep(3)
    create_folder(TEMP_DATA_PATH)
    # Removing previous file, starting from a clean slate
    # Structure might have changed since last run.
    try:
        os.remove(TEMP_DATA_PATH + '/' + LOG_FILE_NAME)
    except OSError:
        print("Previous CSV file could not be removed, probably does not exist.")
    else:
        print("Previous CSV file removed.")

    log_header = 'timestamp,xp,nextlvl_xp,gold,hp,hp_max,mana,mana_max'
    print(log_header)
    with open(TEMP_DATA_PATH + '/' + LOG_FILE_NAME, 'a') as xp_csv:
        xp_csv.write(log_header + '\n')
    while 1:
        # 1. openCv -> Cut part of the image
        fake_ui.press_button(WHND, fake_ui.C_VK, fake_ui.C_SC)
        # If there is no sleep at all, the screenshot taking happens before the panel is opened.
        # The 0.1 second can be probably optimized but this is not an important detail for now.
        time.sleep(0.1)

        character_tab_screenshot = devil_vision.take_screenshot(
            diablo_window_dimensions)

        fake_ui.press_button(WHND, fake_ui.C_VK, fake_ui.C_SC)

        # Saving this screenshot is widely used for all kinds of debugging purposes.
        # Saving the image is not needed for the program flow, but for practical reasons lets keep this live.
        devil_vision.save_image(
            TEMP_DATA_PATH, "character_screen_captured.png", character_tab_screenshot)

        # FIXME Too much duplication, please clean up.
        # Probably I could map-reduce it

        # XP
        img_of_xp = devil_vision.crop_xp(character_tab_screenshot)
        xp = devil_vision.analyze_number_from_image(img_of_xp)

        # XP needed for next level
        img_of_nextlvl_xp = devil_vision.crop_nextlvl_xp(
            character_tab_screenshot)
        nextlvl_xp = devil_vision.analyze_number_from_image(img_of_nextlvl_xp)

        # GOLD
        img_of_gold = devil_vision.crop_gold(character_tab_screenshot)
        gold = devil_vision.analyze_number_from_image(img_of_gold)

        # HP
        img = devil_vision.crop_hp(character_tab_screenshot)
        hp = devil_vision.analyze_number_from_image(img)

        # HP MAX
        img = devil_vision.crop_hp_max(character_tab_screenshot)
        hp_max = devil_vision.analyze_number_from_image(img)

        # Mana
        img = devil_vision.crop_mana(character_tab_screenshot)
        mana = devil_vision.analyze_number_from_image(img)

        # Mana MAX
        img = devil_vision.crop_mana_max(character_tab_screenshot)
        mana_max = devil_vision.analyze_number_from_image(img)

        # Logging
        log_line = '{},{},{},{},{},{},{},{}'.format(
            time.time(), xp, nextlvl_xp, gold, hp, hp_max, mana, mana_max)
        print(log_line)
        with open(TEMP_DATA_PATH + '/' + LOG_FILE_NAME, 'a') as xp_csv:
            xp_csv.write(log_line + '\n')

        # Let's do periodic checks on how the value is changing.
        time.sleep(3)


if __name__ == '__main__':
    if sizeof(c_voidp) == 8:
        sys.exit("64 bit Python detected, stopping. Please use a 32bit Python distribution, this is a requirement for win32 api.")

    WHND, rect = fake_ui.initalize_window_handler()
    diablo_window_dimensions = devil_vision.initialize_window_size(rect)

    xp_thread = threading.Thread(
        target=report_current_xp, args=(diablo_window_dimensions,))
    xp_thread.daemon = True
    xp_thread.start()

    devil_vision.opencv_fun(diablo_window_dimensions, TEMP_DATA_PATH)
