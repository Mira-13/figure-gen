from . import implementation

class Error(Exception):
    def __init__(self, message):
        self.message = message

class Module:
    pass

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

    def get_set_props(self, name):
        try:
            val = self.layout[name]
        except:
            return None
        return val

    def set_padding(self, top=None, left=None, bottom=None, right=None, column=None, row=None):
        '''
        unit: mm (float) for top/left/bottom/right
        '''
        if top is not None:
            self.layout['padding.north'] = top
        if left is not None:
            self.layout['padding.west'] = left
        if bottom is not None:
            self.layout['padding.south'] = bottom
        if right is not None:
            self.layout['padding.east'] = right
        if column is not None:
            self.layout['column_space'] = column
        if row is not None:
            self.layout['row_space'] = row
        return self

    def _set_text_properties(self, name, position, field_size_mm, 
                             offset_mm=None, fontsize=None, txt_rotation=None, txt_color=None, line_space=None, bg_color=None):
        '''
        Internal function to avoid code dublication
        '''
        if _is_north_or_south(position):
            self.layout[name + ".height"] = field_size_mm
        else:
            self.layout[name + ".width"] = field_size_mm

        if offset_mm is not None:
            self.layout[name +".offset"] = offset_mm
        if txt_rotation is not None:
            self.layout[name + ".rotation"] = txt_rotation
        if fontsize is not None:
            self.layout[name + ".fontsize"] = fontsize
        if txt_color is not None:
            self.layout[name + ".text_color"] = txt_color
        if line_space is not None:
            self.layout[name + ".line_space"] = line_space
        if bg_color is not None:
            if 'row_titles' in name.split('.') or 'column_titles' in name.split('.'):
                self.layout[name + ".background_colors"] = bg_color
            else:
                self.layout[name + ".background_color"] = bg_color
        return self

    def set_caption(self, height_mm, offset_mm=None, fontsize=None, txt_rotation=None, txt_color=None, line_space=None):
        '''
        Currently we support only the south caption for all backends, which is why if the user sets a caption, 
        it will be the south caption.
        In the future, this function could be a reference for north/east/west captions.
        '''
        name = "element_config.captions.south"
        self._set_text_properties(name, 'south', height_mm, 
                             offset_mm, fontsize, txt_rotation, txt_color, line_space, bg_color=None)
        return self

    def set_title(self, position, field_size_mm, offset_mm=None, fontsize=None, txt_rotation=None, 
                  txt_color=None, line_space=None, bg_color=None):
        name = 'titles.' + _transfer_position(position)
        self._set_text_properties(name, position, field_size_mm, 
                             offset_mm, fontsize, txt_rotation, txt_color, line_space, bg_color)
        return self

    def set_row_titles(self, position, field_size_mm, offset_mm=None, fontsize=None, txt_rotation=None, 
                       txt_color=None, line_space=None, bg_color=None):
        name = 'row_titles.' + _transfer_position(position)
        self._set_text_properties(name, position, field_size_mm, 
                             offset_mm, fontsize, txt_rotation, txt_color, line_space, bg_color)
        return self

    def set_col_titles(self, position, field_size_mm, offset_mm=None, fontsize=None, txt_rotation=None, 
                       txt_color=None, line_space=None, bg_color=None):
        name = 'column_titles.' + _transfer_position(position)
        self._set_text_properties(name, position, field_size_mm, 
                             offset_mm, fontsize, txt_rotation, txt_color, line_space, bg_color)
        return self

    def _set_field_size_if_not_set(self, name, pos, field_size_mm=5):
        '''
        Makes sure, that the corresponding field_size of new added content will be set (not zero) and, therefore, 
        visible for the user. 
        '''
        if _is_north_or_south(pos):
            field_size = self.get_set_props(name+'.height')
        else:
            field_size = self.get_set_props(name+'.width')
        if field_size is None:
            self._set_text_properties(name, pos, field_size_mm)

