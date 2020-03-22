import os
import sys
import json

from .tex import compile_tex, make_tex

def run_create_figure(main_path, wd_path, module_path):
    script_name = 'create_figure.py'
    with open(os.path.join(main_path, 'app', 'logic', script_name), 'r') as f:
        src = f.read()
    compiled_script = compile(src, filename=os.path.join(main_path, 'app', 'logic', script_name), mode='exec')

    sys.path.append(main_path)
    import util
    sys.path.append(wd_path)
    import manage_images
    
    exec(compiled_script, {'util': util, 'manage_images': manage_images,'module_path': module_path, 
    'content_filename': 'gen_content.json'})

def create_tex_file(module_path, tex_filename):
    with open(os.path.join(module_path, 'gen_figure.json')) as json_file:
        data = json.load(json_file)

    content = make_tex.gen_content(data)
    make_tex.write_into_tex_file(module_path, content, tex_filename, background_color=data['background_color'])

def main():
    main_path = r'C:\Users\admin\Documents\MasterThesis\mtc\generator'
    wd_path = r'C:\Users\admin\Documents\MasterThesis\mtc\workDir'
    fig_path = os.path.join(wd_path, 'figures')
    module_path = os.path.join(fig_path, 'fig1', 'grid1')

    run_create_figure(main_path, wd_path, module_path)

    tex_filename = 'gen_tex_file.tex'
    create_tex_file(module_path, tex_filename)
    compile_tex.compile(module_path, tex_filename, pdf_filename='gen_pdf_file.pdf')

if __name__ == "__main__":
    main()

# fig_name, fig_module = str(sys.argv[1]), str(sys.argv[2])
# module_path = os.path.join(fig_path, fig_name, fig_module)