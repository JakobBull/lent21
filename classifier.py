

from sklearn.feature_extraction.text  import TfidfVectorizer
import pandas as pd
import pickle
import numpy as np

data = pd.read_csv('data_2.csv')
data = data.iloc[np.random.permutation(len(data))]

Tfidf = TfidfVectorizer(ngram_range=(1, 2))


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


RFClass = RandomForestClassifier(n_estimators=500, criterion="gini", random_state=77)
#X_train, X_test, y_train, y_test = train_test_split(data['finaltext'], data["label"], test_size = 1/5, random_state = 50)
X_train = data['finaltext']
y_train = data['label']

tfidf_features = Tfidf.fit(X_train)
X_train = tfidf_features.transform(X_train)
#X_test = tfidf_features.transform(X_test)

RFClass.fit(X_train,y_train)
#prediction = RFClass.predict(X_test)
#print("accuracy score:")
#print(accuracy_score(y_test, prediction))

#for y, pred in zip(y_test, prediction):
#    print("label:", y, ", prediction:", pred)

pickle.dump(RFClass, open("model.pkl", "wb"))

#store the content
with open("features.pkl", 'wb') as handle:
                    pickle.dump(tfidf_features, handle)
