import asyncio

import cv2
import os

import numpy
import tensorflow
from PIL import Image, ImageDraw
import tensorflow_hub
from tensorflow.python.framework.ops import EagerTensor


class Seeker:
    def __init__(self, path="./model/"):

        self.model = tensorflow_hub.load(path).signatures["default"]
        self.count = 0

    def image(self, path, save: bool = True):
        with Image.open(path) as image:
            self.model_work(image, save)

    def model_work(self, img, save: bool = True, crop=None):

        if crop is None:
            crop = (0, 0, *img.size)
        image = img.crop(crop)
        converted_image: EagerTensor = \
            tensorflow.image.convert_image_dtype(tensorflow.convert_to_tensor(image), tensorflow.float32)[
                tensorflow.newaxis, ...]
        res = self.model(converted_image)
        res = {key: value for key, value in res.items()}

        people = []
        for entity_i in range(len(res["detection_class_entities"])):
            entity = res["detection_class_entities"][entity_i]
            if entity in ("Person", "Man", "Woman") and res["detection_scores"][entity_i] >= 0.13:
                box = res['detection_boxes'][entity_i]
                people.append({"detection_scores": res["detection_scores"][entity_i],
                               "entity": "Person",
                               "box": (box[1], box[0], box[3], box[2])})
        if not people:
            self.count = 0
            image.save("res.jpg")
        else:
            boxes = [pep["box"] for pep in people]
            selected_indices = tensorflow.image.non_max_suppression(boxes, [pep["detection_scores"] for pep in people],
                                                                    99999, iou_threshold=0.35)
            selected_boxes = tensorflow.gather(boxes, selected_indices)

            self.count = len(selected_boxes)
            if save:
                width, height = image.size
                draw = ImageDraw.Draw(img)
                for box in selected_boxes:
                    draw.rectangle((box[0] * width + crop[0], box[1] * height + crop[1],
                                    box[2] * width + crop[0], box[3] * height + crop[1]), width=3,
                                   outline="green")
                img.save("res.jpg")
