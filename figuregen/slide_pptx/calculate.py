class Error(Exception):
    def __init__(self, message):
        self.message = message

def mm_to_inch(x):
    return x * 0.0393701

def pt_to_inch(x):
    return x * 0.0138889

def relative_position(img_width_px, img_height_px, img_used_width, img_used_height):
    width_factor = img_used_width * 1/img_width_px 
    height_factor = img_used_height * 1/img_height_px
    return width_factor, height_factor

def img_size_inches(data, factor):
    w = data['element_config']['img_width']
    h = data['element_config']['img_height']
    return mm_to_inch(w) * factor, mm_to_inch(h) * factor

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
        raise Error("Error: Invalid direction value: " + direction +". (slide_pptx module)")

def _get_size(space, offset):
    if space == 0.0:
        return 0.0, 0.0
    return space, offset # TODO refactor: use named values (dict or class)

def img_pos(data, column, row, factor, offset_left_mm=0.0, offset_top_mm=0.0):
    '''
    Note: this does not include element captions, yet. Because it was never really used in tikz or elsewhere.
    Except for south titles! #new
    '''
    title_top = sum(size_of(data['titles'], 'north'))
    title_left = sum(size_of(data['titles'], 'west'))
    col_title_top = sum(size_of(data['column_titles'], 'north'))
    row_title_left = sum(size_of(data['row_titles'], 'west'))
    img_south_capt = sum(size_of(data['element_config']['captions'], 'south')) * (row-1) #new
    top = offset_top_mm + data['padding']['north'] + title_top + col_title_top + (data['row_space'] + data['element_config']['img_height'])*(row-1) + img_south_capt #new
    left = offset_left_mm + data['padding']['west'] + title_left + row_title_left + (data['column_space'] + data['element_config']['img_width'])*(column-1)
    return mm_to_inch(top) * factor, mm_to_inch(left) * factor

def south_caption_pos(data, column, row, factor, offset_left_mm=0.0, offset_top_mm=0.0):
    offset_top_mm += data['element_config']['img_height'] + data['element_config']['captions']['south']['offset'] #new
    return img_pos(data, column, row, factor, offset_left_mm, offset_top_mm)

def titles_pos(data, direction, factor, offset_left_mm=0.0, offset_top_mm=0.0):
    '''
    Note: this does not include element captions, yet. Because it was never really used in tikz or elsewhere.
    Except for south titles! #new
    '''
    offset_left = offset_left_mm + data['padding']['west']
    offset_top = offset_top_mm + data['padding']['north']

    if direction == 'north' or direction == 'south':
        width = data['element_config']['img_width'] * data['num_columns'] + data['column_space']*(data['num_columns'] - 1)
        height = size_of(data['titles'], direction)[0]

        offset_left += sum(size_of(data['titles'], 'west')) + sum(size_of(data['row_titles'], 'west'))
        if direction == 'south':
            offset_top += sum(size_of(data['element_config']['captions'], 'south')) * data['num_rows'] #new
            offset_top += data['padding']['north'] + sum(size_of(data['titles'], 'north')) + sum(size_of(data['column_titles'], 'north'))
            offset_top += (data['row_space']*(data['num_rows'] - 1)) + data['element_config']['img_height'] * data['num_rows']
            offset_top += sum(size_of(data['column_titles'], 'south')) + size_of(data['titles'], 'south')[1]
        
        position = [mm_to_inch(offset_top) * factor, mm_to_inch(offset_left) * factor]
        size = [mm_to_inch(width) * factor, mm_to_inch(height) * factor]
        return position, size 

    elif direction == 'east' or direction == 'west':
        height = data['element_config']['img_height'] * data['num_rows'] + data['row_space']*(data['num_rows'] - 1)
        height += sum(size_of(data['element_config']['captions'], 'south')) * (data['num_rows'] -1) #new
        width = size_of(data['titles'], direction)[0]

        offset_top += sum(size_of(data['titles'], 'north'))
        offset_top += sum(size_of(data['column_titles'], 'north'))
        if direction == 'east':
            offset_left += sum(size_of(data['titles'], 'west')) + sum(size_of(data['row_titles'], 'west'))
            offset_left += (data['column_space']*(data['num_columns'] - 1)) + data['element_config']['img_width'] * data['num_columns']
            offset_left += sum(size_of(data['row_titles'], 'east')) + size_of(data['titles'], 'east')[1]

        position = [mm_to_inch(offset_top) * factor, mm_to_inch(offset_left) * factor]
        size = [mm_to_inch(width) * factor, mm_to_inch(height) * factor]
        return position, size
    
    else:
        raise Error("Error: Invalid direction value: " + direction +". (slide_pptx module)")


def row_titles_pos(data, cur_row, direction, factor, offset_left_mm=0.0, offset_top_mm=0.0):
    '''
    Note: this does not include element captions, yet. Because it was never really used in tikz or elsewhere.
    '''
    if not(direction == 'east' or direction == 'west'):
        raise Error("Error: Invalid direction value for row titles: " + direction +". Expected 'east' or 'west'.")

    width = size_of(data['row_titles'], direction)[0]
    height = data['element_config']['img_height']

    offset_left = offset_left_mm + data['padding']['west'] + sum(size_of(data['titles'], 'west'))
    offset_top = offset_top_mm + data['padding']['north'] + sum(size_of(data['titles'], 'north')) + sum(size_of(data['column_titles'], 'north'))
    offset_top += (data['row_space'] + data['element_config']['img_height']) * (cur_row - 1)
    offset_top += sum(size_of(data['element_config']['captions'], 'south')) * (cur_row-1) #new
    if direction == 'east':
        offset_left += sum(size_of(data['row_titles'], 'west')) 
        offset_left += (data['column_space']*(data['num_columns'] - 1)) + data['element_config']['img_width'] * data['num_columns']
        offset_left += size_of(data['row_titles'], 'east')[1]

    position = [mm_to_inch(offset_top) * factor, mm_to_inch(offset_left) * factor]
    size = [mm_to_inch(width) * factor, mm_to_inch(height) * factor]
    return position, size

def column_titles_pos(data, cur_column, direction, factor, offset_left_mm=0.0, offset_top_mm=0.0):
    '''
    Note: this does not include element captions, yet. Because it was never really used in tikz or elsewhere.
    Except for south captions! #new
    '''
    if not(direction == 'north' or direction == 'south'):
        raise "Error: Invalid direction value for column titles: " + direction +". Expected 'north' or 'south'."

    width = data['element_config']['img_width']
    height = size_of(data['column_titles'], direction)[0]

    offset_top = offset_top_mm + data['padding']['north'] + sum(size_of(data['titles'], 'north'))
    offset_left = offset_left_mm + data['padding']['west'] + sum(size_of(data['titles'], 'west'))
    offset_left += (data['column_space'] + data['element_config']['img_width']) *(cur_column - 1)
    offset_left += sum(size_of(data['row_titles'], 'west'))
    if direction == 'south':
        offset_top += sum(size_of(data['element_config']['captions'], 'south')) * data['num_rows'] #new
        offset_top += sum(size_of(data['column_titles'], 'north'))
        offset_top += (data['row_space']*(data['num_rows'] - 1)) + data['element_config']['img_height'] * data['num_rows']
        offset_top += size_of(data['column_titles'], 'south')[1]

    position = [mm_to_inch(offset_top) * factor, mm_to_inch(offset_left) * factor]
    size = [mm_to_inch(width) * factor, mm_to_inch(height) * factor]
    return position, size