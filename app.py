import time
import numpy
import cv2
from mss import mss

# Please start Diablo according to the resolution configured here
# Optimized for full HD screens, you might need to fiddle with the coordinates to properly set the capture.
monitor = {"top": 320, "left": 590, "width": 640 , "height": 480}

sct = mss()
print("Press q to exit.")

while 1:
    last_time = time.time()
    img = numpy.array(sct.grab(monitor))
    cv2.imshow('test', img)
    print("fps: {}".format(1 / (time.time() - last_time)))

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
