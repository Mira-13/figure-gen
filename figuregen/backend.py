from typing import List, Tuple
from dataclasses import dataclass
import os
from .figuregen import *
from . import calculate as calc
from .element_data import *

@dataclass
class Bounds:
    top: float
    left: float
    width: float
    height: float

@dataclass
class Component:
    bounds: Bounds
    figure_idx: int
    grid_idx: int
    row_idx: int
    col_idx: int

@dataclass
class ImageComponent(Component):
    data: ElementData
    has_frame: bool
    frame_linewidth: float
    frame_color: Tuple[float, float, float]

@dataclass
class TextComponent(Component):
    content: str
    rotation: float
    fontsize: float
    color: Tuple[float, float, float]
    background_color: Tuple[float, float, float]
    type: str
    horizontal_alignment: str = "center"
    padding: calc.Size = calc.Size(0, 0)
    vertical_alignment: str = "center"

@dataclass
class RectangleComponent(Component):
    color: Tuple[float, float, float]
    linewidth: float
    dashed: bool

@dataclass
class LineComponent(Component):
    from_x: float
    from_y: float
    to_x: float
    to_y: float
    linewidth: float
    color: Tuple[float, float, float]

class Backend:
    def generate(self, grids: List[List[Grid]], width_mm: float, filename: str):
        output_dir = os.path.dirname(filename)

        gen_rows = []
        top = 0
        row_idx = 0
        for row in grids:
            sizes = self.compute_aligned_sizes(row, width_mm)

            # generate all grids
            gen_grids = []
            left = 0
            for grid_idx in range(len(row)):
                bounds = Bounds(top, left, sizes[grid_idx][0].width_mm, sizes[grid_idx][0].height_mm)
                components = self.gen_grid(grids[row_idx][grid_idx], bounds, sizes[grid_idx][1])

                # Set the correct figure and grid indices on all components
                for c in components:
                    c.figure_idx = row_idx
                    c.grid_idx = grid_idx

                gen_grids.append(self.assemble_grid(components, output_dir))
                left += sizes[grid_idx][0].width_mm

            bounds = Bounds(top, 0, width_mm, sizes[0][0].height_mm)
            gen_rows.append(self.combine_grids(gen_grids, row_idx, bounds))
            top += sizes[0][0].height_mm
            row_idx += 1

        # Combine all rows
        result = self.combine_rows(gen_rows, Bounds(0, 0, width_mm, top))
        self.write_to_file(result, filename)

    def compute_aligned_sizes(self, grids: List[Grid], width_mm: float) -> List[Tuple[calc.Size, calc.Size]]:
        """
        Computes the sizes of all grids and contained images so that their heights match and they fill the given
        width exactly.

        Returns:
            a list where each element is a tuple of (grid size, image size)
        """
        num_modules = len(grids)
        assert(num_modules != 0)

        if num_modules == 1:
            elem_size = calc.element_size_from_width(grids[0], width_mm)
            h = calc.total_height(grids[0], elem_size)
            return [ (calc.Size(width_mm, h), elem_size) ]

        sum_inverse_aspect_ratios = 0
        inverse_aspect_ratios = []
        for g in grids:
            a = g.rows / g.cols * g.aspect_ratio
            sum_inverse_aspect_ratios += 1/a
            inverse_aspect_ratios.append(1/a)

        sum_fixed_deltas = 0
        i = 0
        for m in grids:
            w_fix = calc.min_width(m)
            h_fix = calc.min_height(m)
            sum_fixed_deltas += w_fix - h_fix * inverse_aspect_ratios[i]
            i += 1

        height = (width_mm - sum_fixed_deltas) / sum_inverse_aspect_ratios

        sizes = []
        for m in grids:
            elem_size = calc.element_size_from_height(m, height)
            w = calc.total_width(m, elem_size)
            sizes.append((calc.Size(w, height), elem_size))
        return sizes

    def gen_lines(self, element: ElementView, img_pos_top, img_pos_left, img_size: calc.Size) -> List[Component]:
        try:
            lines = element.elem['lines']
        except:
            return []

        if lines == []:
            return []

        if isinstance(element.image, RasterImage):
            # Coordinates are in pixels
            w_scale = img_size.width_mm / element.image.width_px
            h_scale = img_size.height_mm / element.image.height_px
        else:
            # Coordinates are between 0 and 1.
            w_scale = img_size.width_mm
            h_scale = img_size.height_mm

        result = []
        for l in lines:
            start_h = l['from'][0] * h_scale + img_pos_top
            start_w = l['from'][1] * w_scale + img_pos_left
            end_h = l['to'][0] * h_scale + img_pos_top
            end_w = l['to'][1] * w_scale + img_pos_left
            rgb = (l['color'][0], l['color'][1], l['color'][2])
            bounds = Bounds(img_pos_top, img_pos_left, img_size.width_mm, img_size.height_mm)
            result.append(LineComponent(bounds, -1, -1, -1, -1, start_w, start_h, end_w, end_h, l['linewidth'], rgb))

        return result

    def _gen_label(self, img_pos_top, img_pos_left, img_width, img_height, cfg, label_pos) -> TextComponent:
        try:
            cfg = cfg[label_pos]
        except KeyError:
            return None

        alignment = label_pos.split('_')[-1]
        is_top = (label_pos.split('_')[0] == 'top')

        rect_width, rect_height = cfg['width_mm'], cfg['height_mm']

        # determine the correct offsets depending on wether it is in the corner or center
        if alignment == 'center':
            offset_w, offset_h = 0, cfg['offset_mm']
        else:
            offset_w = cfg['offset_mm'][0]
            offset_h = cfg['offset_mm'][1]

        # determine pos_top of rectangle
        if is_top:
            pos_top = img_pos_top + offset_h
        else:
            pos_top = img_pos_top + img_height - rect_height - offset_h

        # determine pos_left of rectangle based on alignment
        if alignment == 'center':
            pos_left = img_pos_left + (img_width * 1/2.) - (rect_width * 1/2.)
        elif alignment == 'left':
            pos_left = img_pos_left + offset_w
        else: # right
            pos_left = img_pos_left + img_width - rect_width - offset_w

        bounds = Bounds(pos_top, pos_left, rect_width, rect_height)

        padding = calc.Size(cfg['padding_mm'], cfg['padding_mm'])

        c = TextComponent(bounds, -1, -1, -1, -1, cfg["text"], 0, cfg['fontsize'], cfg['text_color'],
            cfg['background_color'], "label-" + label_pos, alignment, padding, "top" if is_top else "bottom")

        return c

    def gen_labels(self, element: ElementView, img_pos_top, img_pos_left, img_size: calc.Size) -> List[Component]:
        try:
            cfg = element.elem['label']
        except:
            return []

        labels = []
        for label_pos in ['top_center', 'top_left', 'top_right', 'bottom_center', 'bottom_left', 'bottom_right']:
            l = self._gen_label(img_pos_top, img_pos_left, img_size.width_mm, img_size.height_mm, cfg, label_pos)
            if l is None:
                continue
            labels.append(l)
        return labels

    def gen_markers(self, element: ElementView, img_pos_top, img_pos_left, img_size: calc.Size) -> List[Component]:
        try:
            markers = element.elem['crop_marker']
        except:
            return []

        if isinstance(element.image, RasterImage):
            # Coordinates are in pixels
            w_scale = img_size.width_mm / element.image.width_px
            h_scale = img_size.height_mm / element.image.height_px
        else:
            # Coordinates are between 0 and 1.
            w_scale = img_size.width_mm
            h_scale = img_size.height_mm

        result = []
        for m in markers:
            if m['linewidth'] > 0.0:
                pos_top = img_pos_top + (m['pos'][1] * h_scale)
                pos_left = img_pos_left + (m['pos'][0] * w_scale)
                w = m['size'][0] * w_scale
                h = m['size'][1] * h_scale
                bounds = Bounds(pos_top, pos_left, w, h)
                result.append(RectangleComponent(bounds, -1, -1, -1, -1, m['color'], m['linewidth'], m['dashed']))
        return result

    def gen_images(self, grid: Grid, grid_bounds: Bounds, img_size: calc.Size) -> List[Component]:
        """ Generates a list of figure components for all images and their lables, captions, frames, and markers """
        images = []
        for row_idx in range(grid.rows):
            for col_idx in range(grid.cols):
                element = grid[row_idx, col_idx]
                assert element.image is not None
                assert isinstance(element.image, ElementData)

                # Position of the main image
                pos_top, pos_left = calc.image_pos(grid, img_size, col_idx, row_idx)
                pos_top += grid_bounds.top
                pos_left += grid_bounds.left
                bounds = Bounds(pos_top, pos_left, img_size.width_mm, img_size.height_mm)

                # If there is a frame, get is properties
                has_frame = "frame" in element.elem and element.elem["frame"] is not None
                linewidth = 0
                color = [0,0,0]
                if has_frame:
                    linewidth = element.elem["frame"]["line_width"]
                    color = element.elem["frame"]["color"]

                images.append(ImageComponent(bounds, -1, -1, row_idx, col_idx, element.image,
                    has_frame, linewidth, color))

                markers = self.gen_lines(element, pos_top, pos_left, img_size)
                for m in markers:
                    m.row_idx = row_idx
                    m.col_idx = col_idx
                images.extend(markers)

                markers = self.gen_labels(element, pos_top, pos_left, img_size)
                for m in markers:
                    m.row_idx = row_idx
                    m.col_idx = col_idx
                images.extend(markers)

                markers = self.gen_markers(element, pos_top, pos_left, img_size)
                for m in markers:
                    m.row_idx = row_idx
                    m.col_idx = col_idx
                images.extend(markers)
        return images

    def gen_south_captions(self, grid: Grid, grid_bounds: Bounds, img_size: calc.Size) -> List[Component]:
        layout = grid.layout.layout['element_config']['captions']['south']
        if layout['height'] == 0:
            return []

        captions = []
        for row_idx in range(grid.rows):
            for col_idx in range(grid.cols):
                if 'captions' not in grid[row_idx, col_idx].elem:
                    continue

                txt_content = grid[row_idx, col_idx].elem['captions']['south']

                if txt_content == '':
                    continue

                (top, left) = calc.south_caption_pos(grid, img_size, col_idx, row_idx)
                bounds = Bounds(top + grid_bounds.top, left + grid_bounds.left,
                    img_size.width_mm, layout['height'])

                captions.append(TextComponent(bounds, -1, -1, row_idx, col_idx, txt_content, layout['rotation'],
                    layout['fontsize'], layout['text_color'], [255, 255, 255], "caption", vertical_alignment="top"))

        return captions

    def gen_titles(self, grid: Grid, grid_bounds: Bounds, img_size: calc.Size) -> List[Component]:
        titles = []
        for direction in ['north', 'east', 'south', 'west']:
            if direction not in grid.data['titles']:
                continue

            content = grid.data['titles'][direction]
            (top, left, width, height) = calc.titles_pos_and_size(grid, img_size, direction)
            bounds = Bounds(top + grid_bounds.top, left + grid_bounds.left, width, height)

            if width == 0 or height == 0 or content == "":
                continue

            t = grid.layout.layout['titles'][direction]
            titles.append(TextComponent(bounds, -1, -1, -1, -1, content, t['rotation'], t['fontsize'],
                t['text_color'], t['background_color'], "title-" + direction))
        return titles

    def _compute_bg_colors(self, bg_color_properties, num):
        if bg_color_properties is None: # no background color
            return [None for i in range(num)]
        elif not isinstance(bg_color_properties[0], list): # constant color for all
            return [bg_color_properties for i in range(num)]
        else: # individual background colors
            return bg_color_properties

    def _gen_row_col_titles(self, direction: str, layout, num: int, pos_fn, contents: List[str], is_row):
        titles = []
        if calc.size_of(layout, direction)[0] != 0.0:
            bg_colors = self._compute_bg_colors(layout[direction]['background_colors'], num)
            t = layout[direction]

            for i in range(num):
                bounds = pos_fn(i)
                if bounds.width == 0 or bounds.height == 0:
                    continue

                txt = contents[i]
                if txt == "":
                    continue

                if is_row:
                    titles.append(TextComponent(bounds, -1, -1, i, -1, txt, t['rotation'], t['fontsize'],
                        t['text_color'], bg_colors[i], "rowtitle-" + direction))
                else:
                    titles.append(TextComponent(bounds, -1, -1, -1, i, txt, t['rotation'], t['fontsize'],
                        t['text_color'], bg_colors[i], "coltitle-" + direction))
        return titles

    def gen_row_titles(self, grid: Grid, grid_bounds: Bounds, img_size: calc.Size) -> List[Component]:
        titles = []
        for direction in ['east', 'west']:
            def pos_fn(idx):
                (top, left, width, height) = calc.row_titles_pos(grid, img_size, idx + 1, direction)
                return Bounds(top + grid_bounds.top, left + grid_bounds.left, width, height)

            if direction not in grid.data['row_titles']:
                continue

            contents = grid.data['row_titles'][direction]['content']
            t = self._gen_row_col_titles(direction, grid.layout.layout['row_titles'], grid.rows, pos_fn,
                contents, True)
            titles.extend(t)

        return titles

    def gen_column_titles(self, grid: Grid, grid_bounds: Bounds, img_size: calc.Size) -> List[Component]:
        titles = []
        for direction in ['north', 'south']:
            def pos_fn(idx):
                (top, left, width, height) = calc.column_titles_pos(grid, img_size, idx + 1, direction)
                return Bounds(top + grid_bounds.top, left + grid_bounds.left, width, height)

            if direction not in grid.data['column_titles']:
                continue

            contents = grid.data['column_titles'][direction]['content']
            t = self._gen_row_col_titles(direction, grid.layout.layout['column_titles'], grid.cols, pos_fn,
                contents, False)
            titles.extend(t)

        return titles

    def gen_grid(self, grid: Grid, bounds: Bounds, img_size: calc.Size) -> List[Component]:
        result = []
        result.extend(self.gen_images(grid, bounds, img_size))
        result.extend(self.gen_south_captions(grid, bounds, img_size))
        result.extend(self.gen_titles(grid, bounds, img_size))
        result.extend(self.gen_row_titles(grid, bounds, img_size))
        result.extend(self.gen_column_titles(grid, bounds, img_size))
        return result

    def assemble_grid(self, components: List[Component], output_dir: str):
        raise NotImplementedError()

    def combine_grids(self, data, idx: int, bounds: Bounds):
        raise NotImplementedError()

    def combine_rows(self, data, bounds: Bounds):
        raise NotImplementedError()

    def write_to_file(self, data, filename):
        raise NotImplementedError()
