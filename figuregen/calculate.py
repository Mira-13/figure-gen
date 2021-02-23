from dataclasses import dataclass
from .figuregen import *

@dataclass
class Size:
    width_mm: float
    height_mm: float

def pt_to_mm(x):
    return x * 0.352778

def _get_space_type(position: str) -> str:
    if position == 'east' or position == 'west':
        return 'width'
    return 'height'

def sum_caption_spacing(layout: LayoutView, position: str, factor: float) -> float:
    sum = 0
    caption = layout.layout['element_config']['captions'][position]
    spacing = _get_space_type(position)
    if (caption[spacing] > 0.0):
        sum = caption['offset'] + caption[spacing]
    return sum * factor

def sum_title_spacing(layout: LayoutView, position):
    title = layout.layout['titles'][position]
    spacing = _get_space_type(position)
    if (title[spacing] > 0.0):
        return title['offset'] + title[spacing]
    return 0

def sum_row_title_spacing(layout: LayoutView, position):
    if (layout.layout['row_titles'][position]['width'] > 0.0):
        return layout.layout['row_titles'][position]['offset'] + layout.layout['row_titles'][position]['width']
    return 0

def sum_col_title_spacing(layout: LayoutView, position):
    if (layout.layout['column_titles'][position]['height'] > 0.0):
        return layout.layout['column_titles'][position]['height'] + layout.layout['column_titles'][position]['offset']
    return 0

def min_width(grid: Grid):
    '''
    Minimum width is the sum of all fixed space/padding based on the json-config file, including titles, offsets, paddings, etc.
    So basically: everything except for the images.
    '''
    min_width = grid.layout.layout['column_space'] * (grid.cols - 1)# + (muliplied by num -1)
    min_width += grid.layout.layout['padding']['west']
    min_width += grid.layout.layout['padding']['east']
    min_width += sum_caption_spacing(grid.layout, 'east', grid.cols)
    min_width += sum_caption_spacing(grid.layout, 'west', grid.cols)
    min_width += sum_title_spacing(grid.layout, 'east')
    min_width += sum_title_spacing(grid.layout, 'west')
    min_width += sum_row_title_spacing(grid.layout, 'east')
    min_width += sum_row_title_spacing(grid.layout, 'west')
    return min_width

def fixed_inner_width(grid: Grid):
    '''
    Fixed inner width is the sum of spacing between all images, which also includes element captions
    '''
    inner_width = grid.layout.layout['column_space'] * (grid.cols - 1)
    inner_width += sum_caption_spacing(grid.layout,'east', grid.cols - 1)
    inner_width += sum_caption_spacing(grid.layout,'west', grid.cols - 1)
    return inner_width

def body_width(grid: Grid, image_size: Size):
    '''
    body means: all images and their spaces/padding inbetween the images.
    Not included are: column/row titles and titles as well as their corresping offsets.
    '''
    return fixed_inner_width(grid) + grid.cols * image_size.width_mm

def total_width(grid: Grid, image_size: Size):
    '''
    Includes everything that takes up width: padding, images, captions, row titles,
    east/west titles and all corresponding offsets
    '''
    total_width = body_width(grid, image_size)
    total_width += sum_caption_spacing(grid.layout, 'east', 1) # add to inner body one more
    total_width += sum_caption_spacing(grid.layout, 'west', 1) # same reason as above

    # add outer titles
    total_width += sum_row_title_spacing(grid.layout, 'east')
    total_width += sum_row_title_spacing(grid.layout, 'west')
    total_width += sum_title_spacing(grid.layout, 'east')
    total_width += sum_title_spacing(grid.layout, 'west')

    total_width += grid.layout.layout['padding']['west'] + grid.layout.layout['padding']['east']
    return total_width

def min_height(grid: Grid):
    '''
    Minimum height is the sum of all fixed space/padding based on the json-config file, including titles, offsets, paddings, etc.
    So basically: everything except for the images.
    '''
    min_height = grid.layout.layout['row_space'] * (grid.rows -1)
    min_height += grid.layout.layout['padding']['north']
    min_height += grid.layout.layout['padding']['south']
    min_height += sum_caption_spacing(grid.layout, 'north', grid.rows)
    min_height += sum_caption_spacing(grid.layout, 'south', grid.rows)
    min_height += sum_title_spacing(grid.layout, 'north')
    min_height += sum_title_spacing(grid.layout, 'south')
    min_height += sum_col_title_spacing(grid.layout, 'north')
    min_height += sum_col_title_spacing(grid.layout, 'south')
    return min_height

