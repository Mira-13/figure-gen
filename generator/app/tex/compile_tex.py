import subprocess
import sys
import os
from shutil import rmtree
from shutil import copy

def gen_tmp_folder(path):
    try: 
        tmp_folder_path = os.path.join(path, 'tmp')
        os.makedirs(tmp_folder_path)
    except OSError:
        rmtree(tmp_folder_path)
        os.makedirs(tmp_folder_path)
    return tmp_folder_path

def copy_pdf_file(tmp_folder_path, to_path, tex_filename, pdf_filename):
    tex_filename = tex_filename.replace('.tex', '.pdf') # already compiled so tex -> pdf
    old_pathfile = os.path.join(tmp_folder_path, tex_filename)
    new_pathfile = os.path.join(to_path, pdf_filename)

    # if to_path has already a pdf file, delete it, so it can be overwritten
    try:
        os.remove(new_pathfile)
    except:
        print("File already deleted or did not exist in the first place ", new_pathfile)

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

def call_pdflatex(is_os_windows, is_latex_on_linux, tmp_path, pathfile):
    # TODO try to write code for each case (win/lin)
    # TODO handle pdflatex errors 
    if is_os_windows and is_latex_on_linux:
        # call pdflatex ('wsl', '-e',)
        try:
            subprocess.check_call(['wsl', '-e', 'pdflatex', '-interaction=nonstopmode', '-output-directory=' + tmp_path, pathfile])
        except subprocess.CalledProcessError:
            pass 
    elif is_os_windows: # TODO test it
        try:
            subprocess.check_call(['pdflatex', '-interaction=nonstopmode', '-output-directory=' + tmp_path, pathfile])
        except subprocess.CalledProcessError:
            pass # TODO handle pdflatex errors
    else: # os and latex on linux (we do not consider os_lin but not latex on lin)
        # TODO
        pass

def compile(module_path, tex_filename, pdf_filename, is_os_windows=True, is_latex_on_linux=False): 
    '''
        Compiles a .tex file to .pdf
    Generates a temporary folder, where pdflatex will compile the output in in addition with it's default other files,
    copies only the generated pdf file into the same path where the .tex file lies and delete the tmp folder afterwards.
    '''
    # TODO cases for windows/linux
    pathfile = os.path.join(module_path, tex_filename)
    tmp_path = gen_tmp_folder(module_path)
    os_tmp_path = tmp_path # just in case

    if is_os_windows and is_latex_on_linux:
        change_includegraphics_paths_based_on_os(pathfile)
        pathfile = wslpath(pathfile)
        tmp_path = wslpath(tmp_path)

    call_pdflatex(is_os_windows, is_latex_on_linux, tmp_path, pathfile)

    # copy generated pdf file out of temporary folder
    copy_pdf_file(os_tmp_path, module_path, tex_filename, pdf_filename)
    # delete tmp folder
    rmtree(os_tmp_path)

if __name__ == "__main__":
    compile(module_path, tex_filename, pdf_filename)