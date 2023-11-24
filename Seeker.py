import tensorflow
from PIL import Image, ImageDraw
import tensorflow_hub





class Seeker:
    def __init__(self, path="./model/"):

        self.model = detector = tensorflow_hub.load(path).signatures["default"]


    def model_work(self, path):
        with Image.open(path) as image:
            converted_image = tensorflow.image.convert_image_dtype(tensorflow.convert_to_tensor(image), tensorflow.float32)[tensorflow.newaxis, ...]
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
            people = self.model_work(path)[0]
            if not people:
                return 0
            boxes = [pep["box"] for pep in people]
            selected_indices = tensorflow.image.non_max_suppression(boxes, [pep["detection_scores"] for pep in people],
                                                                    99999, iou_threshold=0.35)
            selected_boxes = tensorflow.gather(boxes, selected_indices)

            return selected_boxes, image

    def count(self, path):

        selected_boxes = self.model_work(path)[0]
        count = len(selected_boxes)

        return count

    def generate_image(self, path):
        selected_boxes, image = self.model_work(path)
        width, height = image.size
        draw = ImageDraw.Draw(image)
        for box in selected_boxes:
            draw.rectangle((box[0] * width, box[1] * height, box[2] * width, box[3] * height), width=3, outline="green")
        image.save("res.jpg")
