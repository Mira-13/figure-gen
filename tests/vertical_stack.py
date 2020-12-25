import figuregen
from figuregen import util
import pyexr
import os

# ---------- Data Gathering ----------
method_list = [None, 'path', 'upsmcmc']
method_titles = ['Reference', 'PT', 'VCM+MLT']

def get_image(method=None, cropbox=None):
    '''
    Example how to load and process image data (pyexr to srgb).

    arg:
        method (str): if None, load the reference image 
        cropbox (util.image.Cropbox): if None, don't crop the image

    return:
        srgb image
    '''
    scene, seconds = 'pool', 60

    if method is None: 
        path = os.path.join('images', scene, scene+".exr")
    else:
        sec_string = '-'+str(seconds)+'s-'
        path = os.path.join('images', scene, scene+sec_string+method+".exr")

    img = pyexr.read(path)
    if isinstance(cropbox, util.image.Cropbox):
        img = cropbox.crop(img)
    return util.image.lin_to_srgb(img)

#helper
def place_label(element, txt, pos='bottom_left'):
    element.set_label(txt, pos, width_mm=7.8, height_mm=3.1, offset_mm=[0.2, 0.2], 
                fontsize=6, bg_color=[20,20,20], txt_color=[255,255,255], txt_padding_mm=1.2)

def get_error(method, cropbox=None):
    m_img = get_image(method, cropbox)
    r_img = get_image(None, cropbox)
    rMSE = figuregen.util.image.relative_mse(img=m_img, ref=r_img)
    return str(round(rMSE, 5))

# define Crops
crop_1 = util.image.Cropbox(top=120, left=400, height=30, width=40, scale=5)
crop_2 = util.image.Cropbox(top=81, left=595, height=30, width=40, scale=5)
crops = [crop_1, crop_2]
crop_colors = [[255,110,0], [0,200,100]]


# ---------- Horizontal Figure TOP ----------
top_cols = len(method_list)
n_rows = 1
top_grid = figuregen.Grid(num_rows=n_rows, num_cols=top_cols)

t_images = [get_image(m) for m in method_list]

# fill grid with image data
for row in range(n_rows):
    for col in range(top_cols):
        e = top_grid.get_element(row,col)
        e.set_image(figuregen.PNG(t_images[col]))

        if col == 0: # reference
            place_label(e, txt='relMSE')
        else: # Method
            rmse = get_error(method_list[col])
            place_label(e, txt=rmse)

        c_idx = 0
        for c in crops:
            e.set_marker(c.get_marker_pos(), c.get_marker_size(), 
                        color=crop_colors[c_idx], linewidth_pt=0.5)
            c_idx +=1

top_grid.set_col_titles('top', method_titles)

# Specify paddings (unit: mm)
top_lay = top_grid.get_layout()
top_lay.set_padding(column=1.0, bottom=0.25)

# ---------- Horizontal Figure BOTTOM ----------
bottom_cols = len(crops)
bottom_rows = 1

bottom_grid1 = figuregen.Grid(num_rows=bottom_rows, num_cols=bottom_cols)
bottom_grid2 = figuregen.Grid(num_rows=bottom_rows, num_cols=bottom_cols)
bottom_grid3 = figuregen.Grid(num_rows=bottom_rows, num_cols=bottom_cols)

bottom_grids = [bottom_grid1, bottom_grid2, bottom_grid3]

# fill grid with images
sub_fig_idx = 0
for sub_fig in bottom_grids:
    for row in range(bottom_rows):
        for col in range(bottom_cols):
            method = method_list[sub_fig_idx]
            image = get_image(method, crops[col])
            e = sub_fig.get_element(row,col).set_image(figuregen.PNG(image))
            e.set_frame(linewidth=0.8, color=crop_colors[col])
            if sub_fig_idx != 0: # Method
                rmse = get_error(method, crops[col])
                place_label(e, txt=rmse)
    sub_fig_idx += 1

# Specify paddings (unit: mm)
for sub_fig in bottom_grids:
    sub_fig.get_layout().set_padding(column=0.5, right=1.0, row=0.5)

bottom_grids[-1].get_layout().set_padding(right=0.0) # remove last padding


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