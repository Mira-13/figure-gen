# load images
reference = manage_images.vdoor60_ref

# get an image for the resolution 
a = manage_images.vdoor60_ref

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
            "content": ["\\textsc{Veach Door}", "col top 2", "col top 3", "col pottom 4", "col top 5", "col top 6"]
        },
        "south": {
            "height": 0.0,
            "offset": 0.0,
            "rotation": 0,
            "fontsize": 7, 
            "line_space": 1.2,
            "text_color": [0,0,0],
            "background_colors": [255, 255, 255],
            "content": ["\\textsc{Veach Door}", "col pottom 2", "col bottom 3", "col pottom 4", "col bottom 5", "col bottom 6"]
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
            "background_colors": [255, 255, 255],
            "content": ["\\textsc{Veach Door}", "row b 2", "row c 3", "row d 4", "row e 5", "row f 6"]
        },
        "west": {
            "width": 0.0,
            "offset": 0.0,
            "rotation": 90,
            "fontsize": 7, 
            "line_space": 1.2,
            "text_color": [0,0,0],
            "background_colors": [255, 255, 255],
            "content": ["\\textsc{Veach Door}", "row b 2", "row c 3", "row d 4", "row e 5", "row f 6"]
        }
    },
    "elements_content": [
        [
            {
                "image": util.image.lin_to_srgb(reference),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.2, "dashed": False, 
                                "list": [
                                    {"pos": manage_images.vdoor_crop(1), "color": [242, 113, 0]}, 
                                    {"pos": manage_images.vdoor_crop(2), "color": [242, 113, 0]}
                                    ]
                            }
            }
        ]  
    ],
    "num_rows": 1,
    "num_columns": 1
}
# TODO num rows and columns are not calculated, but should be, because it will be less work for the user
