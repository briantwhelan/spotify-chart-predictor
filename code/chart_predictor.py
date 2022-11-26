import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# Import the data.
df = pd.read_csv("./data/data.csv")
X = df.iloc[:, 3:]
y = df.iloc[:, 2]

# Split data into training and validation data.
X_train, X_validate, y_train, y_validate = train_test_split(X, y, test_size=0.2, random_state=9801)

# Establish baseline model.
baseline_model = DummyClassifier(strategy="most_frequent")
baseline_model.fit(X_train, y_train)
baseline_preds = baseline_model.predict(X_validate)
print(confusion_matrix(y_validate, baseline_preds))
print(classification_report(y_validate, baseline_preds))
