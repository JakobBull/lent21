import mathpix_api.mathpix as mathpix
import json
import pandas as pd
import os


try:
    from PIL import Image
except:
    import Image

import pytesseract


def return_label(name):
    label_list = ["algebra", "indeces", "inequalities", "numbers", "probability", "proof", "ratios", "simultaneous", "stats"]
    for item in label_list:
        if item in str(name):
            return item

    return "unknown"

#path = os.path.join()
directory = 'questions'

image_links = []
image_names = []
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"): 
         image_links.append(os.path.join(directory, filename))
         image_names.append(return_label(filename))
    else:
        continue

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

data = pd.DataFrame(list(zip(numerical_texts, latex, texts, filename), columns = ['numerical_text', 'latex', 'text', 'label']))

data.to_csv('data_1.csv')