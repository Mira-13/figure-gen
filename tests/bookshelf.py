import generator
import generator.util
import os
import pyexr
import json
import numpy as np

# load the two images
scene = 'bookshelf'
seconds = 120
baseline = 2
method_list = ['path', 'upsmcmc', 'radiance', 'full', None]
method_titles = ['PT', 'VCM+MLT', 'M\\\"uller et al.', 'Ours', 'Reference']

def get_image(scene, seconds, method=None, crop_args=None):
    if method is None:
        path = os.path.join('images', scene, scene+".exr")
    else:
        sec_string = '-'+str(seconds)+'s-'
        path = os.path.join('images', scene, scene+sec_string+method+".exr")

    img = pyexr.read(path)
    if crop_args is not None:
        img = generator.util.image.crop(img, crop_args)
        img = generator.util.image.zoom(img)
    return generator.util.image.lin_to_srgb(img)

# left, top, width, height
crops = [
    [369, 191, 40, 30], 
    [238, 108, 40, 30]
]

images_crop1 = [
    get_image(scene=scene, seconds=seconds, method=method, crop_args=crops[0]) for method in method_list
]
images_crop2 = [
    get_image(scene=scene, seconds=seconds, method=method, crop_args=crops[1]) for method in method_list
]

def get_error(scene, method, seconds, metric='MRSE*'):
    p = os.path.join('errors', scene, scene+'__'+method+'.json')
    with open(p) as json_file:
        data = json.load(json_file)
    idx = data['timesteps'].index(seconds)
    error = data['data'][idx][metric]
    return round(error, 8)

def get_captions(errors, method_titles, baseline, seconds):
    i = 0
    captions = []

    for method in method_titles[:-1]:
        relMSE = round(errors[i], 3)
        if i == baseline:
            speedup = '(baseline)'
        else:
            speedup = round(errors[baseline] * 1/relMSE, 1)
            speedup = '('+str(speedup)+'x)'

        string_caption = method + '\n' + str(relMSE) + ' ' + speedup
        captions.append(string_caption)
        i+=1

    captions.append('Reference'+'\n'+'relMSE ('+str(seconds)+'s)')
    return captions

errors = [
    get_error(scene=scene, method=method, seconds=seconds) for method in method_list[:-1]
]
errors_string = [
    str(e) for e in errors
]
errors_string.append('--')

captions = get_captions(errors, method_titles, baseline, seconds)

g_elements = [ # rows
    [ # first row
        {
            "image": images_crop1[0],
        },
        {
            "image": images_crop1[1],
        },
        {
            "image": images_crop1[2],
        },
        {
            "image": images_crop1[3],
        },
        {
            "image": images_crop1[4],
        },
    ], # end first row
    [
        {
            "image": images_crop2[0],
        },
        {
            "image": images_crop2[1],
        },
        {
            "image": images_crop2[2],
        },
        {
            "image": images_crop2[3],
        },
        {
            "image": images_crop2[4],
        },    
    ]
]

ref_elements = [ # rows
    [ # first row
        {
            "image": get_image(scene, seconds, method=None, crop_args=None),
            "crop_marker": {
                "line_width": .2, "dashed": False, 
                "list": [
                    { "pos": [crops[0][0],crops[0][1]], "size": [crops[0][2],crops[0][3]], "color": [242, 113, 0] },
                    { "pos": [crops[1][0],crops[1][1],1], "size": [crops[1][2],crops[1][3]], "color": [242, 113, 0] }
                ]
            }
        }
    ] # end first row
]

g_column_titles = {
    "south": { 
        "text_color": [0,0,0],
        "background_colors": [ 
            [232, 181, 88],
            [5, 142, 78],
            [94, 163, 188],
            [181, 63, 106], 
            [255, 255, 255]
        ],
        "content": captions
    }
}

titles = {
    "north": "",
    "south": scene.title(),
    "east": "",
    "west": ""
}
####### Begin PLOT Type #########

def load_error(scene, method, metric='MRSE*', clip=True):
    with open('errors/%s/%s__%s.json' % (scene, scene, method)) as json_file:
        data = json.load(json_file)
    
    x = data['timesteps']
    y = [ e[metric] for e in data['data'] ]
    
    si = 0
    x, y = x[si:], y[si:]
    
    rmin = 0
    ddx, ddy = [], []
    for i in range(len(y)):
        if i == 0 or (y[i-1] != y[i] and (not clip or y[i] < rmin)):
            ddx.append(x[i])
            ddy.append(y[i])# * x[i])
            rmin = y[i]
    
    return (ddx, ddy)

data = [
    load_error(scene=scene, method=method, metric='MRSE*', clip=True) for method in method_list[:-1]
]

plot_color = [ 
    [232, 181, 88],
    [5, 142, 78],
    [94, 163, 188],
    [181, 63, 106]
]

axis_labels = {
    "x": {
        "text": "Time [s]",
        "rotation": "horizontal"
    },
    "y": {
        "text": "Error\n[relMSE]",
        "rotation": "vertical"
    }
}

axis_properties = {
    "x": {
        "range": [2.5, 800],
        "ticks": [3, 20, 120],
        "use_log_scale": True,
        "use_scientific_notations": False
    },
    "y": {
        "ticks": [0.01, 0.1, 1.0],
        "use_log_scale": True,
        "use_scientific_notations": False
    }
}

markers = {
    "vertical_lines": [
        {
            "pos": 28.32,
            "color": [94, 163, 188],
            "linestyle": (0,(4,6)),
            "linewidth_pt": 0.6,
        },
        {
            "pos": 28.78,
            "color": [181, 63, 106],
            "linestyle": (-5,(4,6)),
            "linewidth_pt": 0.6,
        }
    ]
}

############################

modules = [
    { 
        "type": "grid",
        "elements": ref_elements, 
        "row_titles": {}, 
        "column_titles": {}, 
        "titles": titles, 
        "layout": {
              "padding.right": 0.5,
              "padding.bottom": 0.1,
              "titles.south.height": 7,
              "titles.south.offset": 0.5,
              "titles.south.fontsize": 7
        }
    },
    { 
        "type": "grid",
        "elements": g_elements, 
        "row_titles": {}, 
        "column_titles": g_column_titles, 
        "titles": titles, 
        "layout": {
              "padding.right": 0.5,
              "padding.bottom": 0.1,
              "padding.top": 0.0,
              "column_titles.south.height": 7,
              "column_titles.south.offset": 0.5,
              "column_titles.south.fontsize": 7,

              "column_space": 0.8,
              "row_space": 0.8
        }
    },
    { 
        "type": "plot",
        "data": data,
        "plot_color": plot_color,
        "axis_labels": axis_labels,
        "axis_properties": axis_properties,
        "markers": markers,
        "layout": {}
    }
]

if __name__ == "__main__":
    generator.horizontal_figure(modules, width_cm=18., backend='tikz', out_dir=".")
    generator.horizontal_figure(modules, width_cm=18., backend='pptx', out_dir=".")
    generator.horizontal_figure(modules, width_cm=18., backend='html', out_dir=".")
