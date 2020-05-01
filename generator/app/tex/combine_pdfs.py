import glob
import os

def create_header():
    documentclass = r"\documentclass{standalone}\n"
    packages = ["{graphicx}", "[utf8]{inputenc}"]
    usepackages = [r"\usepackage" + p + r"\n" for p in packages]
    header = documentclass + ''.join(usepackages) + r'\begin{document}\n'
    return header 

def include_graphics(path, search_for_filename='gen_pdf'):
    pattern = os.path.join(path, search_for_filename + '*.pdf')
    files = glob.glob(pattern)
    
    code = ['\includegraphics[]{' + f + '}%' for f in files]
    code.append('')
    code.append('\end{document}')
    content = '\n'.join(code)
    return content


#\includegraphics[]{gen_pdf_file1.pdf}%
#\includegraphics[]{gen_pdf_file2.pdf}%
#\includegraphics[]{gen_plot.pdf}



#\end{document}

