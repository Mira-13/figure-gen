import figuregen
from figuregen.util import image
import os
import pyexr
import json

# ---------- Data Gathering ----------
idx = 2 # scene_idx, only pool scene will be in repo included
scene = ['bookshelf', 'glossy-kitchen', 'pool']
seconds = [120, 90, 60]
baseline = 2
method_list = ['path', 'upsmcmc', 'radiance', 'full', None]
method_titles = ['Method A)', 'Method B)', 'Method C)', 'Method D)', 'Reference']

crops = [
    [ # bookshelf
        image.Cropbox(top=191, left=369, height=30, width=40, scale=5),
        image.Cropbox(top=108, left=238, height=30, width=40, scale=5)
    ],
    [ # glossy-kitchen
        image.Cropbox(top=120, left=100, height=30, width=40, scale=5),
        image.Cropbox(top=325, left=212, height=30, width=40, scale=5)
    ],
    [ # pool
        image.Cropbox(top=120, left=400, height=30, width=40, scale=5),
        image.Cropbox(top=81, left=595, height=30, width=40, scale=5)
    ]
]
colors = [
    [232, 181, 88],
    [5, 142, 78],
    [94, 163, 188],
    [181, 63, 106],
    [255, 255, 255]
]

def get_image(scene, seconds, method=None, cropbox=None):
    if method is None:
        path = os.path.join('images', scene, scene+".exr")
    else:
        sec_string = '-'+str(seconds)+'s-'
        path = os.path.join('images', scene, scene+sec_string+method+".exr")

    img = pyexr.read(path)
    if isinstance(cropbox, image.Cropbox):
        img = cropbox.crop(img)
    return image.lin_to_srgb(img)

# ----- Helper for Comparision Module to generate content -----
def get_error(scene, method, seconds, metric='MRSE*'):
    p = os.path.join('errors', scene, scene+'__'+method+'.json')
    with open(p) as json_file:
        data = json.load(json_file)
    idx = data['timesteps'].index(seconds)
    error = data['data'][idx][metric]
    return round(error, 8)

def get_captions(scene, method_titles, baseline, seconds):
    i = 0
    captions = []
    errors = [ get_error(scene, method, seconds) for method in method_list[:-1] ]

    for method in method_titles[:-1]:
        relMSE = round(errors[i], 3)
        if i == baseline:
            speedup = '(baseline)'
        else:
            speedup = round(errors[baseline] * 1/relMSE, 2)
            speedup = '('+str(speedup)+'x)'

        string_caption = method + '\n' + str(relMSE) + ' ' + speedup
        captions.append(string_caption)
        i+=1

    captions.append('Reference'+'\n'+'relMSE ('+str(seconds)+'s)')

    return captions

# ----- Helper for Plot Module to generate content -----
def load_error(scene, method, metric='MRSE*', clip=True):
    with open('errors/%s/%s__%s.json' % (scene, scene, method)) as json_file:
        data = json.load(json_file)

    x = data['timesteps']
    y = [ e[metric] for e in data['data'] ]

    si = 0
    x, y = x[si:], y[si:]

    rmin = 0
    ddx, ddy = [], []
    for i in range(len(y)):
        if i == 0 or (y[i-1] != y[i] and (not clip or y[i] < rmin)):
            ddx.append(x[i])
            ddy.append(y[i])# * x[i])
            rmin = y[i]

    return (ddx, ddy)

def get_plot_data(scene, method_list):
    return [
        load_error(scene, method, metric='MRSE*', clip=True) for method in method_list[:-1]
    ]

# ---------- REFERENCE Module ----------
ref_grid = figuregen.Grid(1,1)
ref_img = get_image(scene[idx], seconds[idx])
reference = ref_grid.get_element(0,0).set_image(figuregen.PNG(ref_img))

# marker
for crop in crops[idx]:
    reference.set_marker(pos=crop.get_marker_pos(), size=crop.get_marker_size(),
                        color=[242, 113, 0], linewidth_pt=0.6)
# titles
ref_grid.set_title('south', scene[idx].replace('-',' ').title())

# layout
ref_layout = ref_grid.get_layout().set_padding(bottom=0.1, right=0.5)
ref_layout.set_title('south', field_size_mm=7., offset_mm=0.5, fontsize=8)


# ---------- COMPARE Module ----------
num_rows = len(crops[idx])
num_cols = len(method_list)
comp_grid = figuregen.Grid(num_rows, num_cols)

# set images
for row in range(0,num_rows):
    for col in range(0,num_cols):
        img = get_image(scene[idx], seconds[idx], method=method_list[col], cropbox=crops[idx][row])
        e = comp_grid.get_element(row, col)
        e.set_image(figuregen.PNG(img))

# titles
comp_grid.set_col_titles('south', get_captions(scene[idx], method_titles, baseline, seconds[idx]))

# layout
c_layout = comp_grid.get_layout().set_padding(bottom=0.1, right=0.5, row=0.5, column=0.5)
c_layout.set_col_titles('south', field_size_mm=7., offset_mm=0.5, fontsize=8, bg_color=colors)

# ---------- PLOT Module ----------
xticks = [
    [3, 20, s] for s in seconds
]
vline_positions = [
    (28.32, 28.78),
    (19.92, 20.23),
    (11.44, 11.17),
    (13.97, 18.62)
]

plot = figuregen.MatplotLinePlot(aspect_ratio=1.1, data=get_plot_data(scene[idx], method_list))
plot.set_colors(colors)

plot.set_axis_label('x', "Time [s]")
plot.set_axis_label('y', "Error\n[relMSE]")

plot.set_axis_properties('x', ticks=xticks[idx], range=[2.5, 800])
plot.set_axis_properties('y', ticks=[0.01, 0.1, 1.0])

plot.set_v_line(pos=vline_positions[idx][0], color=colors[baseline], linestyle=(0,(4,6)), linewidth_pt=0.6)
plot.set_v_line(pos=vline_positions[idx][1], color=colors[3], linestyle=(-5,(4,6)), linewidth_pt=0.6)

plot_module = figuregen.Grid(1,1)
plot_module.get_element(0,0).set_image(plot)

# ---- TOGETHER ----
modules = [ref_grid, comp_grid, plot_module]

if __name__ == "__main__":
    figuregen.horizontal_figure(modules, width_cm=18., filename=scene[idx]+'-siggraph.pdf')
    figuregen.horizontal_figure(modules, width_cm=18., filename=scene[idx]+'-siggraph.pptx')
    figuregen.horizontal_figure(modules, width_cm=18., filename=scene[idx]+'-siggraph.html')

    try:
        from figuregen.util import jupyter
        jupyter.convert(scene[idx]+'-siggraph.pdf', 300)
    except:
        print('Warning: pdf could not be converted to png')