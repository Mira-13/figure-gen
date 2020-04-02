# load images
reference = manage_images.gloskitch120_ref
first = manage_images.gloskitch120_patht
second = manage_images.gloskitch120_bdpt
fourth = manage_images.gloskitch120_radia
third = manage_images.gloskitch120_upscmc
fifth = manage_images.gloskitch120_ofull

# get an image for the resolution 
a = manage_images.glossyKitchenInset1(reference)

def mse(img, ref):
    return util.image.mean(util.image.luminance(util.image.squared_error(img, ref)))

def imgInset1(img):
    return util.image.lin_to_srgb(manage_images.glossyKitchenInset1(img))

def imgInset2(img):
    return util.image.lin_to_srgb(manage_images.glossyKitchenInset2(img))

# define figure data
data = {
    "img_width_px": len(a[0]),
    "img_height_px": len(a),
    "column_titles": {
        "north": { 
            "height": 4.8,
            "offset": 0.2,
            "rotation": 0,
            "fontsize": 7, 
            "line_space": 1.2,
            "text_color": [0,0,0],
            "content": 
            [r"\textbf{PT}\strut\\" + "${0:.2f}$\\strut".format(mse(first, reference)),
             r"\textbf{BDPT}\strut\\"+"${0:.2f}$\\strut".format(mse(second, reference)),
             "\\textbf{VCM+MLT}\\strut\\\\"+"${0:.2f}$\\strut".format(mse(third, reference)),
             "\\textbf{M\\\"uller et al.}\\strut\\\\"+"${0:.2f}$\\strut".format(mse(fourth, reference)),
             "\\textbf{Ours}\\strut\\\\"+"${0:.2f}$\\strut".format(mse(fifth, reference)),
             "\\textbf{Reference}\\strut\\\\-\\strut"
            ]
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
                "image": imgInset1(first),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": imgInset1(second),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": imgInset1(third),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": imgInset1(fourth),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": imgInset1(fifth),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": imgInset1(reference),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            }
        ],
        [
            {
                "image": imgInset2(first),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": imgInset2(second),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": imgInset2(third),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": imgInset2(fourth),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": imgInset2(fifth),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": imgInset2(reference),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            }
        ]  
    ],
    "num_rows": 2,
    "num_columns": 6
}
# TODO num rows and columns are not calculated, but should be, because it will be less work for the user
