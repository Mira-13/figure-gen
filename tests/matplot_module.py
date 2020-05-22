import generator
import generator.util
import numpy as np

# generate test data
# plot lines (styles)

seconds = np.linspace(1, 60, 42)
errors_1 = 100/seconds
errors_2 = 80/seconds

data = [
    (seconds, errors_1), (seconds, errors_2)
]

axis_labels = {
    "x": {
        "text": "Time [s]",
        "rotation": "horizontal"
    },
    "y": {
        "text": "Error\n[relMSE]",
        "rotation": "vertical"
    }
}

axis_properties = {
    "x": {
        "range": [1, 65],
        "ticks": [ 3, 20, 50],
        "use_log_scale": True,
        "use_scientific_notations": False
    },
    "y": {
        "range": [10, 105],
        "ticks": [ 10, 50, 80],
        "use_log_scale": True,
        "use_scientific_notations": False
    }
}

markers = {
    "vertical_lines": [
        {
            "pos": 10.5,
            "color": [ 242, 113, 0 ],
            "linestyle": (0,(4,6)),
            "linewidth_pt": 0.6,
        },
        {
            "pos": 12.0,
            "color": [ 242, 113, 0 ],
            "linestyle": (0,(4,6)),
            "linewidth_pt": 0.6,
        }
    ]
}

modules = [
    { 
        "type": "plot",
        "data": data,
        "axis_labels": axis_labels,
        "axis_properties": axis_properties,
        "markers": markers,
        "layout": "plot_layout.json"
    }
]

if __name__ == "__main__":
    generator.horizontal_figure(modules, width_cm=18., backend='tikz')