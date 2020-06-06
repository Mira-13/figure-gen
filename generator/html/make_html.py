import os
import json
from . import html_element
'''
in HTML format we 
 - ignore background colors (for now)
 - ignore element captions (north/east/south/west content of each img) as we didn't even use them once before
 - do not support 'dashed' frames - if a frame is 'dashed' the frame will be normal (but still has a frame)
 - only support text rotation by 0° and +-90°
''' 
def html_header_and_styles():
    header_beginning = '<head> <style type="text/css">' + '\n'
    module = '.module { position: absolute; }' + '\n'
    title_container = '.title-container { position: absolute; margin-top: 0; margin-bottom: 0; display: flex; align-items: center; justify-content: center}' + '\n'
    title_content = '.title-content { margin-top: 0; margin-bottom: 0; }' + '\n'
    element = '.element { position: absolute; }' + '\n'
    header_ending = '</style></head>' + '\n'
    return header_beginning + module + title_container + title_content + element + header_ending + '\n'
    

def generate(module_data, to_path, index, delete_gen_files=False):
    html_code = "<!DOCTYPE html><html>" + '\n'
    html_code += html_header_and_styles() + '<body>' + '\n'

    # generate content
    html_code += html_element.gen_module_unit_mm(module_data['total_width'], module_data['total_height'])
    html_code += html_element.gen_images(module_data)
    html_code += html_element.gen_titles(module_data)
    html_code += html_element.gen_row_titles(module_data)
    html_code += html_element.gen_column_titles(module_data)

    html_code += '\n' + '</div></body></html>'
    with open(os.path.join(to_path, 'gen_html'+str(index)+'.html'), "w") as file:
        file.write(html_code)

def combine(data, to_path, delete_gen_files=False):
    # TODO
    for d in data:
        pass