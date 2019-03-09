import numpy
import cv2
from mss import mss

monitor = {"top": 160, "left": 160, "width": 160, "height": 135}

sct = mss()

while 1:
    img = numpy.array(sct.grab(monitor))
    cv2.imshow('test', img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
