import os 
import pandas as pd
import re
import numpy as np

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


data = pd.read_csv("data_1.csv")

columns = data.columns

for column in columns:
    data[column]= data[column].transform(normalize_whitespace)
