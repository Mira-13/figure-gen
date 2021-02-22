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

def compute_min_width(grid: Grid):
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

def compute_fixed_inner_width(grid: Grid):
    '''
    Fixed inner width is the sum of spacing between all images, which also includes element captions
    '''
    inner_width = grid.layout.layout['column_space'] * (grid.cols - 1)
    inner_width += sum_caption_spacing(grid.layout,'east', grid.cols - 1)
    inner_width += sum_caption_spacing(grid.layout,'west', grid.cols - 1)
    return inner_width

def compute_body_width(grid: Grid, image_size: Size):
    '''
    body means: all images and their spaces/padding inbetween the images.
    Not included are: column/row titles and titles as well as their corresping offsets.
    '''
    return compute_fixed_inner_width(grid) + grid.cols * image_size.width_mm

def compute_total_width(grid: Grid, image_size: Size):
    '''
    Includes everything that takes up width: padding, images, captions, row titles,
    east/west titles and all corresponding offsets
    '''
    total_width = compute_body_width(grid, image_size)
    total_width += sum_caption_spacing(grid.layout, 'east', 1) # add to inner body one more
    total_width += sum_caption_spacing(grid.layout, 'west', 1) # same reason as above

    # add outer titles
    total_width += sum_row_title_spacing(grid.layout, 'east')
    total_width += sum_row_title_spacing(grid.layout, 'west')
    total_width += sum_title_spacing(grid.layout, 'east')
    total_width += sum_title_spacing(grid.layout, 'west')

    total_width += grid.layout['padding']['west'] + grid.layout['padding']['east']
    return total_width

def compute_min_height(grid: Grid):
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

def compute_fixed_inner_height(grid: Grid):
    '''
    Fixed inner height is the sum of spacing between all images, which also includes element captions
    '''
    inner_height = grid.layout.layout['row_space'] * (grid.rows -1)
    inner_height += sum_caption_spacing(grid.layout, 'north', grid.rows-1)
    inner_height += sum_caption_spacing(grid.layout, 'south', grid.rows-1)

    return inner_height

def compute_body_height(grid: Grid, image_size: Size):
    '''
    body means: all images and their spaces/padding inbetween the images.
    Not included are: column/row titles and titles as well as their corresping offsets.
    '''
    return compute_fixed_inner_height(grid) + grid.rows * image_size.height_mm

def compute_total_height(grid: Grid, image_size: Size):
    '''
    Includes everything that takes up height: padding, images, captions, column titles,
    north/south titles and all corresponding offsets
    '''
    total_height = compute_body_height(grid, image_size)
    total_height += sum_caption_spacing(grid.layout, 'north', 1) # add to inner body one more
    total_height += sum_caption_spacing(grid.layout, 'south', 1) # add to inner body one more

    # add outer titles
    total_height += sum_col_title_spacing(grid.layout, 'north')
    total_height += sum_col_title_spacing(grid.layout, 'south')
    total_height += sum_title_spacing(grid.layout, 'north')
    total_height += sum_title_spacing(grid.layout, 'south')

    total_height += grid.layout.layout['padding']['north'] + grid.layout.layout['padding']['south']
    return total_height

def compute_element_size_from_width(grid: Grid, total_width: float) -> Size:
    """ Computes the size of all individual images in the grid based on the given total width. """
    min_width = compute_min_width(grid)
    width_per_img = (total_width - min_width) / grid.cols
    if width_per_img < 1.0:
        if width_per_img < 0.0:
            print(f'Warning: Element width computed to be negative. Probably due to an extreme aspect ratio.'
                  f'Total height: ({total_width} - {min_width}) / {grid.cols} = {width_per_img}')
        else:
            print(f'Warning: Width per element is {width_per_img}, which is less than 1mm.'
                   'Probably due to an extreme aspect ratio or too many elements.')

    return Size(width_per_img, width_per_img * grid.aspect_ratio)

def compute_element_size_from_height(grid: Grid, total_height: float) -> Size:
    """ Computes the size of all individual images in the grid based on the given total height. """
    min_height = compute_min_height(grid)
    height_per_img = (total_height - min_height) / grid.rows
    if height_per_img < 1.0:
        if height_per_img < 0.0:
            print(f'Warning: Element height computed to be negative. Probably due to an extreme aspect ratio.'
                  f'Total height: ({total_height} - {min_height}) / {grid.rows} = {height_per_img}')
        else:
            print(f'Warning: Height per element is {height_per_img} which is less than 1mm.'
                   'Probably due to an extreme aspect ratio or too many elements.')
    return Size(height_per_img * grid.aspect_ratio, height_per_img)