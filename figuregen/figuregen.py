from typing import List
from . import implementation
from .default_layouts import layouts as _default_layout
from .element_data import *
import numpy as np
import copy
import os

class Error(Exception):
    def __init__(self, message):
        self.message = message

class GridError(Exception):
    def __init__(self, row, col, message):
        self.message = f"Error in row {row}, column {col}: {message}"

def _transfer_position(position):
    if position == 'top':
        return 'north'
    if position == 'bottom':
        return 'south'
    if position == 'left':
        return 'west'
    if position == 'right':
        return 'east'

    if position in ['north', 'east', 'south', 'west']:
        return position

    raise Error('Incorrect position. Try: "top"/"left"/... or "north"/"west"/...')

def _is_north_or_south(pos):
    if pos in ['north', 'south', 'top', 'bottom']:
        return True
    return False

class LayoutView:
    '''
    This class is used to make changes in a 'Grid' layout to be more user friendly.
    '''

    def __init__(self, grid):
        self.layout = grid.data['layout']

    def set_padding(self, top=None, left=None, bottom=None, right=None, column=None, row=None):
        '''
        unit: mm (float) for top/left/bottom/right, same for column/row
        '''
        if top is not None:
            self.layout['padding']['north'] = top
        if left is not None:
            self.layout['padding']['west'] = left
        if bottom is not None:
            self.layout['padding']['south'] = bottom
        if right is not None:
            self.layout['padding']['east'] = right
        if column is not None:
            self.layout['column_space'] = column
        if row is not None:
            self.layout['row_space'] = row
        return self

    def _set_text_properties(self, field, position, field_size_mm, offset_mm=None, fontsize=None,
                             txt_rotation=None, txt_color=None, line_space=None):
        if _is_north_or_south(position):
            field["height"] = field_size_mm
        else:
            field["width"] = field_size_mm

        if offset_mm is not None:
            field["offset"] = offset_mm
        if txt_rotation is not None:
            field["rotation"] = txt_rotation
        if fontsize is not None:
            field["fontsize"] = fontsize
        if txt_color is not None:
            field["text_color"] = txt_color
        if line_space is not None:
            field["line_space"] = line_space
        return self

    def set_caption(self, height_mm, offset_mm=None, fontsize=None, txt_rotation=None, txt_color=None, line_space=None):
        '''
        Writes text below/south (each) image of that grid.
        '''
        field = self.layout["element_config"]["captions"]["south"]
        self._set_text_properties(field, 'south', height_mm, offset_mm, fontsize, txt_rotation, txt_color, line_space)
        return self

    def set_title(self, position, field_size_mm, offset_mm=None, fontsize=None, txt_rotation=None,
                  txt_color=None, line_space=None, bg_color=None):
        '''
        Writes a grid/subfigure title.
        '''

        field = self.layout['titles'][_transfer_position(position)]
        self._set_text_properties(field, position, field_size_mm, offset_mm, fontsize, txt_rotation,
            txt_color, line_space)
        if bg_color is not None:
            field["background_color"] = bg_color
        return self

    def set_row_titles(self, position, field_size_mm, offset_mm=None, fontsize=None, txt_rotation=None,
                       txt_color=None, line_space=None, bg_color=None):
        field = self.layout['row_titles'][_transfer_position(position)]
        self._set_text_properties(field, position, field_size_mm, offset_mm, fontsize, txt_rotation,
            txt_color, line_space)
        if bg_color is not None:
            field["background_colors"] = bg_color
        return self

    def set_col_titles(self, position, field_size_mm, offset_mm=None, fontsize=None, txt_rotation=None,
                       txt_color=None, line_space=None, bg_color=None):
        field = self.layout['column_titles'][_transfer_position(position)]
        self._set_text_properties(field, position, field_size_mm, offset_mm, fontsize, txt_rotation,
            txt_color, line_space)
        if bg_color is not None:
            field["background_colors"] = bg_color
        return self

    def _set_field_size_if_not_set(self, component, pos, field_size_mm=5):
        '''
        Makes sure, that the corresponding field_size of new added content will be set (not zero) and, therefore,
        visible for the user.
        '''
        if _is_north_or_south(pos):
            field_size = component[pos]['height']
        else:
            field_size = component[pos]['width']
        if field_size is None or field_size == 0:
            self._set_text_properties(component[pos], pos, field_size_mm)

