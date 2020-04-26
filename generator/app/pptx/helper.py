import os
import json
import numpy
from pptx import Presentation
from pptx.util import Inches, Pt
# from . import calculate

'''
in PPTX format we ignore background colors and element captions (north/east/south/west content of each img) 
as we didn't even use them once before.
In addition, the frame option 'dashed' will not be supported in pptx - the frame will ne a normal frame instead. 
'''

#default slide size: 13.333 x 7.5 inch

module_path = 'C:/Users/admin/Documents/MasterThesis/mtc/workDir/figures/fig4/grid2/'
img_path = module_path + 'images/image-1-1.png'

with open(os.path.join(module_path, 'gen_figure.json')) as json_file:
    data = json.load(json_file)
    
def mm_to_inch(x):
    return x * 0.0393701 

def calculate_img_size_inches(data, factor):
    w = data['element_config']['img_width']
    h = data['element_config']['img_height']
    return mm_to_inch(w) * factor, mm_to_inch(h) * factor

def calculate_padding(space, offset):
    if space == 0.0:
        return 0.0
    return space + offset

def calculate_img_pos_for_slide(data, column, row, factor, offset_left_mm=0.0, offset_top_mm=0.0):
    img_width, img_height = calculate_img_size_inches(data, factor)
    title_top = calculate_padding(data['titles']['north']['height'], data['titles']['north']['offset'])
    title_left = calculate_padding(data['titles']['west']['width'], data['titles']['west']['offset'])
    col_title_top = calculate_padding(data['column_titles']['north']['height'], data['column_titles']['north']['offset'])
    row_title_left = calculate_padding(data['row_titles']['west']['width'], data['row_titles']['west']['offset'])
    top = offset_top_mm + data['padding']['top'] + title_top + col_title_top + (data['row_space'] + data['element_config']['img_height'])*(row-1)
    left = offset_left_mm + data['padding']['left'] + title_left + row_title_left + (data['column_space'] + data['element_config']['img_width'])*(column-1)
    return mm_to_inch(top) * factor, mm_to_inch(left) * factor

# def extract_img_col_and_row(img_path):
#     img_filename = img_path.split('/')[-1] # image-row-col.png
#     splitted_filename = (img_filename.replace('.png', '')).split('-') 
#     row = int(splitted_filename[1])
#     column = int(splitted_filename[2])
#     return column, row

factor = 10 / mm_to_inch(data['total_width'])
print(data['total_width'])
print(mm_to_inch(data['total_width']))
# height_factor = data['total_height'] / 7.5 if we use both the resolution of the images might be distorted

def get_images(slide, data, factor):
    '''
    Generates tikz nodes for each element/image based on the number of columns and rows
    '''
    width_inch, height_inch = calculate_img_size_inches(data, factor)

    img_matrix = numpy.zeros((data['num_columns'],data['num_rows']))
    rowIndex = 1
    for row in data['elements_content']:
        colIndex = 1
        if rowIndex <= data['num_rows']:
            for element in row:
                if colIndex <= data['num_columns']:
                    pos_top, pos_left = calculate_img_pos_for_slide(data, colIndex, rowIndex, factor)
                    slide.shapes.add_picture(element['filename'], Inches(pos_left), Inches(pos_top), width=Inches(width_inch))
                    print(element['filename'], pos_top, pos_left)
                    # img_matrix[colIndex-1][rowIndex-1] = ([element['filename'], element['frame'], element['insets'], 
                    #                                     calculate_img_pos_for_slide(data, colIndex, rowIndex, factor)])
                    colIndex += 1
            rowIndex += 1
    return img_matrix

# print(get_images(slide, data, factor)[0][0])

def place_image_on_slide(slide, img_path, pos_top, pos_left, width_inch, height_inch):
    pass
    

prs = Presentation()
# TODO set slide size (configurable by user?)
blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)

left = top = Inches(1)
path = r'C:\Users\admin\Documents\MasterThesis\mtc\workDir\figures\fig4\grid2\images\image-1-1.png '
pic = slide.shapes.add_picture(path, left, top, height=top)

get_images(slide, data, factor)

prs.save('test.pptx')

def gen_pptx_frame(img_sizes, pos_top, pos_left):
    pass

def gen_pptx_text(content, rotation, fontsize, pos_center):
    pass

def gen_pptx_img(path, width, height, pos_top, pos_left):
    pass

