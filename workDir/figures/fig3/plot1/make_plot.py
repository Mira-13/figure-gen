'''
    THIS IS UNFISHED BUSINESS. Goal was to wrap those ugly functions and let the user fill out
    json format very similar to content.py
'''

import json
# import matplotlib
# matplotlib.use('pgf')
import matplotlib.pyplot as plt

def label_name(integrator):
    return {
        "path": "PT w/ NEE",
        "radiance": "PG (radiance)",
        "full": "PG (ours)",
        "upsmcmc": "UPSMCMC",
        
        "MRSE*": "relMSE*",
        "MRSE": "relMSE"
    }.get(integrator, integrator)

def plot_style(integrator, linewidth_pt):
    return {
        "path": { "color": scaleRGB(232, 181, 88), "linewidth": linewidth_pt},
        "radiance": { "color": scaleRGB(94, 163, 188), "linewidth": linewidth_pt},
        "full": { "color": scaleRGB(181, 63, 106), "linewidth": linewidth_pt}, # ours
        "upsmcmc": { "color": scaleRGB(5, 142, 78), "linewidth": linewidth_pt}
    }.get(integrator, {})

def load_error(path, scene, integrator, metric='MRSE*', clip=True):
    path = os.path.join(path, scene, scene+'__'+integrator+'.json')
    with open(path) as json_file:
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
    
    return ddx, ddy

def plot_lines(error_path, ax, scene, integrators, linewidth_pt=0.6, metric='MRSE'):
    for integrator in integrators:
        ax.plot(*load_error(error_path, scene, integrator, metric), label=label_name(integrator), **plot_style(integrator, linewidth_pt))

    ax.set_xscale('log')
    ax.set_yscale('log')

def main(path, scene, figsize_width_mm, figsize_height_mm, plot_linewidth_pt, tick_linewidth_pt, label_fontsize_pt=7):
    plt, fig, ax = create_base_figure(figsize_width_mm, figsize_height_mm, tex_font_package='libertine', font_family='sans-serif')
    
    # PLOT
    plot_lines(path, ax, scene, integrators=['path', 'upsmcmc', 'radiance', 'full'], linewidth_pt=plot_linewidth_pt, metric="MRSE*")

    # TICKS AND LABELS
    plt.tick_params(width=tick_linewidth_pt, length=(tick_linewidth_pt * 4),
        labelsize=label_fontsize_pt, pad=(tick_linewidth_pt * 2))
    set_labels(fig, ax, label_fontsize_pt, xlabel="Time [s]", xrotation="horizontal", 
                ylabel="Error\n[relMSE]", yrotation="vertical", pad=(tick_linewidth_pt * 6))
    set_ticks(ax, xticks=[3, 20, 60], yticks=[0.01, 0.1], use_scientific_notations=False)

    # STYLE
    figure_style(plt, ax, has_no_upper_and_left_axes=True, has_grid=True)

    # mark sth
    ax.axvline(x=13.97, color=scaleRGB(94, 163, 188), linewidth=0.6, linestyle=(0, (4, 6)))
    ax.axvline(x=18.62, color=scaleRGB(181, 63, 106), linewidth=0.6, linestyle=(0, (4, 6)))

    plt.savefig("gen_plot.pdf", pad_inches=0.0)

main(path='C:/Users/admin/Documents/MasterThesis/mtc/workDir/errors/',
    scene='living-room',
    figsize_width_mm=40.0, figsize_height_mm=40.0, 
    plot_linewidth_pt=0.8, tick_linewidth_pt=0.6, label_fontsize_pt=7)

plot_data = {
    'path': 'C:/Users/admin/Documents/MasterThesis/mtc/workDir/errors/',
    'scene': 'living-room',
    'unit': 'mm',
    "total_width": 40.0, 
    "total_height": 37.0,
    'plot_config': {
        'plot_linewidth_pt': 0.8,
        'tick_linewidth_pt': 0.6,
        'font': {
            'tex_package': 'libertine',
            'font_family': 'sans-serif',
            'fontsize_pt': 7
        },
        'grid': {
            'color': [230, 230, 230],
            'linewidth_pt': 0.25,
            'linestyle': '-'
        },
        'has_upper_axes': False,
        'has_right_axes': False
    },
    'plot_content': {
        'titles': 'not implemented yet',
        'labels': {
            'x_axes': {
                'content': "Time [s]",
                'rotation': 'horizontal'
            },
            'y_axes': {
                'content': "Error\n[relMSE]",
                'rotation': 'vertical'
            }
        }
        'ticks': {
            'x_axes': {
                'content': [3, 20, 60],
                'use_scientific_notations': False 
            },
            'y_axes': {
                'content': [0.01, 0.1],
                'use_scientific_notations': False
            }
        },
        'vertical_lines': {
            'linewidth_pt': 0.6,
            "list": [
                    {"pos": 10.5, "color": [242, 113, 0], 'linestyle': (0, (4, 6))}, 
                    {"pos": 12.0, "color": [242, 113, 0], 'linestyle': (0, (4, 6))}
                    ]
        }
    }
    
}