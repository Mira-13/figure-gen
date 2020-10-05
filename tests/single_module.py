import pyexr
import numpy as np
import figuregen
import figuregen.util

colors = [ 
    [232, 181, 88], #yellow
    [5, 142, 78], #green
    [94, 163, 188], #light-blue
    [181, 63, 106], #pink
    [82, 110, 186], #blue
    [186, 98, 82] #orange-crab
]

# generate test images
blue = np.tile([x / 255 for x in colors[2]], (32, 64, 1))
yellow = np.tile([x / 255 for x in colors[0]], (32, 64, 1))
pyexr.write("images/blue.exr", blue)
pyexr.write("images/yellow.exr", yellow)

# load the two images
images = [
    figuregen.util.image.lin_to_srgb(pyexr.read("images/blue.exr")),
    figuregen.util.image.lin_to_srgb(pyexr.read("images/yellow.exr"))
]

# ------ create 'empty' Grid with num_rows, num_cols ---------
grid = figuregen.Grid(2, 3)
layout = grid.get_layout()
layout.set_padding(top=0.5, bottom=1.5)

# fill grid with image data
e1 = grid.get_element(0,0).set_image(images[0])
e2 = grid.get_element(0,1).set_image(images[1])
e3 = grid.get_element(0,2).set_image(images[0])
e4 = grid.get_element(1,0).set_image(images[1])
e5 = grid.get_element(1,1).set_image(images[0])
e6 = grid.get_element(1,2).set_image(images[1])

# marker
e1.set_marker(pos=[32,12], size=[15,10], color=colors[4])
e1.set_marker(pos=[1,1], size=[15,10], color=colors[-1], linewidth_pt=0.6, is_dashed=True)

# frame
e2.set_frame(linewidth=2., color=colors[4])

# subtitles for specific elements
e1.set_caption('hallo!')
e2.set_caption('und')
e3.set_caption('tschau!tschau!')
e4.set_caption('hallo!')
e5.set_caption('und')
e6.set_caption('tschau!tschau!')
layout.set_caption(height_mm=4.0, fontsize=9, txt_color=[170,170,170])

# labels (examples, each element can have in total 6 labels on each valid position)
e4.set_label("bottom center", pos='bottom_center', width_mm=25., height_mm=4.0, offset_mm=[1.0, 1.0], 
                  fontsize=9, bg_color=None)
e4.set_label("top\\\\right", pos='top_right', width_mm=8., height_mm=7.0, offset_mm=[1.0, 1.0], 
                  fontsize=9, bg_color=[255,255,255])
e4.set_label("top\\\\left", pos='top_left', width_mm=8., height_mm=7.0, offset_mm=[1.0, 1.0], 
                  fontsize=9, bg_color=colors[-1], txt_color=[255,255,255])

# grid specific titles
grid.set_title('top', 'Top Title')
layout.set_title('top', 5., offset_mm=2.,fontsize=12, bg_color=colors[5], txt_color=[255,255,255])

grid.set_title('left', 'Left Title')
layout.set_title('left', 4., offset_mm=2.,fontsize=12)

# Row and column titles
grid.set_row_titles('left', ['Row Titles', 'are better'])
layout.set_row_titles('left', 10., offset_mm=1., fontsize=9, txt_rotation=0, bg_color=[colors[4],colors[2]])

grid.set_col_titles('north', ['Col Titles', 'are', 'The Best'])
#layout.set_col_titles('north', 10., offset_mm=1., fontsize=9, bg_color=[200, 180, 220])

if __name__ == "__main__":
    figuregen.horizontal_figure([grid], width_cm=28., filename='singlemodule_test.pdf')
    figuregen.horizontal_figure([grid], width_cm=28., filename='singlemodule_test.pptx')
    figuregen.horizontal_figure([grid], width_cm=28., filename='singlemodule_test.html')