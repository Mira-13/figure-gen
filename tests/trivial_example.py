
import pyexr
import numpy as np
import generator
import generator.util

# generate test images
blue = np.tile([0.2,0.3,0.9], (32, 64, 1))
yellow = np.tile([0.9,0.8,0.2], (32, 64, 1))
pyexr.write("blue.exr", blue)
pyexr.write("yellow.exr", yellow)

# load the two images
images = [
    generator.util.image.lin_to_srgb(pyexr.read("blue.exr")),
    generator.util.image.lin_to_srgb(pyexr.read("yellow.exr"))
]

elements = [ # rows
    [ # first row
        {
            "image": images[0],
        },
        {
            "image": images[1],
        },
    ] # end first row
]

column_titles = {
}

row_titles = {
}

titles = {
    "north": "North Title",
    "south": "South Title",
    "west": "West Title",
}

modules = [
    { 
        "type": "grid",
        "elements": elements, 
        "row_titles": row_titles, 
        "column_titles": column_titles, 
        "titles": titles, 
        "layout": "layout-trivial.json" 
    }
]

if __name__ == "__main__":
    generator.horizontal_figure(modules, width_cm=28., backend='html', out_dir=".")