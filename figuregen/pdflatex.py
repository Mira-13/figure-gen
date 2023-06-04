import tempfile
import os
import shutil
import subprocess
from .tikz import TikzBackend
from .backend import Backend, Component, Bounds
from typing import List

class PdfBackend(Backend):
    """
    Generates a TikZ picture and compiles it with pdflatex to a .pdf
    Requires pdflatex in the PATH.

    Currently only supports a single figure being created at a time. That is, multi-threaded applications
    need to create one PdfBackend object per figure. Further, if an intermediate directory is set, that directory
    cannot be the same for two figures that are created at the same time, as they might overwrite each other's files.
    """

    def __init__(self, intermediate_dir = None, preamble_lines=[ "\\usepackage[utf8]{inputenc}",
            "\\usepackage[T1]{fontenc}", "\\usepackage{libertine}" ]):
        self._custom_preamble = "\n".join(preamble_lines)
        self._tikz_gen = TikzBackend(False)

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

    @property
    def preamble(self) -> str:
        return '\n'.join([
            "\\documentclass[varwidth=500cm, border=0pt]{standalone}",
        ])

    def assemble_grid(self, components: List[Component], output_dir: str):
        return self._tikz_gen.assemble_grid(components, self._intermediate_dir)

    def combine_grids(self, data, idx: int, bounds: Bounds):
        return self._tikz_gen.combine_grids(data, idx, bounds)

    def combine_rows(self, data, bounds: Bounds):
        return self._tikz_gen.combine_rows(data, bounds)

    def write_to_file(self, data, filename):
        _, ext = os.path.splitext(filename)
        assert ext.lower() == ".pdf", "Filename should have .pdf extension!"

        tikz_filename = os.path.join(self._intermediate_dir, "figure.tikz")
        self._tikz_gen.write_to_file(data, tikz_filename)

        tex_code = "\n".join([
            self.preamble,
            self._custom_preamble,
            self._tikz_gen.preamble,
            self._tikz_gen.header,
            "\\begin{document}",
            "\\input{figure.tikz}",
            "\\end{document}",
        ])

        tex_filename = os.path.join(self._intermediate_dir, "figure.tex")
        pdf_filename = os.path.join(self._intermediate_dir, "figure.pdf")
        with open(tex_filename, "w") as f:
            f.write(tex_code)

        try:
            subprocess.check_call([
                    "pdflatex",
                    "-interaction=batchmode",
                    "figure.tex"
                ], cwd=self._intermediate_dir, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            from texsnip import extract_errors, red

            logfile = os.path.join(self._intermediate_dir, "figure.log")
            if not os.path.exists(logfile):
                print("Error: pdflatex failed, but no log was written.")
            else:
                print("Error: pdflatex failed with the following errors:")
                print("\n".join([errline for errline in extract_errors(logfile)]))
            print(red(f"Error: pdflatex failed. You can view the full log in {logfile}. "
                "This path can be changed by specifying an intermediate_dir"))

        shutil.copy(pdf_filename, filename)