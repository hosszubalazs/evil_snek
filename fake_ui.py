from win32 import win32gui
import win32con
import sys
import time


# Please check MSDN documentation on these WIN32 codes
# Looks scary, but really not so bad
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
MK_LBUTTON = 0x0001

WM_KEYDOWN = 0x0100
# WM_KEYUP = 0x0101
# WM_CHAR = 0x0102

# Virtual code and scan code for the letter 'c'
C_VK = 0x43
C_SC = 0x2E



# Coordinates for clicking. This part is unstable.
# If no OpenCV window is open, the coordinates are different inside Diablo, for some reason.
# character_tab_lparam = int('00000001001011110000000000011111', 2)
opencv_map_coordinates = int('00000001101011110000000000011111', 2)
opencv_quests_coordinates = int('00000001100000110000000000011111', 2)
opencv_chartab_coordinates = int('00000001011100110000000000011111', 2)


def initalize_window_handler(window_title='DIABLO'):
    WHND = win32gui.FindWindowEx(None, None, None, window_title)
    if WHND == 0:
        sys.exit("Diablo was not found. Please makes sure Diablo is running, and you are running this program with sufficient rights.")
    return WHND

def press_button(whnd,virtual_key, scan_code):
    if whnd == 0:
        sys.exit(
            "Window handle not configfured. Please use initalize_window_handle().")
    key_down = int('000000000000001'+'{0:08b}'.format(scan_code)+'00000000', 2)

    # Diablo IN YOUR FACE
    win32gui.SetForegroundWindow(whnd)

    # Using only the KEYDOWN event is enough, no need for KEYUP
    win32gui.PostMessage(whnd, WM_KEYDOWN, virtual_key, key_down)


def left_click(whnd,coordinates):
    if whnd == 0:
        sys.exit(
            "Window handle not configfured. Please use initalize_window_handle().")
    # Using Spy++ the needed location of the click can be determined
    # lparam is 32 bit in lenght, each coordinate is stored on 16 bits
    # the order of the coordinates is : y,x

    win32gui.PostMessage(whnd, WM_LBUTTONDOWN,
                         MK_LBUTTON, coordinates)
    # Let's wait just a little bit, to make sure the events register
    time.sleep(0.1)
    win32gui.PostMessage(whnd, WM_LBUTTONUP, 0, coordinates)
