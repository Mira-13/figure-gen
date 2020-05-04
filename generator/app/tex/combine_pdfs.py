import glob
import os
from . import compile_tex

def create_header(list_packages):
    documentclass = "\\documentclass[varwidth=500cm, border=0pt]{standalone}\n"
    packages = ["{graphicx}", "[utf8]{inputenc}"]
    packages.extend(list_packages)
    usepackages = [r"\usepackage" + p + "\n" for p in packages]
    header = documentclass + ''.join(usepackages) + '\\begin{document}\n'
    return header 

def include_graphics(path, search_for_filenames):
    pattern = os.path.join(path, search_for_filenames)
    files = glob.glob(pattern)
    
    code = ['\includegraphics[]{' + f.replace('\\', '/') + '}%' for f in files]
    code.append('')
    body_content = '\n'.join(code)
    return body_content

def end_document():
    return '\end{document}'

def create_tex_file(content, path, filename):
    f = open(os.path.join(path, filename), 'w')
    f.write(content)
    f.close()

def make_pdf(path, search_for_filenames='gen_pdf*.pdf', list_packages=[]):
    header = create_header(list_packages)
    body = include_graphics(path, search_for_filenames)
    ending = end_document()
    content = header + body + ending
    tex_filename = 'gen_tex.tex'
    create_tex_file(content, path, filename=tex_filename)
    compile_tex.compile(path, tex_filename, pdf_filename='gen_figure.pdf')
    
