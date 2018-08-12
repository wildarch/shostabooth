from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *

import cv2
from datetime import datetime
import time
import os
import math
from slideshow import Slideshow
from button import Button

PHOTO_DIR='photos/'
PICTURE_TIMEOUT = 6
SLIDESHOW_TIME_PER_PHOTO = 1
BUTTON_GPIO_PIN = 18
BUTTON_KEYBOARD_KEY = 's'
BUTTON_PRESS_TIME = 2

def save_photo(img):
    time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    path = "{}{}.jpg".format(PHOTO_DIR, time)
    cv2.imwrite(path, img)

def put_text_center(img, text):
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    SCALE = 2
    THICKNESS = 5

    text_size = cv2.getTextSize(text, FONT, SCALE, THICKNESS)[0]
    x = (img.shape[1] - text_size[0]) / 2
    y = (img.shape[0] - text_size[1]) / 2

    cv2.putText(img, text, (int(x), int(y)), FONT, SCALE, (0, 0, 255), THICKNESS)

if __name__ == '__main__':
    try:
        os.mkdir(PHOTO_DIR)
    except OSError:
        # Directory exists
        pass

    picture_time = None

    # Open webcam first one found
    webcam = cv2.VideoCapture(0)

    # Create a full-screen window
    #cv2.namedWindow('webcam', cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty("webcam",cv2.WND_PROP_FULLSCREEN, 1)

    slideshow = Slideshow(PHOTO_DIR, SLIDESHOW_TIME_PER_PHOTO)
    button = Button(BUTTON_GPIO_PIN, BUTTON_KEYBOARD_KEY)
    
    try:
        while True:
            k = cv2.waitKey(1) & 0xFF
            _, img = webcam.read()
            cv2.imshow('webcam', img)
            if k == 27:
                # Escape key pressed
                print("Goodbye!")
                break
            elif button.pressed(BUTTON_PRESS_TIME, k) and picture_time is None:
                picture_time = time.time() + PICTURE_TIMEOUT

            if picture_time is not None:
                time_left = math.ceil(picture_time - time.time())

                with_text = img.copy()
                if time_left > 1.0:
                    put_text_center(with_text, str(int(time_left) - 1))
                elif time_left > 0.0:
                    put_text_center(with_text, "Cheese!")
                elif time_left > -1.0:
                    put_text_center(with_text, "Boterkoek ;)")
                else:
                    picture_time = None
                    save_photo(img)
                    slideshow.refresh()
                cv2.imshow('webcam', with_text)
            else:
                # TODO slideshow
                cv2.imshow('webcam', slideshow.get_current_image())
    except KeyboardInterrupt:
        webcam.release()
        cv2.destroyAllWindows()
