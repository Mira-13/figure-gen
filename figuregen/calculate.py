from dataclasses import dataclass
from typing import Tuple
from .figuregen import *

@dataclass
class Size:
    width_mm: float
    height_mm: float

def pt_to_mm(x):
    return x * 0.352778

def compute_sum_space(txtField: TextFieldLayout):
    return txtField.offset + txtField.size if txtField.size > 0.0 else 0

def sum_caption_spacing(layout: GridLayout, position: str, factor: float) -> float:
    return factor * compute_sum_space(layout.captions[position])

def sum_title_spacing(layout: GridLayout, position: str):
    return compute_sum_space(layout.titles[position])

def sum_row_title_spacing(layout: GridLayout, position):
    return compute_sum_space(layout.row_titles[position])

def sum_col_title_spacing(layout: GridLayout, position):
    return compute_sum_space(layout.column_titles[position])

def min_width(grid: Grid):
    '''
    Minimum width is the sum of all fixed space/padding based on the json-config file, including titles, offsets, paddings, etc.
    So basically: everything except for the images.
    '''
    return (
        grid.layout.column_space * (grid.cols - 1)
        + grid.layout.padding['west']
        + grid.layout.padding['east']
        + sum_caption_spacing(grid.layout, 'east', grid.cols)
        + sum_caption_spacing(grid.layout, 'west', grid.cols)
        + sum_title_spacing(grid.layout, 'east')
        + sum_title_spacing(grid.layout, 'west')
        + sum_row_title_spacing(grid.layout, 'east')
        + sum_row_title_spacing(grid.layout, 'west')
    )

def fixed_inner_width(grid: Grid):
    '''
    Fixed inner width is the sum of spacing between all images, which also includes element captions
    '''
    return (
        grid.layout.column_space * (grid.cols - 1)
        + sum_caption_spacing(grid.layout, 'east', grid.cols - 1)
        + sum_caption_spacing(grid.layout, 'west', grid.cols - 1)
    )

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
    return (
        body_width(grid, image_size)
        + sum_caption_spacing(grid.layout, 'east', 1) # add to inner body one more
        + sum_caption_spacing(grid.layout, 'west', 1) # same reason as above

        # add outer titles
        + sum_row_title_spacing(grid.layout, 'east')
        + sum_row_title_spacing(grid.layout, 'west')
        + sum_title_spacing(grid.layout, 'east')
        + sum_title_spacing(grid.layout, 'west')

        + grid.layout.padding['west'] + grid.layout.padding['east']
    )

def min_height(grid: Grid):
    '''
    Minimum height is the sum of all fixed space/padding based on the json-config file, including titles, offsets, paddings, etc.
    So basically: everything except for the images.
    '''
    return (
        grid.layout.row_space * (grid.rows -1)
        + grid.layout.padding['north']
        + grid.layout.padding['south']
        + sum_caption_spacing(grid.layout, 'north', grid.rows)
        + sum_caption_spacing(grid.layout, 'south', grid.rows)
        + sum_title_spacing(grid.layout, 'north')
        + sum_title_spacing(grid.layout, 'south')
        + sum_col_title_spacing(grid.layout, 'north')
        + sum_col_title_spacing(grid.layout, 'south')
    )

def fixed_inner_height(grid: Grid):
    '''
    Fixed inner height is the sum of spacing between all images, which also includes element captions
    '''
    return (
        grid.layout.row_space * (grid.rows -1)
        + sum_caption_spacing(grid.layout, 'north', grid.rows-1)
        + sum_caption_spacing(grid.layout, 'south', grid.rows-1)
    )

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
    return (
        body_height(grid, image_size)
        + sum_caption_spacing(grid.layout, 'north', 1) # add to inner body one more
        + sum_caption_spacing(grid.layout, 'south', 1) # add to inner body one more

        # add outer titles
        + sum_col_title_spacing(grid.layout, 'north')
        + sum_col_title_spacing(grid.layout, 'south')
        + sum_title_spacing(grid.layout, 'north')
        + sum_title_spacing(grid.layout, 'south')

        + grid.layout.padding['north'] + grid.layout.padding['south']
    )

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

def size_of(txt_layout: dict[str, TextFieldLayout], direction: str) -> Tuple[float, float]:
    if direction not in ['north', 'east', 'south', 'west']:
        raise Error("Error: Invalid direction value: " + direction +".")

    d = txt_layout[direction]
    return (0, 0) if d.size == 0 else (d.size, d.offset)

def image_pos(grid: Grid, image_size: Size, column, row):
    """ Computes the position of an image in the given grid, relative to the grid's top left corner. """
    title_top = sum(size_of(grid.layout.titles, 'north'))
    title_left = sum(size_of(grid.layout.titles, 'west'))
    col_title_top = sum(size_of(grid.layout.column_titles, 'north'))
    row_title_left = sum(size_of(grid.layout.row_titles, 'west'))
    img_south_capt = sum(size_of(grid.layout.captions, 'south')) * (row)

    top = grid.layout.padding['north'] + title_top + col_title_top
    top += (grid.layout.row_space + image_size.height_mm)*(row) + img_south_capt

    left =  grid.layout.padding['west'] + title_left + row_title_left
    left += (grid.layout.column_space + image_size.width_mm)*(column)

    return top, left

