# load images
reference = manage_images.gloskitch120_ref

# get an image for the resolution 
a = manage_images.gloskitch120_ref

def mse(img, ref):
    return util.image.mean(util.image.luminance(util.image.squared_error(img, ref)))



# define figure data
data = {
    "img_width_px": len(a[0]),
    "img_height_px": len(a),
    "column_titles": {
        "north": { 
            "height": 0.0,
            "offset": 0.0,
            "rotation": 0,
            "fontsize": 7, 
            "line_space": 1.2,
            "text_color": [0,0,0],
            "content": ["col top 1", "col top 2", "col top 3", "col pottom 4", "col top 5", "col top 6"]
        },
        "south": {
            "height": 0.0,
            "offset": 0.0,
            "rotation": 0,
            "fontsize": 7, 
            "line_space": 1.2,
            "text_color": [255,255,255],
            "background_colors": [41, 96, 188],
            "content": ["col bottom 1", "col pottom 2", "col bottom 3", "col pottom 4", "col bottom 5", "col bottom 6"]
        }
    },

    "row_titles": {
        "east": { 
            "width": 0.0,
            "offset": 0.0,
            "rotation": -90,
            "fontsize": 7, 
            "line_space": 1.2,
            "text_color": [0,0,0],
            "background_colors": [[41, 96, 188], [221, 191, 38], [66, 180, 70], [231, 191, 78], [180, 55, 68], [210, 135, 38]],
            "content": ["row a 1", "row b 2", "row c 3", "row d 4", "row e 5", "row f 6"]
        },
        "west": {
            "width": 0.0,
            "offset": 0.0,
            "rotation": 90,
            "fontsize": 7, 
            "line_space": 1.2,
            "text_color": [0,0,0],
            "background_colors": [[41, 96, 188], [221, 191, 38], [66, 180, 70], [231, 191, 78], [180, 55, 68], [210, 135, 38]],
            "content": ["row a 1", "row b 2", "row c 3", "row d 4", "row e 5", "row f 6"]
        }
    },
    "elements_content": [
        [
            {
                "image": util.image.lin_to_srgb(manage_images.glossyKitchenRef()),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.1, "dashed": False, 
                                "list": [
                                    {"pos": [0.5, 0.5, 0.6, 0.6], "color": [41, 96, 188]}, 
                                    {"pos": [0.3, 0.3, 0.4, 0.4], "color": [221, 191, 38]}
                                ]
                            }
            }
        ]  
    ],
    "num_rows": 1,
    "num_columns": 1
}
# TODO num rows and columns are not calculated, but should be, because it will be less work for the user
