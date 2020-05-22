import json

def mm_to_inch(x):
    return x * 0.0393701 

def width_factor(slide_cm_width, figure_cm_width):
    slide_inch = mm_to_inch(slide_cm_width*10.)
    figure_inch = mm_to_inch(figure_cm_width*10.)
    return slide_inch / figure_inch

def img_size_inches(data, factor):
    w = data['element_config']['img_width']
    h = data['element_config']['img_height']
    return mm_to_inch(w) * factor, mm_to_inch(h) * factor

def get_padding(space, offset):
    if space == 0.0:
        return 0.0
    return space + offset

def img_pos_for_slide(data, column, row, factor, offset_left_mm=0.0, offset_top_mm=0.0):
    img_width, img_height = img_size_inches(data, factor)
    title_top = get_padding(data['titles']['north']['height'], data['titles']['north']['offset'])
    title_left = get_padding(data['titles']['west']['width'], data['titles']['west']['offset'])
    col_title_top = get_padding(data['column_titles']['north']['height'], data['column_titles']['north']['offset'])
    row_title_left = get_padding(data['row_titles']['west']['width'], data['row_titles']['west']['offset'])
    top = offset_top_mm + data['padding']['top'] + title_top + col_title_top + (data['row_space'] + data['element_config']['img_height'])*(row-1)
    left = offset_left_mm + data['padding']['left'] + title_left + row_title_left + (data['column_space'] + data['element_config']['img_width'])*(column-1)
    return mm_to_inch(top) * factor, mm_to_inch(left) * factor
