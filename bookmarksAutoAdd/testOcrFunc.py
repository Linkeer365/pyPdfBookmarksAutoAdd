from pytesseract import pytesseract
from PIL import Image as PI

# open image
image = PI.open('D:\AllDowns\pufxwq.png')
code = pytesseract.image_to_string(image,lang='chi_sim')
print(code)

