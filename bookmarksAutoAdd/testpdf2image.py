import pdf2image
import pytesseract
from PIL import Image as PI
import io
import os
pdf_path='D:/目录.pdf'
outputDir='D:/pdfImg'
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
images=pdf2image.convert_from_path(pdf_path,800,output_folder='d:/')
for idx,img in enumerate(images):
    img.save(os.path.join(outputDir,'page_{}.png'.format(idx)))


print('done.')
