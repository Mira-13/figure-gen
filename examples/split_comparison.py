import figuregen
from figuregen.util import image
import numpy as np

# ---------- Data Gathering ----------
# define some colors (r,g,b)
yellow=[232, 181, 88]
l_blue=[94, 163, 188]
blue=[82, 110, 186]
orange=[186, 98, 82]

# generate test images
img_blue = np.tile([x / 255 for x in blue], (320, 640, 1))
img_l_blue = np.tile([x / 255 for x in l_blue], (320, 640, 1))
img_yellow = np.tile([x / 255 for x in yellow], (320, 640, 1))
img_orange = np.tile([x / 255 for x in orange], (320, 640, 1))

# load images
images = [
    [
    image.SplitImage([img_blue, img_l_blue, img_yellow], degree=-20, weights=[0.5, 0.8, 0.5]),
    image.SplitImage([img_yellow, img_orange], degree=15, vertical=False, weights=[0.5, 1.0])
    ],
    [
    image.SplitImage([img_yellow, img_orange], weights=[1.0, 1.0], degree=30),
    image.SplitImage([img_yellow, img_l_blue, img_blue], vertical=False, weights=[1, 2, 3], degree=0),
    ]
]

# ---------- Simple Grid with SplitImages ----------
n_rows = 2
top_cols = 2
top_grid = figuregen.Grid(num_rows=n_rows, num_cols=top_cols)

# fill grid with image data
for row in range(n_rows):
    for col in range(top_cols):
        s_img = images[row][col]
        raw_img = figuregen.PNG(s_img.get_image())
        e = top_grid.get_element(row,col).set_image(raw_img)
        e.draw_lines(s_img.get_start_positions(), s_img.get_end_positions(), linewidth_pt=0.5, color=[0,0,0])

top_grid.set_col_titles('top', ['Horizontal Split', 'Vertical Split', 'C)', 'D)'])

# LAYOUT: Specify paddings (unit: mm)
top_lay = top_grid.get_layout()
top_lay.set_padding(column=1.0, right=1.5)
top_lay.set_col_titles('top', field_size_mm=5.0)

if __name__ == "__main__":
    from figuregen import figure
    from figuregen.tikz import TikzBackend
    figure([[top_grid]], width_cm=15., filename='split-comparison.tikz', backend=TikzBackend())
    # figuregen.horizontal_figure([top_grid], width_cm=15., filename='split-comparison.html')
    # figuregen.horizontal_figure([top_grid], width_cm=15., filename='split-comparison.pptx')
    # figuregen.horizontal_figure([top_grid], width_cm=15., filename='split-comparison.pdf', tex_packages=["[T1]{fontenc}", "{arev}"])

    # try:
    #     from figuregen.util import jupyter
    #     jupyter.convert('split-comparison.pdf', 300)
    # except:
    #     print('Warning: pdf could not be converted to png')