#from classifier import RFClass
import mathpix
import json
import pandas as pd
import os
import time
import socket
import pytesseract
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from sklearn.feature_extraction.text  import TfidfVectorizer
import pandas as pd
import pickle

nltk.download('stopwords')
nltk.download("words")
nltk.download('wordnet')
nltk.download('punkt')

class Predict:

    def __init__(self):
        self.directory = 'questions'
        self.formats = ['latex_simplified', 'text']
        self.numerical_texts = []
        self.latex = []
        self.texts = []
        self.confidence = []
        self.lemmatizer = WordNetLemmatizer()
    

    def predict(self, path):
        data = self.image_to_text(path)
        columns = data.columns

        for column in columns:
            data[column]= data[column].transform(self.normalize_whitespace)
            data[column] = data[column].str.lower()
            data[column] = data[column].transform(self.simplify_punctuation)

            data[column] = data[column].transform(self.keep_string)
            data[column]= data[column].transform(self.normalize_whitespace)
            data[column].fillna("unknown", inplace=True)
            data[column].replace("", "unknown", inplace=True)

        data['text'] = data['text'].transform(self.lemmatize)
        data['text'] = data['text'].transform(self.remove_stopwords)
        data['text'].fillna("unknown", inplace=True)
        data['text'].replace("", "unknown", inplace=True)

        data['finaltext'] = data[['text', 'latex']].agg(' '.join, axis=1)

        label = self.compute_label(data)
        
        return label


    def compute_label(self, data):
        X = data['finaltext']
        #load the content
        tfidf = pickle.load(open("features.pkl", "rb" ) )

        try:
            X = tfidf.transform(X)
            RFClass = pickle.load(open("model.pkl", 'rb'))

            prediction = RFClass.predict(X)
            
            return prediction[0]
        except ValueError:
            return "error"

    def image_to_text(self, link):
        try:
            from PIL import Image
        except:
            import Image

        self.r = mathpix.latex({
            'src': mathpix.image_uri(link),
            'formats': self.formats
        })
        '''except socket.error:
            print('hi i am naresh')
            pass'''

        try:

            self.element = self.r['latex_confidence']

            if self.element != None:
                self.confidence.append(self.element)
            else:
                self.confidence.append("0")

            element = self.r['latex_simplified']

            if element != None:
                self.latex.append(element)
            else:
                self.latex.append("error")

            element = self.r['text']

            if element != None:
                self.numerical_texts.append(element)
            else:
                self.numerical_texts.append("error")
        except KeyError:
            self.latex.append("error")
            self.numerical_texts.append("error")

        element = pytesseract.image_to_string(Image.open(link))
        
        if element != None:
            self.texts.append(element)
        else:
            self.texts.append("error")

        self.data = pd.DataFrame(list(zip(self.numerical_texts, self.latex, self.confidence, self.texts)), columns = ['numerical_text', 'latex', 'confidence', 'text'])
        return self.data

    @staticmethod
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

    @staticmethod
    def simplify_punctuation(text):
        try:
            corrected = str(text)
            slash = re.compile(r"\\")
            corrected = re.sub(r'[!?,;{}\\]+', "", corrected)
            
            return corrected
        except AttributeError:
            return np.NaN

    @staticmethod
    def remove_stopwords(text):
        text_tokens = word_tokenize(text)
        tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
        words = set(nltk.corpus.words.words())
        text = " ".join(tokens_without_sw)
        return " ".join(w for w in nltk.wordpunct_tokenize(text) \
            if w.lower() in words or not w.isalpha())

    
    def lemmatize(self, text):
        text = [self.lemmatizer.lemmatize(word) for word in text]
        return "".join(text)

    @staticmethod
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



'''if __name__ == "__main__":
    Pred = Predict()
    print("models prediction is:", Pred.predict("image.png"))'''