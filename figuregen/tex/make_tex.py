import os
import shutil

from . import tikz
from . import calculate
from . import compile_tex
from . import combine_pdfs
from ..element_data import *

class Error(Exception):
    def __init__(self, message):
        self.message = message

class GridError(Exception):
    def __init__(self, row, col, message):
        self.message = f"Error in row {row}, column {col}: {message}"

def gen_content(data):
    '''
    Generates LaTeX/TikZ content, basically  like a body for html, which includes images and
    titles/captions as well as their positions, sizes, and other properties.
    '''
    # img/element blocks
    # Usually an img/block consists only of an image node (with or without frames) and some paddings between other image nodes.
    # However, it can also contain south captions, markers, labels, etc. - if so desired.
    content = tikz.gen_all_image_blocks(data)

    # titles that have content for each row or column
    content += tikz.add_col_and_row_titles(data)

    # figure title (positions around the figure facing: north, south, east, west)
    content += tikz.add_big_titles(data)

    # outer spacing
    content += tikz.add_all_outer_paddings(data)

    # write into json height and width
    data['total_height'] = calculate.get_total_height(data)
    data['total_width'] = calculate.get_total_width(data)

    return content

def begin_tikz_document(background_color):
    beginnig = '\\usetikzlibrary{backgrounds} \n'
    beginnig += '\\begin{document}\n'
    beginnig += '\\tikzstyle{background rectangle}=[fill='+ tikz.gen_tikZ_rgb255(background_color) + '] \n'
    beginnig += '\\begin{tikzpicture}[show background rectangle,inner frame sep=0pt]\n\n'
    return beginnig

def create_header(background_color, tex_packages):
    header = combine_pdfs.documentclass()

    # LaTeX package Error and Warning messages
    if not type(tex_packages) is list:
        raise Error('Figure generation: provided "tex_packages" needs to be of type list. '\
            r'Valid packages looks like ["{comment}", "[T1]{fontenc}"]. They do not include the prefix "\usepackage"!')
    if any(r"\usepackage" in e for e in tex_packages):
        raise Error('Figure generation: provided "tex_packages" contain somewhere the prefix '\
            r'"\usepackage". Valid packages looks like ["{comment}", "[T1]{fontenc}"].')
    # if tex_packages != ["[T1]{fontenc}", "{libertine}"]:
        # print('Info: You have included LaTeX-Packages: '+ str(tex_packages) +'. If you encounter problems, provide a "temp_folder", which contains all generated LaTeX output files (e.g. log) for easier debugging.')
    packs = ["{comment}", "{amsmath}", "{tikz}"] # "[T1]{fontenc}", "{libertine}"
    packs.extend(tex_packages)
    header += combine_pdfs.use_packages(packs)
    header += begin_tikz_document(background_color)
    return header

def write_into_tex_file(path, body_content, file_name, background_color, tex_packages):
    header = create_header(background_color, tex_packages)
    ending = '\n\\end{tikzpicture}\n\\end{document}'
    whole_content = header + body_content + ending

    f = open(os.path.join(path, file_name), 'w')
    f.write(whole_content)
    f.close()

def export_images(module, figure_idx, module_idx, path):
    for row in range(module["num_rows"]):
        for col in range(module["num_columns"]):
            elem = module["elements_content"][row][col]
            file = elem["image"]

            if isinstance(file, Plot):
                try:
                    filename = f'img-{row+1}-{col+1}-{figure_idx+1}-{module_idx+1}.pdf'
                    file_path = os.path.join(path, filename)
                    try:
                        file.make_pdf(module['element_config']['img_width'], module['element_config']['img_height'], file_path)
                    except NotImplementedError:
                        file_path.replace('.pdf', '.png')
                        file.make_png(module['element_config']['img_width'], module['element_config']['img_height'], file_path)
                except NotImplementedError:
                    raise GridError(row, col, 'Could not convert plot to .pdf!')

            elif isinstance(file, Image):
                if file.is_raster_image:
                    filename = f'img-{row+1}-{col+1}-{figure_idx+1}-{module_idx+1}.png'
                    file_path = os.path.join(path, filename)
                    file.convert2png(file_path)
                elif isinstance(file, PDF) or isinstance(file, PNG):
                    file_path = file.filename
                else:
                    raise Error('LaTeX backend only supports for images: ' \
                        'raw image data, PNG, or PDF files. HTML is not supported. Given file: '+ str(file))

            else:
                raise Error('LaTeX backend only supports for images: ' \
                        'raw image data, PNG, or PDF files. HTML is not supported. Given file: '+ str(file))

            elem["image"] = file_path

def generate(module_data, figure_idx, module_idx, temp_folder, tex_packages):
    '''
    tex_packages: valid packages looks like ["{comment}", "{amsmath}", "[T1]{fontenc}", "{libertine}"] (these are included per default).
    If you want to add a package, please also do not include "\\usepackage", but what comes afterwards.
    '''
    tex_filename = f'gen_tex{figure_idx:03d}-{module_idx:04d}.tex'
    pdf_filename = tex_filename.replace('tex', 'pdf')

    export_images(module_data, figure_idx, module_idx, path=temp_folder)
    content = gen_content(module_data)
    write_into_tex_file(temp_folder, content, tex_filename, background_color=module_data['background_color'], tex_packages=tex_packages)
    compile_tex.compile(temp_folder, tex_filename, pdf_filename)
    return pdf_filename

def combine(data, filename, temp_folder):
    combine_pdfs.make_pdf(temp_folder, data)
    gen = os.path.join(temp_folder, "gen_figure.pdf")
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    shutil.copy(gen, filename)