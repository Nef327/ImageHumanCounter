import asyncio

import cv2
import os
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

    def model_work(self, image, save: bool = True):
        image = Image.fromarray(image.astype('uint8'), mode="RGB")
        converted_image: EagerTensor = \
        tensorflow.image.convert_image_dtype(tensorflow.convert_to_tensor(image), tensorflow.float32)[
            tensorflow.newaxis, ...]
        res = self.model(converted_image)
        res = {key: value for key, value in res.items()}

        people = []
        for entity_i in range(len(res["detection_class_entities"])):
            entity = res["detection_class_entities"][entity_i]
            if entity in ("Person", "Man", "Woman") and res["detection_scores"][entity_i] >= 0.1:
                box = res['detection_boxes'][entity_i]
                people.append({"detection_scores": res["detection_scores"][entity_i],
                               "entity": "Person",
                               "box": ((box[1], box[0], box[3], box[2]))})
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
                draw = ImageDraw.Draw(image)
                for box in selected_boxes:
                    draw.rectangle((box[0] * width, box[1] * height, box[2] * width, box[3] * height), width=3,
                                   outline="green")
                image.save("res.jpg")


"""class FSeeker(Seeker):
    def __init__(self, path="./model_0/"):


        # load the class label names from disk, one label per line
        # CLASS_NAMES = open("coco_labels.txt").read().strip().split("\n")

        CLASS_NAMES = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
                       'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog',
                       'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella',
                       'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
                       'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle',
                       'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
                       'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant',
                       'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
                       'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                       'teddy bear', 'hair drier', 'toothbrush']

        class SimpleConfig(mrcnn.config.Config):
            # Give the configuration a recognizable name
            NAME = "coco_inference"

            # set the number of GPUs to use along with the number of images per GPU
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1

            # Number of classes = number of classes + 1 (+1 for the background). The background class is named BG
            NUM_CLASSES = len(CLASS_NAMES)

        # Initialize the Mask R-CNN model for inference and then load the weights.
        # This step builds the Keras model architecture.
        self.model = mrcnn.model.MaskRCNN(mode="inference",
                                     config=SimpleConfig(),
                                     model_dir=os.getcwd())
        self.model.load_weights(filepath="mask_rcnn_coco.h5",
                           by_name=True)
        self.count = 0"""