import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve 

# Import the data.
charted = pd.read_csv("./data/charted_songs.csv")
charted['charted'] = True
uncharted = pd.read_csv("./data/uncharted_songs.csv")
uncharted['charted'] = False
songs = pd.concat([charted.iloc[:len(uncharted.axes[0])], uncharted.iloc[:len(charted.axes[0])]])
all_songs = pd.read_csv("./data/features.csv")

# Normalise features.
songs["duration_ms"] = (songs["duration_ms"] - all_songs["duration_ms"].min()) / (all_songs["duration_ms"].max() - all_songs["duration_ms"].min())   
songs["tempo"] = (songs["tempo"] - all_songs["tempo"].min()) / (all_songs["tempo"].max() - all_songs["tempo"].min())    
songs["loudness"] = (songs["loudness"] - (-60)) / (0 - (-60))
print("------------------------Features------------------------")
print(songs)

# Select features.
y = songs.iloc[:, 15]
print("Speechiness correlation: ", songs["speechiness"].corr(y))
print("Duration correlation: ", songs["duration_ms"].corr(y))
print("Tempo correlation: ", songs["tempo"].corr(y))
print("Energy correlation: ", songs["energy"].corr(y))
print("Acousticness correlation: ", songs["acousticness"].corr(y))
print("Valence correlation: ", songs["valence"].corr(y))
print("Instrumentalness correlation: ", songs["instrumentalness"].corr(y))
print("Liveness correlation: ", songs["liveness"].corr(y))
print("Loudness correlation: ", songs["loudness"].corr(y))
print("Danceability correlation: ", songs["danceability"].corr(y))
print(songs.iloc[:, [1,2,3,4,5,6,8,9,10,11]].corr(method='pearson'))
X = songs.iloc[:, [4,6,8,11]]

# Split data into training and validation data.
X_train, X_validate, y_train, y_validate = train_test_split(X, y, test_size=0.2, random_state=9801)

# Establish baseline model.
baseline_model = DummyClassifier(strategy="most_frequent")
baseline_model.fit(X_train, y_train)
baseline_preds = baseline_model.predict(X_validate)
print("------------------------Baseline------------------------")
print(confusion_matrix(y_validate, baseline_preds))
print(classification_report(y_validate, baseline_preds, zero_division=0))

# Perform cross validation to select q.
mean_error = []
std_error = []
q_range = [1, 2, 3, 4, 5, 6]
kf = KFold(n_splits=5)
for q in q_range:
  X_poly = PolynomialFeatures(q).fit_transform(X_train)
  model = LogisticRegression(penalty="l2", C=1, max_iter=1000)
  scores = cross_val_score(model, X_poly, y_train, cv=kf, scoring="f1")
  mean_error.append(np.array(scores).mean())
  std_error.append(np.array(scores).std())
plt.rc("font", size=18)
plt.errorbar(q_range, mean_error, yerr=std_error, linewidth=3)
plt.xlabel("q")
plt.ylabel("F1 Score")
plt.title("q Cross Validation for Logistic Regression Model")
plt.savefig("./plots/lr-q-cross-validation.png")
plt.clf()

# Perform cross validation to select C.
mean_error = []
std_error = []
c_range = [0.01, 0.1, 1, 5, 10, 15, 20, 100]
kf = KFold(n_splits=5)
for c in c_range:
  model = LogisticRegression(penalty="l2", C=c, max_iter=1000)
  scores = cross_val_score(model, X_train, y_train, cv=kf, scoring="f1")
  mean_error.append(np.array(scores).mean())
  std_error.append(np.array(scores).std())
plt.rc("font", size=18)
plt.rcParams["figure.constrained_layout.use"] = True
plt.errorbar(c_range, mean_error, yerr=std_error, linewidth=3)
plt.xlabel("C")
plt.ylabel("F1 Score")
plt.title("C Cross Validation for Logistic Regression Model")
plt.savefig("./plots/lr-C-cross-validation.png")
plt.clf()

# Train logistic regression classifier (with L2 penalty) with hyperparameters selected from cross-validation.
lrl2_model = LogisticRegression(penalty="l2", C=1, max_iter=1000)
poly = PolynomialFeatures(4)
lrl2_model.fit(poly.fit_transform(X_train), y_train)
lrl2_preds = lrl2_model.predict(poly.fit_transform(X_validate))
# lrl2_model.fit(X_train, y_train)
# lrl2_preds = lrl2_model.predict(X_validate)
print("------------------Logistic Regression------------------")
print(lrl2_model.coef_[0])
print(confusion_matrix(y_validate, lrl2_preds))
print(classification_report(y_validate, lrl2_preds))

# Perform cross validation to select k.
mean_error = []
std_error = []
k_range = [1, 5, 10, 20, 50, 100, 200, 300, 400, 500, 600]
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
plt.savefig("./plots/kNN-k-cross-validation.png")
plt.clf()

# Train kNN classifier with k selected from cross-validation.
kNN_model = KNeighborsClassifier(n_neighbors=200)
kNN_model.fit(X_train, y_train)
kNN_preds = kNN_model.predict(X_validate)
print("--------------------------kNN--------------------------")
print(confusion_matrix(y_validate, kNN_preds))
print(classification_report(y_validate, kNN_preds))

