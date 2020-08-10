import pyexr
import numpy as np
import generator
import generator.util

# generate test images
blue = np.tile([0.2,0.3,0.9], (32, 64, 1))
yellow = np.tile([0.9,0.8,0.2], (32, 64, 1))
pyexr.write("images//blue.exr", blue)
pyexr.write("images//yellow.exr", yellow)

# load the two images
images = [
    generator.util.image.lin_to_srgb(pyexr.read("images//blue.exr")),
    generator.util.image.lin_to_srgb(pyexr.read("images//yellow.exr"))
]

# ------ create 'empty' Grid with num_rows, num_cols ---------
grid = generator.Grid(2, 3)
layout = grid.get_layout()
layout.set_padding(top=0.5, bottom=1.5)

# fill grid with image data
e1 = grid.get_element(0,0).set_image(images[0])
e2 = grid.get_element(0,1).set_image(images[1])
e3 = grid.get_element(0,2).set_image(images[0])
e4 = grid.get_element(1,0).set_image(images[1])
e5 = grid.get_element(1,1).set_image(images[0])
e6 = grid.get_element(1,2).set_image(images[1])

# marker (default marker props)
e1.set_marker([32,12], [15,10], [242, 113, 250])
e1.set_marker([1,1], [15,10], [50,230,10])

# frame
e2.set_frame(linewidth=2., rgb=[50,230,10])

# subtitles for specific elements
e1.set_caption('hallo!')
e2.set_caption('und')
e3.set_caption('tschau!tschau!')
e4.set_caption('hallo!')
e5.set_caption('und')
e6.set_caption('tschau!tschau!')
layout.set_caption(height_mm=4.0, fontsize=9, txt_color=[33,113,12])

# labels (2 examples, each element can have in total 6 labels on each valid position)
e1.set_label("hey", pos='bottom_center', width_mm=6., height_mm=4.0, offset_mm=[1.0, 1.0], 
                  fontsize=9, bg_color=[255,255,255])
e1.set_label("hoh", pos='top_right', width_mm=6., height_mm=4.0, offset_mm=[1.0, 1.0], 
                  fontsize=9, bg_color=[255,255,255])

# grid specific titles
grid.set_title('top', 'My Title')
layout.set_title('top', 4., offset_mm=2.,fontsize=12, bg_color=[133,213,112])

grid.set_title('left', 'My Title')
layout.set_title('left', 4., offset_mm=2.,fontsize=12, bg_color=[133,213,112])

# Row and column titles
grid.set_row_titles('left', ['Row Title', 'are', 'The Best'])
layout.set_row_titles('left', 10., offset_mm=1., fontsize=9, txt_rotation=0, bg_color=[[200, 180, 220],[133,213,112]])

grid.set_col_titles('north', ['Col Titles', 'are', 'The Best'])
#layout.set_col_titles('north', 10., offset_mm=1., fontsize=9, bg_color=[200, 180, 220])

if __name__ == "__main__":
    generator.horizontal_figure([grid], width_cm=28., filename='singlemodule_test.pdf')
    generator.horizontal_figure([grid], width_cm=28., filename='singlemodule_test.pptx')
    generator.horizontal_figure([grid], width_cm=28., filename='singlemodule_test.html')