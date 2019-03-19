import cv2
from mss import mss
import numpy
import os
import time


def initialize_window_size(window_parameters):
    # FIXME the margins only work in 4:3 windowed mode
    side_margin = 1
    top_margin = 32
    bottom_margin = 1
    window_dimensions = {
        "top": window_parameters.top + top_margin,
        "left": window_parameters.left + side_margin,
        "width": window_parameters.right - window_parameters.left - 2*side_margin,
        "height": window_parameters.bottom - (window_parameters.top + top_margin) - bottom_margin
    }
    return window_dimensions


def create_folder(folder_path):
    try:
        os.mkdir(folder_path)
    except OSError:
        print("Creation of the directory %s failed" % folder_path)
    else:
        print("Successfully created the directory %s " % folder_path)


def take_screenshot(window_dimensions):
    with mss() as sct:
        screenshot = numpy.array(sct.grab(window_dimensions))
    return screenshot


def save_image(folder_path, filename, image):
    cv2.imwrite(
        r'{}\{}'.format(folder_path, filename), image)


def crop_xp(character_tab_screenshot):
    height, width, channels = character_tab_screenshot.shape
    x_start = int(0.34 * width)
    x_size = int(70/640 * width)

    y_start = int(0.115 * height)
    y_size = int(15/480 * height)
    cropped = character_tab_screenshot[y_start:y_start +
                                       y_size, x_start:x_start+x_size]

    # imagem = cv2.bitwise_not(cropped)

    return cropped


def crop_gold(character_tab_screenshot):
    height, width, channels = character_tab_screenshot.shape

    x_start = int(240/640 * width)
    x_size = int(60/640 * width)

    y_start = int(133/480 * height)
    y_size = int(16/480 * height)
    return character_tab_screenshot[y_start:y_start+y_size, x_start:x_start+x_size]


def crop_hp(character_tab_screenshot):
    height, width, channels = character_tab_screenshot.shape
    x_start = int(142/640 * width)
    x_size = int(35/640 * width)

    y_start = int(293/480 * height)
    y_size = int(15/480 * height)
    cropped = character_tab_screenshot[y_start:y_start +
                                       y_size, x_start:x_start+x_size]

    # grayed = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    # normalized = cv2.normalize(grayed, grayed, 0, 255, cv2.NORM_MINMAX)

    # ret, thresh1 = cv2.threshold(normalized, 170, 400, cv2.THRESH_BINARY)

    # cannied = cv2.Canny(normalized, 570, 750)
    # gaussian_blurred_2 = cv2.GaussianBlur(thresh1, (3, 3), 0)
    return cropped


def opencv_fun(window_dimensions, temp_data_path):
    print("lol")
    print(window_dimensions)

    # Dummy initialization
    previous_frame = 0
    while 1:
        last_time = time.time()

        diablo_scrnsht = take_screenshot(window_dimensions)

        scrnsht_hsv = cv2.cvtColor(diablo_scrnsht, cv2.COLOR_BGR2HSV)
        canny_on_hue = cv2.Canny(scrnsht_hsv[:, :, 0], 100, 200)
        save_image(temp_data_path, "canny_on_hue.png", canny_on_hue)
        cv2.imshow('Canny on Hue channel', canny_on_hue)

        frame_difference = canny_on_hue - previous_frame
        time_diff = (time.time() - last_time)
        if time_diff > 0:
            fps = format(1 / time_diff, '.2f')
            # print("fps:", fps)
        cv2.putText(frame_difference, "FPS={}".format(fps),
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2)

        save_image(temp_data_path, "frame_difference.png", frame_difference)
        cv2.imshow('Difference between HSV frames', frame_difference)
        previous_frame = canny_on_hue

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
