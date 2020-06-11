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
            "crop_marker": {
                "line_width": 1.0, "dashed": False, 
                "list": [
                    { "pos": [32,12], "size": [15,10], "color": [242, 113, 250] },
                    { "pos": [1,1], "size": [15,10], "color": [50,230,10] }
                ]
            }
        },
        {
            "image": images[1],
            "captions": {
                "north": "North Caption",
                "south": "Yellow"
            },
            "frame": { "line_width": 5.0, "color": [50,230,10] },
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
        "background_colors": [30, 255, 255],
        "content": [ "Awesome pictures" ]
    }
}

titles = {
    "north": "North\nTitle",
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
    generator.horizontal_figure(modules, width_cm=28., backend='tikz', out_dir=".")
    generator.horizontal_figure(modules, width_cm=28., backend='pptx', out_dir=".")
    generator.horizontal_figure(modules, width_cm=28., backend='html', out_dir=".")