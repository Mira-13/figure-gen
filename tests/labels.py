import pyexr
import numpy as np
import generator
import generator.util

# generate test images
blue = np.tile([0.2,0.3,0.9], (32, 64, 1))
yellow = np.tile([0.9,0.8,0.2], (32, 64, 1))
pyexr.write("images//blue.exr", blue)
pyexr.write("images//yellow.exr", yellow)

# load the two images
images = [
    generator.util.image.lin_to_srgb(pyexr.read("images//blue.exr")),
    generator.util.image.lin_to_srgb(pyexr.read("images//yellow.exr"))
]

elements = [ # rows
    [ # first row
        {
            "image": images[0],
            "label": {
                "bottom_left": {
                    "text": "hi\nlabel",
                    "fontsize": 5,
                    "line_space": 1.2,
                    "text_color": [0,0,0],
                    "background_color": None,
                    "width_mm": 15.,
                    "height_mm": 5.,
                    "offset_mm": [5.2, 2.0],
                    "padding_mm": 1.0
                },
                "bottom_right": {
                    "text": "hi label",
                    "fontsize": 5,
                    "line_space": 1.2,
                    "text_color": [0,0,0],
                    "background_color": [200, 200, 200],
                    "width_mm": 15.,
                    "height_mm": 5.,
                    "offset_mm": [2.2, 1.0],
                    "padding_mm": 1.0
                },
                "top_center": {
                    "text": "hi label",
                    "fontsize": 5,
                    "line_space": 1.2,
                    "text_color": [0,0,0],
                    "background_color": [200, 200, 200],
                    "width_mm": 15.,
                    "height_mm": 5.,
                    "offset_mm": 2.2,
                    "padding_mm": 1.0
                }
            }
        },
        {
            "image": images[1],
            "captions": {
                "north": "North Caption",
                "south": "Yellow"
            },
            "frame": { "line_width": 1.0, "color": [50,30,210] }
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
        "layout": {
          "padding.east": 0.1,
          "padding.north": 0.5,
          "titles.north.height": 8,
          "titles.north.background_color": [ 29, 60, 100 ],
          "titles.north.text_color": [ 255, 255, 250 ],
          "column_titles.north.width": 4,
          "column_titles.north.offset": 2,

          "column_space": 1,
          "row_space": 2
        }
    }
]

if __name__ == "__main__":
    generator.horizontal_figure(modules, width_cm=18., filename='label_test.pdf')
    generator.horizontal_figure(modules, width_cm=18., filename='label_test.pptx')
    generator.horizontal_figure(modules, width_cm=18., filename='label_test.html')
