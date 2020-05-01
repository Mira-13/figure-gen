import imageio
import os
import json
import sys
from shutil import rmtree


class CreateFigurePNGs:
    ''' Process array image data in content dictionary
    Make out of array image data new image files: give them unique.png-names and save them in separate folder, 
    update content dictionary with new pathfile and delete old array image data,
    create new content.json file with the new content dictionary.
    '''
    def __init__(self, module_path):
        self.module_path = module_path

        content_script = 'content.py'
        with open(os.path.join(self.module_path, content_script), 'r') as f:
            src = f.read()
        compiled_script = compile(src, filename=os.path.join(self.module_path, content_script), mode='exec')

        script_variables = {}
        exec(compiled_script, {'util': util, 'manage_images': manage_images}, script_variables)
        self.data = script_variables['data']

        img_path = self.gen_empty_image_folder()
        self.process_images(img_path)

    def gen_empty_image_folder(self):
        try: 
            img_folder_path = os.path.join(self.module_path, 'images')
            os.makedirs(img_folder_path)
        except OSError:
            rmtree(img_folder_path)
            os.makedirs(img_folder_path)
        return img_folder_path

    def save_to_png(self, img, filename):
        # scipy.misc.toimage(img, cmin=0.0, cmax=1.0).save(filename)
        imageio.imwrite(filename, img)

    def process_images(self, img_folder_path):
        rowIndex = 0
        for row in self.data['elements_content']:
            rowIndex += 1
            colIndex = 0
            for elem in row:
                colIndex += 1
                unique_name = 'image-'+str(rowIndex)+'-'+str(colIndex) + '.png'

                image = elem['image']
                
                # IN CASE SOMEONE WANTS PLOTS IN THEIR GRID: THEREFORE, 2 cases
                if str(type(image)) == "<class 'numpy.ndarray'>": #image data = array/list
                    elem['filename'] = os.path.join(img_folder_path, unique_name)  
                    self.save_to_png(image, elem['filename'])
                else:# else 'wherever/plot.pdf'
                    # naming convention does not matter, because it does not matter for tikz as long as it is a legit path-file
                    elem['filename'] = image
                
                del elem['image'] # call image raw data before json export

    def create_content_json(self, content_filename):
        with open(os.path.join(self.module_path, content_filename), 'w') as f:
            json.dump(self.data, f, indent=2)
        

class CreateFigureJSON:
    ''' Combines the content and layout dictionaries into a single .json file
    
    Merge figure content dictionary with the layout and design and process images: 
    create a content json out of content dictionary and combine content json and layout json to one json file.
    In case, the user took the option to adjust img_width and img_height based on img_width_px or
    img_height_px we do that before saving the final json file. This makes sure, that the picture will 
    not be distorted.
    '''
    def __init__(self, module_path):
        self.module_path = module_path

    def merge(self, dict1, dict2): 
        res = {**dict1, **dict2} 
        return res
    
    def adjust_image_res(self, jsonMerged, is_img_res_based_on_width, is_img_res_based_on_height):
        if is_img_res_based_on_width:
            calculate.overwrite_image_resolution_based_on_total_width(jsonMerged)
        elif is_img_res_based_on_height: 
            calculate.overwrite_image_resolution_based_on_total_height(jsonMerged)
        return jsonMerged # not sure if I need to return it or if it is already overwritten?

    def merge_content_and_config_files(self, content_filename, is_img_res_based_on_width, is_img_res_based_on_height):
        with open(os.path.join(self.module_path, 'layout_and_design.json'), 'r') as json_file:
            dict_configs = json.load(json_file)

        with open(os.path.join(self.module_path, content_filename), 'r') as json_file2:
            dict_content = json.load(json_file2)

        jsonMerged = self.merge(dict_configs, dict_content)

        jsonMerged = self.adjust_image_res(jsonMerged, is_img_res_based_on_width, is_img_res_based_on_height)
        
        with open(os.path.join(self.module_path, 'gen_figure.json'), 'w') as file:
            json.dump(jsonMerged, file)
        print('Merged content and config to one file.')


a = CreateFigurePNGs(module_path)
a.create_content_json(content_filename)

b = CreateFigureJSON(module_path)
b.merge_content_and_config_files(content_filename, is_img_res_based_on_width, is_img_res_based_on_height)