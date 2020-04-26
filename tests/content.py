
# load the two images
import pyexr
import util

images = [
    util.image.lin_to_srgb(pyexr.read("blue.exr")),
    util.image.lin_to_srgb(pyexr.read("yellow.exr"))
]

content = [ # rows
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
            "frame": { "line_width": 1.0, "color": [100,90,10] },
        },
    ] # end first row
]

column_titles = [ "Orange", "Blue" ]

row_titles = [ "Awesome pictures" ]

# define figure data
data = { 
    "column_titles": {
        "north": { 
            "height": 10.0,
            "offset": 0.2,
            "fontsize": 7, 
            "line_space": 1.2,
            "text_color": [0,0,0],
            "background_colors": [[255, 200, 10], [10, 10, 200]],
            "content": column_titles
        }
    },

    "row_titles": {
        "east": { 
            "width": 5.0,
            "offset": 0.2,
            "rotation": -90,
            "fontsize": 7, 
            "line_space": 1.2,
            "text_color": [0,0,0],
            "background_colors": [255, 255, 255],
            "content": row_titles
        }
    },

    "elements_content": content,
}