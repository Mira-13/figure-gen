import os

import figuregen as fig
from figuregen.util import image
import simpleimageio

scene, seconds = 'pool', 60
method_list = ['path', 'upsmcmc', 'radiance', 'full', None]
method_titles = ['PT', 'VCM+MLT', 'Method A', 'Method B', 'Reference']
baseline = 2

# left, top, width, height
crops = [[400, 120, 40, 30], [595, 81, 40, 30], [123, 300, 40, 30]]

# ---------- Data Gathering: images -------------
def get_image(method=None):
    if method is None:
        path = os.path.join('images', scene, scene+".exr")
    else:
        sec_string = '-'+str(seconds)+'s-'
        path = os.path.join('images', scene, scene+sec_string+method+".exr")

    img = simpleimageio.read(path)
    return image.lin_to_srgb(simpleimageio.read(path))

ref_img = get_image()
m_images = [get_image(m) for m in method_list[:-1]]

#-------- Data Gathering: errors & captions ----------
def get_error(method_img):
    rMSE = image.relative_mse(img=method_img, ref=ref_img)
    return rMSE

def get_captions():
    i = 0
    captions = []
    errors = [ get_error(method_img) for method_img in m_images ]

    for method in method_titles[:-1]:
        relMSE = round(errors[i], 3)
        if i == baseline:
            speedup = '(base)'
        else:
            speedup = round(errors[baseline] * 1/relMSE, 1)
            speedup = '('+str(speedup)+'x)'

        string_caption = method + '\n' + str(relMSE) + ' ' + speedup
        captions.append(string_caption)
        i+=1

    captions.append('Reference'+'\n'+'relMSE ('+str(seconds)+'s)')

    return captions


# ---------- REFERENCE Module ----------
ref_grid = fig.Grid(1,1)
reference = ref_grid.get_element(0,0).set_image(fig.PNG(ref_img))

# marker
for crop in crops:
    reference.set_marker(pos=[crop[0], crop[1]], size=[crop[2], crop[3]], color=[255, 255, 255], linewidth_pt=0.6)

# titles
ref_grid.set_title('top', 'Pool')

# layout
ref_layout = ref_grid.layout
ref_layout.padding[fig.TOP] = 0.1
ref_layout.padding[fig.RIGHT] = 0.5
ref_layout.titles[fig.TOP] = fig.TextFieldLayout(size=6., offset=0.2, fontsize=8)


# ---------- COMPARE Module ----------
num_rows = len(crops)
num_cols = len(method_list)
comp_grid = fig.Grid(num_rows, num_cols)

def crop_image(img, crop_args):
    img = image.crop(img, *crop_args)
    img = image.zoom(img, 10)
    return img

for row in range(0,num_rows):
    for col in range(0,num_cols):
        img = fig.PNG(crop_image(get_image(method_list[col]), crops[row]))
        e = comp_grid.get_element(row, col).set_image(img)

# titles
comp_grid.set_col_titles('top', get_captions())

# layout
c_layout = comp_grid.layout
c_layout.padding[fig.TOP] = 0.1
c_layout.row_space = 0.4
c_layout.column_space = 0.4
c_layout.column_titles[fig.TOP] = fig.TextFieldLayout(size=6., offset=0.2, fontsize=8)

# ------ create figure --------
if __name__ == "__main__":
    fig.horizontal_figure([ref_grid, comp_grid], width_cm=15., filename=scene+'.pdf')
    fig.horizontal_figure([ref_grid, comp_grid], width_cm=15., filename=scene+'.pptx')
    fig.horizontal_figure([ref_grid, comp_grid], width_cm=15., filename=scene+'.html')