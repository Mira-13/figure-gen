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

plot = figuregen.MatplotLinePlot(1.15, data)
plot.set_axis_label('x', "sec", rotation="horizontal")
plot.set_axis_label('y', "error", rotation="vertical")
plot.set_axis_properties('x', range=[1, 65], ticks=[5, 25, 50], use_log_scale=False, use_scientific_notations=False)
plot.set_axis_properties('y', range=None, ticks=[5, 10, 30, 50], use_log_scale=True, use_scientific_notations=False)
plot.set_v_line(pos=10.5, color=[242, 113, 0], linestyle=(0,(4,6)), linewidth_pt=0.6)
plot.set_colors(plot_color)
plot.set_linestyle(1, "dashed")
plot.set_legend(["first line", "second line"])

# ----- PLOT Module -----
plot_module = figuregen.Grid(1,1)
plot_module.get_element(0,0).set_image(plot)

if __name__ == "__main__":
    figuregen.horizontal_figure([plot_module], width_cm=11., filename='matplot_test.pdf')
    figuregen.horizontal_figure([plot_module], width_cm=11., filename='matplot_test.pptx')
    figuregen.horizontal_figure([plot_module], width_cm=11., filename='matplot_test.html')