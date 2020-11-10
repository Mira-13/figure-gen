import figuregen
import numpy as np
import single_module

# generate test images
blue = np.tile([0.2,0.3,0.9], (32, 32, 1))
yellow = np.tile([0.9,0.8,0.2], (32, 32, 1))

# load the two images
images = [
    figuregen.PNG(raw=blue),
    figuregen.PNG(raw=yellow)
]

# ---- Grid Module ----
grid0 = figuregen.Grid(1, 1)
grid0.get_layout().set_padding(right=0.5)
e0 = grid0.get_element(0,0).set_image(images[1])
e0.set_frame(0.3, [0,0,0])
e0.set_marker(pos=[2,12], size=[10,10], color=[155, 155, 155], linewidth_pt=0.6)
e0.set_marker(pos=[15,1], size=[10,15], color=[186, 98, 82], linewidth_pt=0.6)

# ---- Grid Module ----
grid1 = figuregen.Grid(2, 2)
layout1 = grid1.get_layout()
layout1.set_padding(top=0.2, right=0.5)

# fill grid with image data
for row in range(2):
    for col in range(2):
        img = images[col]
        e = grid1.get_element(row,col).set_image(img)
        e.set_frame(0.3, [0,0,0])

grid1.set_col_titles('south', ['Blue', 'Yellow'])
layout1.set_col_titles('south', field_size_mm=4., offset_mm=0.2, bg_color=[[200, 200, 255], [255, 255, 200]])

grid1.set_row_titles('east', ['Awesome 1', 'Awesome 2'])
layout1.set_row_titles('east', field_size_mm=3. ,bg_color=[186, 98, 82], txt_color=[255,255,255])

grid1.set_title('north', 'Top Title')


# ---- Grid Module ----
grid2 = single_module.grid


# ------ ALL ------
modules = [
    grid0,
    grid1,
    grid2
]

if __name__ == "__main__":
    figuregen.horizontal_figure(modules, width_cm=18., filename='multimodule_test.pdf')
    figuregen.horizontal_figure(modules, width_cm=18., filename='multimodule_test.pptx')
    figuregen.horizontal_figure(modules, width_cm=18., filename='multimodule_test.html')