import os

def generate_image(element):
    pass

def generate(module_data, to_path, filename):
    html_code = ""

    # generate all elements of the grid
    for elem in module_data['elements_content']:
        html_code += generate_image(elem)

    with open(os.path.join(to_path, filename), "w") as file:
        file.write(html_code)