def south_caption_pos(grid: Grid, image_size: Size, column, row):
    top, left = image_pos(grid, image_size, column, row)
    top += image_size.height_mm + grid.layout.captions['south'].offset
    return top, left

def titles_pos_and_size(grid: Grid, image_size: Size, direction: str):
    '''
    Note: this does not include element captions, yet. Because it was never really used in tikz or elsewhere.
    '''
    offset_left = grid.layout.padding['west']
    offset_top =  grid.layout.padding['north']

    if direction == 'north' or direction == 'south':
        width = image_size.width_mm * grid.cols + grid.layout.column_space*(grid.cols - 1)
        height = size_of(grid.layout.titles, direction)[0]

        offset_left += sum(size_of(grid.layout.titles, 'west')) + sum(size_of(grid.layout.row_titles, 'west'))
        if direction == 'south':
            offset_top += sum(size_of(grid.layout.captions, 'south')) * grid.rows
            offset_top += grid.layout.padding['north'] + sum(size_of(grid.layout.titles, 'north')) + sum(size_of(grid.layout.column_titles, 'north'))
            offset_top += (grid.layout.row_space*(grid.rows - 1)) + image_size.height_mm * grid.rows
            offset_top += sum(size_of(grid.layout.column_titles, 'south')) + size_of(grid.layout.titles, 'south')[1]

        return offset_top, offset_left, width, height

    elif direction == 'east' or direction == 'west':
        height = image_size.height_mm * grid.rows + grid.layout.row_space*(grid.rows - 1)
        height += sum(size_of(grid.layout.captions, 'south')) * (grid.rows - 1)
        width = size_of(grid.layout.titles, direction)[0]

        offset_top += sum(size_of(grid.layout.titles, 'north'))
        offset_top += sum(size_of(grid.layout.column_titles, 'north'))
        if direction == 'east':
            offset_left += sum(size_of(grid.layout.titles, 'west')) + sum(size_of(grid.layout.row_titles, 'west'))
            offset_left += (grid.layout.column_space*(grid.cols - 1)) + image_size.width_mm * grid.cols
            offset_left += sum(size_of(grid.layout.row_titles, 'east')) + size_of(grid.layout.titles, 'east')[1]

        return offset_top, offset_left, width, height

    else:
        assert False, "Error: Invalid direction value: " + direction +". (html module)"

def row_titles_pos(grid: Grid, image_size: Size, cur_row, direction):
    if not(direction == 'east' or direction == 'west'):
        raise Error("Error: Invalid direction value for row titles: " + direction +". Expected 'east' or 'west'.")

    width = size_of(grid.layout.row_titles, direction)[0]
    height = image_size.height_mm

    offset_left = grid.layout.padding['west'] + sum(size_of(grid.layout.titles, 'west'))
    offset_top = grid.layout.padding['north'] + sum(size_of(grid.layout.titles, 'north')) + sum(size_of(grid.layout.column_titles, 'north'))
    offset_top += (grid.layout.row_space + image_size.height_mm) * (cur_row - 1)
    offset_top += sum(size_of(grid.layout.captions, 'south')) * (cur_row-1)
    if direction == 'east':
        offset_left += sum(size_of(grid.layout.row_titles, 'west'))
        offset_left += (grid.layout.column_space*(grid.cols - 1)) + image_size.width_mm * grid.cols
        offset_left += size_of(grid.layout.row_titles, 'east')[1]

    return offset_top, offset_left, width, height

def column_titles_pos(grid: Grid, image_size: Size, cur_column, direction):
    if not(direction == 'north' or direction == 'south'):
        raise "Error: Invalid direction value for column titles: " + direction +". Expected 'north' or 'south'."

    width = image_size.width_mm
    height = size_of(grid.layout.column_titles, direction)[0]

    offset_top = grid.layout.padding['north'] + sum(size_of(grid.layout.titles, 'north'))
    offset_left = grid.layout.padding['west'] + sum(size_of(grid.layout.titles, 'west'))
    offset_left += (grid.layout.column_space + image_size.width_mm) *(cur_column - 1)
    offset_left += sum(size_of(grid.layout.row_titles, 'west'))
    if direction == 'south':
        offset_top += sum(size_of(grid.layout.captions, 'south')) * grid.rows
        offset_top += sum(size_of(grid.layout.column_titles, 'north'))
        offset_top += (grid.layout.row_space*(grid.rows - 1)) + image_size.height_mm * grid.rows
        offset_top += size_of(grid.layout.column_titles, 'south')[1]

    return offset_top, offset_left, width, height