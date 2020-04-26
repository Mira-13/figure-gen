import json
from .tex import make_tex
import os
#from .pptx import make_pptx

backends = {
    "tikz": make_tex,
    "pptx": None, #make_pptx,
    "html": None,
    "sdl2": None
}

def overwrite(name: list, val, layout: dict):
    if len(name) == 1:
        layout[name[0]] = val
        return
    overwrite(name[1:], val, layout[name[0]])

def replace_option(name: str, val, layout: dict):
    # first.second.third -> [ first, second, third ]
    path = name.split(sep='.')
    overwrite(path, val, layout)

def modify_default_layout(layout_filename: str):
    with open(layout_filename) as json_file:
        user = json.load(json_file)

    default_filename = os.path.join(os.path.dirname(__file__), "default_layout.json")
    with open(default_filename) as json_file:
        default = json.load(json_file)

    for key,val in user.items():
        replace_option(key, val, default)

    return default

def merge_data_into_layout(data, layout):
    directions = ["north", "south", "east", "west"]

    num_rows = len(data["elements"])
    num_cols = len(data["elements"][0])

    # merge the captions of each element
    for d in directions:
        # initialize the captions to a matrix of empty strings
        elem = layout["element_config"]["captions"][d]
        elem["content"] = [[""] * num_cols] * num_rows

        # replace the empty strings if there is a value from the user
        for row in range(num_rows):
            for col in range(num_cols):
                try:
                    elem["content"][row][col] = data["elements"][row][col]["captions"][d]
                except: # keep the default (empty string)
                    pass
    
    # merge the frame

    # merge the crop marker

    # merge the image data itself (raw)

def merge(modules: dict, layouts: dict):
    for i in range(len(modules)):
        merge_data_into_layout(modules[i], layouts[i])

def align_modules(layouts):
    pass

def horizontal_figure(modules: dict, backend: str):
    layouts = []
    for m in modules:
        layouts.append(modify_default_layout(m['layout']))

    merge(modules, layouts)
    align_modules(layouts)

    for i in range(len(modules)):
        backends[backend].generate(modules[i], layouts[i])