def fixed_inner_height(grid: Grid):
    '''
    Fixed inner height is the sum of spacing between all images, which also includes element captions
    '''
    inner_height = grid.layout.layout['row_space'] * (grid.rows -1)
    inner_height += sum_caption_spacing(grid.layout, 'north', grid.rows-1)
    inner_height += sum_caption_spacing(grid.layout, 'south', grid.rows-1)

    return inner_height

def body_height(grid: Grid, image_size: Size):
    '''
    body means: all images and their spaces/padding inbetween the images.
    Not included are: column/row titles and titles as well as their corresping offsets.
    '''
    return fixed_inner_height(grid) + grid.rows * image_size.height_mm

def total_height(grid: Grid, image_size: Size):
    '''
    Includes everything that takes up height: padding, images, captions, column titles,
    north/south titles and all corresponding offsets
    '''
    total_height = body_height(grid, image_size)
    total_height += sum_caption_spacing(grid.layout, 'north', 1) # add to inner body one more
    total_height += sum_caption_spacing(grid.layout, 'south', 1) # add to inner body one more

    # add outer titles
    total_height += sum_col_title_spacing(grid.layout, 'north')
    total_height += sum_col_title_spacing(grid.layout, 'south')
    total_height += sum_title_spacing(grid.layout, 'north')
    total_height += sum_title_spacing(grid.layout, 'south')

    total_height += grid.layout.layout['padding']['north'] + grid.layout.layout['padding']['south']
    return total_height

def element_size_from_width(grid: Grid, total_width: float) -> Size:
    """ Computes the size of all individual images in the grid based on the given total width. """
    min_w = min_width(grid)
    width_per_img = (total_width - min_w) / grid.cols
    if width_per_img < 1.0:
        if width_per_img < 0.0:
            print(f'Warning: Element width computed to be negative. Probably due to an extreme aspect ratio.'
                  f'Total height: ({total_width} - {min_w}) / {grid.cols} = {width_per_img}')
        else:
            print(f'Warning: Width per element is {width_per_img}, which is less than 1mm.'
                   'Probably due to an extreme aspect ratio or too many elements.')

    return Size(width_per_img, width_per_img * grid.aspect_ratio)

def element_size_from_height(grid: Grid, total_height: float) -> Size:
    """ Computes the size of all individual images in the grid based on the given total height. """
    min_h = min_height(grid)
    height_per_img = (total_height - min_h) / grid.rows
    if height_per_img < 1.0:
        if height_per_img < 0.0:
            print(f'Warning: Element height computed to be negative. Probably due to an extreme aspect ratio.'
                  f'Total height: ({total_height} - {min_h}) / {grid.rows} = {height_per_img}')
        else:
            print(f'Warning: Height per element is {height_per_img} which is less than 1mm.'
                   'Probably due to an extreme aspect ratio or too many elements.')
    return Size(height_per_img / grid.aspect_ratio, height_per_img)

def size_of(data_part, direction: str):
    assert direction in data_part

    def _get_size(space, offset):
        if space == 0.0:
            return 0.0, 0.0
        return space, offset

    if direction == 'north' or direction == 'south':
        return _get_size(data_part[direction]['height'], data_part[direction]['offset'])
    elif direction == 'east' or direction == 'west':
        return _get_size(data_part[direction]['width'], data_part[direction]['offset'])
    else:
        raise Error("Error: Invalid direction value: " + direction +". (html module)")

def image_pos(grid: Grid, image_size: Size, column, row):
    """ Computes the position of an image in the given grid, relative to the grid's top left corner. """
    title_top = sum(size_of(grid.layout.layout['titles'], 'north'))
    title_left = sum(size_of(grid.layout.layout['titles'], 'west'))
    col_title_top = sum(size_of(grid.layout.layout['column_titles'], 'north'))
    row_title_left = sum(size_of(grid.layout.layout['row_titles'], 'west'))
    img_south_capt = sum(size_of(grid.layout.layout['element_config']['captions'], 'south')) * (row)

    top = grid.layout.layout['padding']['north'] + title_top + col_title_top
    top += (grid.layout.layout['row_space'] + image_size.height_mm)*(row) + img_south_capt

    left =  grid.layout.layout['padding']['west'] + title_left + row_title_left
    left += (grid.layout.layout['column_space'] + image_size.width_mm)*(column)

    return top, left

def south_caption_pos(grid: Grid, image_size: Size, column, row):
    top, left = image_pos(grid, image_size, column, row)
    top += image_size.height_mm + grid.layout.layout['element_config']['captions']['south']['offset']
    return top, left

