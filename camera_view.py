from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *

import cv2

webcam = cv2.VideoCapture(0)
cv2.namedWindow('webcam', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("webcam",cv2.WND_PROP_FULLSCREEN, 1)

try:
    while True:
        _, frame = webcam.read()
        rows, cols, _ = frame.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
        dst = cv2.warpAffine(frame, M, (cols,rows))
        cv2.imshow('webcam', dst)
        cv2.waitKey(1)
except KeyboardInterrupt:
    webcam.release()
    cv2.destroyAllWindows()
    print('Goodbye!')