class ElementView:
    '''
    A 'Grid' contains one or multiple elements depending on num_row and num_col.
    This class will help make changes in the settings for each element.
    You should however 'set_images' for each element, else unknown behaviour.
    '''
    def __init__(self, grid, row, col):
        self.elem = grid.data["elements"][row][col]
        self.row = row
        self.col = col
        self.layout = grid.get_layout()

    @property
    def image(self) -> ElementData:
        return self.elem['image']

    @image.setter
    def image(self, image: ElementData):
        self.set_image(image)

    def set_image(self, image: ElementData):
        if not isinstance(image, ElementData):
            try:
                image = PNG(image)
            except:
                raise GridError(self.row, self.col, 'set_image needs an image of type figuregen.Image (e.g. figuregen.PNG)'
                    'or of type figuregen.Plot (e.g. figuregen.MatplotLinePlot)')
            print("Deprecation warning: interpreted image raw data as figuregen.PNG")
        self.elem['image'] = image
        return self

    def set_frame(self, linewidth, color=[0,0,0]):
        '''
        linewidth (float): unit is in pt
        color: [r,g,b] each channel with int range (0-255)
        '''
        self.elem['frame'] = { "line_width": linewidth, "color": color }
        return self

    def draw_lines(self, start_positions, end_positions, linewidth_pt=0.5, color=[0,0,0]):
        '''
        start_positions/end_positions (list of tuples): defines the position of the line to draw
            on top of the image. Needs a tuple (x: row, y: column) in pixel.
        '''
        # Validate arguments
        if linewidth_pt <= 0.0:
            raise GridError(self.row, self.col, f'invalid linewidth: {linewidth_pt}. Please choose a '
                    'positive linewidth_pt > 0.')
        if not isinstance(start_positions, list) or start_positions == []:
            raise GridError(self.row, self.col, 'Invalid argument "start_positions" needs to be a '
                    f'list that is not empty. Given: {start_positions}.')
        if not isinstance(end_positions, list) or end_positions == []:
            raise GridError(self.row, self.col, 'Invalid argument "end_positions" needs to be a '
                    f'list that is not empty. Given: {end_positions}.')
        if len(start_positions) != len(end_positions):
            raise GridError(self.row, self.col, 'You have more start positions than end positions (or reverse).')
        if len(start_positions[0]) != 2 or len(end_positions[0]) != 2:
            raise GridError(self.row, self.col, 'Invalid argument "start_positions"/"end_positions" should'
                'be a list of tuples. Each tuple represents the x and y coordination in pixels.')

        try:
            self.elem["lines"].append({"from": start_positions[0], "to": end_positions[0], "color": color, "linewidth": linewidth_pt})
        except:
            self.elem["lines"] = []
            self.elem["lines"].append({"from": start_positions[0], "to": end_positions[0], "color": color, "linewidth": linewidth_pt})

        for i in range(1, len(start_positions)):
            self.elem["lines"].append({"from": start_positions[i], "to": end_positions[i], "color": color, "linewidth": linewidth_pt})

    def set_marker_properties(self, linewidth=1.5, is_dashed=False):
        print('Warning, function does not change marker properties anymore: set_marker_properties got replaced by set_marker.')
        return self

    def set_marker(self, pos, size, color=[255,255,255], linewidth_pt=1.0, is_dashed=False):
        '''
            Draws a rectangle on top of an image.

            args:
                pos (tuple): starting position (left, top) in pixel
                size (tuple): size of the rectangle (width, height) in pixel
        '''
        if linewidth_pt <= 0.0:
            raise Error('set_marker: invalid linewidth "'+str(linewidth_pt)+'". Please choose a positive linewidth_pt > 0.')

        try:
            test = self.elem["crop_marker"][0]
        except:
            self.elem["crop_marker"] = []

        self.elem["crop_marker"].append({"pos": pos, "size": size, "color": color, "linewidth": linewidth_pt, "dashed": is_dashed})
        return self

    def set_caption(self, txt_content):
        '''
        A (south) caption is placed below an image.
        In case the corresponding field height is not set yet, we set a 'default' value. This makes sure, that
        the content (provided by the user) will be shown. The user can set/overwrite the layout for captions anytime.
        '''
        self.elem["captions"] = {}
        self.elem["captions"]["south"] = str(txt_content)

        # check if caption layout is already set, if not, set a field_size,
        # so that the user is not confused, why content isn't shown
        self.layout._set_field_size_if_not_set(self.layout.layout['element_config']['captions'], pos='south', field_size_mm=6.)
        return self

    def set_label(self, txt_content, pos, width_mm=10., height_mm=3.0, offset_mm=[1.0, 1.0],
                  fontsize=6, bg_color=None, txt_color=[0,0,0], txt_padding_mm=1.0):
        '''
            Write text on top of an image.

            args:
                pos (str): e.g. 'bottom_right', 'top_left', 'top_center' (= 'top'), ...
                offset_mm (tuple): defines where the label is placed exactly.
                        We recommend to set bg_color, if you want to experiment with offsets.
                fontsize (float): unit point
                bg/txt_color (list): rgb integers ranging from 0 to 255.
        '''

        if not(pos in ['bottom', 'top', 'bottom_left', 'bottom_right', 'bottom_center', 'top_left', 'top_right', 'top_center']):
            raise Error("Label position '"+ pos +"' is invalid. Valid positions are: 'bottom_left',"
                "'bottom_right', 'bottom_center' (= 'bottom'), 'top_left', 'top_right', or 'top_center' (= 'top').")
        if pos == 'bottom' or pos == 'top':
            pos += '_center'

        try:
            self.elem["label"][pos] = {}
        except:
            self.elem["label"] = {}

        if 'center' in pos:
            try:
                offset_mm = offset_mm[0]
            except:
                pass

        self.elem["label"][pos] = {
            "text": str(txt_content),
            "fontsize": fontsize,
            "line_space": 1.2,
            "text_color": txt_color,
            "background_color": bg_color,
            "width_mm": width_mm,
            "height_mm": height_mm,
            "offset_mm": offset_mm,
            "padding_mm": txt_padding_mm
        }


