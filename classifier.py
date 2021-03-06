
indeces = ["^"]
algebra = ["factorise", "sqrt", "solve", "expand", "work out", "simplify", "formula", "in terms of", "algebraic"]
ratios = ["ratio", "%", "VAT", "proportion"]
stats = ["distribution"]
simultaneous = ["simultaneous"]
inequalities = ["<", ">", "inequality", "inequalities"]
probability = ["probability", "dice", "tree diagram", "chance"]
proof = ["prove"]
numbers = ["express", "prime", "write"]

from sklearn.feature_extraction.text  import TfidfVectorizer
import pandas as pd
import pickle

data = pd.read_csv('data_2.csv')

Tfidf = TfidfVectorizer(ngram_range=(1, 2))


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


RFClass = RandomForestClassifier(n_estimators=500, criterion="gini", random_state=77)
X_train, X_test, y_train, y_test = train_test_split(data['finaltext'], data["label"], test_size = 1/5, random_state = 50)


tfidf_features = Tfidf.fit(X_train)
X_train = tfidf_features.transform(X_train)
X_test = tfidf_features.transform(X_test)

RFClass.fit(X_train,y_train)
prediction = RFClass.predict(X_test)
print("accuracy score:")
print(accuracy_score(y_test, prediction))

pickle.dump(RFClass, open("model.pkl", "wb"))

#store the content
with open("features.pkl", 'wb') as handle:
                    pickle.dump(tfidf_features, handle)
