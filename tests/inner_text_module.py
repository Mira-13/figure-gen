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
            "label": {
                "bottom_left": {
                    "text": "hi label",
                    "fontsize": 5,
                    "line_space": 1.2,
                    "text_color": [0,0,0],
                    "background_color": [200, 200, 200],
                    "width_mm": 15.,
                    "height_mm": 5.,
                    "offset": 2.2,
                    "offset_width": 5.2,
                    "offset_height": 2.0,
                    "offset_text": 1.0
                },
                "bottom_right": {
                    "text": "hi label",
                    "fontsize": 5,
                    "line_space": 1.2,
                    "text_color": [0,0,0],
                    "background_color": [200, 200, 200],
                    "width_mm": 15.,
                    "height_mm": 5.,
                    "offset": 2.2,
                    "offset_width": 5.2,
                    "offset_height": 2.0,
                    "offset_text": 1.0
                },
                "bottom_center": {
                    "text": "hi label",
                    "fontsize": 5,
                    "line_space": 1.2,
                    "text_color": [0,0,0],
                    "background_color": [200, 200, 200],
                    "width_mm": 15.,
                    "height_mm": 5.,
                    "offset": 2.2,
                    "offset_width": 5.2,
                    "offset_height": 2.0,
                    "offset_text": 1.0
                }
            }
        },
        {
            "image": images[1],
            "captions": {
                "north": "North Caption",
                "south": "Yellow"
            },
            "frame": { "line_width": 1.0, "color": [50,230,10] }
        },
    ] # end first row
]

column_titles = {
    "north": { 
        "text_color": [0,0,0],
        "background_colors": [[10, 10, 200], [255, 200, 10]],
        "content": [ "Blue", "Yellow" ]
    }
}

row_titles = {
    "west": { 
        "text_color": [0,0,0],
        "background_colors": [255, 255, 255],
        "content": [ "Awesome pictures" ]
    }
}

titles = {
    "north": "North Title",
    "south": "South Title",
    "east": "East Title",
    "west": "West Title"
}

modules = [
    { 
        "type": "grid",
        "elements": elements, 
        "row_titles": row_titles, 
        "column_titles": column_titles, 
        "titles": titles, 
        "layout": "layout.json" 
    }
]

if __name__ == "__main__":
    generator.horizontal_figure(modules, width_cm=18., backend='tikz', out_dir=".")
