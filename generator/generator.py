import json
import numpy
import os
import copy
import imageio
import shutil
#from skimage import img_as_ubyte

from .tex import make_tex, calculate, combine_pdfs
from .slide_pptx import make_pptx
from .html import make_html
from . import default_layouts

backends = {
    "tikz": make_tex,
    "pptx": make_pptx,
    "html": make_html
}

def png_export(img_raw, filename):
    clipped = numpy.clip(0, 255, img_raw * 255).astype('uint8')
    imageio.imwrite(filename, clipped)

def overwrite(name: list, val, layout: dict):
    if len(name) == 1:
        layout[name[0]] = val
        return
    overwrite(name[1:], val, layout[name[0]])

def replace_option(name: str, val, layout: dict):
    # first.second.third -> [ first, second, third ]
    path = name.split(sep='.')
    overwrite(path, val, layout)

def modify_default_layout(user: dict, type: str):
    default = copy.deepcopy(default_layouts.layouts[type])

    for key,val in user.items():
        replace_option(key, val, default)

    return default

def merge_plot_data_into_layout(data, layout):
    layout['type'] = data['type']
    layout["data"] = data['data']
    layout["plot_color"] = data['plot_color']
    layout["axis_labels"] = data['axis_labels']
    layout["axis_properties"] = data['axis_properties']
    layout["markers"] = data['markers']
    return layout

def merge_data_into_layout(data, layout):
    layout['type'] = data['type']
    directions = ["north", "south", "east", "west"]

    num_rows = len(data["elements"])
    num_cols = len(data["elements"][0])
    layout['num_rows'] = num_rows
    layout['num_columns'] = num_cols

    # initialize empty matrix for elements
    layout["elements_content"] = [[{} for i in range(num_cols)] for i in range (num_rows)]

    for row in range(num_rows):
        for col in range(num_cols):
            elem = layout["elements_content"][row][col]
            data_elem = data["elements"][row][col]

            try:
                elem["label"] = data_elem["label"]
            except KeyError:
                pass

            # copy captions, if set
            for d in directions:
                try:
                    caption = data_elem["captions"][d]
                except:
                    caption = ""
                elem[d] = caption

            # add frame from user (optional, default: no frame)
            try:
                frame = data_elem["frame"]
            except: # do not set the frame
                frame = None
            if frame is not None: elem["frame"] = frame

            # add crop marker (optional, default: no marker)
            try:
                marker = data_elem["crop_marker"]
            except: # do not set marker
                marker = None
            if marker is not None: elem["marker"] = marker

            # add the image data itself (raw): matrix of rgb
            # assert ((data_elem["image"]).shape[2] == 3)
            elem["filename"] = data_elem["image"]


    # add column_titles
    for d in ['north', 'south']:
        # change text color
        try:
            layout["column_titles"][d]["text_color"] = data["column_titles"][d]["text_color"]
        except: # keep default
            pass

        # change background color of column text field
        try:
            layout["column_titles"][d]["background_colors"] = data["column_titles"][d]["background_colors"]
        except: # keep default: [0,0,0]
            pass

        # add content
        try:
            layout["column_titles"][d]["content"] = data["column_titles"][d]["content"]
        except: # set default: list of empty strings
            layout["column_titles"][d]["content"] = [""] * num_cols

    # add row_titles
    for d in ['east', 'west']:
        # change text color
        try:
            layout["row_titles"][d]["text_color"] = data["row_titles"][d]["text_color"]
        except: # keep default
            pass

        # change background color of column text field
        try:
            layout["row_titles"][d]["background_colors"] = data["row_titles"][d]["background_colors"]
        except: # keep default: [0,0,0]
            pass

        # add text-based content
        try:
            layout["row_titles"][d]["content"] = data["row_titles"][d]["content"]
        except: # set default: list of empty strings
            layout["row_titles"][d]["content"] = [""] * num_rows

    # titles
    for d in directions:
        # add text-based content
        try:
            layout['titles'][d]['content'] = data['titles'][d]
        except: # set default: empty string
            layout['titles'][d]['content'] = ''

    # set px size based on the first image
    try:
        first = layout["elements_content"][0][0]["filename"][0]["image"]
    except:
        first = layout["elements_content"][0][0]["filename"]
    layout["img_width_px"] = first.shape[1]
    layout["img_height_px"] = first.shape[0]
    return layout

def merge(modules: dict, layouts: dict):
    merged_dicts = []
    for i in range(len(modules)):
        if modules[i]['type'] == 'plot':
            merged_dicts.append(merge_plot_data_into_layout(modules[i], layouts[i]))
        else:
            merged_dicts.append(merge_data_into_layout(modules[i], layouts[i]))
    return merged_dicts


