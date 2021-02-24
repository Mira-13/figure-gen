from typing import Union
from .backend import *
import importlib.resources as pkg_resources
from concurrent.futures import ThreadPoolExecutor, Future

class TikzBackend(Backend):
    """ Generates the code for a TikZ picture representing the figure.
    Default file ending is .tikz, use \\input{figure.tikz} to include in LaTeX.
    """

    def __init__(self, include_header=True):
        """
        Args:
            include_header: boolean, set to false to not include the macro definitions in the generated file.
        """
        self._include_header = include_header
        self._thread_pool = ThreadPoolExecutor()

    def add_overlay(self, tikz_code: str):
        """ Adds overlay code that will be stitched on top of the generated figure. """
        pass

    @property
    def header(self) -> str:
        """ The TikZ macros used for the figure components """
        return pkg_resources.read_text(__package__, 'commands.tikz')

    @property
    def preamble(self) -> str:
        """ The minimum set of \\usepackage's for the figure to display correctly. """
        return '\n'.join(["\\usepackage{calc}", "\\usepackage{tikz}"])

    def _sanitize_latex_path(self, path):
        # Assume that pdflatex will be run from the same folder and strip the directory name from the path
        return "\\detokenize{" + os.path.basename(path) + "}"

    def _latex_color(self, rgb):
        if rgb is None:
            return ""
        return "rgb,255:red," + str(rgb[0]) + ";green," + str(rgb[1]) + ";blue," + str(rgb[2])

    def _make_image(self, c: ImageComponent, dims: str, anchor: str, output_dir: str, elem_id: str) -> str:
        # Generate the image data
        prefix = "img-" + elem_id
        file_prefix = os.path.join(output_dir, prefix)
        try:
            filename = c.data.make_pdf(c.bounds.width, c.bounds.height, file_prefix)
        except NotImplementedError:
            filename = c.data.make_raster(c.bounds.width, c.bounds.height, file_prefix)

        # Assemble the position arguments
        fname = "{" + self._sanitize_latex_path(filename) + "}"
        name = "{" + prefix + "}"

        # Check if there is a frame and emit the correct command
        if c.has_frame:
            linewidth = "{" + f'{c.frame_linewidth}pt' + "}"
            color = "{" + self._latex_color(c.frame_color) + "}"
            return "\\makeframedimagenode" + dims + fname + name + anchor + color + linewidth + "\n"
        else:
            return "\\makeimagenode" + dims + fname + name + anchor + "\n"

    def assemble_grid(self, components: List[Component], output_dir: str) -> List[Union[Future, str]]:
        tikz_lines = []
        for c in components:
            elem_id = f"fig{c.figure_idx}-grid{c.grid_idx}"
            if c.row_idx >= 0:
                elem_id += f"-row{c.row_idx}"
            if c.col_idx >= 0:
                elem_id += f"-col{c.col_idx}"

            # Position arguments are the same for all components
            if c.bounds is not None:
                dims = "{" + f"{c.bounds.width}" + "mm}" + "{" + f"{c.bounds.height}" + "mm}"
                anchor = "{(" + f"{c.bounds.left}mm, {-c.bounds.top}mm" + ")}"

            if isinstance(c, ImageComponent):
                tikz_lines.append(self._thread_pool.submit(
                    self._make_image, c, dims, anchor, output_dir, elem_id))

            if isinstance(c, TextComponent):
                prefix = c.type + "-" + elem_id
                name = "{" + prefix + "}"
                fontsize = "{" + f'{c.fontsize}pt' + "}"
                color = "{" + self._latex_color(c.color) + "}"
                content = "{" + c.content + "}"
                rotation = "{" + str(c.rotation) + "}"
                fill_color = "{" + self._latex_color(c.background_color) + "}"

                node = "\\maketextnode" if c.rotation % 180 < 20 else "\\maketextnodeflipped"

                vert_align = "{c}"
                if c.vertical_alignment == "top":
                    vert_align = "{t}"
                elif c.vertical_alignment == "bottom":
                    vert_align = "{b}"

                horz_align = "{\\centering}"
                if c.horizontal_alignment == "left":
                    horz_align = "{\\raggedright}"
                elif c.horizontal_alignment == "right":
                    horz_align = "{\\raggedleft}"

                pad_vert = "{" + str(c.padding.height_mm) + "mm}"
                pad_horz = "{" + str(c.padding.width_mm) + "mm}"

                tikz_lines.append(node + dims + name + anchor + color + fontsize + fill_color + rotation +
                    vert_align + horz_align + pad_vert + pad_horz + content)

            if isinstance(c, RectangleComponent):
                color = "{" + self._latex_color(c.color) + "}"
                linewidth = "{" + str(c.linewidth) + "pt}"
                linestyle = "{dashed}" if c.dashed else "{solid}"
                tikz_lines.append("\\makerectangle" + dims + anchor + color + linewidth + linestyle)

            if isinstance(c, LineComponent):
                parent_name = "{" + "img-" + elem_id + "}"
                color = "{" + self._latex_color(c.color) + "}"
                linewidth = "{" + str(c.linewidth) + "pt}"
                start = "{" + f"({c.from_x}mm, {-c.from_y}mm)"+ "}"
                end = "{" + f"({c.to_x}mm, {-c.to_y}mm)"+ "}"
                tikz_lines.append("\\makeclippedline" + parent_name + start + end + linewidth + color)

        return tikz_lines

    def combine_grids(self, data, idx: int, bounds: Bounds) -> List[Union[Future, str]]:
        # Create an empty "background" node to make sure that outer paddings are not cropped away
        figure_id = "{figure-" + str(idx) + "}"
        dims = "{" + f"{bounds.width}" + "mm}" + "{" + f"{bounds.height}" + "mm}"
        anchor = "{(" + f"{bounds.left}mm, {-bounds.top}mm" + ")}"
        tikz_code = "\\makebackgroundnode" + dims + anchor + figure_id + "\n"

        # Flatten the list of list into a single list with one element per component
        result = [tikz_code]
        for grid in data:
            for d in grid:
                result.append(d)
        return result

    def combine_rows(self, data: List[List[Union[Future, str]]], bounds: Bounds) -> str:
        # Synchronize all export futures and combine the lines
        tikz_code = ""
        for fig in data:
            for c in fig:
                if isinstance(c, Future):
                    tikz_code += c.result() + "\n"
                else:
                    tikz_code += c + "\n"
        return tikz_code

    def write_to_file(self, data: str, filename: str):
        with open(filename, "w") as f:
            if self._include_header:
                f.write(self.header)
                f.write("\n")
            f.write("\\begin{tikzpicture}\n")
            f.write(data)
            f.write("\\end{tikzpicture}")