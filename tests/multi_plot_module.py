import multi_module
import matplot_module
import figuregen
import figuregen.util

multi_type_modules = [
    multi_module.grid0,
    multi_module.grid1,
    matplot_module.plot_module,
]

if __name__ == "__main__":
    figuregen.horizontal_figure(multi_type_modules, width_cm=18., filename='multiplot_test.pdf')
    figuregen.horizontal_figure(multi_type_modules, width_cm=18., filename='multiplot_test.pptx')
    figuregen.horizontal_figure(multi_type_modules, width_cm=18., filename='multiplot_test.html')