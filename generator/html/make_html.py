import os
import json
from . import html_element
'''
in HTML format we 
 - ignore background colors
 - ignore element captions (north/east/south/west content of each img) as we didn't even use them once before
 - do not support 'dashed' frames - if a frame is 'dashed' the frame will be normal (but still has a frame)
 - only support text rotation by 0° and +-90°
''' 

def generate(module_data, to_path, index, delete_gen_files=False):
    html_code = ""

    # generate content
    html_code += html_element.gen_images(module_data['elements_content'])
    html_code += html_element.gen_titles(module_data['titles'])

    with open(os.path.join(to_path, filename), "w") as file:
        file.write(html_code)

def combine(data, to_path, delete_gen_files=False):
    # TODO
    for d in data:
        pass