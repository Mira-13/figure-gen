import subprocess
import sys
import os
from shutil import rmtree
from shutil import copy

def copy_pdf_file(tmp_folder_path, to_path, tex_filename, pdf_filename):
    old_pathfile = os.path.join(tmp_folder_path, tex_filename.replace('.tex', '.pdf'))
    new_pathfile = os.path.join(to_path, pdf_filename)

    # if to_path has already a pdf file, delete it, so it can be overwritten
    try:
        os.remove(new_pathfile)
    except:
        pass

    # get file and copy into other path
    copy(old_pathfile, new_pathfile)

def wslpath(path):
    return subprocess.check_output(['wsl', 'wslpath', '-a', path.replace('\\','\\\\')]).decode('utf8')[:-1]

def change_includegraphics_paths_based_on_os(pathfile):
    with open(pathfile, 'r') as f:
        content = f.read()

    import re
    content = re.sub(r'\\includegraphics\[([^\}]*)\]\{([^\}]*)\}', lambda match: '\\includegraphics[' + match.groups()[0] + ']{' + wslpath(match.groups()[1]) + '}', content) # braces (}) in filename not supported!

    with open(pathfile, 'w') as f:
        f.write(content)

def call_pdflatex(is_os_windows, is_latex_on_linux, tmp_path, filename):
    try:
        subprocess.check_call(['pdflatex', '-interaction=nonstopmode', filename], cwd=tmp_path,
            stdout=subprocess.DEVNULL) # TODO make this an option: piping to DEVNULL suppresses all LaTeX output
    except subprocess.CalledProcessError:
        pass # TODO handle pdflatex errors

def compile(module_path, tex_filename, pdf_filename, is_os_windows=True, is_latex_on_linux=False):
    '''
        Compiles a .tex file to .pdf
    arg 'pdf_filename' needs to include '.pdf'-ending
    Generates a temporary folder, where pdflatex will compile the output in in addition with it's default other files,
    copies only the generated pdf file into the same path where the .tex file lies and delete the tmp folder afterwards.
    '''
    call_pdflatex(is_os_windows, is_latex_on_linux, module_path, tex_filename)
    copy_pdf_file(module_path, module_path, tex_filename, pdf_filename)