class Grid:
    def __init__(self, num_rows, num_cols):
        ''' Create an empty grid
        '''
        self.data = {
            "elements": [[{} for i in range(num_cols)] for i in range(num_rows)],
            "row_titles": {},
            "column_titles": {},
            "titles": {},
            "layout": copy.deepcopy(_default_layout["grid"])
        }
        self.rows = num_rows
        self.cols = num_cols

    def __getitem__(self, rowcol) -> ElementView:
        return self.get_element(*rowcol)

    def get_element(self, row, col) -> ElementView:
        return ElementView(self, row, col)

    @property
    def aspect_ratio(self):
        """ Aspect ratio (height / width) of all images in the grid.
        Currently assumes that the user set them correctly such that they are all equal to
        the top left image.
        """
        return self[0, 0].image.aspect_ratio

    @property
    def layout(self):
        return self.get_layout()

    def get_layout(self):
        return LayoutView(self)

    def copy_layout(self, other: 'Grid') -> None:
        ''' Copies the layout of another grid. Useful to quickly align paddings and font settings.

        Args:
            other: the Grid object to copy the layout from
        '''
        assert isinstance(other, Grid)
        self.data["layout"] = copy.deepcopy(other.data["layout"])

    def set_title(self, position, txt_content) -> 'Grid':
        '''
        If the user has not specified the title size in the layout yet, it will be set to a default value of 6mm.

        Args:
            position: one of 'north'/'west'/... or 'top'/'right'/...

        Returns:
            This object (for chaining purposes)
        '''
        pos = _transfer_position(position)
        self.data["titles"][pos] = str(txt_content)

        # set a field_size (if not already done), so that the user is not confused, why content isn't shown
        self.get_layout()._set_field_size_if_not_set(self.layout.layout['titles'], pos=pos, field_size_mm=6.)
        return self

    def set_row_titles(self, position: str, txt_list: list):
        '''
        Args:
            position: string (valid: 'west'/'east' or 'right'/'left')
            txt_list: string list with one title for each row
        '''
        pos = _transfer_position(position)
        if pos in ['north', 'south']:
            raise Error("Invalid position for row_title. Try: 'west'/'east' or 'right'/'left'")

        assert isinstance(txt_list, list), "Please provide a list of strings, not a simple string."
        assert len(txt_list) >= self.rows, "Please provide a title for every row."

        try:
            self.data['row_titles'][pos]['content'] = txt_list
        except:
            self.data['row_titles'][pos] = {}
            self.data['row_titles'][pos]['content'] = txt_list

        # set a field_size (if not already done), so that the user is not confused, why content isn't shown
        self.get_layout()._set_field_size_if_not_set(self.layout.layout['row_titles'], pos=pos, field_size_mm=3.)
        return self

    def set_col_titles(self, position, txt_list):
        '''
        position: string (valid: 'north'/'south' or 'top'/'bottom')
        txt_list: string list of num_cols
        '''
        pos = _transfer_position(position)
        if pos in ['west', 'east']:
            raise Error('Invalid position for column_title. Try: "north"/"south" or "top"/"bottom"')
        if not isinstance(txt_list, list):
            raise Error ("'set_col_titles': Please give a list of strings, not a simple string. The length of the list should cover the number of columns.")
        if len(txt_list) < self.cols:
            raise Error ("'set_col_titles': length of provided list is less than number of columns.")

        try:
            self.data['column_titles'][pos]['content'] = txt_list
        except:
            self.data['column_titles'][pos] = {}
            self.data['column_titles'][pos]['content'] = txt_list

         # set a field_size (if not already done), so that the user is not confused, why content isn't shown
        self.get_layout()._set_field_size_if_not_set(self.layout.layout['column_titles'], pos=pos, field_size_mm=3.)
        return self

