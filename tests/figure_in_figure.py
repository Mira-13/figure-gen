import figuregen
import os
import numpy as np
import vertical_stack

# Note: LaTeX and PPTX-backend do not support html files
# if test_html is True, we only generate the figure with the html backend
test_html = False

# PNG test
blue=[82, 110, 186]
img_blue = np.tile([x / 255 for x in blue], (32, 32, 1))
img_png = figuregen.PNG(raw=img_blue)

if test_html:
    # HTML test
    figuregen.figure(vertical_stack.v_grids, width_cm=15., filename='v-stacked.html')
    htmlfile = os.path.abspath('v-stacked.html')
    img_test = figuregen.HTML(htmlfile, aspect_ratio=0.3)
else:
    # PDF test
    figuregen.figure(vertical_stack.v_grids, width_cm=15., filename='v-stacked.pdf')
    pdffile = os.path.abspath('v-stacked.pdf')
    img_test = figuregen.PDF(pdffile)

images = [
    img_test, 
    img_png, 
]

# ---- GRIDS ----
grid = figuregen.Grid(1, 1)
grid.get_layout().set_padding(right=1.5, bottom=1.0)
e1 = grid.get_element(0,0).set_image(images[0])

grid2 = figuregen.Grid(1, 1)
e2 = grid2.get_element(0,0).set_image(images[1])
grid2.get_layout().set_padding(bottom=1.0)

all_grids = [
    [grid, grid],
    [grid, grid2]
]

if __name__ == "__main__":
    if test_html:
        figuregen.figure(all_grids, width_cm=28., filename='figure_in_figure.html')
    else:
        figuregen.figure(all_grids, width_cm=28., filename='figure_in_figure.html')
        figuregen.figure(all_grids, width_cm=28., filename='figure_in_figure.pptx')
        figuregen.figure(all_grids, width_cm=28., filename='figure_in_figure.pdf')