import figuregen
from figuregen import util
import simpleimageio
import os

# ---------- Data Gathering ----------
method_titles = ['Reference', 'PT', 'VCM+MLT']
method_filenames = ['pool.exr', 'pool-60s-path.exr', 'pool-60s-upsmcmc.exr']
method_filenames = [os.path.join('images', 'pool', f) for f in method_filenames]

def get_image(filename=None, cropbox=None):
    '''
    Example how to load and process image data (simpleimageio to srgb).

    return:
        srgb image
    '''
    img = simpleimageio.read(filename)
    if isinstance(cropbox, util.image.Cropbox):
        img = cropbox.crop(img)
    return util.image.lin_to_srgb(img)

# define cropping positions and marker colors
crops = [
    util.image.Cropbox(top=120, left=400, height=30, width=40, scale=5),
    util.image.Cropbox(top=81, left=595, height=30, width=40, scale=5)
]
crop_colors = [
    [255,110,0],
    [0,200,100]
]

def get_error(method, cropbox=None):
    m_img = get_image(method, cropbox)
    r_img = get_image(method_filenames[0], cropbox)
    rMSE = figuregen.util.image.relative_mse(img=m_img, ref=r_img)
    return str(round(rMSE, 5))

def place_label(element, txt, pos='bottom_left'):
    element.set_label(txt, pos, width_mm=7.8, height_mm=2.5, offset_mm=[0.4, 0.4],
        fontsize=6, bg_color=[20,20,20], txt_color=[255,255,255], txt_padding_mm=0.2)

# ---------- Horizontal Figure TOP ----------
top_cols = len(method_filenames)
top_grid = figuregen.Grid(num_rows=1, num_cols=top_cols)

# fill grid with image data
for col in range(top_cols):
    e = top_grid.get_element(0, col)
    e.set_image(figuregen.PNG(get_image(method_filenames[col])))

    if col == 0: # reference
        place_label(e, txt='relMSE')
    else: # Method
        rmse = get_error(method_filenames[col])
        place_label(e, txt=rmse)

    # Add markers for all crops
    c_idx = 0
    for c in crops:
        e.set_marker(c.get_marker_pos(), c.get_marker_size(),
                    color=crop_colors[c_idx], linewidth_pt=0.5)
        c_idx += 1

top_grid.set_col_titles('top', method_titles)

# Specify paddings (unit: mm)
top_lay = top_grid.layout
top_lay.column_space = 1.0
top_lay.padding[figuregen.BOTTOM] = 0.25

# ---------- Horizontal Figure BOTTOM ----------
# One grid for each method
bottom_cols = len(crops)
bottom_grids = [figuregen.Grid(num_rows=1, num_cols=bottom_cols) for _ in range(len(method_filenames))]

# fill grid with images
sub_fig_idx = 0
for sub_fig in bottom_grids:
    for col in range(bottom_cols):
        method = method_filenames[sub_fig_idx]
        image = get_image(method, crops[col])
        e = sub_fig.get_element(0, col).set_image(figuregen.PNG(image))

        e.set_frame(linewidth=0.8, color=crop_colors[col])

        if sub_fig_idx != 0: # Method
            rmse = get_error(method, crops[col])
            place_label(e, txt=rmse)
    sub_fig_idx += 1

# Specify paddings (unit: mm)
for sub_fig in bottom_grids:
    sub_fig.layout.set_padding(column=0.5, right=1.0, row=0.5)
bottom_grids[-1].layout.set_padding(right=0.0) # remove last padding

# ---------- V-STACK of Horizontal Figures (create figure) ----------
v_grids = [
    [top_grid],
    bottom_grids
]

if __name__ == "__main__":
    figuregen.figure(v_grids, width_cm=18., filename='vertical-stack.pdf')
    figuregen.figure(v_grids, width_cm=18., filename='vertical-stack.pptx')
    figuregen.figure(v_grids, width_cm=18., filename='vertical-stack.html')

    try:
        from figuregen.util import jupyter
        jupyter.convert('vertical-stack.pdf', 300)
    except:
        print('Warning: pdf could not be converted to png')