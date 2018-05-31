from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *
from flickr import flickr_api
import cv2
from datetime import datetime

PHOTOSET_TITLE = 'Photobooth'
COVER_PICTURE = 'dmitri.jpg'
TEMP_PICTURE_PATH = 'img.jpg'

def get_photoset(user):
    sets = user.getPhotosets()
    try:
        photoset = next(filter(lambda s: s.title == PHOTOSET_TITLE, sets))
    except StopIteration:
        cover = flickr_api.upload(photo_file=COVER_PICTURE, title='Cover', is_public='0')
        photoset = flickr_api.Photoset.create(title=PHOTOSET_TITLE, primary_photo=cover)
    return photoset

def upload_image(path, photoset):
    image = flickr_api.upload(photo_file=path, title=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), is_public='0')
    photoset.addPhoto(photo=image)

if __name__ == '__main__':
    user = flickr_api.test.login()
    photoset = get_photoset(user)
    webcam = cv2.VideoCapture()
    webcam.open(1)
    cv2.namedWindow('webcam', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("webcam",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    
    while True:
        k = cv2.waitKey(10) & 0xFF
        _, img = webcam.read()
        cv2.imshow('webcam', img)
        if k == 27:
            # Escape key pressed
            print("Goodbye!")
            break
        elif k == ord('s'):
            with_message = img.copy()
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(with_message,'Moment geduld aub..',(0, 200), font, 2, (255,255,255),2,cv2.LINE_AA)
            cv2.imshow('webcam', with_message)
            cv2.waitKey(1)
            print("Showing image with message")
            cv2.imwrite(TEMP_PICTURE_PATH, img)
            upload_image(TEMP_PICTURE_PATH, photoset)
            print("Saved.")
    
