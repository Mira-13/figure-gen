import figuregen
from figuregen import util
import numpy as np

# ---------- Data Gathering ----------
# define some colors (r,g,b)
yellow=[232, 181, 88]
l_blue=[94, 163, 188]
blue=[82, 110, 186]
orange=[186, 98, 82]

# generate test images
img_blue = np.tile([x / 255 for x in l_blue], (32, 64, 1))
img_yellow = np.tile([x / 255 for x in yellow], (32, 64, 1))
img_orange = np.tile([x / 255 for x in orange], (32, 64, 1))

# load the two images
t_images = [
    figuregen.PNG(img_blue),
    figuregen.PNG(img_yellow),
    figuregen.PNG(img_orange)
]

# generate test images
img_blue = np.tile([x / 255 for x in l_blue], (20, 25, 1))
img_yellow = np.tile([x / 255 for x in yellow], (20, 25, 1))
img_orange = np.tile([x / 255 for x in orange], (20, 25, 1))

b_images = [
    figuregen.PNG(img_blue),
    figuregen.PNG(img_yellow),
    figuregen.PNG(img_orange)
]

n_rows = 1
# ---------- Horizontal Figure TOP ----------
top_cols = 3
top_grid = figuregen.Grid(num_rows=n_rows, num_cols=top_cols)

# fill grid with image data
for row in range(n_rows):
    for col in range(top_cols):
        e = top_grid.get_element(row,col).set_image(t_images[col])
        e.set_frame(linewidth=0.2, color=[0,0,0])

# LAYOUT: Specify paddings (unit: mm)
top_lay = top_grid.get_layout()
top_lay.set_padding(column=1.0, bottom=0.5)

# ---------- Horizontal Figure BOTTOM ----------
bottom_cols = 2
bottom_rows = 1

bottom_grid1 = figuregen.Grid(num_rows=bottom_rows, num_cols=bottom_cols)
bottom_grid2 = figuregen.Grid(num_rows=bottom_rows, num_cols=bottom_cols)
bottom_grid3 = figuregen.Grid(num_rows=bottom_rows, num_cols=bottom_cols)

bottom_grids = [bottom_grid1, bottom_grid2, bottom_grid3]

# FILL: with images
idx = 0
for sub_fig in bottom_grids:
    for row in range(bottom_rows):
        for col in range(bottom_cols):
            e = sub_fig.get_element(row,col).set_image(b_images[idx])
            e.set_frame(linewidth=0.2, color=[0,0,0])
    idx +=1

# LAYOUT: Specify paddings (unit: mm)
for sub_fig in bottom_grids:
    sub_fig.get_layout().set_padding(column=0.5, right=1.0, row=0.5)

bottom_grids[-1].get_layout().set_padding(right=0.0) # remove last padding


# ---------- V-STACK of Horizontal Figures (create figure) ----------
v_grids = [
    [top_grid], 
    bottom_grids
    ]
if __name__ == "__main__":
    figuregen.figure(v_grids, width_cm=15., filename='v-stacked.pdf')
    figuregen.figure(v_grids, width_cm=15., filename='v-stacked.pptx')
    figuregen.figure(v_grids, width_cm=15., filename='v-stacked.html')