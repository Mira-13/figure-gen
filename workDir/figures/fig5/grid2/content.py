# load images
scene='glossy-kitchen'
reference = manage_images.load_image(scene)
baseline = 2

names = ['PT', 'VCM+MLT', 'M\\\"uller et al.', 'Ours']
method_names = ['path', 'upsmcmc', 'radiance', 'full']
images = [
    manage_images.load_image(scene='glossy-kitchen', method=method_name) for method_name in method_names
]
colors = [
    [232, 181, 88],
    [5, 142, 78],
    [94, 163, 188],
    [181, 63, 106]
]
errors = [
    manage_images.get_error(scene='glossy-kitchen', method=method) for method in method_names
]

methods = zip(names, images, errors, colors)

# get an image for the resolution 
a = manage_images.get_cropped_img(scene, method=method_names[0], crop_num=0)

def perfect_cropped_srgb(img, crop_num, scene):
    crop_args = manage_images.get_crop_list(scene)[crop_num]
    cropped_img = manage_images.crop(img, crop_args[0], crop_args[1], crop_args[2], crop_args[3])
    zoomed = util.image.zoom(cropped_img, scale=20)
    return util.image.lin_to_srgb(zoomed)

global method_caption
def method_caption(name, image, error, rgb_list):
    global reference
    global baseline
    global errors
    global names
    #r"\definecolor{orangu}{rgb}{1,0.5,0}{\color{orangu}\hrule height 10pt}\vspace*{1pt}\textbf{PT}\strut\\" 
    vline_color = r"{\definecolor{orangu}{rgb}" + util.image.scale_and_convert_rgb(rgb_list) + r"{\color{orangu}\hrule height 2.5pt}\vspace*{2.5pt}}"
    
    if name == names[-1]: # if Ours then highlight
        title = "\\textsf{\\textbf{" + name + r"}}"
        speedup = "\\textsf{\\textbf{" + "("+ f"{errors[baseline] * 1./error:.1f}" + "x)" + r"}}"
    else:
        title = "\\textsf{"+name+"}\\textbf{ }"
        speedup = "\\textsf{("+ f"{errors[baseline] * 1./error:.1f}" + "x)}"
    relMSE = "\\textsf{"+f"{error:.3f}"+"}"
    if name == names[baseline]:
        speedup = "\\textsf{(baseline)}"
    return vline_color + title + "\n" + relMSE + "\\textbf{ }" + speedup

captions = [
    method_caption(name, image, error, colorcode) for (name, image, error, colorcode) in methods
]
captions.append(r"\vspace*{5.0pt}\textsf{Reference}\textbf{ }" + "\n" + r"\textsf{\emph{relMSE} ("+ str(manage_images.get_time_sec(scene='bookshelf')) +"s)}")

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
            [
            method_caption('PT', images[0], errors[0], [232, 181, 88]),
            method_caption('VCM+MLT', images[1], errors[1], [5, 142, 78]),
            method_caption('M\\\"uller et al.', images[2], errors[2], [94, 163, 188]),
            method_caption('Ours', images[3], errors[3], [181, 63, 106]),
             r"\vspace*{6pt}Reference" + "\n" + r"\emph{relMSE}"
            ]
        },
        "south": {
            "height": 7.0,
            "offset": 0.5,
            "rotation": 0,
            "fontsize": 7, 
            "line_space": 1.2,
            "text_color": [0, 0, 0],
            "background_colors": [255, 255, 255],
            "content": captions
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
            "background_colors": [[242, 113, 0], [0, 89, 186], [66, 180, 70], [231, 191, 78], [180, 55, 68], [210, 135, 38]],
            "content": ["", "", "row c 3", "row d 4", "row e 5", "row f 6"]
        }
    },
    "elements_content": [
        [
            {
                "image": perfect_cropped_srgb(images[0],0, scene),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": perfect_cropped_srgb(images[1],0, scene),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": perfect_cropped_srgb(images[2],0, scene),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": perfect_cropped_srgb(images[3],0, scene),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": perfect_cropped_srgb(reference,0, scene),
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
                "image": perfect_cropped_srgb(images[0],1, scene),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": perfect_cropped_srgb(images[1],1, scene),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": perfect_cropped_srgb(images[2],1, scene),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": perfect_cropped_srgb(images[3],1, scene),
                "north":"",
                "east": "",
                "south": "",
                "west": "",
                "frame": { "line_width": 0.0, "color": [100,100,100] },
                "insets": {"line_width": 0.0, "dashed": False, "list": []}
            },
            {
                "image": perfect_cropped_srgb(reference,1, scene),
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