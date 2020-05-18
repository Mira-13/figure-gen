import os
import json
import numpy
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
#from pptx.dml.fill import FillFormat
from pptx.dml.line import LineFormat
from pptx.dml.color import ColorFormat, RGBColor
from pptx.util import Inches, Pt
from . import calculate


def add_img_to_slide(slide, path, width_inch, pos_top, pos_left):
    slide.shapes.add_picture(path, Inches(pos_left), Inches(pos_top), width=Inches(width_inch))

def add_frame_on_top(slide, pos_top, pos_left, width_inch, height_inch, color, thickness_pt):
    slide.shapes.add_shape(
        #LineFormat(thickness_pt),
        #ColorFormat(RGBColor(color)),
        MSO_SHAPE.RECTANGLE, pos_left, pos_top, width_inch, height_inch
    )

def has_frame(rowIndex, colIndex):
    return False # TODO

def place_images_and_frames(slide, data, factor, offset_width_mm):
    '''
    Reads module data and puts images on the slide. 
    args:
        factor; is slide_width / figure_width, which is used to position elements on the slide accordingly
    '''
    width_inch, height_inch = calculate.img_size_inches(data, factor)

    rowIndex = 1
    for row in data['elements_content']:
        colIndex = 1
        if rowIndex <= data['num_rows']:
            for element in row:
                if colIndex <= data['num_columns']:
                    pos_top, pos_left = calculate.img_pos_for_slide(data, colIndex, rowIndex, factor, offset_left_mm=offset_width_mm)
                    add_img_to_slide(slide, element['filename'], width_inch, pos_top, pos_left)
                    #print(element['filename'], pos_top, pos_left)
                    if has_frame(rowIndex, colIndex):
                        add_frame_on_top(slide, color, thickness_pt, pos_top, pos_left, width_inch, height_inch)
                    colIndex += 1
            rowIndex += 1
    add_frame_on_top(slide, pos_top, pos_left, width_inch, height_inch, color=(40, 200, 10), thickness_pt=0.25)

def add_text(slide, content, rotation, fontsize, factor, pos_top, pos_left):
    pass # TODO

def place_titles(slide, data, factor):
    pass # TODO

def place_row_titles(slide, data, factor):
    pass # Todo

def place_col_titles(slide, data, factor):
    pass #Todo





