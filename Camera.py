import cv2
import datetime


# set path in which you want to save images

class Cam:
    def __init__(self, path='video/vid_1.mp4'):
        self.video = cv2.VideoCapture(path)
        self.path = path
        self.amount_of_frames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

    def new_path(self, path):
        self.video = cv2.VideoCapture(path)

    def parse(self):
        cur_time = datetime.datetime.now()
        cur_time = datetime.datetime(cur_time.year, cur_time.month, cur_time.day)
        delta_time = (datetime.datetime.now() - cur_time).seconds * self.fps
        frame = int(delta_time % self.amount_of_frames)
        self.video.set(cv2.CAP_PROP_POS_FRAMES, frame - 1)
        ret, img = self.video.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #print(self.amount_of_frames, frame, self.fps, self.amount_of_frames)
        return img