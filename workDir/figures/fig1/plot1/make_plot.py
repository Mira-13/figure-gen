import numpy as np

import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt

def setup_fonts(plt):
    plt.rcParams.update({
    "text.usetex": True,     # use inline math for tikz
    "pgf.rcfonts": False,    # don't setup fonts from rc parameters
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": [
         r"\usepackage[utf8]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         r"\usepackage{libertine}"
         ]
    })

setup_fonts(plt)

# SIZE (font, lines, whole plot, etc.)
filename = 'abc_fz_10'
plot_width_mm = 30
plot_height_mm = 50.63225806451613
tick_font_size_pt = 10 # unit: points
line_widths_pt = 0.5 # unit: points
outer_padding_pt = 0.0

# PLOT STYLES and RANGE
xmin_val, xmax_val = 0, 100
ymin_val, ymax_val = 0, 100
add_offset_on_x_axes_max_val = 5
add_offset_on_y_axes_max_val = 5

linestyle_list = ['--', '-']
color_list = [(.18, .61, .51),(.68, .21, .11)]
xs_list = [np.arange(xmin_val, xmax_val), np.arange(xmin_val, xmax_val)]
ys_list = [np.arange(xmin_val, xmax_val), np.arange(xmin_val, xmax_val) * 0.5]

# AXES STYLE: Arrow/Box (if arrow true -> no box drawn even if box = True)
has_arrow_along_axes = True
has_box = False

# GRID
grid_line_width = 0.25 # 0 = no grid
grid_color = (0.95,0.95,0.95) # rgb as tripel, each value has range from 0.0 to 1.0
grid_linestyle = '-'



def plot_lines(xs_list, ys_list, color_list, linestyle_list, line_width):
    count = 0
    for xs in xs_list:
        ax.plot(xs, ys_list[count], color=color_list[count], linestyle=linestyle_list[count], linewidth=line_width)
        count += 1

def draw_arrow_along_axes(fig, ax, line_width):
    # get width and height of axes object to compute 
    # matching arrowhead length and width
    xmin, xmax = ax.get_xlim() 
    ymin, ymax = ax.get_ylim()

    dps = fig.dpi_scale_trans.inverted()
    bbox = ax.get_window_extent().transformed(dps)
    width, height = bbox.width, bbox.height

    # manual arrowhead width and length
    x_arrow_head_width = 1./25.*(ymax-ymin) * line_width
    x_arrow_head_length = 1./25.*(xmax-xmin) * line_width
    line_width = line_width # axis line width
    overhang = 0.2 # arrow overhang: fraction that the arrow is swept back (0 overhang means triangular shape). Can be negative or greater than one.
    
    # compute matching arrowhead length and width
    y_arrow_head_width = x_arrow_head_width/(ymax-ymin)*(xmax-xmin)* height/width 
    y_arrow_head_length = x_arrow_head_length/(xmax-xmin)*(ymax-ymin)* width/height

    # draw x and y axis
    ax.arrow(xmin, 0, xmax-xmin, 0., fc='k', ec='k', lw = line_width, 
            head_width=x_arrow_head_width, head_length=x_arrow_head_length, overhang = overhang, 
            length_includes_head= True, clip_on = False, zorder=100) 
    
    ax.arrow(0, ymin, 0., ymax-ymin, fc='k', ec='k', lw = line_width, 
            head_width=y_arrow_head_width, head_length=y_arrow_head_length, overhang = overhang, 
            length_includes_head= True, clip_on = False, zorder=101) 

plot_width_inch = plot_width_mm * 0.03937007874
plot_height_inch = plot_height_mm * 0.03937007874
figsize=(plot_width_inch, plot_height_inch)

xmin, xmax = xlim = 0, (xmax_val + add_offset_on_x_axes_max_val)
ymin, ymax = ylim = 0, (ymax_val + add_offset_on_y_axes_max_val)

fig, ax = plt.subplots(figsize=figsize) # inches! figsize needs to be adjusted manually
plot_lines(xs_list, ys_list, color_list, linestyle_list, line_widths_pt)
ax.set(xlim=xlim, ylim=ylim, autoscale_on=False)

plt.tick_params(width=line_widths_pt, length=(line_widths_pt * 4),labelsize=tick_font_size_pt, pad=(line_widths_pt * 2))
plt.tight_layout(pad=outer_padding_pt)
plt.grid(color=grid_color, linestyle=grid_linestyle, linewidth=grid_line_width)

if has_arrow_along_axes:
    plt.box(on=False)
    draw_arrow_along_axes(fig, ax, line_widths_pt)
if has_box and not has_arrow_along_axes:
    plt.box(on=True)

fig.savefig('plottings/'+filename+'.pdf')

# styling TODO s
# x/y label placement + text size
# legend