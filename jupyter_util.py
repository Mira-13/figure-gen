from pdf2image import convert_from_path
import IPython
from IPython.display import Image
import cv2
import numpy as np

def loadpdf(pdfname):
    images = convert_from_path(pdfname, dpi=1000)
    return np.array(images[0])

def convert(pdfname):
    img = loadpdf(pdfname)
    cv2.imwrite(pdfname.replace('.pdf', '.png'), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    return pdfname.replace('.pdf', '.png')

def display(pdfname):
    img = convert(pdfname)
    IPython.display.display(Image(pdfname.replace('.pdf', '.png')))