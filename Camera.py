import cv2

from Seeker import Seeker


# set path in which you want to save images

class Cam:
    def __init__(self, path='video/vid_1.mp4'):
        self.video = cv2.VideoCapture(path)
        self.path = path
        self.process = False

    def re_path(self):
        self.video = cv2.VideoCapture(self.path)

    def parse(self, seeker: Seeker):
        while True:
            while self.video.isOpened():
                ret, img = self.video.read()
                while self.video.isOpened() and ret:
                    ret, img = self.video.read()
                    cv2.waitKey(1300)
                    if self.process:
                        seeker.model_work(img, True)

            self.re_path()
