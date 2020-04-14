# load images
reference = manage_images.vdoor60_ref
first = manage_images.vdoor60_patht
fourth = manage_images.vdoor60_radia
third = manage_images.vdoor60_upscmc
fifth = manage_images.vdoor60_ofull

# get an image for the resolution 
a = manage_images.veachDoorCrop1(reference)

def cropAndZoom(img, cropFn):
    crop = cropFn(img)
    return util.image.zoom(crop, scale=20)

def crop_1(img):
    global cropAndZoom
    zoomedCrop = cropAndZoom(img, manage_images.veachDoorCrop1)
    return util.image.lin_to_srgb(zoomedCrop)

def crop_2(img):
    zoomedCrop = cropAndZoom(img, manage_images.veachDoorCrop2)
    return util.image.lin_to_srgb(zoomedCrop)

def method_caption(name, image, rgbString):
    global reference
    #r"\definecolor{orangu}{rgb}{1,0.5,0}{\color{orangu}\hrule height 10pt}\vspace*{1pt}\textbf{PT}\strut\\" + "${0:.2f}$\\strut".format(util.image.relative_mse(first, reference)),
    c = r"{\definecolor{orangu}{rgb}" + rgbString + r"{\color{orangu}\hrule height 5pt}\vspace*{1pt}}"
    return c + "\\textbf{" + name + "}\n" + f"${util.image.relative_mse(image, reference):.3f}$"

def scale_and_convert_rgb(r,g,b, scale=255):
    r = round(r * 1/scale, 2)
    g = round(g * 1/scale, 2)
    b = round(b * 1/scale, 2)
    return '{'+str(r)+","+str(g)+","+ str(b)+'}'

# define figure data
data = { 
    "img_width_px": len(a[0]),
    "img_height_px": len(a),
    "column_titles": {
        "north": { 
            "height": 0.0,
            "offset": 0.2,
            "rotation": 0,
            "fontsize": 7, 
            "line_space": 1.2,
            "text_color": [0,0,0],
            "background_colors": [255, 255, 255],
            "content": 
            [r"\textbf{PT}\strut\\" + "${0:.2f}$\\strut".format(util.image.relative_mse(first, reference)),
             "\\textbf{VCM+MLT}\\strut\\\\"+"${0:.2f}$\\strut".format(util.image.relative_mse(third, reference)),
             "\\textbf{M\\\"uller et al.}\\strut\\\\"+"${0:.2f}$\\strut".format(util.image.relative_mse(fourth, reference)),
             "\\textbf{Ours}\\strut\\\\"+"${0:.2f}$\\strut".format(util.image.relative_mse(fifth, reference)),
             r"\textbf{Reference}\strut\\\emph{relMSE}\strut"
            ]
        },
        "south": {
            "height": 5.8,
            "offset": 0.5,
            "rotation": 0,
            "fontsize": 7, 
            "line_space": 1.2,
            "text_color": [0, 0, 0],
            "background_colors": [255, 255, 255],
            "content": 
            [
            method_caption('PT', first, scale_and_convert_rgb(232, 181, 88)),
            method_caption('VCM+MLT', third, scale_and_convert_rgb(5, 142, 78)),
            method_caption('M\\\"uller et al.', fourth, scale_and_convert_rgb(94, 163, 188)),
            method_caption('Ours', fifth, scale_and_convert_rgb(181, 63, 106)),
             r"\vspace*{6pt}\textbf{Reference}" + "\n" + r"\emph{relMSE}"
            ]
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
            "content": ["", "", "row c 3", "row d 4", "row e 5", "row f 6"]
        }
    },
    "elements_content": [
        [
            {
                "image": crop_1(first),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": crop_1(third),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": crop_1(fourth),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": crop_1(fifth),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": crop_1(reference),
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
                "image": crop_2(first),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": crop_2(third),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": crop_2(fourth),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": crop_2(fifth),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": crop_2(reference),
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
    "num_columns": 5
}
# TODO num rows and columns are not calculated, but should be, because it will be less work for the user
