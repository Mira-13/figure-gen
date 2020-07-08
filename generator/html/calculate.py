import json

class Error(Exception):
    def __init__(self, message):
        self.message = message

def pt_to_mm(x):
    return x * 0.352778

def relative_position(img_width_px, img_height_px, img_used_width, img_used_height):
    width_factor = img_used_width * 1/img_width_px 
    height_factor = img_used_height * 1/img_height_px
    return width_factor, height_factor

def size_of(data_part, direction):
    try:
        data_part[direction]
    except:
        raise Error("Incorrect usage of 'padding_of' function. First and second argument are not combineable.")

    if direction == 'north' or direction == 'south':
        return _get_size(data_part[direction]['height'], data_part[direction]['offset'])
    elif direction == 'east' or direction == 'west':
        return _get_size(data_part[direction]['width'], data_part[direction]['offset'])
    else:
        raise Error("Error: Invalid direction value: " + direction +". (html module)")

def _get_size(space, offset):
    if space == 0.0:
        return 0.0, 0.0
    return space, offset # TODO refactor: use named values (dict or class)

def img_pos(data, column, row):
    '''
    Note: this does not include element captions, yet. Because it was never really used in tikz or elsewhere.
    '''
    img_width  = data['element_config']['img_width']
    img_height = data['element_config']['img_height']

    title_top = sum(size_of(data['titles'], 'north'))
    title_left = sum(size_of(data['titles'], 'west'))
    col_title_top = sum(size_of(data['column_titles'], 'north'))
    row_title_left = sum(size_of(data['row_titles'], 'west'))

    top = data['padding']['north'] + title_top + col_title_top + (data['row_space'] + data['element_config']['img_height'])*(row-1)
    left =  data['padding']['west'] + title_left + row_title_left + (data['column_space'] + data['element_config']['img_width'])*(column-1)
    return top, left

def titles_pos_and_size(data, direction):
    '''
    Note: this does not include element captions, yet. Because it was never really used in tikz or elsewhere.
    '''
    offset_left = data['padding']['west']
    offset_top =  data['padding']['north']

    if direction == 'north' or direction == 'south':
        width = data['element_config']['img_width'] * data['num_columns'] + data['column_space']*(data['num_columns'] - 1)
        height = size_of(data['titles'], direction)[0]

        offset_left += sum(size_of(data['titles'], 'west')) + sum(size_of(data['row_titles'], 'west'))
        if direction == 'south':
            offset_top += data['padding']['north'] + sum(size_of(data['titles'], 'north')) + sum(size_of(data['column_titles'], 'north'))
            offset_top += (data['row_space']*(data['num_rows'] - 1)) + data['element_config']['img_height'] * data['num_rows']
            offset_top += sum(size_of(data['column_titles'], 'south')) + size_of(data['titles'], 'south')[1]
       
        position = [offset_top, offset_left]
        size = [width, height]
        return position, size 

    elif direction == 'east' or direction == 'west':
        height = data['element_config']['img_height'] * data['num_rows'] + data['row_space']*(data['num_rows'] - 1)
        width = size_of(data['titles'], direction)[0]

        offset_top += sum(size_of(data['titles'], 'north'))
        if direction == 'east':
            offset_left += sum(size_of(data['titles'], 'west')) + sum(size_of(data['row_titles'], 'west'))
            offset_left += (data['column_space']*(data['num_columns'] - 1)) + data['element_config']['img_width'] * data['num_columns']
            offset_left += sum(size_of(data['row_titles'], 'east')) + size_of(data['titles'], 'east')[1]

        position = [offset_top, offset_left]
        size = [width, height]
        return position, size
    
    else:
        raise Error("Error: Invalid direction value: " + direction +". (html module)")

def row_titles_pos(data, cur_row, direction):
    '''
    Note: this does not include element captions, yet. Because it was never really used in tikz or elsewhere.
    '''
    if not(direction == 'east' or direction == 'west'):
        raise Error("Error: Invalid direction value for row titles: " + direction +". Expected 'east' or 'west'.")

    width = size_of(data['row_titles'], direction)[0]
    height = data['element_config']['img_height']

    offset_left = data['padding']['west'] + sum(size_of(data['titles'], 'west'))
    offset_top = data['padding']['north'] + sum(size_of(data['titles'], 'north')) + sum(size_of(data['column_titles'], 'north'))
    offset_top += (data['row_space'] + data['element_config']['img_height']) * (cur_row - 1)
    if direction == 'east':
        offset_left += sum(size_of(data['row_titles'], 'west')) 
        offset_left += (data['column_space']*(data['num_columns'] - 1)) + data['element_config']['img_width'] * data['num_columns']
        offset_left += size_of(data['row_titles'], 'east')[1]

    position = [offset_top, offset_left]
    size = [width, height]
    return position, size

def column_titles_pos(data, cur_column, direction):
    '''
    Note: this does not include element captions, yet. Because it was never really used in tikz or elsewhere.
    '''
    if not(direction == 'north' or direction == 'south'):
        raise "Error: Invalid direction value for column titles: " + direction +". Expected 'north' or 'south'."

    width = data['element_config']['img_width']
    height = size_of(data['column_titles'], direction)[0]

    offset_top = data['padding']['north'] + sum(size_of(data['titles'], 'north'))
    offset_left = data['padding']['west'] + sum(size_of(data['row_titles'], 'west'))
    offset_left += (data['column_space'] + data['element_config']['img_width']) *(cur_column - 1)
    if direction == 'south':
        offset_top += sum(size_of(data['column_titles'], 'north'))
        offset_top += (data['row_space']*(data['num_rows'] - 1)) + data['element_config']['img_height'] * data['num_rows']
        offset_top += size_of(data['column_titles'], 'south')[1]

    position = [offset_top, offset_left]
    size = [width, height]
    return position, size