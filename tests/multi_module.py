import copy
import numpy as np
import pyexr
import single_module
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

# ---- Grid Module ----
grid0 = generator.Grid(1, 1)
grid0.get_layout().set_padding(right=0.5)
e0 = grid0.get_element(0,0).set_image(images[1])

# ---- Grid Module ----
grid1 = generator.Grid(2, 2)
layout1 = grid1.get_layout()
layout1.set_padding(top=0.5, bottom=1.5, right=0.5)

e1_1 = grid1.get_element(0,0).set_image(images[1])
e1_1.set_marker(pos=[32,12], size=[15,10], rgb=[242, 113, 250])
e1_1.set_marker_properties(1.)

e1_2 = grid1.get_element(0,1).set_image(images[0])
e1_2.set_frame(1., [50,230,10])
e1_2.set_caption('Yellow')

e1_4 = grid1.get_element(1,1).set_image(images[1])
e1_4.set_marker(pos=[32,12], size=[15,10], rgb=[242, 113, 250])
e1_4.set_marker_properties(1.)

e1_3 = grid1.get_element(1,0).set_image(images[0])
e1_3.set_frame(1., [50,230,10])
e1_3.set_caption('Yellow')

grid1.set_col_titles('south', ['Blue', 'Yellow'])
layout1.set_col_titles('south', field_size_mm=6.,bg_color=[[10, 10, 200], [255, 200, 10]])

grid1.set_row_titles('east', ['Awesome Pic 1', 'Awesome Pic 2'])
layout1.set_row_titles('east', field_size_mm=3. ,bg_color=[10, 10, 200])

grid1.set_title('north', 'North Title')


# ---- Grid Module ----
grid2 = single_module.grid


# ------ ALL ------
modules = [
    grid0,
    grid1,
    grid2
]

if __name__ == "__main__":
    generator.horizontal_figure(modules, width_cm=18., filename='multimodule_test.pdf')
    generator.horizontal_figure(modules, width_cm=18., filename='multimodule_test.pptx')
    generator.horizontal_figure(modules, width_cm=18., filename='multimodule_test.html')