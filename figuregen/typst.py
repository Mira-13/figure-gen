from typing import Union
from .backend import *
import importlib.resources as pkg_resources
from concurrent.futures import ThreadPoolExecutor, Future

class TypstBackend(Backend):
    """ Generates Typst code for the figure.
    """

    def __init__(self, include_header=True):
        """
        Args:
            include_header: boolean, set to false to not include the macro definitions in the generated file.
        """
        self._include_header = include_header
        self._thread_pool = ThreadPoolExecutor()

    @property
    def header(self) -> str:
        """ The Typst macros used for the figure components """
        return pkg_resources.read_text(__package__, 'commands.typ')

    def _typst_color(self, rgb):
        if rgb is None:
            return "none"
        return f"rgb({rgb[0]},{rgb[1]},{rgb[2]})"

    def _make_image(self, c: ImageComponent, dims: str, output_dir: str, elem_id: str) -> str:
        # Generate the image data
        prefix = "img-" + elem_id
        file_prefix = os.path.join(output_dir, prefix)
        # TODO implement a make_svg() and use make_raster here only as a fallback
        filename = c.data.make_raster(c.bounds.width, c.bounds.height, file_prefix)
        filename = os.path.relpath(filename, output_dir) # Typst only accepts relative paths (and they must be next to or below the .typ file...)
        filename = str.replace(filename, "\\", "\\\\") # escape backslashes

        if c.has_frame:
            frame = f"{c.frame_linewidth}pt + {self._typst_color(c.frame_color)}"
        else:
            frame = "none"

        return f"place-image({dims}, \"{filename}\", stroke:{frame})"

    def assemble_grid(self, components: List[Component], output_dir: str) -> List[Union[Future, str]]:
        typst_lines = []
        for c in components:
            elem_id = f"fig{c.figure_idx}-grid{c.grid_idx}"
            if c.row_idx >= 0:
                elem_id += f"-row{c.row_idx}"
            if c.col_idx >= 0:
                elem_id += f"-col{c.col_idx}"

            # Position arguments are the same for all components
            if c.bounds is not None:
                dims = f"(width: {c.bounds.width:.2f}mm, height: {c.bounds.height:.2f}mm),(x: {c.bounds.left:.2f}mm, y: {c.bounds.top:.2f}mm)"

            if isinstance(c, ImageComponent):
                typst_lines.append(self._thread_pool.submit(self._make_image, c, dims, output_dir, elem_id))

            if isinstance(c, TextComponent):
                align = f"{c.horizontal_alignment}+{c.vertical_alignment}"
                padding = f"(x:{c.padding.width_mm}mm,y:{c.padding.height_mm}mm)"
                txt = str.replace(c.content, "\\", "\\\\") # escape backslashes
                txt = str.replace(txt, "\\\\\\\\", "\\n") # legacy convention support for LaTeX style line breaks
                typst_lines.append(f"text-box({dims},{self._typst_color(c.color)},{c.fontsize}pt,{self._typst_color(c.background_color)},-{c.rotation}deg,{align},{padding},\"{txt}\")")

            if isinstance(c, RectangleComponent):
                dash = "dashed" if c.dashed else "solid"
                typst_lines.append(f"clipped-rectangle({dims},stroke:(thickness: {c.linewidth}pt, paint: {self._typst_color(c.color)}, dash: \"{dash}\"),fill:none)")

            if isinstance(c, LineComponent):
                dash = "solid"
                typst_lines.append(f"clipped-line({dims},({c.from_x:.2f}mm, {c.from_y:.2f}mm),({c.to_x:.2f}mm, {c.to_y:.2f}mm),(thickness: {c.linewidth}pt, paint: {self._typst_color(c.color)}, dash: \"{dash}\"))")

        return typst_lines

    def combine_grids(self, data, idx: int, bounds: Bounds) -> List[Union[Future, str]]:
        result = []
        for grid in data:
            for d in grid:
                result.append(d)
        return result

    def combine_rows(self, data: List[List[Union[Future, str]]], bounds: Bounds) -> str:
        # Synchronize all export futures and combine the lines
        typst_code = f"#block(width:{bounds.width}mm,height:{bounds.height}mm,clip: true,{{"
        for fig in data:
            for c in fig:
                if isinstance(c, Future):
                    typst_code += c.result() + "\n"
                else:
                    typst_code += c + "\n"
        return typst_code + "})\n"

    def write_to_file(self, data: str, filename: str):
        with open(filename, "w") as f:
            if self._include_header:
                f.write(self.header)
                f.write("\n")
            f.write(data)