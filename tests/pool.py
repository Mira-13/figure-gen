import figuregen
import figuregen.util
import os
import pyexr

scene, seconds = 'pool', 60
method_list = ['path', 'upsmcmc', 'radiance', 'full', None]
method_titles = ['PT', 'VCM+MLT', 'Method A', 'Method B', 'Reference']
baseline = 2

# left, top, width, height
crops = [[400, 120, 40, 30], [595, 81, 40, 30], [123, 300, 40, 30]] 

# ---------- Data Gathering: images -------------
def get_image(method=None, crop_args=None):
    if method is None:
        path = os.path.join('images', scene, scene+".exr")
    else:
        sec_string = '-'+str(seconds)+'s-'
        path = os.path.join('images', scene, scene+sec_string+method+".exr")

    img = pyexr.read(path)
    if crop_args is not None:
        img = figuregen.util.image.crop(img, crop_args)
        img = figuregen.util.image.zoom(img)
    return figuregen.util.image.lin_to_srgb(img)

ref_img = get_image() 
m_images = [get_image(m) for m in method_list[:-1]]

#-------- Data Gathering: errors & captions ----------
def get_error(method_img):
    rMSE = figuregen.util.image.relative_mse(img=method_img, ref=ref_img)
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
ref_grid = figuregen.Grid(1,1)
reference = ref_grid.get_element(0,0).set_image(figuregen.PNG(ref_img))
 
# marker
for crop in crops:
    reference.set_marker(pos=[crop[0], crop[1]], size=[crop[2], crop[3]], color=[255, 255, 255], linewidth_pt=0.6)

# titles
ref_grid.set_title('top', 'Pool')

# layout
ref_layout = ref_grid.get_layout().set_padding(top=0.1, right=0.5)
ref_layout.set_title('top', field_size_mm=6., offset_mm=0.2, fontsize=8)


# ---------- COMPARE Module ----------
num_rows = len(crops)
num_cols = len(method_list)
comp_grid = figuregen.Grid(num_rows, num_cols)

# set images
for row in range(0,num_rows):
    for col in range(0,num_cols):
        img = figuregen.PNG(get_image(method=method_list[col], crop_args=crops[row]))
        e = comp_grid.get_element(row, col).set_image(img)

# titles
comp_grid.set_col_titles('top', get_captions())

# layout
c_layout = comp_grid.get_layout().set_padding(top=0.1, right=0.5, row=0.4, column=0.4)
c_layout.set_col_titles('top', field_size_mm=6., offset_mm=0.2, fontsize=8)

# ------ create figure --------
if __name__ == "__main__":
    figuregen.horizontal_figure([ref_grid, comp_grid], width_cm=15., filename=scene+'.pdf')
    figuregen.horizontal_figure([ref_grid, comp_grid], width_cm=15., filename=scene+'.pptx')
    figuregen.horizontal_figure([ref_grid, comp_grid], width_cm=15., filename=scene+'.html')