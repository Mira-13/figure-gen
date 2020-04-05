import os
import sys
import json

from .tex import compile_tex, make_tex, calculate
from pdf2image import convert_from_path

def run_create_module(main_path, wd_path, module_path, is_img_res_based_on_width, is_img_res_based_on_height):
    '''
        Step 1) 
        create_figurePY takes the user input content.py and design_and_layout.json from a module(_path).
        It combines two data packs from those input files into one json file. 
        This json file contains all information to create a suitable tikz/tex file (step 2), that will
        represent one module.
        A module can be a part of a figure or the whole figure if so desired. 
    '''
    script_name = 'create_figure.py' # TODO maybe rename to create_module.py ?
    with open(os.path.join(main_path, 'app', 'logic', script_name), 'r') as f:
        src = f.read()
    compiled_script = compile(src, filename=os.path.join(main_path, 'app', 'logic', script_name), mode='exec')

    sys.path.append(main_path)
    import util
    sys.path.append(wd_path)
    import manage_images
    
    exec(compiled_script, {'util': util, 'manage_images': manage_images, 'calculate': calculate, 
    'module_path': module_path, 'content_filename': 'gen_content.json',
    'is_img_res_based_on_width': is_img_res_based_on_width, 'is_img_res_based_on_height': is_img_res_based_on_height})
    

def align_two_modules(main_path, wd_path, module_path1, module_path2):
    run_create_module(main_path, wd_path, module_path1)
    run_create_module(main_path, wd_path, module_path2)

    with open(os.path.join(module_path1, 'gen_figure.json')) as json_file:
        data1 = json.load(json_file)
    with open(os.path.join(module_path2, 'gen_figure.json')) as json_file:
        data2 = json.load(json_file)


def create_tex_file(module_path, tex_filename):
    '''
        Step 2)
        This one takes the data from step 1) and creates a corresponding tex file. This output will be used
        to compile it to an pdf/png etc (next step).
    '''
    with open(os.path.join(module_path, 'gen_figure.json')) as json_file:
        data = json.load(json_file)

    content = make_tex.gen_content(data)
    make_tex.write_into_tex_file(module_path, content, tex_filename, background_color=data['background_color'])

def main():
    main_path = r'C:\Users\admin\Documents\MasterThesis\mtc\generator'
    wd_path = r'C:\Users\admin\Documents\MasterThesis\mtc\workDir'
    fig_path = os.path.join(wd_path, 'figures')
    module_path = os.path.join(fig_path, sys.argv[1], sys.argv[2]) # e.g. 'fig1' 'grid1'

    tex_filename = 'gen_tex_file.tex'
    pdf_filename = 'gen_pdf_file.pdf'

    # options
    is_img_res_based_on_width=True 
    is_img_res_based_on_height=False
    
    # Create the module: (part of) a figure.
    # Step 1) combine user input to one json file, that contains all information needed
    run_create_module(main_path, wd_path, module_path, is_img_res_based_on_width, is_img_res_based_on_height)

    # Step 2) use output of step 1) and create a suitable tikz/tex file
    create_tex_file(module_path, tex_filename)

    # Step 3) use output of step 2) and compile the tex file to pdf ...
    compile_tex.compile(module_path, tex_filename, pdf_filename)
    # .. and png
    images = convert_from_path(pdf_path=os.path.join(module_path, pdf_filename), dpi=500)
    images[0].save(os.path.join(module_path, 'gen_png_file.png'))

if __name__ == "__main__":
    main()