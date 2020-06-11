import json

def pt_to_mm(x):
    return x * 0.352778

# helper
def get_space_type(position):
    if position == 'east' or position == 'west':
        return 'width'
    return 'height'

def sum_caption_spacing(data, position, muliplied): # e.g. multiplied = num_cols
    sum = 0
    caption = data['element_config']['captions'][position]
    spacing = get_space_type(position)
    
    if (caption[spacing] > 0.0):
        sum = caption['offset'] + caption[spacing]
    return sum * muliplied

def sum_title_spacing(data, position):
    title = data['titles'][position]
    spacing = get_space_type(position)
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
    min_width += data['padding']['left']
    min_width += data['padding']['right']
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
    min_height += data['padding']['top']
    min_height += data['padding']['bottom']
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
    Careful: Frames are not considered if frame line width > spaces/paddings! <--TODO 
    Not included are: column/row titles and titles as well as their corresping offsets.
    '''
    return get_fixed_inner_width(data) + data['num_columns'] * data['element_config']['img_width']

def get_body_height(data):
    '''
    body means: all images and their spaces/padding inbetween the images.
    Careful: Frames are not considered if frame line width > spaces/paddings! <--TODO  
    Not included are: column/row titles and titles as well as their corresping offsets.
    '''
    return get_fixed_inner_height(data) + data['num_rows'] * data['element_config']['img_height']

def get_total_width(data):
    '''
    Includes everything that takes up width: padding, images, captions, row/column titles, 
    and all corresponding offsets
    '''
    total_width = get_body_width(data)
    total_width += sum_caption_spacing(data, 'east', 1) # add to inner body one more
    total_width += sum_caption_spacing(data, 'west', 1) # same reason as above
    
    # add outer titles
    total_width += sum_row_title_spacing(data, 'east')
    total_width += sum_row_title_spacing(data, 'west')
    total_width += sum_title_spacing(data, 'east')
    total_width += sum_title_spacing(data, 'west')
    
    total_width += data['padding']['left'] + data['padding']['right']
    return total_width 

def get_total_height(data):
    '''
    Includes everything that takes up height: padding, images, captions, row/column titles, 
    and all corresponding offsets
    '''
    total_height = get_body_height(data)
    total_height += sum_caption_spacing(data, 'north', 1) # add to inner body one more
    total_height += sum_caption_spacing(data, 'south', 1) # add to inner body one more

    # add outer titles
    total_height += sum_col_title_spacing(data, 'north')
    total_height += sum_col_title_spacing(data, 'south')
    total_height += sum_title_spacing(data, 'north')
    total_height += sum_title_spacing(data, 'south')
    
    total_height += data['padding']['top'] + data['padding']['bottom']
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
    '''
    num_cols = data['num_columns']
    num_rows = data['num_rows']
    total_width = data['total_width']
    width_to_height_ratio = data['img_height_px'] / data['img_width_px']

    min_height = get_min_height(data)
    min_width = get_min_width(data)
    width_left_per_img = (total_width - min_width) / num_cols
    if width_left_per_img < 1.0:
        if width_left_per_img < 0.0:
            print('consider less columns or allow as total_width more than '+ str(total_width) + 
            ', because the image width of all images are below 0.0 ' + data['units']+ '. ')
        else: 
            print('consider less columns or allow as total_width more than '+ str(total_width) + 
            ', because the image width of all images are below 1.0 ' + data['units']+ 
            '. If that is fine by you then ignore this message.')

    # force width/height ratio of origin img 
    data['element_config']['img_width'] = width_left_per_img
    data['element_config']['img_height'] = width_left_per_img * width_to_height_ratio
    return width_left_per_img, (width_left_per_img * width_to_height_ratio)

def resize_to_match_total_height(data):
    '''
    You overwrite the local value. If you use this function and want to have the value used permanently
    then you need to make sure to save it in a file.
    '''
    # TODO test function at some point
    num_cols = data['num_columns']
    num_rows = data['num_rows']
    total_height = data['total_height'] 
    heigth_to_width_ratio = data['img_width_px'] / data['img_height_px']

    min_height = get_min_height(data)
    min_width = get_min_width(data)

    height_left_per_img = (total_height - min_height) / num_rows
    if height_left_per_img < 1.0:
        if height_left_per_img < 0.0:
            print('consider less rows or allow as total_height more than '+ str(total_height) + 
            ', because the image height of the images are below 0.0 ' + data['units']+ '. ')
        else: 
            print('consider less rows or allow as total_height more than '+ str(total_height) + 
            ', because the image height of the images are below 1.0 ' + data['units']+ 
            '. If that is fine by you then ignore this message.')
    
    # force width/height ratio of origin img 
    data['element_config']['img_width'] = height_left_per_img * heigth_to_width_ratio
    data['element_config']['img_height'] = height_left_per_img


def get_combined_minimum_widths(data1, data2):
    a = get_min_width(data1)
    b = get_min_width(data2)
    return a + b

