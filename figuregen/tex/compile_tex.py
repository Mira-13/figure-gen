import subprocess
import os
from shutil import copy

def copy_pdf_file(tmp_folder_path, to_path, tex_filename, pdf_filename):
    old_filename = os.path.join(tmp_folder_path, tex_filename.replace('.tex', '.pdf'))
    new_filename = os.path.join(to_path, pdf_filename)

    # if to_path has already a pdf file, delete it, so it can be overwritten
    try:
        os.remove(new_filename)
    except:
        pass

    # get file and copy into other path
    copy(old_filename, new_filename)

def call_pdflatex(tmp_path, filename):
    subprocess.check_call(['pdflatex', '-interaction=nonstopmode', filename], cwd=tmp_path, stdout=subprocess.DEVNULL)

def compile(module_path, tex_filename, pdf_filename):
    '''
        Compiles a .tex file to .pdf
    arg 'pdf_filename' needs to include '.pdf'-ending
    Generates a temporary folder, where pdflatex will compile the output in in addition with it's default other files,
    copies only the generated pdf file into the same path where the .tex file lies and delete the tmp folder afterwards.
    '''
    call_pdflatex(module_path, tex_filename)
    copy_pdf_file(module_path, module_path, tex_filename, pdf_filename)
