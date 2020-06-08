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
    header_beginning = "<!DOCTYPE html><html>" + '\n' + '<head> <style type="text/css">' + '\n'
    module = '.module { position: absolute; }' + '\n'
    title_container = '.title-container { position: absolute; margin-top: 0; margin-bottom: 0; display: flex; align-items: center; justify-content: center}' + '\n'
    title_content = '.title-content { margin-top: 0; margin-bottom: 0; }' + '\n'
    element = '.element { position: absolute; }' + '\n'
    header_ending = '</style></head>' + '\n'
    return header_beginning + module + title_container + title_content + element + header_ending + '\n'
 
def gen_body_content(module_data, offset_top, offset_left):
    body = html_element.gen_module_unit_mm(module_data['total_width'], module_data['total_height'], offset_top, offset_left)
    body += html_element.gen_images(module_data)
    body += html_element.gen_titles(module_data)
    body += html_element.gen_row_titles(module_data)
    body += html_element.gen_column_titles(module_data)

    return body + '\n' + '</div>'

def generate(module_data, to_path, index, delete_gen_files=False):
    return module_data

def combine(data, to_path, delete_gen_files=False):
    html_code = html_header_and_styles() + '<body>' + '\n'

    offset_left = 0
    for d in data:
        html_code += gen_body_content(d, offset_top=0, offset_left=offset_left) + '\n'
        offset_left += d['total_width']

    html_code += '\n' + '</div></body></html>'

    with open(os.path.join(to_path, 'gen_html.html'), "w") as file:
        file.write(html_code)