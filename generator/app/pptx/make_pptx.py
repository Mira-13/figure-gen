import os
from . import helper

def gen_content(data):
    # outer spacing, only upper and left 'needed'
    content += helper.add_all_outer_paddings(data, str_appendix)

    # upper and left
    # figure title (positions around the figure facing: north, south, east, west)
    content += helper.add_big_titles(data, str_appendix)

    # upper and left 
    # titles that have content for each row or column
    content += helper.add_col_and_row_titles(data, str_appendix)

    content = helper.gen_all_image_blocks(data, str_appendix)

    # right and bottom
    # titles that have content for each row or column
    content += helper.add_col_and_row_titles(data, str_appendix)

    # right and bottom
    # figure title (positions around the figure facing: north, south, east, west)
    content += helper.add_big_titles(data, str_appendix)

def put_into_slide(data):
    pass

    
    