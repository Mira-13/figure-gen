import numpy as np
import figuregen

# --- define colors and images ---
colors = [ 
    [232, 181, 88], #yellow
    [5, 142, 78], #green
    [94, 163, 188], #light-blue
    [181, 63, 106], #pink
    [82, 110, 186], #blue
    [186, 98, 82] #orange-crab
]

# generate test images
img_blue = np.tile([x / 255 for x in colors[2]], (32, 64, 1))
img_yellow = np.tile([x / 255 for x in colors[0]], (32, 64, 1))

# load the two images
images = [
    img_blue,
    img_yellow
]

# ------ Create Grid including markers, frames, (sub)titles, labels, etc. -------
n_rows, n_cols = 2, 3
grid = figuregen.Grid(n_rows, n_cols)

# fill grid with image data
for row in range(n_rows):
    for col in range(n_cols):
        img = figuregen.PNG(images[row])
        grid.get_element(row,col).set_image(img)

layout = grid.get_layout()
layout.set_padding(top=0.5, bottom=1.5)

# marker
grid.get_element(0,0).set_marker(pos=[32,12], size=[15,10], color=colors[4])
grid.get_element(0,0).set_marker(pos=[1,1], size=[15,10], color=colors[-1], linewidth_pt=0.9, 
                                is_dashed=True)

# frame
grid.get_element(0,1).set_frame(linewidth=2., color=colors[4])

# subtitles for specific elements
grid.get_element(0,0).set_caption('caption a)')
grid.get_element(0,1).set_caption('caption b)')
grid.get_element(0,2).set_caption('caption c)')
grid.get_element(1,0).set_caption('caption d)')
grid.get_element(1,1).set_caption('caption e)')
grid.get_element(1,2).set_caption('caption f)')
layout.set_caption(height_mm=4.0, fontsize=9, txt_color=[170,170,170])

# labels (examples, each element can have in total 6 labels on each valid position)
e4 = grid.get_element(1,0)
e4.set_label("bottom center", pos='bottom_center', width_mm=25., height_mm=4.0, offset_mm=[1.0, 1.0], 
                  fontsize=9, bg_color=None)
e4.set_label("top\\\\right", pos='top_right', width_mm=8., height_mm=7.0, offset_mm=[1.0, 1.0], 
                  fontsize=9, bg_color=[255,255,255], txt_padding_mm=0.4)
e4.set_label("top\\\\left", pos='top_left', width_mm=8., height_mm=7.0, offset_mm=[1.0, 1.0], 
                  fontsize=9, bg_color=colors[-1], txt_color=[255,255,255], txt_padding_mm=1.5)

# grid specific titles
grid.set_title('top', 'Top Title')
layout.set_title('top', 5., offset_mm=2.,fontsize=12, bg_color=colors[5], txt_color=[255,255,255])

grid.set_title('south', 'Bottom Title') #use defaults

grid.set_title('right', 'Right Title') #use defaults

grid.set_title('left', 'Left Title')
layout.set_title('left', 4., offset_mm=2.,fontsize=12)

# Row and column titles
grid.set_row_titles('left', ['Row titles', 'are better'])
layout.set_row_titles('left', 10., offset_mm=1., fontsize=9, txt_rotation=0, bg_color=[colors[4],colors[2]])

grid.set_col_titles('north', ['Column titles', 'are', 'the best'])
#layout.set_col_titles('north', 10., offset_mm=1., fontsize=9, bg_color=[200, 180, 220])

if __name__ == "__main__":
    figuregen.horizontal_figure([grid], width_cm=18., filename='single-grid.pdf')
    figuregen.horizontal_figure([grid], width_cm=18., filename='single-grid.pptx')
    figuregen.horizontal_figure([grid], width_cm=18., filename='single-grid.html')

    try:
        from figuregen.util import jupyter
        jupyter.convert('single-grid.pdf', 300)
    except:
        print('Warning: pdf could not be converted to png')