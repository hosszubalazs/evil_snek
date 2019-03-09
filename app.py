import time
import numpy
import cv2
from mss import mss

monitor = {"top": 160, "left": 160, "width": 160, "height": 135}

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