def get_body_widths_for_equal_heights(data1, data2, sum_total_width):
    '''
    GOAL: fullfill the following two constrains for optimal results:
    (1) body height of reference/data1 (bh1) = body height of grid/data2 (bh2)
    (2) body width of ref (bw1) + body width of grid (bw2) + fixed width = sum total width  

    In more detail, if you want to understand how those constrains are applied:
    bw1: body_width_reference = flexible width_reference = only contains the images widths (usually one image)
    bw2: body_width_grid = flexible width_grid = only contains the images widths
    xF: sum_total_width, must be given (user defines)
    wF: width fix = includes all the stuff that is fixed (e.g. paddings, offsets, text-field sizes defined by user in config.jsons)
    hF2: grid; fixed inner body height that needs to be considered in a2
    a: aspect ratio = bh / bw (respectively a1, a2)

    (1) a1 * bw1 = a2 * bw2 + hF2 <=> bw1 = a2/a1 * bw2 + hF2/a1
    (2) bw1 + bw2 + wF = xF
    (1 in 2) a2/a1 * bw2 + hF2/a1 + bw2 + wF = xF  <=> bw2 = (xF - wF)/(a2/a1 + 1)
    '''
    ref_data = data1
    grid_data = data2

    hF2 = get_fixed_inner_height(grid_data)
    a2 = (grid_data['img_height_px'] * grid_data['num_rows']) / (grid_data['img_width_px'] * grid_data['num_columns'])
    a1 = (ref_data['img_height_px'] * ref_data['num_rows']) / (ref_data['img_width_px'] * ref_data['num_columns'])
    xF = sum_total_width
    wF = get_combined_minimum_widths(grid_data, ref_data)
    bw2 = (xF - wF - hF2/a1) / (a2/a1 + 1)

    bw1 = xF - wF - bw2 
    return bw1, bw2

def get_height_paddings_with_titles(data):
    captions_with_offset_top = sum_col_title_spacing(data, 'north')
    captions_with_offset_top += sum_caption_spacing(data, 'north', 1)

    captions_with_offset_bottom = sum_col_title_spacing(data, 'south')
    captions_with_offset_bottom += sum_caption_spacing(data, 'south', 1)
    
    height_alignments = {
        'top': {
            'padding': data['padding']['top'],
            'title+offset': sum_title_spacing(data, 'north'),
            'captions+offset': captions_with_offset_top
        },
        'bottom': {
            'padding': data['padding']['bottom'],
            'title+offset': sum_title_spacing(data, 'south'),
            'captions+offset': captions_with_offset_bottom
        }
    }
    return height_alignments
# END CALCULATIONS

def align_heights(data_to_be_aligned, data):
    data_to_be_aligned['padding']['top'] = data['padding']['top']
    data_to_be_aligned['padding']['bottom'] = data['padding']['bottom']

    data_to_be_aligned['titles']['north']['height'] = data['titles']['north']['height']
    data_to_be_aligned['titles']['north']['offset'] = data['titles']['north']['offset']
    data_to_be_aligned['titles']['south']['height'] = data['titles']['south']['height']
    data_to_be_aligned['titles']['south']['offset'] = data['titles']['north']['offset']

    data_to_be_aligned['column_titles']['north']['height'] = data['column_titles']['north']['height']
    data_to_be_aligned['column_titles']['north']['offset'] = data['column_titles']['north']['offset']
    data_to_be_aligned['column_titles']['south']['height'] = data['column_titles']['south']['height']
    data_to_be_aligned['column_titles']['south']['offset'] = data['column_titles']['south']['offset']

    return data_to_be_aligned

# TEST
def load_test_data():
    import os
    wd_path = r'C:\Users\admin\Documents\MasterThesis\mtc\workDir'
    fig_path = os.path.join(wd_path, 'figures')
    module_path = os.path.join(fig_path, 'fig2', 'grid2') # e.g. 'fig1' 'grid1'

    with open(os.path.join(module_path, 'gen_figure.json')) as json_file:
        data = json.load(json_file)
    
    return data

def compare_values(val1, val2):
    if val1 != val2:
        print(False)
        print(val1)
        print(val2)
    else:
        print(True)
        print(val1)
        print(val2)

def test_caption():
    data = load_test_data()

    val1 = 0
    val2 = 0
    num_cols = data['num_columns']
    if (data['element_config']['captions']['east']['width'] > 0.0): # + (muliplied by num)
        val1 += data['element_config']['captions']['east']['offset'] * num_cols # if width # else ignore (muliplied by num)
        val1 += data['element_config']['captions']['east']['width'] * num_cols
    val2 += sum_caption_spacing(data, 'east', num_cols)

    compare_values(val1, val2)

def test_row_title():
    data = load_test_data()

    val1 = 0
    val2 = 0

    if (data['row_titles']['east']['width'] > 0.0): # + 
        val1 += data['row_titles']['east']['offset'] + data['row_titles']['east']['width']
    if (data['row_titles']['west']['width'] > 0.0): # + 
        val1 += data['row_titles']['west']['offset'] + data['row_titles']['west']['width']
    
    val2 += sum_row_title_spacing(data, 'east')
    val2 += sum_row_title_spacing(data, 'west')

    compare_values(val1, val2)

def test_fixed_inner_width():
    data = load_test_data()

    val1 = 0
    val2 = 0
    num_columns = data['num_columns']

    val2 += sum_caption_spacing(data,'east', num_columns-1)
    val2 += sum_caption_spacing(data,'west', num_columns-1)

    print(str(sum_caption_spacing(data,'east', 1)) + ' * ' + str(num_columns))

    if (data['element_config']['captions']['east']['width'] > 0.0):
        val1 += data['element_config']['captions']['east']['width'] * (num_columns -1)
        val1 += data['element_config']['captions']['east']['offset'] * (num_columns -1)
    if (data['element_config']['captions']['west']['width'] > 0.0):
        val1 += data['element_config']['captions']['west']['width'] * (num_columns -1)
        val1 += data['element_config']['captions']['west']['offset'] * (num_columns -1)

    compare_values(val1, val2)