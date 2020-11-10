import os
from ..mplot import make_plot
from pptx import Presentation
from pptx.util import Inches
from . import place_element, calculate

'''
in PPTX format we
 - ignore background colors
 - For now, allow ONLY south captions for each img: we ignore element captions of north/east/west content of each img as we didn't even use them once before
 - do not support 'dashed' frames - if a frame is 'dashed' the frame in pptx will be normal (but still has a frame)
 - only support text rotation by 0° and +-90° (this is a limitation of python-pptx)
'''

class Error(Exception):
    def __init__(self, message):
        self.message = message

def export_images(module, figure_idx, module_idx, path):
    for row in range(module["num_rows"]):
        for col in range(module["num_columns"]):
            elem = module["elements_content"][row][col]
            file = elem["image"]

            if file.is_raster_image or file.img_type == 'PDF': #export to png
                filename = f'img-{row+1}-{col+1}-{figure_idx+1}-{module_idx+1}.png'
                file_path = os.path.join(path, filename)
                file.convert2png(file_path)
            elif file.img_type == 'PNG':
                file_path = file.filename
            else:
                raise Error('PPTX backend only supports for images: ' \
                    'raw image data, PNG, or PDF files. HTML is not supported. Given file: '+ str(file))

            elem["image"] = file_path

def generate(module_data, figure_idx, module_idx, temp_folder, delete_gen_files=True, tex_packages=[]):
    if module_data['type'] == 'grid':
        export_images(module_data, figure_idx, module_idx, path=temp_folder)
    return module_data

def place_modules(data, to_path, slide):
    offset_top_mm = 0
    for fig_idx in range(len(data)):
        cur_width_mm = 0
        idx = 0
        for d in data[fig_idx]:
            if d['type'] == 'plot':
                plot_png = os.path.join(to_path, f"plot{idx}.png")
                make_plot.generate(d, to_path, f"plot{idx}.png")
                place_element.add_image(slide, plot_png, calculate.mm_to_inch(d['total_width']), calculate.mm_to_inch(offset_top_mm), calculate.mm_to_inch(cur_width_mm))
                idx += 1
            else:
                place_element.images_and_frames_and_labels(slide, d, 1, cur_width_mm, offset_top_mm)
                place_element.titles(slide, d, 1, cur_width_mm, offset_top_mm)
                place_element.row_titles(slide, d, 1, cur_width_mm, offset_top_mm)
                place_element.col_titles(slide, d, 1, cur_width_mm, offset_top_mm)
                place_element.south_captions(slide, d, 1, cur_width_mm, offset_top_mm)
            cur_width_mm += d['total_width']
        offset_top_mm += data[fig_idx][0]['total_height']

def combine(data, filename, temp_folder, delete_gen_files=True):
    to_path = os.path.dirname(filename)

    # calculate correct width scaling so that the figure fills out the slide
    sum_total_width_mm = 0
    for d in data[0]:
        sum_total_width_mm += d['total_width']

    figure_height = 0.
    for d in data:
        figure_height += d[0]['total_height']
    
    if figure_height < 25.4: # mm
        figure_height = 25.4
        print("Warning: pptx computed height is less than the minimum of 2,54cm. The slide heights will be set on 2,54cm.")

    #create slide
    prs = Presentation()
    prs.slide_height = Inches(calculate.mm_to_inch(figure_height))
    prs.slide_width = Inches(calculate.mm_to_inch(sum_total_width_mm))
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # place modules and their corresponding elements
    place_modules(data, to_path, slide)

    # save
    prs.save(filename)