# Perform cross validation to select C.
mean_error = []
std_error = []
c_range = [0.01, 0.1, 1, 10, 100]
kf = KFold(n_splits=5)
for c in c_range:
  model = SVC(C=c, kernel="rbf", gamma=1, probability=True).fit(X_train, y_train)
  scores = cross_val_score(model, X_train, y_train, cv=kf, scoring="f1")
  mean_error.append(np.array(scores).mean())
  std_error.append(np.array(scores).std())
plt.rc("font", size=18)
plt.rcParams["figure.constrained_layout.use"] = True
plt.errorbar(c_range, mean_error, yerr=std_error, linewidth=3)
plt.xlabel("C")
plt.ylabel("F1 Score")
plt.title("C Cross Validation for Kernalized SVM Model")
plt.savefig("./plots/svm-C-cross-validation.png")
plt.clf()

# Perform cross validation to select gamma.
mean_error = []
std_error = []
gamma_range = [0.01, 0.1, 1, 10]
kf = KFold(n_splits=5)
for g in gamma_range:
  model = SVC(C=1, kernel="rbf", gamma=g, probability=True).fit(X_train, y_train)
  scores = cross_val_score(model, X_train, y_train, cv=kf, scoring="f1")
  mean_error.append(np.array(scores).mean())
  std_error.append(np.array(scores).std())
plt.rc("font", size=18)
plt.rcParams["figure.constrained_layout.use"] = True
plt.errorbar(gamma_range, mean_error, yerr=std_error, linewidth=3)
plt.xlabel("C")
plt.ylabel("F1 Score")
plt.title("Gamma Cross Validation for Kernalized SVM Model")
plt.savefig("./plots/svm-gamma-cross-validation.png")
plt.clf()

# Train kernalised SVM classifier with hyperparameters from cross-validation.
svm_model = SVC(C=1, kernel="rbf", gamma=1, probability=True).fit(X_train, y_train)
svm_preds = svm_model.predict(X_validate)
print("---------------------Kernelized SVM---------------------")
print(confusion_matrix(y_validate, svm_preds))
print(classification_report(y_validate, svm_preds))

# Plot ROC curves for baseline, logistic regression classifier, kNN classifier.
fig = plt.figure()
plt.rc("font", size=10)
plt.rcParams["figure.constrained_layout.use"] = True

probs = baseline_model.predict_proba(X_validate)  
fpr, tpr, _ = roc_curve(y_validate, probs[:, 1])
plt.plot(fpr, tpr, color="red", label="Baseline Classifier")

probs = lrl2_model.predict_proba(poly.fit_transform(X_validate))
# probs = lrl2_model.predict_proba(X_validate)
fpr, tpr, _ = roc_curve(y_validate, probs[:, 1])
plt.plot(fpr, tpr, color="blue", label="Logistic Regression Classifier")

probs = kNN_model.predict_proba(X_validate)  
fpr, tpr, _ = roc_curve(y_validate, probs[:, 1])
plt.plot(fpr, tpr, color="orange", label="kNN Classifier")

probs = svm_model.predict_proba(X_validate)  
fpr, tpr, _ = roc_curve(y_validate, probs[:, 1])
plt.plot(fpr, tpr, color="purple", label="Kernalized SVM Classifier")

plt.plot([0,1], [0,1], color="green", linestyle="--", label="Random Classifier")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves")
plt.legend()
plt.savefig("./plots/ROC-curves.png")

# Write results to file.
with open ("results.txt", 'w') as out_file:
  print("------------------------Features------------------------", file=out_file)
  print(songs, file=out_file)  
  print("Speechiness correlation: ", songs["speechiness"].corr(y), file=out_file)
  print("Duration correlation: ", songs["duration_ms"].corr(y), file=out_file)
  print("Tempo correlation: ", songs["tempo"].corr(y), file=out_file)
  print("Energy correlation: ", songs["energy"].corr(y), file=out_file)
  print("Acousticness correlation: ", songs["acousticness"].corr(y), file=out_file)
  print("Valence correlation: ", songs["valence"].corr(y), file=out_file)
  print("Instrumentalness correlation: ", songs["instrumentalness"].corr(y), file=out_file)
  print("Liveness correlation: ", songs["liveness"].corr(y), file=out_file)
  print("Loudness correlation: ", songs["loudness"].corr(y), file=out_file)
  print("Danceability correlation: ", songs["danceability"].corr(y), file=out_file)
  print(songs.iloc[:, [1,2,3,4,5,6,8,9,10,11]].corr(method='pearson'), file=out_file)

  print("------------------------Baseline------------------------", file=out_file)
  print(confusion_matrix(y_validate, baseline_preds), file=out_file)
  print(classification_report(y_validate, baseline_preds, zero_division=0), file=out_file)

  print("------------------Logistic Regression------------------", file=out_file)
  print(lrl2_model.coef_[0], file=out_file)
  print(confusion_matrix(y_validate, lrl2_preds), file=out_file)
  print(classification_report(y_validate, lrl2_preds), file=out_file)

  print("--------------------------kNN--------------------------", file=out_file)
  print(confusion_matrix(y_validate, kNN_preds), file=out_file)
  print(classification_report(y_validate, kNN_preds), file=out_file)

  print("---------------------Kernelized SVM---------------------", file=out_file)
  print(confusion_matrix(y_validate, svm_preds), file=out_file)
  print(classification_report(y_validate, svm_preds), file=out_file)