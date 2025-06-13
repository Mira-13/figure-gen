import subprocess
from .backend import *
from .typst import TypstBackend

class SvgBackend(Backend):
    """
    Generates a Typst version of the figure and compiles it to .svg
    Requires typst in the PATH.

    Currently only supports a single figure being created at a time. That is, multi-threaded applications
    need to create one PdfBackend object per figure. Further, if an intermediate directory is set, that directory
    cannot be the same for two figures that are created at the same time, as they might overwrite each other's files.
    """

    def __init__(self, intermediate_dir = None, preamble_lines: List[str] = [ "#set text(font: \"Linux Biolinum\")" ]):
        self._typst_gen = TypstBackend()

        self._preamble = "\n".join(preamble_lines) + "\n" + "#set page(width: auto, height: auto, margin: 0pt, fill: none)"

        if intermediate_dir is not None:
            self._temp_folder = None
            self._intermediate_dir = intermediate_dir
            os.makedirs(intermediate_dir, exist_ok=True)
        else:
            self._temp_folder = tempfile.TemporaryDirectory()
            self._intermediate_dir = self._temp_folder.name

    def __del__(self):
        if self._temp_folder is not None:
            self._temp_folder.cleanup()
            self._temp_folder = None

    def assemble_grid(self, components: List[Component], output_dir: str):
        return self._typst_gen.assemble_grid(components, self._intermediate_dir)

    def combine_grids(self, data, idx: int, bounds: Bounds):
        return self._typst_gen.combine_grids(data, idx, bounds)

    def combine_rows(self, data, bounds: Bounds):
        return self._typst_gen.combine_rows(data, bounds)

    def write_to_file(self, data, filename):
        _, ext = os.path.splitext(filename)
        assert ext.lower() == ".svg", "Filename should have .svg extension!"

        typ_filename = os.path.join(self._intermediate_dir, "figure.typ")
        self._typst_gen.write_to_file(data, typ_filename)

        with open(typ_filename, "r") as f:
            typ_code = f.read()
        with open(typ_filename, "w") as f:
            typ_code = f.write(self._preamble + "\n" + typ_code)

        svg_filename = os.path.join(self._intermediate_dir, "figure.svg")

        try:
            subprocess.check_call([
                    "typst",
                    "c",
                    "figure.typ",
                    "-f", "svg"
                ], cwd=self._intermediate_dir, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print(f"Error: Typst compilation failed. Try specifying an `intermediate_dir` to manually compile and check.")

        shutil.copy(svg_filename, filename)