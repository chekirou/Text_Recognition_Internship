
from wand.image import Image as Img
from PIL import Image
import pytesseract
import pyocr
import pyocr.builders
from tika import parser # pip install tika



"""
Note : La librairie open-source ocrmypdf peut être utilisée conjointement a ces OCR afin de profiter des prétraitements qu'elle implémente
"""



"""
Cette fonction pré-traite un document pdf pour créer des images correspondant aux différentes pages qui le composent
ATTENTION : Pour les receuil en entier cette opération peut prendre excessivement beaucoup de temps.
"""
def preporcess_pdf(path,quality=99):
    with Img(filename=path, resolution=300) as img:
        img.compression_quality = quality
        img.save(filename=path.split(".")[0]+".jpg")



"""
OCR 
"""
def textract_ocr(path_to_im):
    import textract
    text = textract.process(path_to_im, encoding='ascii', method='tesseract')
    return text

def pytesseract_ocr(path_to_im):
    text = pytesseract.image_to_string(Image.open(path_to_im))
    return (text)


def pyocr_ocr(path_to_im):
    tools = pyocr.get_available_tools()[0]
    text = tools.image_to_string(Image.open(path_to_im), builder=pyocr.builders.TextBuilder())
    return (text)

def tika_readpdf(path_to_pdf):
    raw = parser.from_file(path_to_pdf)
    return (raw['content'])

