from .backend import *

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
        """ Adds overlay code that will be stitched on top of the generated figure. """
        pass

    @property
    def header(self) -> str:
        """ The TikZ macros used for the figure components """
        return ""

    def _sanitize_latex_path(self, path):
        p = path.replace('\\', '/')
        return "\\detokenize{" + p + "}"

    def assemble_grid(self, components: List[Component], output_dir: str) -> str:
        tikz_code = ""
        for c in components:
            if isinstance(c, ImageComponent):
                # Generate the image data
                prefix = f'img-fig{c.figure_idx}-grid{c.grid_idx}-row{c.row_idx}-col{c.col_idx}'
                prefix = os.path.join(output_dir, prefix)
                try:
                    filename = c.data.make_pdf(c.bounds.width, c.bounds.height, prefix)
                except NotImplementedError:
                    filename = c.data.make_raster(c.bounds.width, c.bounds.height, prefix)

                # Emit the command
                tikz_code += "\\makeimagenode{" + self._sanitize_latex_path(filename) + "}\n"
        return tikz_code

    def combine_grids(self, data: List[str]) -> str:
        return '\n'.join(data)

    def combine_rows(self, data: List[str]) -> str:
        return '\n'.join(data)

    def write_to_file(self, data: str, filename: str):
        with open(filename, "w") as f:
            if self._include_header:
                f.write(self.header)
                f.write("\n")
            f.write(data)