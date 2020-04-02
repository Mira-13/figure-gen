import json

# CALCULATIONS FOR HEIGHTS AND WIDTHS
def get_min_width(data):
    '''
    Minimum width is the sum of all fixed space/padding based on the json-config file, including titles, offsets, paddings, etc.
    So basically: everything except for the images.
    '''
    num_cols = data['num_columns']

    min_width = data['column_space'] * (num_cols - 1)# + (muliplied by num -1)
    min_width += data['padding']['left'] # +
    min_width += data['padding']['right'] # +
    if (data['element_config']['captions']['east']['width'] > 0.0): # + (muliplied by num)
        min_width += data['element_config']['captions']['east']['offset'] * num_cols # if width # else ignore (muliplied by num)
        min_width += data['element_config']['captions']['east']['width'] * num_cols
    if (data['element_config']['captions']['west']['width'] > 0.0): # + (muliplied by num)
        min_width += data['element_config']['captions']['west']['offset'] * num_cols # if width # else ignore (muliplied by num)
        min_width += data['element_config']['captions']['west']['width'] * num_cols
    if (data['titles']['east']['width'] > 0.0): # + 
        min_width += data['titles']['east']['offset'] + data['titles']['east']['width']
    if (data['titles']['west']['width'] > 0.0): # + 
        min_width += data['titles']['west']['offset'] + data['titles']['west']['width']
    if (data['row_titles']['east']['width'] > 0.0): # + 
        min_width += data['row_titles']['east']['offset'] + data['row_titles']['east']['width']
    if (data['row_titles']['west']['width'] > 0.0): # + 
        min_width += data['row_titles']['west']['offset'] + data['row_titles']['west']['width']
    
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
    if (data['element_config']['captions']['north']['height'] > 0.0):
        min_height += data['element_config']['captions']['north']['height'] * num_rows
        min_height += data['element_config']['captions']['north']['offset'] * num_rows
    if (data['element_config']['captions']['south']['height'] > 0.0):
        min_height += data['element_config']['captions']['south']['height'] * num_rows
        min_height += data['element_config']['captions']['south']['offset'] * num_rows
    if (data['titles']['north']['height'] > 0.0):
        min_height += data['titles']['north']['height'] + data['titles']['north']['offset']
    if (data['titles']['south']['height'] > 0.0):
        min_height += data['titles']['south']['height'] + data['titles']['south']['offset']
    if (data['column_titles']['north']['height'] > 0.0):
        min_height += data['column_titles']['north']['height'] + data['column_titles']['north']['offset']
    if (data['column_titles']['south']['height'] > 0.0):
        min_height += data['column_titles']['south']['height'] + data['column_titles']['south']['offset']

    return min_height

def get_fixed_inner_height(data):
    '''
    Fixed inner height is the sum of spacing between all images, which also includes element captions 
    '''
    num_rows = data['num_rows']

    inner_height = data['row_space'] * (num_rows -1)
    if (data['element_config']['captions']['north']['height'] > 0.0):
        inner_height += data['element_config']['captions']['north']['height'] * (num_rows -1)
        inner_height += data['element_config']['captions']['north']['offset'] * (num_rows -1)
    if (data['element_config']['captions']['south']['height'] > 0.0):
        inner_height += data['element_config']['captions']['south']['height'] * (num_rows -1)
        inner_height += data['element_config']['captions']['south']['offset'] * (num_rows -1)

    return inner_height

