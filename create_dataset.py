import mathpix
import json
import pandas as pd
import os
import time
import socket

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
confidence = []

calls = 0

for link in image_links:

    calls += 1

    if calls <100:
        pass

    else:
        print("Waiting for API")
        time.sleep(60)
        calls = 0

    print(calls)

    try:

        r = mathpix.latex({
            'src': mathpix.image_uri(link),
            'formats': formats
        })
    except socket.error:
        print(link)
        pass

 

    try:

        element = r['latex_confidence']

        if element != None:
            confidence.append(element)
        else:
            confidence.append("0")

        element = r['latex_simplified']

        if element != None:
            latex.append(element)
        else:
            latex.append("error")

        element = r['text']

        if element != None:
            numerical_texts.append(element)
        else:
            numerical_texts.append("error")
    except KeyError:
        latex.append("error")
        numerical_texts.append("error")

    element = pytesseract.image_to_string(Image.open(link))
    
    if element != None:
        texts.append(element)
    else:
        texts.append("error")

print(len(latex), len(numerical_texts), len(texts))

data = pd.DataFrame(list(zip(numerical_texts, latex, texts, image_names)), columns = ['numerical_text', 'latex', 'text', 'label'])

data.to_csv('data_1.csv')