"""Apply a bunch of OpenCV2 filters to the original Diablo 1 game, for fun and profit."""
import time
import numpy
import cv2
from mss import mss

# Please start Diablo according to the resolution configured here
# Optimized for full HD screens, you might need to fiddle
# with the coordinates to properly set the capture.
DIABLO_WINDOW = {"top": 320, "left": 590, "width": 640, "height": 480}

def main():
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

        fps = format(1 / (time.time() - last_time), '.2f')
        print("fps:", fps)
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

if __name__ == '__main__':
    main()
