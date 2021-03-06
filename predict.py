from classifier import RFClass
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

image_links = ['image.png']
image_names = []
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"): 
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

data = pd.DataFrame(list(zip(numerical_texts, latex, confidence, texts, image_names)), columns = ['numerical_text', 'latex', 'confidence', 'text', 'label'])

import os 
import pandas as pd
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk


nltk.download('stopwords')
nltk.download("words")
lemmatizer = WordNetLemmatizer()

corpus_list = []

def normalize_whitespace(text):
    try:
        corrected = str(text)
        corrected = re.sub(r"//t",r"\t", corrected)
        corrected = re.sub(r"( )\1+",r"\1", corrected)
        corrected = re.sub(r"(\n)\1+",r"\1", corrected)
        corrected = re.sub(r"(\r)\1+",r"\1", corrected)
        corrected = re.sub(r"(\t)\1+",r"\1", corrected)
        return corrected.strip(" ")
    except AttributeError:
        return np.NaN

def simplify_punctuation(text):
    try:
        corrected = str(text)
        slash = re.compile(r"\\")
        corrected = re.sub(r'[!?,;{}\\]+', "", corrected)
        
        return corrected
    except AttributeError:
        return np.NaN

def remove_stopwords(text):
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    words = set(nltk.corpus.words.words())
    text = " ".join(tokens_without_sw)
    return " ".join(w for w in nltk.wordpunct_tokenize(text) \
         if w.lower() in words or not w.isalpha())

def lemmatize(text):
    text = [lemmatizer.lemmatize(word) for word in text]
    return "".join(text)

def keep_string(text):
    text = re.sub('\-+', " ", text)
    text = re.sub('[^0-9a-zA-Z ]+', '', text)
    text = re.sub('[0-9]+', 'number', text)
    text = re.sub(r"\b[a-zA-Z]\b", "", text)

    words = set()
    result = ''
    for word in text.split():
        if word not in words:
            result = result + word + ' '
            words.add(word)
    return result

columns = data.columns

for column in columns:
    data[column]= data[column].transform(normalize_whitespace)
    data[column] = data[column].str.lower()
    data[column] = data[column].transform(simplify_punctuation)

    data[column] = data[column].transform(keep_string)
    data[column]= data[column].transform(normalize_whitespace)
    data[column].fillna("unknown", inplace=True)
    data[column].replace("", "unknown", inplace=True)

data['text'] = data['text'].transform(lemmatize)
data['text'] = data['text'].transform(remove_stopwords)
data['text'].fillna("unknown", inplace=True)
data['text'].replace("", "unknown", inplace=True)

data['finaltext'] = data[['text', 'latex']].agg(' '.join, axis=1)

for item in data['text']:
    text_tokens = word_tokenize(item)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    corpus_list = corpus_list + tokens_without_sw

freq_corpus = {}
for item in corpus_list:
    if item in freq_corpus.keys():
        freq_corpus[item] += 1
    else:
        freq_corpus[item] = 1

freq_sorted = sorted(freq_corpus.items(), key=lambda item: item[1], reverse=True)


common = [item for item in freq_sorted if item[1] >1]

from sklearn.feature_extraction.text  import TfidfVectorizer
import pandas as pd
import pickle

X = data['finaltext']

#load the content
tfidf = pickle.load(open("features.pkl", "rb" ) )

X = tfidf.transform(X)
RFClass = pickle.load(open("model.pkl", 'rb'))

prediction = RFClass.predict(X)

print("models prediction is:", prediction[0])