def titles_pos_and_size(grid: Grid, image_size: Size, direction: str):
    '''
    Note: this does not include element captions, yet. Because it was never really used in tikz or elsewhere.
    '''
    offset_left = grid.layout.layout['padding']['west']
    offset_top =  grid.layout.layout['padding']['north']

    if direction == 'north' or direction == 'south':
        width = image_size.width_mm * grid.cols + grid.layout.layout['column_space']*(grid.cols - 1)
        height = size_of(grid.layout.layout['titles'], direction)[0]

        offset_left += sum(size_of(grid.layout.layout['titles'], 'west')) + sum(size_of(grid.layout.layout['row_titles'], 'west'))
        if direction == 'south':
            offset_top += sum(size_of(grid.layout.layout['element_config']['captions'], 'south')) * grid.rows
            offset_top += grid.layout.layout['padding']['north'] + sum(size_of(grid.layout.layout['titles'], 'north')) + sum(size_of(grid.layout.layout['column_titles'], 'north'))
            offset_top += (grid.layout.layout['row_space']*(grid.rows - 1)) + image_size.height_mm * grid.rows
            offset_top += sum(size_of(grid.layout.layout['column_titles'], 'south')) + size_of(grid.layout.layout['titles'], 'south')[1]

        return offset_top, offset_left, width, height

    elif direction == 'east' or direction == 'west':
        height = image_size.height_mm * grid.rows + grid.layout.layout['row_space']*(grid.rows - 1)
        height += sum(size_of(grid.layout.layout['element_config']['captions'], 'south')) * (grid.rows - 1)
        width = size_of(grid.layout.layout['titles'], direction)[0]

        offset_top += sum(size_of(grid.layout.layout['titles'], 'north'))
        offset_top += sum(size_of(grid.layout.layout['column_titles'], 'north'))
        if direction == 'east':
            offset_left += sum(size_of(grid.layout.layout['titles'], 'west')) + sum(size_of(grid.layout.layout['row_titles'], 'west'))
            offset_left += (grid.layout.layout['column_space']*(grid.cols - 1)) + image_size.width_mm * grid.cols
            offset_left += sum(size_of(grid.layout.layout['row_titles'], 'east')) + size_of(grid.layout.layout['titles'], 'east')[1]

        return offset_top, offset_left, width, height

    else:
        assert False, "Error: Invalid direction value: " + direction +". (html module)"

def row_titles_pos(grid: Grid, image_size: Size, cur_row, direction):
    if not(direction == 'east' or direction == 'west'):
        raise Error("Error: Invalid direction value for row titles: " + direction +". Expected 'east' or 'west'.")

    data = grid.layout.layout

    width = size_of(data['row_titles'], direction)[0]
    height = image_size.height_mm

    offset_left = data['padding']['west'] + sum(size_of(data['titles'], 'west'))
    offset_top = data['padding']['north'] + sum(size_of(data['titles'], 'north')) + sum(size_of(data['column_titles'], 'north'))
    offset_top += (data['row_space'] + image_size.height_mm) * (cur_row - 1)
    offset_top += sum(size_of(data['element_config']['captions'], 'south')) * (cur_row-1)
    if direction == 'east':
        offset_left += sum(size_of(data['row_titles'], 'west'))
        offset_left += (data['column_space']*(grid.cols - 1)) + image_size.width_mm * grid.cols
        offset_left += size_of(data['row_titles'], 'east')[1]

    return offset_top, offset_left, width, height

def column_titles_pos(grid: Grid, image_size: Size, cur_column, direction):
    if not(direction == 'north' or direction == 'south'):
        raise "Error: Invalid direction value for column titles: " + direction +". Expected 'north' or 'south'."

    data = grid.layout.layout

    width = image_size.width_mm
    height = size_of(data['column_titles'], direction)[0]

    offset_top = data['padding']['north'] + sum(size_of(data['titles'], 'north'))
    offset_left = data['padding']['west'] + sum(size_of(data['titles'], 'west'))
    offset_left += (data['column_space'] + image_size.width_mm) *(cur_column - 1)
    offset_left += sum(size_of(data['row_titles'], 'west'))
    if direction == 'south':
        offset_top += sum(size_of(data['element_config']['captions'], 'south')) * grid.rows
        offset_top += sum(size_of(data['column_titles'], 'north'))
        offset_top += (data['row_space']*(grid.rows - 1)) + image_size.height_mm * grid.rows
        offset_top += size_of(data['column_titles'], 'south')[1]

    return offset_top, offset_left, width, height