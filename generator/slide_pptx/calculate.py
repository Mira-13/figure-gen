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

def padding_of(data_part, direction):
    if direction == 'north' or direction == 'south':
        return get_padding(data_part[direction]['height'], data_part[direction]['offset'])
    elif direction == 'east' or direction == 'west':
        return get_padding(data_part[direction]['width'], data_part[direction]['offset'])
    else:
        raise "Error: Invalid direction value: " + direction +". (slide_pptx module)"

def get_padding(space, offset):
    if space == 0.0:
        return [0., 0.]
    return [space, offset]

def img_pos_for_slide(data, column, row, factor, offset_left_mm=0.0, offset_top_mm=0.0):
    '''
    Note: this does not include element captions, yet. Because it was never really used in tikz or elsewhere.
    '''
    img_width, img_height = img_size_inches(data, factor)
    title_top = sum(padding_of(data['titles'], 'north'))
    title_left = sum(padding_of(data['titles'], 'west'))
    col_title_top = sum(padding_of(data['column_titles'], 'north'))
    row_title_left = sum(padding_of(data['row_titles'], 'west'))
    top = offset_top_mm + data['padding']['top'] + title_top + col_title_top + (data['row_space'] + data['element_config']['img_height'])*(row-1)
    left = offset_left_mm + data['padding']['left'] + title_left + row_title_left + (data['column_space'] + data['element_config']['img_width'])*(column-1)
    return mm_to_inch(top) * factor, mm_to_inch(left) * factor
