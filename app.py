"""Apply a bunch of OpenCV2 filters to the original Diablo 1 game, for fun and profit."""
import time
import numpy
import cv2
from mss import mss
import sys
import win32gui
import win32con
import threading

import pytesseract


# Please start Diablo according to the resolution configured here
# Optimized for full HD screens, you might need to fiddle
# with the coordinates to properly set the capture.
DIABLO_WINDOW = {"top": 290, "left": 640, "width": 640, "height": 480}


def opencv():
    # Dummy initialization
    previous_frame = 0
    while 1:
        last_time = time.time()
        with mss() as sct:
            diablo_scrnsht = numpy.array(sct.grab(DIABLO_WINDOW))

        scrnsht_hsv = cv2.cvtColor(diablo_scrnsht, cv2.COLOR_BGR2HSV)
        new_frame = scrnsht_hsv
        cv2.imshow('Hue->Canny', cv2.Canny(scrnsht_hsv[:, :, 0], 100, 200))

        frame_difference = new_frame - previous_frame
        time_diff = (time.time() - last_time)
        if time_diff > 0:
            fps = format(1 / time_diff, '.2f')
            #print("fps:", fps)
        cv2.putText(frame_difference, fps,
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2)

        cv2.imshow('Difference between HSV frames', frame_difference)
        previous_frame = new_frame

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        # h, s, v = HSV[:, :, 0], HSV[:, :, 1], HSV[:, :, 2]
        # cv2.imshow('HSV->Canny', cv2.Canny(HSV, 300, 800))
        # cv2.imshow('Grayscale Diablo', h)
        # cv2.imshow('Grayscale Diablo', s)
        # cv2.imshow('Grayscale Diablo', cv2.Canny(h, 100, 800))
        # cv2.imshow('Grayscale Diablo', cv2.Canny(img, 150, 600))
        # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # kernel_size = 3
        # gaussian_blurred = cv2.GaussianBlur(
        #    HSV, (kernel_size, kernel_size), 0)
        # blurred_edge = cv2.Canny(gaussian_blurred, 100, 800)
        # new_frame = blurred_edge
        # final = blurred_edge


def interaction():
    # Please check MSDN documentation on these WIN32 codes
    # Looks scary, but really not so bad
    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP = 0x0202
    MK_LBUTTON = 0x0001

    WM_KEYDOWN = 0x0100
    #WM_KEYUP = 0x0101

    #WM_CHAR = 0x0102
    C_VK = 0x43
    # c scan code = 0x2E  # 00101110
    c_key_down = int('000000000000001'+'00101110'+'00000000', 2)

    whnd = win32gui.FindWindowEx(None, None, None, "DIABLO")
    if whnd == 0:
        sys.exit("Diablo was not found. Please makes sure Diablo is running, and you are running this program with sufficient rights.")

    # Diablo IN YOUR FACE
    win32gui.SetForegroundWindow(whnd)

    # As a tech demo, lets:
    # Open the character tab with the 'c' key
    # Wait a couple of seconds to marvel in the beauty
    # Close the character tab with a mouse click

    # Using only the KEYDOWN event is enough, no need for KEYUP
    win32gui.PostMessage(whnd, WM_KEYDOWN, C_VK, c_key_down)

    # 3 seconds of sleep
    time.sleep(3)

    # Using Spy++ the needed location of the click can be determined
    # lparam is 32 bit in lenght, each coordinate is stored on 16 bits
    # the order of the coordinates is : y,x
    # If no OpenCV window is open, these are the correct coordinates
    # character_tab_lparam = int('00000001001011110000000000011111', 2)
    #opencv_map_coordinates = int('00000001101011110000000000011111', 2)
    #opencv_quests_coordinates = int('00000001100000110000000000011111', 2)

    # If OpenCV is open, we need these modified coordinates
    opencv_chartab_coordinates = int('00000001011100110000000000011111', 2)

    win32gui.PostMessage(whnd, WM_LBUTTONDOWN,
                         MK_LBUTTON, opencv_chartab_coordinates)
    # Let's wait just a little bit, to make sure the events register
    time.sleep(0.1)
    win32gui.(whnd, WM_LBUTTONUP, 0, opencv_chartab_coordinates)

def press_c():


def report_current_xp():
    while 1:
        # 1. openCv -> Cut part of the image

        with mss() as sct:
            character_tab_screenshot = numpy.array(sct.grab(DIABLO_WINDOW))

        cv2.imwrite(
            r'C:\Users\hosszub\projects\evil_snek\temp_data\character_screen_captured.png', character_tab_screenshot)
        #img = cv2.imread(
        #    r'C:\Users\hosszub\projects\evil_snek\temp_data\character_screen.png')
        img_of_xp = character_tab_screenshot[55:70, 230:275]
        cv2.imwrite(
            r'C:\Users\hosszub\projects\evil_snek\temp_data\xp_captured.png', img_of_xp)
        # 2. Optional --> apply filters on image to easy OCR processes later on
        # 3. pytesseract --> read the number
        xp = pytesseract.image_to_string(
            img_of_xp, lang="digits_comma", config="--psm 8")
        # 4. report the number, maybe just log it, maybs show a more complex insight
        print(time.time(), ": xp=", xp)
        with open('temp_data/xp_log.csv', 'a') as xp_csv:
            xp_csv.write('{},{}\n'.format(time.time(), xp))
        # Let's do periodic check on how the value is changing.
        time.sleep(3)


if __name__ == '__main__':
    interaction_thread = threading.Thread(target=interaction)
    # classifying as a daemon, so they will die when the main dies
    interaction_thread.daemon = True
    # begins, must come after daemon definition
    # interaction_thread.start()

    xp_thread = threading.Thread(target=report_current_xp)
    xp_thread.daemon = True
    xp_thread.start()

    opencv()