def get_fixed_inner_width(data):
    '''
    Fixed inner width is the sum of spacing between all images, which also includes element captions 
    '''
    num_columns = data['num_columns']

    inner_width = data['column_space'] * (num_columns -1)
    if (data['element_config']['captions']['east']['width'] > 0.0):
        inner_width += data['element_config']['captions']['east']['width'] * (num_columns -1)
        inner_width += data['element_config']['captions']['east']['offset'] * (num_columns -1)
    if (data['element_config']['captions']['west']['width'] > 0.0):
        inner_width += data['element_config']['captions']['west']['width'] * (num_columns -1)
        inner_width += data['element_config']['captions']['west']['offset'] * (num_columns -1)

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
    Careful: Frames are not considered if frame line widht > spaces/paddings! <--TODO  
    Not included are: column/row titles and titles as well as their corresping offsets.
    '''
    return get_fixed_inner_height(data) + data['num_rows'] * data['element_config']['img_height']

def get_total_width(data):
    total_width = get_body_width(data)
    if (data['element_config']['captions']['east']['width'] > 0.0):
        total_width += data['element_config']['captions']['east']['width']
        total_width += data['element_config']['captions']['east']['offset']
    if (data['element_config']['captions']['west']['width'] > 0.0):
        total_width += data['element_config']['captions']['west']['width']
        total_width += data['element_config']['captions']['west']['offset']

    if data['row_titles']['west']['width']!=0.0:
        total_width += data['row_titles']['west']['width'] + data['row_titles']['west']['offset']
    if data['row_titles']['east']['width']!=0.0:
        total_width += data['row_titles']['east']['width'] + data['row_titles']['east']['offset']

    if data['titles']['west']['width']!=0.0:
        total_width += data['titles']['west']['width'] + data['titles']['west']['offset']
    if data['titles']['east']['width']!=0.0:
        total_width += data['titles']['east']['width'] + data['titles']['east']['offset']
    
    total_width += data['padding']['left'] + data['padding']['right']
    return total_width 

def get_total_height(data):
    total_height = get_body_height(data)

    if data['column_titles']['north']['height']!=0.0:
        total_height += data['column_titles']['north']['height'] + data['column_titles']['north']['offset']
    if data['column_titles']['south']['height']!=0.0:
        total_height += data['column_titles']['south']['height'] + data['column_titles']['south']['offset']

    if data['titles']['north']['height']!=0.0:
        total_height += data['titles']['north']['height'] + data['titles']['north']['offset']
    if data['titles']['south']['height']!=0.0:
        total_height += data['titles']['south']['height'] + data['titles']['south']['offset']
    
    total_height += data['padding']['top'] + data['padding']['bottom']
    return total_height

def get_vertical_figure_title_height(data):
    vert_title_height = get_body_height(data)

    if data['column_titles']['north']['height']!=0.0:
        vert_title_height += data['column_titles']['north']['height'] + data['column_titles']['north']['offset']
    if data['column_titles']['south']['height']!=0.0:
        vert_title_height += data['column_titles']['south']['height'] + data['column_titles']['south']['offset']

    return vert_title_height

def overwrite_image_resolution_based_on_total_width(data):
    # TODO those overwrites are never used yet (bc we don't call make_tex and compile_tex afterwards)
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

def overwrite_image_resolution_based_on_total_height(data):
    # TODO test function at some point
    # TODO those overwrites are never used yet (bc we don't call make_tex and compile_tex afterwards)
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
    bw1: body_width_reference = flexible width_refernce = only contains the images widths (usually one image)
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
    title_with_offset_top = 0.0
    captions_with_offset_top = 0.0
    title_with_offset_bottom = 0.0
    captions_with_offset_bottom = 0.0

    if (data['titles']['north']['height'] > 0.0):
        title_with_offset_top += data['titles']['north']['height'] + data['titles']['north']['offset']

    if (data['column_titles']['north']['height'] > 0.0):
        captions_with_offset_top += data['column_titles']['north']['height'] + data['column_titles']['north']['offset']
    if (data['element_config']['captions']['north']['height'] > 0.0):
        captions_with_offset_top += data['element_config']['captions']['north']['height'] 
        captions_with_offset_top += data['element_config']['captions']['north']['offset']
    
    if (data['titles']['south']['height'] > 0.0):
        title_with_offset_bottom += data['titles']['south']['height'] + data['titles']['south']['offset']

    if (data['column_titles']['south']['height'] > 0.0):
        captions_with_offset_bottom += data['column_titles']['south']['height'] + data['column_titles']['south']['offset']
    if (data['element_config']['captions']['south']['height'] > 0.0):
        captions_with_offset_bottom += data['element_config']['captions']['south']['height']
        captions_with_offset_bottom += data['element_config']['captions']['south']['offset']
    
    height_alignments = {
        'top': {
            'padding': data['padding']['top'],
            'title+offset': title_with_offset_top,
            'captions+offset': captions_with_offset_top
        },
        'bottom': {
            'padding': data['padding']['bottom'],
            'title+offset': title_with_offset_bottom,
            'captions+offset': captions_with_offset_bottom
        }
    }
    return height_alignments
# END CALCULATIONS