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

def plot_lines(xs_list, ys_list, color_list, linestyle_list, line_width_pt):
    count = 0
    for xs in xs_list:
        ax.plot(xs, ys_list[count], color=color_list[count], linestyle=linestyle_list[count], linewidth=line_width_pt)
        count += 1
    ax.set_xscale("log")

def calculate_inch_fig_size(width_mm, height_mm):
    plot_width_inch = width_mm * 0.03937007874
    plot_height_inch = height_mm * 0.03937007874
    figsize=(plot_width_inch, plot_height_inch)
    return figsize

def draw_arrow_along_axes(fig, ax, line_widths_pt):
    '''
    BROKEN: Matplotlib does not support axes as arrows, which is why in many cases, this will not work
    For example, this will not work if the axes have a log scaling.
    '''
    # get width and height of axes object to compute
    # matching arrowhead length and width
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    dps = fig.dpi_scale_trans.inverted()
    bbox = ax.get_window_extent().transformed(dps)
    width, height = bbox.width, bbox.height

    # manual arrowhead width and length
    x_arrow_head_width = 0# 1./25.*(ymax-ymin) * line_widths_pt
    x_arrow_head_length = 0#1./25.*(xmax-xmin) * line_widths_pt
    line_width = line_widths_pt # axis line width
    overhang = 0.2 # arrow overhang: fraction that the arrow is swept back (0 overhang means triangular shape). Can be negative or greater than one.

    # compute matching arrowhead length and width
    y_arrow_head_width = 0#1.0/50.0 * x_arrow_head_width/(ymax-ymin)*(xmax-xmin)* height/width
    y_arrow_head_length = 0#x_arrow_head_length/(xmax-xmin)*(ymax-ymin)* width/height

    # draw x and y axis
    ''' ax.arrow
         
        x, y: float
        The x and y coordinates of the arrow base.

        dx, dy : float
        The length of the arrow along x and y direction.
    '''
    # x axis
    ax.arrow(x=xmin, y=ymin, dx=xmax-xmin, dy=0, fc='k', ec='k', lw = line_width,
            head_width=x_arrow_head_width, head_length=x_arrow_head_length, overhang = overhang,
            length_includes_head= True, clip_on = False, zorder=100)
    # y axis
    ax.arrow(x=xmin, y=ymin, dx=0, dy=ymax-ymin, fc='k', ec='k', lw = line_width,
            head_width=y_arrow_head_width, head_length=y_arrow_head_length, overhang = overhang,
            length_includes_head= True, clip_on = False, zorder=101)

    print([xmin, ymin, xmax-xmin, ymin])
    print([xmin, ymin, xmin, ymax-ymin])
    print({'head_width':y_arrow_head_width, 'head_length': y_arrow_head_length, 'overhang': overhang})


setup_fonts(plt) # allow pgf

# SIZE (font, lines, whole plot, etc.)
tick_font_size_pt = 10 # unit: points

# PLOT STYLES and RANGE
xmin_val, xmax_val = 800, 1000
ymin_val, ymax_val = 0.001, 1000
add_offset_on_x_axes_max_val = 5
add_offset_on_y_axes_max_val = 5

linestyle_list = ['--', '-']
color_list = [(.18, .61, .51),(.68, .21, .11)]

xs_list = [np.arange(xmin_val, xmax_val)]
ys_list = [1000 * 1/xs_list[0]]

# AXES STYLE: Arrow/Box (if arrow true -> no box drawn even if box = True)
has_arrow_along_axes = True
has_box = False

figsize = calculate_inch_fig_size(30, 50.63225806451613)
line_width_pt = 0.5

xmin, xmax = xmin_val, xmax_val#xlim = 0, (xmax_val + add_offset_on_x_axes_max_val)
ymin, ymax = ymin_val, ymax_val#ylim = 0, (ymax_val + add_offset_on_y_axes_max_val)

fig, ax = plt.subplots(figsize=figsize) # inches! figsize needs to be adjusted manually
# ax.set(xlim=xlim, ylim=ylim, autoscale_on=False)


plt.tick_params(width=line_width_pt, length=(line_width_pt * 4),labelsize=tick_font_size_pt, pad=(line_width_pt * 2))

plot_lines(xs_list, ys_list, color_list, linestyle_list, line_width_pt=line_width_pt)
# tight_layout: only works with pdflatex
plt.tight_layout(pad=0.0)

ax.set_xlim(xmin, xmax)

plt.grid(color=(0.95,0.95,0.95), linestyle='-', linewidth=0.25)

if has_arrow_along_axes:
    plt.box(on=False)
    draw_arrow_along_axes(fig, ax, line_width_pt)
if has_box and not has_arrow_along_axes:
    plt.box(on=True)

fig.savefig('gen_plot.pdf', pad_inches=0.0)

# styling TODO s
# x/y label placement + text size
# legend