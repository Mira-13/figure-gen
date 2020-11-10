import figuregen
import figuregen.util
import numpy as np

# generate test data
seconds = np.linspace(1, 60, 42) #linespace(start, stop, num): Return evenly spaced numbers over a specified interval
errors_1 = 100/seconds
errors_2 = 80/seconds

data = [
    (seconds, errors_1), (seconds, errors_2)
]

plot_color = [
    [30, 180, 202],
    [170, 40, 20]
]

# ----- PLOT Module ----- 
plot_module = figuregen.Plot(data)
#plot_module.set_plot_colors(plot_color)

plot_module.set_axis_label('x', "sec", rotation="horizontal")
plot_module.set_axis_label('y', "error", rotation="vertical")

# for html format, you need to set axis properties (this might change in the future)
plot_module.set_axis_props('x', range=[1, 65], ticks=[5, 25, 50], use_log_scale=False, use_scientific_notations=False)
plot_module.set_axis_props('y', range=None, ticks=[5, 10, 30, 50], use_log_scale=True, use_scientific_notations=False)

plot_module.set_marker_v_line(pos=10.5, color=[242, 113, 0], linestyle=(0,(4,6)), linewidth_pt=0.6)

plot_module.set_width_to_height_aspect_ratio(1.15)

if __name__ == "__main__":
    figuregen.horizontal_figure([plot_module], width_cm=11., filename='matplot_test.pdf')
    figuregen.horizontal_figure([plot_module], width_cm=11., filename='matplot_test.pptx')
    figuregen.horizontal_figure([plot_module], width_cm=11., filename='matplot_test.html')