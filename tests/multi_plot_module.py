import multi_module
import matplot_module
import generator
import generator.util

plot_module = matplot_module.modules[0]


some_modules = multi_module.modules

combined_modules = some_modules
combined_modules.append(plot_module)

if __name__ == "__main__":
    generator.horizontal_figure(modules, width_cm=18., filename='multiplot_test.pdf')
    generator.horizontal_figure(modules, width_cm=18., filename='multiplot_test.pptx')
    generator.horizontal_figure(modules, width_cm=18., filename='multiplot_test.html')