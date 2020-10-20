import os
import shutil

from . import tikz
from . import calculate
from . import compile_tex
from . import combine_pdfs
from ..mplot import make_plot

class Error(Exception):
    def __init__(self, message):
        self.message = message

def gen_content(data, str_appendix=''):
    ''' TODO Describe me please

    A str_appendix is recommended if this script is used to combine the generated tikz code with another set of generated tikz code:
    Allowing to merge two or multiple generated tikz is somewhat in progress and I am not sure if and when this will be completely supported.
    '''
    # img/element blocks
    # Usually an img/block consists only of an image node (with or without frames) and some paddings between other image nodes.
    # However, it can also contain a complex subset of nodes (caption titles on each side) - if so desired.
    content = tikz.gen_all_image_blocks(data, str_appendix)

    # titles that have content for each row or column
    content += tikz.add_col_and_row_titles(data, str_appendix)

    # figure title (positions around the figure facing: north, south, east, west)
    content += tikz.add_big_titles(data, str_appendix)

    # outer spacing
    content += tikz.add_all_outer_paddings(data, str_appendix)

    # write into json height and width
    data['total_height'] = calculate.get_total_height(data)
    data['total_width'] = calculate.get_total_width(data)
    # print('total width of generated tikz module: ', data['total_width'])
    # print('total height of generated tikz module: ', data['total_height'])

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
        raise Error(r'Figure generation: provided "tex_packages" needs to be of type list. Valid packages looks like {comment}, [T1]{fontec}. They do not include the prefix "\usepackage"!')
    if any(r"\usepackage" in e for e in tex_packages):
        raise Error(r'Figure generation: provided "tex_packages" contain somewhere the prefix "\usepackage". Valid packages looks like ["{comment}", "[T1]{fontenc}"].')
    if tex_packages: # check if a list is not empty
        print('Warning: You have included LaTeX-Packages: '+ str(tex_packages) +'. If you encounter problems, provide a "temp_folder", which contains all generated LaTeX output files (e.g. log) for easier debugging.')
    packs = ["{comment}", "{amsmath}", "{tikz}", "[T1]{fontenc}", "{libertine}"]
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

def delete_gen_images(data):
    for row in data['elements_content']:
        for elem in row:
            os.remove(os.path.join(elem['filename']))


def generate(module_data, to_path, figure_idx, module_idx, temp_folder, tex_packages=[]):
    '''
    tex_packages: valid packages looks like ["{comment}", "{amsmath}", "[T1]{fontenc}", "{libertine}"] (these are included per default). 
    If you want to add a package, please also do not include "\\usepackage", but what comes afterwards. 
    '''
    tex_filename = f'gen_tex{figure_idx:03d}-{module_idx:04d}.tex'
    pdf_filename = tex_filename.replace('tex', 'pdf')

    if module_data['type'] == 'grid':
        content = gen_content(module_data)
        write_into_tex_file(temp_folder, content, tex_filename, background_color=module_data['background_color'], tex_packages=tex_packages)
        compile_tex.compile(temp_folder, tex_filename, pdf_filename)
    elif module_data['type'] == 'plot':
        make_plot.generate(module_data, temp_folder, pdf_filename)
    else:
        raise "unsupported module type '" + module_data['type'] + "'"
    
    return pdf_filename

def combine(data, filename, temp_folder):
    combine_pdfs.make_pdf(temp_folder, data)
    gen = os.path.join(temp_folder, "gen_figure.pdf")
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    shutil.copy(gen, filename)