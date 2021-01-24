def pt_to_mm(x):
    return x * 0.352778

# helper
def _get_space_type(position):
    if position == 'east' or position == 'west':
        return 'width'
    return 'height'

def sum_caption_spacing(data, position, muliplied): # e.g. multiplied = num_cols
    sum = 0
    caption = data['element_config']['captions'][position]
    spacing = _get_space_type(position)

    if (caption[spacing] > 0.0):
        sum = caption['offset'] + caption[spacing]
    return sum * muliplied

def sum_title_spacing(data, position):
    title = data['titles'][position]
    spacing = _get_space_type(position)
    if (title[spacing] > 0.0):
        return title['offset'] + title[spacing]
    return 0

def sum_row_title_spacing(data, position):
    if (data['row_titles'][position]['width'] > 0.0):
        return data['row_titles'][position]['offset'] + data['row_titles'][position]['width']
    return 0

def sum_col_title_spacing(data, position):
    if (data['column_titles'][position]['height'] > 0.0):
        return data['column_titles'][position]['height'] + data['column_titles'][position]['offset']
    return 0
# END helper

# CALCULATIONS FOR HEIGHTS AND WIDTHS
def relative_position(img_width_px, img_height_px, img_used_width, img_used_height):
    width_factor = img_used_width * 1/img_width_px
    height_factor = img_used_height * 1/img_height_px
    return width_factor, height_factor

def get_h_offset_for_title(title_offset, caption_config, row_config):
    offset = title_offset
    if caption_config['width']!=0.0:
        offset += caption_config['width'] + caption_config['offset']
    if row_config['width']!=0.0:
        offset += row_config['width'] + row_config['offset']

    return offset

def get_min_width(data):
    '''
    Minimum width is the sum of all fixed space/padding based on the json-config file, including titles, offsets, paddings, etc.
    So basically: everything except for the images.
    '''
    num_cols = data['num_columns']

    min_width = data['column_space'] * (num_cols - 1)# + (muliplied by num -1)
    min_width += data['padding']['west']
    min_width += data['padding']['east']
    min_width += sum_caption_spacing(data, 'east', num_cols)
    min_width += sum_caption_spacing(data, 'west', num_cols)
    min_width += sum_title_spacing(data, 'east')
    min_width += sum_title_spacing(data, 'west')
    min_width += sum_row_title_spacing(data, 'east')
    min_width += sum_row_title_spacing(data, 'west')

    return min_width

def get_min_height(data):
    '''
    Minimum height is the sum of all fixed space/padding based on the json-config file, including titles, offsets, paddings, etc.
    So basically: everything except for the images.
    '''
    num_rows = data['num_rows']

    min_height = data['row_space'] * (num_rows -1)
    min_height += data['padding']['north']
    min_height += data['padding']['south']
    min_height += sum_caption_spacing(data, 'north', num_rows)
    min_height += sum_caption_spacing(data, 'south', num_rows)
    min_height += sum_title_spacing(data, 'north')
    min_height += sum_title_spacing(data, 'south')
    min_height += sum_col_title_spacing(data, 'north')
    min_height += sum_col_title_spacing(data, 'south')

    return min_height

def get_fixed_inner_height(data):
    '''
    Fixed inner height is the sum of spacing between all images, which also includes element captions
    '''
    num_rows = data['num_rows']

    inner_height = data['row_space'] * (num_rows -1)
    inner_height += sum_caption_spacing(data, 'north', num_rows-1)
    inner_height += sum_caption_spacing(data, 'south', num_rows-1)

    return inner_height

def get_fixed_inner_width(data):
    '''
    Fixed inner width is the sum of spacing between all images, which also includes element captions
    '''
    num_columns = data['num_columns']

    inner_width = data['column_space'] * (num_columns -1)
    inner_width += sum_caption_spacing(data,'east', num_columns-1)
    inner_width += sum_caption_spacing(data,'west', num_columns-1)

    return inner_width

def get_body_width(data):
    '''
    body means: all images and their spaces/padding inbetween the images.
    Not included are: column/row titles and titles as well as their corresping offsets.
    '''
    return get_fixed_inner_width(data) + data['num_columns'] * data['element_config']['img_width']

def get_body_height(data):
    '''
    body means: all images and their spaces/padding inbetween the images.
    Not included are: column/row titles and titles as well as their corresping offsets.
    '''
    return get_fixed_inner_height(data) + data['num_rows'] * data['element_config']['img_height']