from .backend import Backend, PptxBackend, HtmlBackend, PdfBackend
from .tikz import TikzBackend

def _backend_from_filename(filename: str) -> Backend:
    """ Guesses the correct backend based on the filename """
    extension = os.path.splitext(filename)[1].lower()
    if extension == ".pptx":
        return PptxBackend()
    elif extension == ".html":
        return HtmlBackend()
    elif extension == ".pdf":
        return PdfBackend()
    elif extension == ".tikz":
        return TikzBackend()
    else:
        raise ValueError(f"Could not derive backend from extension '{filename}'. Please specify.")

def figure(grids: List[List[Grid]], width_cm: float, filename: str, backend: Backend):
    """
    Grid rows: Creates a figure by putting grids next to each other, from left to right.
    Grid columns: stacks rows vertically.
    Aligns the height of the given grids such that they fit the given total width.

    args:
        grids: a list of lists of Grids (figuregen.Grid), which stacks horizontal figures vertically
        width_cm: total width of the figure in centimeters
        intermediate_dir: folder to write .tex and other intermediate files to. If set to None, uses a temporary one.
        tex_packages: a list of strings. Valid packages looks like ['{comment}', '[T1]{fontenc}'] without the prefix '\\usepackage'.
    """
    if backend is None:
        backend = _backend_from_filename(filename)
    backend.generate(grids, width_cm * 10, filename)

def horizontal_figure(grids, width_cm: float, filename, intermediate_dir = None, tex_packages=["[T1]{fontenc}", "{libertine}"]):
    """
    Creates a figure by putting grids next to each other, from left to right.
    Aligns the height of the given grids such that they fit the given total width.

    args:
        grids: a list of Grids (figuregen.Grid)
        width_cm: total width of the figure in centimeters
        intermediate_dir: folder to write .tex and other intermediate files to. If set to None, uses a temporary one.
        tex_packages: a list of strings. Valid packages looks like ['{comment}', '[T1]{fontenc}'] without the prefix '\\usepackage'.
    """
    figure([grids], width_cm, filename, intermediate_dir, tex_packages)