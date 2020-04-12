import json
import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt

def setup_fonts(plt):
    plt.rcParams.update({
    "text.usetex": True,     # use inline math for tikz
    "pgf.rcfonts": False,    # don't setup fonts from rc parameters
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",
    "pgf.preamble": [
         r"\usepackage[utf8]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         r"\usepackage{libertine}"
         ]
    })

def load_error(scene, integrator, metric='MRSE*'):
    with open('errors/%s__%s.json' % (scene, integrator)) as json_file:
        data = json.load(json_file)

    x = data['timesteps']
    y = [ e[metric] for e in data['data'] ]

    si = 0
    x, y = x[si:], y[si:]

    rmin = 0
    ddx, ddy = [], []
    for i in range(len(y)):
        if i == 0 or y[i-1] != y[i]: # y[i] < rmin:
            ddx.append(x[i])
            ddy.append(y[i])
            rmin = y[i]

    return ddx, ddy

def nice_name(integrator):
    return {
        "path": "PT w/ NEE",
        "bdpt": "BDPT",
        "pgrad6": "PG (radiance)",
        "pgfull6": "PG (ours)",
        "di2pgrad6": "PG (rad.+DI)",
        "pgrad9": "PG (radiance)",
        "pgfull9": "PG (ours)",
        "upsmcmc": "UPSMCMC"
    }.get(integrator, integrator)

def scaleRGB(r,g,b):
    return (r * 1.0/255.0, g * 1.0/255.0, b * 1.0/255.0)

def style(integrator, linewidth_pt):
    return {
        "path": { "color": scaleRGB(232, 181, 88), "linewidth": linewidth_pt},
        "pgrad6": { "color": scaleRGB(94, 163, 188), "linewidth": linewidth_pt},
        "pgfull6": { "color": scaleRGB(181, 63, 106), "linewidth": linewidth_pt}, # ours
        "di3pgrad6": { "color": scaleRGB(94, 163, 188), "ls": "--", "linewidth": linewidth_pt},
        "pgrad9": { "color": scaleRGB(94, 163, 188), "ls": ":", "linewidth": linewidth_pt},
        "pgfull9": { "color": scaleRGB(181, 63, 106), "ls": ":", "linewidth": linewidth_pt}, # ours
        "upsmcmc": { "color": scaleRGB(5, 142, 78), "linewidth": linewidth_pt}
    }.get(integrator, {})

def calculate_inch_fig_size(width_mm, height_mm):
    plot_width_inch = width_mm * 0.03937007874
    plot_height_inch = height_mm * 0.03937007874
    figsize=(plot_width_inch, plot_height_inch)
    return figsize

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
    = explicitely use ticks-labels provided by user 
    '''
    ax.set_xticks(xticks)
    if not use_scientific_notations:
        ax.set_xticklabels(xticks)

    ax.set_yticks(yticks)
    if not use_scientific_notations:
        ax.set_yticklabels(yticks)

def plot_lines(ax, scene, integrators=["path","pgrad6","pgfull6","upsmcmc"], linewidth_pt=0.6, metric='MRSE'):
    for integrator in integrators:
        ax.plot(*load_error(scene, integrator, metric), label=nice_name(integrator), **style(integrator, linewidth_pt))

    ax.set_xscale('log')
    ax.set_yscale('log')


def plot_errors(scene, integrators=["path","pgrad6","pgfull6","upsmcmc"], metric='MRSE'):
    setup_fonts(plt) # allow pgf

    # SIZE (font, lines, whole plot, etc.)
    fontsize_pt = 6 # unit: points

    line_width_pt = 0.5

    figsize = calculate_inch_fig_size(width_mm=35.0, height_mm=39.54805194805194)
    #constrained_layout: https://matplotlib.org/3.2.1/tutorials/intermediate/constrainedlayout_guide.html
    fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)

    # PLOT
    plot_lines(ax, scene, integrators, linewidth_pt=0.8, metric=metric)
    
    plt.tick_params(width=line_width_pt, length=(line_width_pt * 4),
        labelsize=fontsize_pt, pad=(line_width_pt * 2))
    remove_upper_and_left_axes(ax)
    
    plt.grid(color=(0.90,0.90,0.90), linestyle='-', linewidth=0.25)

    set_labels(fig, ax, fontsize_pt, xlabel="Time [s]", xrotation="horizontal", 
                ylabel="Error\n[relMSE]", yrotation="vertical", pad=(line_width_pt * 6))

    # if use_scientific_notations True, displaystyle is used in pgf --> offset pf ticks changes 
    set_ticks(ax, xticks=[3, 20, 120], yticks=[0.001,0.01, 0.1], use_scientific_notations=False)

    plt.savefig("gen_plot.pdf", pad_inches=0.0)
    # plt.savefig("gen_plot.pgf", pad_inches=0.0)

plot_errors("living-room", metric="MRSE*")