class ElementView:
    '''
    A 'Grid' contains one or multiple elements depending on num_row and num_col. This class will help make changes 
    in the settings for each element.
    You should however 'set_images' for each element, else unknown behaviour.
    '''
    def __init__(self, grid, row, col):
        self.elem = grid.data["elements"][row][col]
        self.layout = grid.get_layout()    

    def set_image(self, img_data):
        self.elem['image'] = img_data
        return self

    def set_frame(self, linewidth, rgb=[0,0,0]):
        '''
        linewidth unit: pt
        rgb: list or tripel, int range (0-255)
        '''
        self.elem['frame'] = { "line_width": linewidth, "color": rgb }
        return self

    def set_marker_properties(self, linewidth=1.5, is_dashed=False):
        try:
            test = self.elem["crop_marker"]["list"]
        except:
            self.elem["crop_marker"] = {}
            self.elem["crop_marker"]["list"] = []

        self.elem["crop_marker"]["line_width"] = linewidth
        self.elem["crop_marker"]["dashed"] = is_dashed
        return self

    def set_marker(self, pos, size, rgb=[255,255,255]):
        try:
            test = self.elem["crop_marker"]["list"]
        except:
            self.set_marker_properties(linewidth=1.5)

        self.elem["crop_marker"]["list"].append({"pos": pos, "size": size, "color": rgb})
        return self

    def set_caption(self, txt_content):
        '''
        A (south) caption is placed below an image. 
        In case the corresponding field height is not set yet, we set a 'default' value. This makes sure, that 
        the content (provided by the user) will be shown. The user can set (overwrite) the layout for captions anytime.
        '''
        self.elem["captions"] = {}
        self.elem["captions"]["south"] = txt_content

        # check if caption layout is already set, if not, set a field_size, so that the user is not confused, why content isn't shown
        self.layout._set_field_size_if_not_set(name='element_config.captions.south', pos='south', field_size_mm=6.)
        return self

    def set_label(self, txt_content, pos, width_mm=10., height_mm=3.0, offset_mm=[1.0, 1.0], 
                  fontsize=6, bg_color=None, txt_color=[0,0,0], txt_padding_mm=1.0):

        if not(pos in ['bottom_left', 'bottom_right', 'bottom_center', 'top_left', 'top_right', 'top_center']):
            print('Error, pos is invalid.') # TODO

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
            "text": txt_content,
            "fontsize": fontsize,
            "line_space": 1.2,
            "text_color": txt_color,
            "background_color": bg_color,
            "width_mm": width_mm,
            "height_mm": height_mm,
            "offset_mm": offset_mm,
            "padding_mm": txt_padding_mm
        }
                  

class Grid(Module):
    def __init__(self, num_rows, num_cols):
        '''
        initialize empty matrix for elements and fill the matrix with 'image' content
        '''
        self.data = {
            "type": "grid",
            "elements": [[{} for i in range(num_cols)] for i in range (num_rows)],
            "row_titles": {}, 
            "column_titles": {}, 
            "titles": {}, 
            "layout": {}
        }

    def get_element(self, row, col):
        return ElementView(self, row, col)

    def get_layout(self):
        return LayoutView(self)

    def set_title(self, position, txt_content):
        '''
        position: string (valid input: 'north'/'west'/... or 'top'/'right'/...) 
        The corresponding field will be set to some value in case the user didn't set it yet.
        '''
        pos = _transfer_position(position)
        self.data["titles"][pos] = txt_content

        # check if caption layout is already set, if not, set a field_size, so that the user is not confused, why content isn't shown
        self.get_layout()._set_field_size_if_not_set(name='titles.'+pos, pos=pos, field_size_mm=6.)
        return self

    def set_row_titles(self, position, txt_list):
        '''
        position: string (valid: 'west'/'east' or 'right'/'left')
        txt_list: string list of num_rows
        '''
        pos = _transfer_position(position)
        if pos in ['north', 'south']:
            raise Error("Invalid position for row_title. Try: 'west'/'east' or 'right'/'left'")

        try:
            self.data['row_titles'][pos]['content'] = txt_list
        except:
            self.data['row_titles'][pos] = {}
            self.data['row_titles'][pos]['content'] = txt_list
        
        # check if caption layout is already set, if not, set a field_size, so that the user is not confused, why content isn't shown
        self.get_layout()._set_field_size_if_not_set(name='row_titles.'+pos, pos=pos, field_size_mm=3.)
        return self

    def set_col_titles(self, position, txt_list):
        '''
        position: string (valid: 'north'/'south' or 'top'/'bottom')
        txt_list: string list of num_cols
        '''
        pos = _transfer_position(position)
        if pos in ['west', 'east']:
            raise Error('Invalid position for column_title. Try: "north"/"south" or "top"/"bottom"')

        try:
            self.data['column_titles'][pos]['content'] = txt_list
        except:
            self.data['column_titles'][pos] = {}
            self.data['column_titles'][pos]['content'] = txt_list
        
        # check if caption layout is already set, if not, set a field_size, so that the user is not confused, why content isn't shown
        self.get_layout()._set_field_size_if_not_set(name='column_titles.'+pos, pos=pos, field_size_mm=3.)
        return self


