
# load the two images
import pyexr
import util
from app import generator

images = [
    util.image.lin_to_srgb(pyexr.read("blue.exr")),
    util.image.lin_to_srgb(pyexr.read("yellow.exr"))
]

elements = [ # rows
    [ # first row
        {
            "image": images[0],
            "crop_marker": {
                "line_width": 1.0, "dashed": False, 
                "list": [
                    { "pos": [32,32], "size": [15,10], "color": [242, 113, 250] }
                ]
            }
        },
        {
            "image": images[1],
            "captions": {
                "north": "North Caption",
                "south": "Yellow"
            },
            "frame": { "line_width": 1.0, "color": [100,90,10] },
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
    "east": { 
        "text_color": [0,0,0],
        "background_colors": [255, 255, 255],
        "content": [ "Awesome pictures" ]
    }
}

titles = {
    "north": "North Title",
    "south": "South Title",
    "east": "East Title",
    "west": "West Title",
}

modules = [
    { 
        "elements": elements, 
        "row_titles": row_titles, 
        "column_titles": column_titles, 
        "titles": titles, 
        "layout": "layout.json" 
    }
]

generator.horizontal_figure(modules, backend='tikz')