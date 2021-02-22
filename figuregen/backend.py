from typing import List, Tuple
from dataclasses import dataclass
import os
from .figuregen import *
from . import calculate as calc
from .element_data import *
from .tikz import TikzBackend

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

            gen_rows.append(self.combine_grids(gen_grids))
            top += sizes[0][0].height_mm
            row_idx += 1

        # Combine all rows
        result = self.combine_rows(gen_rows)
        self.write_to_file(result, filename)

    def compute_aligned_sizes(self, grids: List[Grid], width_mm: float) -> List[Tuple[calc.Size, calc.Size]]:
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

    def gen_lines(self, element: ElementView, img_pos_top, img_pos_left, img_size: calc.Size) -> List[Component]:
        return []

    def gen_border(self, element: ElementView, img_pos_top, img_pos_left, img_size: calc.Size) -> List[Component]:
        return []

    def gen_labels(self, element: ElementView, img_pos_top, img_pos_left, img_size: calc.Size) -> List[Component]:
        return []

    def gen_markers(self, element: ElementView, img_pos_top, img_pos_left, img_size: calc.Size) -> List[Component]:
        return []

    def gen_images(self, grid: Grid, grid_bounds: Bounds, img_size: calc.Size) -> List[Component]:
        """ Generates a list of figure components for all images and their lables, captions, frames, and markers """
        images = []
        for row_idx in range(grid.rows):
            for col_idx in range(grid.cols):
                element = grid[row_idx, col_idx]
                assert element.image is not None
                assert isinstance(element.image, ElementData)

                # place the main image
                pos_top, pos_left = calc.image_pos(grid, img_size, col_idx, row_idx)
                images.append(ImageComponent(Bounds(
                        pos_top + grid_bounds.top, pos_left + grid_bounds.left,
                        img_size.width_mm, img_size.height_mm
                    ), -1, -1, row_idx, col_idx, element.image))

                images.extend(self.gen_lines(element, pos_top, pos_left, img_size))
                images.extend(self.gen_border(element, pos_top, pos_left, img_size))
                images.extend(self.gen_labels(element, pos_top, pos_left, img_size))
                images.extend(self.gen_markers(element, pos_top, pos_left, img_size))
        return images

    def gen_south_captions(self, grid: Grid, grid_bounds: Bounds) -> List[Component]:
        return []

    def gen_titles(self, grid: Grid, grid_bounds: Bounds) -> List[Component]:
        return []

    def gen_row_titles(self, grid: Grid, grid_bounds: Bounds) -> List[Component]:
        return []

    def gen_column_titles(self, grid: Grid, grid_bounds: Bounds) -> List[Component]:
        return []

    def gen_grid(self, grid: Grid, bounds: Bounds, img_size: calc.Size) -> List[Component]:
        result = []
        result.extend(self.gen_images(grid, bounds, img_size))
        result.extend(self.gen_south_captions(grid, bounds))
        result.extend(self.gen_titles(grid, bounds))
        result.extend(self.gen_row_titles(grid, bounds))
        result.extend(self.gen_column_titles(grid, bounds))
        return result

    def assemble_grid(self, components: List[Component], output_dir: str):
        pass

    def combine_grids(self, data):
        pass

    def combine_rows(self, data):
        pass

    def write_to_file(self, data, filename):
        raise NotImplementedError()

class PdfBackend(Backend):
    """ Generates a TikZ picture and compiles it with pdflatex to a .pdf
    Requires pdflatex in the PATH.
    """

    def __init__(self, intermediate_dir = None, tex_packages=["[T1]{fontenc}", "{libertine}"]):
        self._intermediate_dir = intermediate_dir
        self._packages = tex_packages

class PptxBackend(Backend):
    pass

class HtmlBackend(Backend):
    pass

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
    if backend is None:
        backend = _backend_from_filename(filename)
    backend.generate(grids, width_cm * 10, filename)