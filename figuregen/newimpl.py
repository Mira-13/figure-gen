from typing import List, Tuple
from abc import ABC, abstractmethod
import os
from . import figuregen
from . import calculate as calc

class Backend(ABC):
    def generate(self, grids: List[List[figuregen.Grid]], width_mm: float, filename: str):
        gen_rows = []
        for row in grids:
            # align horizontally (computes sizes of all grids)
            sizes = self.compute_aligned_sizes(row)

            # generate all grids
            gen_grids = []
            for grid in row:
                gen_grids.append(self.make_grid(grids[row][grid]), sizes[grid], grid)
                pass

            # combine the result
            gen_rows.append(self.combine_grids(gen_grids))

        # Combine all rows
        result = self.combine_rows(gen_rows)
        self.write_to_file(result, filename)

    def compute_aligned_sizes(self, grids: List[figuregen.Grid], width_mm: float) -> List[calc.Size]:
        num_modules = len(grids)
        assert(num_modules != 0)

        if num_modules == 1:
            elem_size = calc.compute_element_size_from_width(grids[0], width_mm)
            h = calc.compute_total_height(grids[0], elem_size)
            return [ calc.Size(width_mm, h) ]

        sum_inverse_aspect_ratios = 0
        inverse_aspect_ratios = []
        for g in grids:
            a = g.rows / g.cols * g.aspect_ratio
            sum_inverse_aspect_ratios += 1/a
            inverse_aspect_ratios.append(1/a)

        sum_fixed_deltas = 0
        i = 0
        for m in grids:
            w_fix = calc.compute_min_width(m)
            h_fix = calc.compute_min_height(m)
            sum_fixed_deltas += w_fix - h_fix * inverse_aspect_ratios[i]
            i += 1

        height = (width_mm - sum_fixed_deltas) / sum_inverse_aspect_ratios

        sizes = []
        for m in grids:
            elem_size = calc.compute_element_size_from_height(m, height)
            w = calc.compute_total_width(m, elem_size)
            sizes.append(calc.Size(w, height))

    @abstractmethod
    def make_grid(self, grid: figuregen.Grid, sizes: List[calc.Size], index: int):
        pass

    @abstractmethod
    def combine_grids(self, data):
        pass

    @abstractmethod
    def combine_rows(self, data):
        pass

class TikzBackend(Backend):
    """ Generates the code for a TikZ picture representing the figure.
    Default file ending is .tikz, use \input{figure.tikz} to include in LaTeX.
    """

    def __init__(self, include_header=True):
        """
        Args:
            include_header: boolean, set to false to not include the macro definitions in the generated file.
        """
        self._include_header = include_header

    def add_overlay(self, tikz_code: str):
        pass

    @property
    def header(self) -> str:
        pass

    def write_header(self, filename: str):
        """ Writes the TikZ macros to the given file.
        """
        pass

    def make_grid(self, grid: figuregen.Grid, sizes: List[Tuple[float, float]], index: int):
        pass

    def combine_grids(self, data):
        pass

    def combine_rows(self, data):
        pass

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

def figure(grids: List[List[figuregen.Grid]], width_cm: float, filename: str, backend: Backend):
    if backend is None:
        backend = _backend_from_filename(filename)
    backend.generate(grids, width_cm * 10, filename)