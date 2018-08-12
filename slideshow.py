import os
import cv2
import time

class Slideshow:
    def __init__(self, photo_dir, time_per_photo):
        self.photo_dir = photo_dir
        self.time_per_photo = time_per_photo
        self.refresh()

    def refresh(self):
        files = os.listdir(self.photo_dir)
        self.photos = []
        for file_name in sorted(files, reverse=True):
            if not file_name.endswith('.jpg'):
                continue
            path = os.path.join(self.photo_dir, file_name)
            self.photos.append(cv2.imread(path))
        self.time_start = time.time()

    def get_current_image(self):
        show_time = time.time() - self.time_start
        index = int(show_time / self.time_per_photo) % len(self.photos)
        return self.photos[index]