def get_total_width(data):
    '''
    Includes everything that takes up width: padding, images, captions, row titles,
    east/west titles and all corresponding offsets
    '''
    total_width = get_body_width(data)
    total_width += sum_caption_spacing(data, 'east', 1) # add to inner body one more
    total_width += sum_caption_spacing(data, 'west', 1) # same reason as above

    # add outer titles
    total_width += sum_row_title_spacing(data, 'east')
    total_width += sum_row_title_spacing(data, 'west')
    total_width += sum_title_spacing(data, 'east')
    total_width += sum_title_spacing(data, 'west')

    total_width += data['padding']['west'] + data['padding']['east']
    return total_width

def get_total_height(data):
    '''
    Includes everything that takes up height: padding, images, captions, column titles,
    north/south titles and all corresponding offsets
    '''
    total_height = get_body_height(data)
    total_height += sum_caption_spacing(data, 'north', 1) # add to inner body one more
    total_height += sum_caption_spacing(data, 'south', 1) # add to inner body one more

    # add outer titles
    total_height += sum_col_title_spacing(data, 'north')
    total_height += sum_col_title_spacing(data, 'south')
    total_height += sum_title_spacing(data, 'north')
    total_height += sum_title_spacing(data, 'south')

    total_height += data['padding']['north'] + data['padding']['south']
    return total_height

def get_vertical_figure_title_height(data):
    vert_title_height = get_body_height(data)

    vert_title_height += sum_col_title_spacing(data, 'north')
    vert_title_height += sum_col_title_spacing(data, 'south')

    return vert_title_height

def resize_to_match_total_width(data):
    '''
    You overwrite the local value. If you use this function and want to have the value used permanently
    then you need to make sure to save it in a file.

    Note: If float() is too unprecise, use Decimal()
    '''
    num_cols = data['num_columns']
    total_width = data['total_width']
    width_to_height_ratio = data['img_height_px'] / data['img_width_px']

    min_width = get_min_width(data)
    width_per_img = (total_width - min_width) / num_cols
    if width_per_img < 1.0:
        if width_per_img < 0.0:
            print(f'Warning: Element width computed to be negative. Probably due to an extreme aspect ratio.'
                  f'Total height: ({total_width} - {min_width}) / {num_cols} = {width_per_img}')
        else:
            print(f'Warning: Width per element is {width_per_img} which is less than 1.0 {data["units"]}.'
                   'Probably due to an extreme aspect ratio.')

    # force width/height ratio of origin img
    data['element_config']['img_width'] = width_per_img
    h = width_per_img * float(width_to_height_ratio) # w_to_h_ratio was of type decimal, which is more precise
    data['element_config']['img_height'] = h
    return width_per_img, h

def resize_to_match_total_height(data):
    '''
    You overwrite the local value. If you use this function and want to have the value used permanently
    then you need to make sure to save it in a file.

    Note: If float() is too unprecise, use Decimal()
    '''
    num_rows = data['num_rows']
    total_height = data['total_height']
    heigth_to_width_ratio = data['img_width_px'] / data['img_height_px']

    min_height = get_min_height(data)
    height_per_img = (total_height - min_height) / num_rows
    if height_per_img < 1.0:
        if height_per_img < 0.0:
            print(f'Warning: Element height computed to be negative. Probably due to an extreme aspect ratio.'
                  f'Total height: ({total_height} - {min_height}) / {num_rows} = {height_per_img}')
        else:
            print(f'Warning: Height per element is {height_per_img} which is less than 1.0 {data["units"]}.'
                   'Probably due to an extreme aspect ratio.')

    # force width/height ratio of origin img
    data['element_config']['img_width'] = height_per_img * heigth_to_width_ratio
    data['element_config']['img_height'] = height_per_img
# END CALCULATIONS

def align_heights(data_to_be_aligned, data):
    data_to_be_aligned['padding']['north'] = data['padding']['north']
    data_to_be_aligned['padding']['south'] = data['padding']['south']

    data_to_be_aligned['titles']['north']['height'] = data['titles']['north']['height']
    data_to_be_aligned['titles']['north']['offset'] = data['titles']['north']['offset']
    data_to_be_aligned['titles']['south']['height'] = data['titles']['south']['height']
    data_to_be_aligned['titles']['south']['offset'] = data['titles']['north']['offset']

    data_to_be_aligned['column_titles']['north']['height'] = data['column_titles']['north']['height']
    data_to_be_aligned['column_titles']['north']['offset'] = data['column_titles']['north']['offset']
    data_to_be_aligned['column_titles']['south']['height'] = data['column_titles']['south']['height']
    data_to_be_aligned['column_titles']['south']['offset'] = data['column_titles']['south']['offset']

    return data_to_be_aligned