def align_modules(modules, width):
    num_modules = len(modules)
    assert(num_modules!=0)

    if num_modules == 1:
        modules[0]["total_width"] = width
        if modules[0]["type"] == "grid":
            calculate.resize_to_match_total_width(modules[0])
            modules[0]['total_height'] = calculate.get_total_height(modules[0])
        elif modules[0]['type'] == 'plot':
            modules[0]['total_height'] = width / modules[0]['width_to_height_aspect_ratio']
        else:
            pass
        return

    sum_inverse_aspect_ratios = 0
    inverse_aspect_ratios = []
    for m in modules:
        if m["type"] == "grid":
            image_aspect_ratio = m['img_height_px'] / float(m['img_width_px'])
            a = m['num_rows'] / float(m['num_columns']) * image_aspect_ratio
        elif m["type"] == "plot":
            a = 1 / m['width_to_height_aspect_ratio']
        else:
            raise "unsupported module type '" + m['type'] + "'"
        sum_inverse_aspect_ratios += 1/a
        inverse_aspect_ratios.append(1/a)

    sum_fixed_deltas = 0
    i = 0
    for m in modules:
        if m["type"] == "grid":
            w_fix = calculate.get_min_width(m)
            h_fix = calculate.get_min_height(m)
        else:
            w_fix = 0
            h_fix = 0
        sum_fixed_deltas += w_fix - h_fix * inverse_aspect_ratios[i]
        i += 1

    height = (width - sum_fixed_deltas) / sum_inverse_aspect_ratios

    for m in modules:
        m['total_height'] = height
        if m["type"] == "grid":
            calculate.resize_to_match_total_height(m)
            m['total_width'] = calculate.get_total_width(m)
        elif m['type'] == 'plot':
            m['total_width'] = height * m['width_to_height_aspect_ratio']
        else:
            pass

def export_raw_img_to_png(module, module_idx, path):
    if module['type'] != 'grid':
        return

    for row in range(module["num_rows"]):
        for col in range(module["num_columns"]):
            elem = module["elements_content"][row][col]

            # the element can be either a list of multiple images, or one image
            try:
                file = elem["filename"][0]["image"]
                is_multi = True
            except:
                is_multi = False

            if is_multi:
                for i in range(len(elem["filename"])):
                    img_raw = elem["filename"][i]["image"]
                    filename = 'image-'+str(row+1)+'-'+str(col+1) + '-' + str(i+1) + '-' + str(module_idx+1)+'.png'
                    file_path = os.path.join(path, filename)
                    png_export(img_raw, file_path)
                    elem["filename"][i]["image"] = file_path
            else:
                img_raw = elem["filename"]
                filename = 'image-'+str(row+1)+'-'+str(col+1) + '-' + str(module_idx+1)+'.png'
                file_path = os.path.join(path, filename)
                png_export(img_raw, file_path)
                elem["filename"] = file_path

def get_out_dir_and_backend(filename):
    # Select the correct backend based on the filename
    extension = os.path.splitext(filename)[1].lower()
    if extension == ".pptx":
        backend = 'pptx'
    elif extension == ".html":
        backend = 'html'
    elif extension == ".pdf":
        backend = 'tikz'
    else:
        raise ValueError(f"Could not derive backend from filename '{filename}'")
    out_dir = os.path.dirname(filename)
    return out_dir, backend, extension

def horizontal_figure(modules, width_cm: float, filename):
    """
    Creates a figure by putting modules next to each other, from left to right.
    Aligns the height of the given modules such that they fit the given total width.

    Args:
        modules: a list of dictionaries, one for each module
        backend: can be one of: 'tikz', 'pptx', 'html'
        out_dir: path to the folder that will contain the generated figure and data
    """

    out_dir, backend, extension = get_out_dir_and_backend(filename)

    layouts = []
    for m in modules:
        layouts.append(modify_default_layout(m['layout'], m['type']))

    merged_data = merge(modules, layouts)
    align_modules(merged_data, width_cm*10.)

    # All .pngs for a "/a/b/figure.pdf" are in a folder "/a/b/figure_images"
    image_path, _ = os.path.splitext(filename)
    image_path += "_images"
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    # Export all .png images
    generated_data = []
    for i in range(len(modules)):
        if merged_data[i]['type'] != 'plot':
            export_raw_img_to_png(merged_data[i], module_idx=i, path=image_path)
        generated_data.append(backends[backend].generate(merged_data[i], to_path=out_dir, index=i))

    backends[backend].combine(generated_data, filename)

    # TODO delete the image folder iff the backend is tikz and the .tex files are deleted, too
