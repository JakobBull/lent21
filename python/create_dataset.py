import mathpix 
import json
import pandas as pd

try:
    from PIL import Image
except:
    import Image

import pytesseract




image_links = ['/home/jakob/Documents/Hackathon/lent21/questions/question101.png','/home/jakob/Documents/Hackathon/lent21/questions/question102.png']
formats = ['latex_simplified', 'text']

numerical_texts = []
latex = []
texts = []

for link in image_links:

    r = mathpix.latex({
        'src': mathpix.image_uri(link),
        'formats': formats
    })

    print(r)

    try:
        element = r['latex_simplified']

        if element != None:
            latex.append(element)
        else:
            latex.append("")

        element = r['text']

        if element != None:
            numerical_texts.append(element)
        else:
            numerical_texts.append("")
    except KeyError:
        latex.append("")
        numerical_texts.append("")

    element = pytesseract.image_to_string(Image.open(link))
    
    if element != None:
        texts.append(element)
    else:
        texts.append("")

print(latex, numerical_texts, texts)