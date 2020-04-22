'''
THIS IS UNFISHED WORK, this file was not used yet.
'''

import os
import json
import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt

def setup_fonts(plt, font_family="sans-serif", tex_font_package='libertine'):
    plt.rcParams.update({
    "text.usetex": True,     # use inline math for tikz
    "pgf.rcfonts": False,    # don't setup fonts from rc parameters
    "pgf.texsystem": "pdflatex",
    "font.family": font_family,
    "pgf.preamble": [
         r"\usepackage[utf8]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         r"\usepackage{"+ tex_font_package +r"}"
         ]
    })

def scaleRGB(r,g,b):
    return (round(r * 1.0/255.0, 2), round(g * 1.0/255.0, 2), round(b * 1.0/255.0, 2))


def calculate_inch_fig_size(width_mm, height_mm):
    plot_width_inch = width_mm * 0.03937007874
    plot_height_inch = height_mm * 0.03937007874
    return (plot_width_inch, plot_height_inch)

def remove_upper_and_left_axes(ax):
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

def set_labels(fig, ax, fontsize_pt, xlabel, xrotation, ylabel, yrotation, pad):
    ax.set_xlabel(xlabel, fontsize=fontsize_pt, ha="right", va="top", rotation=xrotation)
    ax.set_ylabel(ylabel, fontsize=fontsize_pt, ha="right", va="bottom", rotation=yrotation)

    # compute axis size in points
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width * 72, bbox.height * 72

    # compute relative padding
    lwX = ax.spines['bottom'].get_linewidth()
    # TODO if use_scientific_notations is True, then take ~70% of fontsize * ~1/4 and add it to the padding

    lwY = 0 #ax.spines['left'].get_linewidth()

    # coordinates in percentage of the figure main body size!
    ax.xaxis.set_label_coords(1, -(pad - lwX) / height)

    # coordinates in percentage of the figure main body size!
    ax.yaxis.set_label_coords(-(pad - lwY) / width, 1)

def set_ticks(ax, xticks, yticks, use_scientific_notations):
    '''
    use_scientific_notations = use_power_of_ten,
    =if not scientific_notations, then explicitely use ticks-labels provided by user 
    '''
    ax.set_xticks(xticks)
    if not use_scientific_notations:
        xticks[-1] = '\\textbf{'+ str(xticks[-1]) + '}'
        ax.set_xticklabels(xticks)

    ax.set_yticks(yticks)
    if not use_scientific_notations:
        ax.set_yticklabels(yticks)


def create_base_figure(figsize_width_mm, figsize_height_mm, tex_font_package, font_family):
    setup_fonts(plt, font_family, tex_font_package) # allow pgf

    figsize = calculate_inch_fig_size(figsize_width_mm, figsize_height_mm)
    #constrained_layout: https://matplotlib.org/3.2.1/tutorials/intermediate/constrainedlayout_guide.html
    fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
    fig.set_constrained_layout_pads(w_pad=0, h_pad=0,
        hspace=0., wspace=0.)
    
    return plt, fig, ax

def figure_style(plt, ax, has_no_upper_and_left_axes, has_grid):
    if has_no_upper_and_left_axes:
        remove_upper_and_left_axes(ax)
    
    if has_grid:
        plt.grid(color=(0.90,0.90,0.90), linestyle='-', linewidth=0.25)
