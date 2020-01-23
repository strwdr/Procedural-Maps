import numpy as np
import random
import image_tools
from PIL import Image

random.seed(1000)
DIMENSIONS_RANGE = (1, 20)


def test_create_img_from_color_map():
    for i in range(100):
        dimensions = random.randint(DIMENSIONS_RANGE[0], DIMENSIONS_RANGE[1]), \
                     random.randint(DIMENSIONS_RANGE[0], DIMENSIONS_RANGE[1])
        color_map = np.zeros([dimensions[0], dimensions[1], 3], dtype=np.uint8)
        img = image_tools.create_image_from_color_map(color_map)
        assert type(img) == Image.Image
        img = image_tools.create_image_from_color_map(color_map, True)
        assert type(img) == Image.Image

