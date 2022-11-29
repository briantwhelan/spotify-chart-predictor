import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve

# Import the data.
charted = pd.read_csv("./data/charted_songs.csv")
uncharted = pd.read_csv("./data/uncharted_songs.csv")
songs = pd.concat([charted.iloc[:100], uncharted.iloc[:100]])
X = songs.iloc[:, 3:]
y = songs.iloc[:, 2]

# Split data into training and validation data.
X_train, X_validate, y_train, y_validate = train_test_split(X, y, test_size=0.2, random_state=9801)

# Establish baseline model.
baseline_model = DummyClassifier(strategy="most_frequent")
baseline_model.fit(X_train, y_train)
baseline_preds = baseline_model.predict(X_validate)
print(confusion_matrix(y_validate, baseline_preds))
print(classification_report(y_validate, baseline_preds))

# Perform cross validation to select q.
mean_error = []
std_error = []
q_range = [1, 2, 3, 4, 5, 6]
kf = KFold(n_splits=5)
for q in q_range:
  X_poly = PolynomialFeatures(q).fit_transform(X_train)
  model = LogisticRegression(penalty="l2", C=1)
  scores = cross_val_score(model, X_poly, y_train, cv=kf, scoring="f1")
  mean_error.append(np.array(scores).mean())
  std_error.append(np.array(scores).std())
plt.rc("font", size=18)
plt.errorbar(q_range, mean_error, yerr=std_error, linewidth=3)
plt.xlabel("q")
plt.ylabel("F1 Score")
plt.title("q Cross Validation for Logistic Regression Model")
plt.legend()
plt.savefig("./plots/lr-q-cross-validation.png")

# Perform cross validation to select C.
mean_error = []
std_error = []
c_range = [0.01, 0.1, 1, 10, 100]
kf = KFold(n_splits=5)
for c in c_range:
  model = LogisticRegression(penalty="l2", C=c)
  scores = cross_val_score(model, X_train, y_train, cv=kf, scoring="f1")
  mean_error.append(np.array(scores).mean())
  std_error.append(np.array(scores).std())
plt.rc("font", size=18)
plt.rcParams["figure.constrained_layout.use"] = True
plt.errorbar(c_range, mean_error, yerr=std_error, linewidth=3)
plt.xlabel("C")
plt.ylabel("F1 Score")
plt.title("C Cross Validation for Logistic Regression Model")
plt.legend()
plt.savefig("./plots/lr-C-cross-validation.png")

# Train logistic regression classifier (with L2 penalty) with hyperparameters from cross-validation.
lrl2_model = LogisticRegression(penalty="l2", C=1000)
lrl2_model.fit(X_train, y_train)
lrl2_preds = lrl2_model.predict(X_validate)
print(confusion_matrix(y_validate, lrl2_preds))
print(classification_report(y_validate, lrl2_preds))
# Perform cross validation to select k.
mean_error = []
std_error = []
k_range = [1, 5, 10, 20, 50, 100]
kf = KFold(n_splits=5)
for k in k_range:
  from sklearn.neighbors import KNeighborsClassifier
  model = KNeighborsClassifier(n_neighbors=k)
  scores = cross_val_score(model, X_train, y_train, cv=kf, scoring="f1")
  mean_error.append(np.array(scores).mean())
  std_error.append(np.array(scores).std())
plt.rc("font", size=18)
plt.rcParams["figure.constrained_layout.use"] = True
plt.errorbar(k_range, mean_error, yerr=std_error, linewidth=3)
plt.xlabel("k")
plt.ylabel("F1 Score")
plt.title("k Cross Validation for kNN Model")
plt.legend()
plt.savefig("./plots/kNN-k-cross-validation.png")

# Train kNN classifier with k selected from cross-validation.
kNN_model = KNeighborsClassifier(n_neighbors=5)
kNN_model.fit(X_train, y_train)
kNN_preds = kNN_model.predict(X_validate)
print(confusion_matrix(y_validate, kNN_preds))
print(classification_report(y_validate, kNN_preds))

# Plot ROC curves for baseline, logistic regression classifier, kNN classifier.
fig = plt.figure()
plt.rc("font", size=10)
plt.rcParams["figure.constrained_layout.use"] = True

probs = lrl2_model.predict_proba(X_validate)
fpr, tpr, _ = roc_curve(y_validate, probs[:, 1])
plt.plot(fpr, tpr, color="blue", label="Logistic Regression Classifier")

probs = kNN_model.predict_proba(X_validate)  
fpr, tpr, _ = roc_curve(y_validate, probs[:, 1])
plt.plot(fpr, tpr, color="orange", label="kNN Classifier")

probs = baseline_model.predict_proba(X_validate)  
fpr, tpr, _ = roc_curve(y_validate, probs[:, 1])
plt.plot(fpr, tpr, color="red", label="Baseline Classifier")

plt.plot([0,1], [0,1], color="green", linestyle="--", label="Random Classifier")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves")
plt.legend()
plt.savefig("./plots/ROC-curves.png")