import tensorflow
from PIL import Image, ImageDraw
import tensorflow_hub


class Seeker:
    def __init__(self, path="./model/"):

        self.model = detector = tensorflow_hub.load(path).signatures["default"]


    def count(self, path, path_to_save="res.jpg", save=True):
        count = 0
        image_dir = "images/1.jpg"
        with Image.open(path) as image:
            converted_image = tensorflow.image.convert_image_dtype(tensorflow.convert_to_tensor(image), tensorflow.float32)[tensorflow.newaxis, ...]
            res = self.model(converted_image)
            res = {key: value for key, value in res.items()}
            width, height = image.size
            draw = ImageDraw.Draw(image)
            for entity_i in range(len(res["detection_class_entities"])):
                entity = res["detection_class_entities"][entity_i]
                if entity in ("Person", "Man", "Woman") and res["detection_scores"][entity_i] >= 0.7:
                    count += 1
                    box = res['detection_boxes'][entity_i]
                    draw.rectangle((box[1] * width, box[0] * height, box[3] * width, box[2] * height), width=3, outline="green")
            if save:
                image.save(path_to_save)
        return count