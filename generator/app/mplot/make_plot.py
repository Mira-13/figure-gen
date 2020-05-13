import json
import os
import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt


def setup_fonts(plt, data):
    font_properties = data['plot_config']['font']

    plt.rcParams.update({
    "text.usetex": True,     # use inline math for tikz
    "pgf.rcfonts": False,    # don't setup fonts from rc parameters
    "pgf.texsystem": "pdflatex",
    "font.family": font_properties['font_family'],
    "pgf.preamble": [
         r"\usepackage[utf8]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         r"\usepackage{"+font_properties['tex_package']+"}"
         ]
    })

def calculate_inch_fig_size(width_mm, height_mm):
    return (width_mm * 0.03937007874, height_mm * 0.03937007874)

def remove_upper_axis(ax):
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')

def remove_right_axis(ax):
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_ticks_position('left')

def label_alignment(rotation : str):
    if rotation=='horizontal': 
        return 'top'
    return 'bottom'

def get_fontsize(data):
    fontsize_pt = data['plot_config']['font']['fontsize_pt']
    return fontsize_pt

def scaleRGB(rgb_list):
    return (rgb_list[0] * 1.0/255.0, rgb_list[1] * 1.0/255.0, rgb_list[2] * 1.0/255.0)

def set_labels(fig, ax, data, pad): #fontsize_pt, xlabel, xrotation, ylabel, yrotation
    axis_labels = data['axis_labels']
    ax.set_xlabel(axis_labels['x']['text'], fontsize=get_fontsize(data), ha="right", 
                  va=label_alignment(axis_labels['x']['rotation']), rotation=axis_labels['x']['rotation'])
    ax.set_ylabel(axis_labels['y']['text'], fontsize=get_fontsize(data), ha="right", 
                  va=label_alignment(axis_labels['y']['rotation']), rotation=axis_labels['y']['rotation'])

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


#def plot_style(integrator, linewidth_pt):
#    return {
#        "path": { "color": scaleRGB(232, 181, 88), "linewidth": linewidth_pt},
#        "radiance": { "color": scaleRGB(94, 163, 188), "linewidth": linewidth_pt},
#        "full": { "color": scaleRGB(181, 63, 106), "linewidth": linewidth_pt}, # ours
#        "upsmcmc": { "color": scaleRGB(5, 142, 78), "linewidth": linewidth_pt}
#    }.get(integrator, {})

#def label_name(method):
#    return {
#        "path": "PT w/ NEE",
#        "radiance": "PG (radiance)",
#        "full": "PG (ours)",
#        "upsmcmc": "UPSMCMC",

#        "MRSE": "relMSE"
#    }.get(method, method)

def plot_lines(ax, data): #error_path, methods, linewidth_pt, has_xscale_log=True, has_yscale_log=True
    for d in data['data']:
        #x, y =  d['x'], d['y']#load_error(error_path, m)
        ax.plot(d, linewidth=data['plot_config']['plot_linewidth_pt']) # m['label'], **plot_style(m, linewidth_pt))

def apply_axes_properties_and_labels(plt, fig, ax, data):
    if data['axis_properties']['x']['use_log_scale']:
        ax.set_xscale('log')
    if data['axis_properties']['y']['use_log_scale']:
        ax.set_yscale('log')

    tick_lw_pt = data['plot_config']['tick_linewidth_pt']

    plt.tick_params(width=tick_lw_pt, length=(tick_lw_pt * 4), labelsize=get_fontsize(data), pad=(tick_lw_pt * 2))
    if not data['plot_config']['has_right_axis']: 
        remove_right_axis(ax)
    if not data['plot_config']['has_upper_axis']: 
        remove_upper_axis(ax)

    set_labels(fig, ax, data, pad=(tick_lw_pt * 6))
    # if use_scientific_notations True, displaystyle is used in pgf --> offset pf ticks changes 
    ax.set_xticks(data['axis_properties']['x']['ticks'])
    if not data['axis_properties']['x']['use_scientific_notations']:
        #xticks[-1] = '\\textbf{'+ str(xticks[-1]) + '}'
        ax.set_xticklabels(data['axis_properties']['x']['ticks'])

    ax.set_yticks(data['axis_properties']['y']['ticks'])
    if not data['axis_properties']['y']['use_scientific_notations']:
        ax.set_yticklabels(data['axis_properties']['y']['ticks'])

def place_marker(ax, data):
    # TODO
    return
    ax.axvline(x=13.97, color=scaleRGB(94, 163, 188), linewidth=0.6, linestyle=(0, (4, 6)))
    ax.axvline(x=18.62, color=scaleRGB(181, 63, 106), linewidth=0.6, linestyle=(0, (4, 6)))

def generate(module_data, to_path, pdf_filename):
    setup_fonts(plt, module_data) 
    figsize = calculate_inch_fig_size(module_data['total_width'], module_data['total_height'])
    #constrained_layout: https://matplotlib.org/3.2.1/tutorials/intermediate/constrainedlayout_guide.html
    fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
    fig.set_constrained_layout_pads(w_pad=0, h_pad=0,
        hspace=0., wspace=0.)

    plot_lines(ax, module_data)
    
    apply_axes_properties_and_labels(plt, fig, ax, module_data)
    
    grid_properties = module_data['plot_config']['grid']
    plt.grid(color=scaleRGB(grid_properties['color']), linestyle=grid_properties['linestyle'], linewidth=grid_properties['linewidth_pt'])

    place_marker(ax, module_data)

    plt.savefig(os.path.join(to_path, pdf_filename), pad_inches=0.0)