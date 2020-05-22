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
    try:
        data_part[direction]
    except:
        raise "Incorrect usage of 'padding_of' function. First and second argument are not combineable."

    if direction == 'north' or direction == 'south':
        return get_padding(data_part[direction]['height'], data_part[direction]['offset'])
    elif direction == 'east' or direction == 'west':
        return get_padding(data_part[direction]['width'], data_part[direction]['offset'])
    else:
        raise "Error: Invalid direction value: " + direction +". (slide_pptx module)"

def get_padding(space, offset):
    if space == 0.0:
        return [0.0, 0.0]
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

def titles_pos_for_slide(data, direction, factor, offset_left_mm=0.0, offset_top_mm=0.0):
    '''
    Note: this does not include element captions, yet. Because it was never really used in tikz or elsewhere.
    '''
    offset_left = offset_left_mm + data['padding']['left']
    offset_top = offset_top_mm + data['padding']['top']

    if direction == 'north' or direction == 'south':
        offset_left += sum(padding_of(data['titles'], 'west')) + sum(padding_of(data['row_titles'], 'west'))
        width = data['element_config']['img_width'] * data['num_columns'] + data['column_space']*(data['num_columns'] - 1)
        height = padding_of(data['titles'], direction)[0]
        if direction == 'south':
            offset_top += data['padding']['top'] + sum(padding_of(data['titles'], 'north')) + sum(padding_of(data['column_titles'], 'north'))
            offset_top += (data['row_space']*(data['num_rows'] - 1)) + data['element_config']['img_height'] * data['num_rows']
            offset_top += sum(padding_of(data['column_titles'], 'south')) + padding_of(data['titles'], 'south')[1]
        
        position = [mm_to_inch(offset_top) * factor, mm_to_inch(offset_left) * factor]
        size = [mm_to_inch(width) * factor, mm_to_inch(height) * factor]
        return position, size 

    elif direction == 'east' or direction == 'west':
        offset_top += sum(padding_of(data['titles'], 'north'))
        height = data['element_config']['img_height'] * data['num_rows'] + data['row_space']*(data['num_rows'] - 1)
        width = padding_of(data['titles'], direction)[0]
        if direction == 'east':
            offset_left += sum(padding_of(data['titles'], 'west')) + sum(padding_of(data['row_titles'], 'west'))
            offset_left += (data['column_space']*(data['num_columns'] - 1)) + data['element_config']['img_width'] * data['num_columns']
            offset_left += sum(padding_of(data['row_titles'], 'east')) + padding_of(data['titles'], 'east')[1]

        position = [mm_to_inch(offset_top) * factor, mm_to_inch(offset_left) * factor]
        size = [mm_to_inch(width) * factor, mm_to_inch(height) * factor]
        return position, size
    
    else:
        raise "Error: Invalid direction value: " + direction +". (slide_pptx module)"

def row_titles_pos_for_slide(data, direction, factor):
    pass # TODO

def column_titles_pos_for_slide(data, direction, factor):
    pass # TODO