class Plot(Module):
    def __init__(self, p_data):
        self.data = {
            "type": "plot",
            "data": p_data,
            "plot_color": None,
            "axis_labels": {},
            "axis_properties": {},
            "markers": {},
            "layout": {}
            }
    
    def _interpret_rotation(self, rotation):
        if rotation == 0:
            return 'horizontal'
        if rotation == 90 or rotation == -90:
            return 'vertical'
        if rotation in ['horizontal', 'vertical']:
            return rotation
        raise Error('Incorrect rotation value. Try: 0/(-)90 or "horizontal"/"vertical".')

    def _check_axis(self, axis):
        if not (axis in ['x', 'y']):
            raise Error('Incorrect axis. Try: "x" or "y".')

    def set_plot_colors(self, rgb_color_list):
        self.data['plot_color'] = rgb_color_list

    def set_axis_label(self, axis, txt, rotation):
        self._check_axis(axis)
        rotation = self._interpret_rotation(rotation)
        
        self.data['axis_labels'][axis] = {}
        self.data['axis_labels'][axis]['text'] = txt
        self.data['axis_labels'][axis]['rotation'] = rotation

    def set_axis_props(self, axis, ticks, range=None, use_log_scale=True, use_scientific_notations=False):
        '''
        So far, we need range and ticks as user input. Would be nice to let 
        '''
        self._check_axis(axis)
        if range is not None and len(range) != 2:
            raise Error('You need exactly two values to specify range: [min, max]')

        self.data['axis_properties'][axis] = {}
        if range is not None:
            self.data['axis_properties'][axis]['range'] = range
        self.data['axis_properties'][axis]['ticks'] = ticks
        self.data['axis_properties'][axis]['use_log_scale'] = use_log_scale
        self.data['axis_properties'][axis]['use_scientific_notations'] = use_scientific_notations

    def set_marker_v_line(self, pos, color, linestyle, linewidth_pt=.8):
        '''
        Currently, we only implemented "vertical_lines"
        linestyle allows matplotlib inputs, e.g. (0,(4,6)) is valid.
        '''
        try:
            test = self.data['markers']['vertical_lines'][0]
        except:
            self.data['markers']['vertical_lines'] = []
        self.data['markers']['vertical_lines'].append({
            'pos': pos,
            'color': color,
            "linestyle": linestyle,
            "linewidth_pt": linewidth_pt,
        })

    def set_font_props(self, fontsize_pt=None, font_family=None, tex_package=None):
        if fontsize_pt is not None:
            self.data['layout']["plot_config.font.fontsize_pt"] = fontsize_pt
        if font_family is not None:
            # TODO: maybe check if font_family has a valid value
            self.data['layout']["plot_config.font.font_family"] = font_family
        if tex_package is not None:
            self.data['layout']["plot_config.font.tex_package"] = tex_package

    def set_grid_props(self, color=None, linewidth_pt=None, linestyle=None):
        if color is not None:
            self.data['layout']["plot_config.grid.color"] = color
        if linewidth_pt is not None:
            self.data['layout']["plot_config.grid.linewidth_pt"] = linewidth_pt
        if linestyle is not None:
            self.data['layout']["plot_config.grid.linestyle"] = linestyle

    def set_width_to_height_aspect_ratio(self, a):
        self.data['layout']['width_to_height_aspect_ratio'] = a

    def show_upper_axis(self):
        self.data['layout']["plot_config.has_upper_axis"] = True

    def show_right_axis(self):
        self.data['layout']["plot_config.has_right_axis"] = True

    def set_linewidth(plot_line_pt=None, tick_line_pt=None):
        if plot_line_pt is not None:
            self.data['layout']['plot_config.plot_linewidth_pt'] = plot_line_pt
        if tick_line_pt is not None:
            self.data['layout']['plot_config.tick_linewidth_pt'] = tick_line_pt


def horizontal_figure(modules, width_cm: float, filename):
    """
    Creates a figure by putting modules next to each other, from left to right.
    Aligns the height of the given modules such that they fit the given total width.

    Args:
        modules: a list of dictionaries, one for each module
        backend: can be one of: 'tikz', 'pptx', 'html'
        out_dir: path to the folder that will contain the generated figure and data
    """
    return implementation.horizontal_figure(modules, width_cm, filename)
