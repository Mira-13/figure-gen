import pyexr
import util
import numpy as np
from app import generator

# generate test images
blue = np.tile([0.2,0.3,0.9], (64, 64, 1))
yellow = np.tile([0.9,0.8,0.2], (64, 64, 1))

# load the two images
images = [
    util.image.lin_to_srgb(blue),
    util.image.lin_to_srgb(yellow)
]

elements = [[{
    "image": [
        { "name": "blue", "image": images[0] },
        { "name": "yellow", "image": images[1] }
    ]
}]]

modules = [{ 
    "elements": elements, 
    "row_titles": {}, 
    "column_titles": {}, 
    "titles": {}, 
    "layout": "layout.json" 
}]

if __name__ == "__main__":
    generator.horizontal_figure(modules, 18, "html")