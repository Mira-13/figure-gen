import multi_module
import matplot_module
import generator
import generator.util

plot_module = matplot_module.plot_module

some_modules = [multi_module.grid0, multi_module.grid1]

multi_type_modules = some_modules
multi_type_modules.append(plot_module)

if __name__ == "__main__":
    generator.horizontal_figure(multi_type_modules, width_cm=18., filename='multiplot_test.pdf')
    generator.horizontal_figure(multi_type_modules, width_cm=18., filename='multiplot_test.pptx')
    #generator.horizontal_figure(multi_type_modules, width_cm=18., filename='multiplot_test.html')