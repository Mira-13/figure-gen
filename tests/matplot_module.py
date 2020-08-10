import generator
import generator.util
import numpy as np

# generate test data
seconds = np.linspace(1, 60, 42)
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
plot_module = generator.Plot(data)
plot_module.set_plot_colors(plot_color)

plot_module.set_axis_label('x', "Time [s]", rotation="horizontal")
plot_module.set_axis_label('y', "Error\n[relMSE]", rotation="vertical")
plot_module.set_axis_props('x', range=[1, 65], ticks=[2, 10, 20], use_log_scale=True, use_scientific_notations=False)
plot_module.set_axis_props('y', range=[10, 105], ticks=[10, 30, 50], use_log_scale=True, use_scientific_notations=False)

plot_module.set_marker_v_line(pos=10.5, color=[242, 113, 0], linestyle=(0,(4,6)), linewidth_pt=0.6)
plot_module.set_marker_v_line(pos=12.0, color=[242, 113, 0], linestyle=(0,(4,6)), linewidth_pt=0.6)

plot_module.set_width_to_height_aspect_ratio(1.15)

if __name__ == "__main__":
    generator.horizontal_figure([plot_module], width_cm=11., filename='matplot_test.pdf')
    generator.horizontal_figure([plot_module], width_cm=11., filename='matplot_test.pptx')
    generator.horizontal_figure([plot_module], width_cm=11., filename='matplot_test.html')