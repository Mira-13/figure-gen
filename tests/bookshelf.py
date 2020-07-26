import generator
import generator.util
import os
import pyexr
import json
import numpy as np

idx = 2
scene = ['bookshelf', 'glossy-kitchen', 'pool', 'veach-door'] #'bookshelf'
seconds = [120, 90, 60, 60] #120
baseline = 2
method_list = ['path', 'upsmcmc', 'radiance', 'full', None]
method_titles = ['PT', 'VCM+MLT', 'Müller et al.', 'Ours', 'Reference'] # LaTeX 'M\\\"uller et al.'
xticks = [
    [3, 20, s] for s in seconds
    ]
vline_positions = [
    (28.32, 28.78),
    (19.92, 20.23),
    (11.44, 11.17),
    (13.97, 18.62)
    ]
# left, top, width, height
crops = [
    [[369, 191, 40, 30], [238, 108, 40, 30]],
    [[100, 120, 40, 30], [212, 325, 40, 30]],
    [[400, 120, 40, 30], [595, 81, 40, 30]],
    [[246, 268, 40, 30], [504, 65, 40, 30]]
]

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

def get_image_crops(scene, seconds, method_list, crop_args_list):
    '''
    crop_args_list: list of [left, top, width, height]
    '''
    return  [ 
                [ 
                    get_image(scene, seconds, method, crop_args) for method in method_list
                ] for crop_args in crop_args_list
            ]

def get_error(scene, method, seconds, metric='MRSE*'):
    p = os.path.join('errors', scene, scene+'__'+method+'.json')
    with open(p) as json_file:
        data = json.load(json_file)
    idx = data['timesteps'].index(seconds)
    error = data['data'][idx][metric]
    return round(error, 8)

def get_captions(scene, method_titles, baseline, seconds):
    i = 0
    captions = []
    errors = [ get_error(scene, method, seconds) for method in method_list[:-1] ]

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

def get_content(scene, method_titles, baseline, seconds):
    return { 
        "text_color": [0,0,0],
        "background_colors": [ 
            [232, 181, 88],
            [5, 142, 78],
            [94, 163, 188],
            [181, 63, 106], 
            [255, 255, 255]
        ],
        "content": get_captions(scene, method_titles, baseline, seconds)
    }

def get_grid_elements(scene, seconds, method_list, crop_args):
    image_crops = get_image_crops(scene, seconds, method_list, crop_args)
    return [ 
        [ 
            {
                "image": img,
            } for img in imgs 
        ] for imgs in image_crops
    ]

def get_ref_element(scene, seconds, crop_args):
    '''
    crop_args: [[left, top, width, height], 
                [left, top, width, height]]
    '''
    return [ # rows
            [ # first row
                {
                    "image": get_image(scene, seconds, method=None, crop_args=None),
                    "crop_marker": {
                        "line_width": 0.6, "dashed": False, 
                        "list": [
                                { "pos": [crop[0], crop[1]], "size": [crop[2], crop[3]], "color": [242, 113, 0] } for crop in crop_args
                            ]
                    }
                }
            ] # end first row
           ]

g_column_titles = {
    "south": get_content(scene[idx], method_titles, baseline, seconds[idx])
}

titles = {
    "north": "",
    "south": scene[idx].replace('-',' ').title(),
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

def get_plot_data(scene, method_list):
    return [
        load_error(scene, method, metric='MRSE*', clip=True) for method in method_list[:-1]
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

def get_axis_properties(xticks):
    return {
        "x": {
            "range": [2.5, 800],
            "ticks": xticks,
            "use_log_scale": True,
            "use_scientific_notations": False
        },
        "y": {
            "ticks": [0.01, 0.1, 1.0],
            "use_log_scale": True,
            "use_scientific_notations": False
        }
    }

def get_vertical_lines(position_tupel):
    return {
        "vertical_lines": [
            {
                "pos": position_tupel[0],
                "color": [94, 163, 188],
                "linestyle": (0,(4,6)),
                "linewidth_pt": 0.6,
            },
            {
                "pos": position_tupel[1],
                "color": [181, 63, 106],
                "linestyle": (-5,(4,6)),
                "linewidth_pt": 0.6,
            }
        ]
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

modules = [
    { 
        "type": "grid",
        "elements": get_ref_element(scene[idx], seconds[idx], crops[idx]), 
        "row_titles": {}, 
        "column_titles": {}, 
        "titles": titles, 
        "layout": {
              "padding.east": 0.5,
              "padding.south": 0.1,
              "titles.south.height": 7,
              "titles.south.offset": 0.5,
              "titles.south.fontsize": 8
        }
    },
    { 
        "type": "grid",
        "elements": get_grid_elements(scene[idx], seconds[idx], method_list, crops[idx]), 
        "row_titles": {}, 
        "column_titles": g_column_titles, 
        "titles": titles, 
        "layout": {
              "padding.east": 0.5,
              "padding.south": 0.1,
              "column_titles.south.height": 7,
              "column_titles.south.offset": 0.5,
              "column_titles.south.fontsize": 8,

              "column_space": 0.8,
              "row_space": 0.8
        }
    },
    { 
        "type": "plot",
        "data": get_plot_data(scene[idx], method_list),
        "plot_color": plot_color,
        "axis_labels": axis_labels,
        "axis_properties": get_axis_properties(xticks=xticks[idx]),
        "markers": get_vertical_lines(vline_positions[idx]),
        "layout": {"width_to_height_aspect_ratio": 1.15}
    }
]

if __name__ == "__main__":
    generator.horizontal_figure(modules, width_cm=25., filename='siggraph2020/'+scene[idx]+'.pdf')
    generator.horizontal_figure(modules, width_cm=25., filename='siggraph2020/'+scene[idx]+'.pptx')
    generator.horizontal_figure(modules, width_cm=25., filename='siggraph2020/'+scene[idx]+'.html')
