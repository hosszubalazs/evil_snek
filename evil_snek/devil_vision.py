import cv2
from mss import mss
import numpy
import os
import time


# Please start Diablo according to the resolution configured here
# Optimized for full HD screens, you might need to fiddle
# with the coordinates to properly set the capture.
DIABLO_WINDOW_FULLHD = {"top": 290, "left": 640, "width": 640, "height": 480}
DIABLO_WINDOW_4K = {"top": 858, "left": 1600, "width": 640, "height": 480}
DIABLO_WINDOW = DIABLO_WINDOW_FULLHD


def create_folder(folder_path):
    try:
        os.mkdir(folder_path)
    except OSError:
        print("Creation of the directory %s failed" % folder_path)
    else:
        print("Successfully created the directory %s " % folder_path)


def take_screenshot():
    with mss() as sct:
        screenshot = numpy.array(sct.grab(DIABLO_WINDOW))
    return screenshot


def save_image(folder_path, filename, image):
    cv2.imwrite(
        r'{}\{}'.format(folder_path, filename), image)


def crop_xp(character_tab_screenshot):
    height, width, channels = character_tab_screenshot.shape
    x_start = int(0.36 * width)
    x_size = int(60/640 * width)

    y_start = int(0.115 * height)
    y_size = int(15/480 * height)
    return character_tab_screenshot[y_start:y_start+y_size, x_start:x_start+x_size]


def crop_gold(character_tab_screenshot):
    height, width, channels = character_tab_screenshot.shape

    x_start = int(240/640 * width)
    x_size = int(60/640 * width)

    y_start = int(133/480 * height)
    y_size = int(16/480 * height)
    return character_tab_screenshot[y_start:y_start+y_size, x_start:x_start+x_size]


def opencv_fun():
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
