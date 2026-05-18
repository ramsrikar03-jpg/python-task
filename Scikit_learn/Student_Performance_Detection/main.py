# =====================================================================
# 🎓 STUDENT PERFORMANCE DETECTION USING MACHINE LEARNING
# =====================================================================

# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ML Libraries
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score


# =====================================================================
# 📂 LOAD DATASET
# =====================================================================

# Load dataset
dataset = pd.read_csv("student-mat.csv")

print(dataset.head())


# =====================================================================
# 📊 DATA PREPROCESSING
# =====================================================================

# Convert categorical columns into numerical values

label_encoder = LabelEncoder()

for column in dataset.columns:
    
    if dataset[column].dtype == 'object':
        dataset[column] = label_encoder.fit_transform(dataset[column])


# =====================================================================
# 🎯 CREATE TARGET VARIABLE
# =====================================================================

# If final grade >= 10 → Pass
# Else → Fail

dataset['performance'] = dataset['G3'].apply(lambda x: 1 if x >= 10 else 0)

# Features
X = dataset.drop(['G3', 'performance'], axis=1)

# Target
y = dataset['performance']


# =====================================================================
# ✂️ SPLIT DATASET
# =====================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# =====================================================================
# 🤖 LOGISTIC REGRESSION
# =====================================================================

log_model = LogisticRegression(max_iter=1000)

log_model.fit(X_train, y_train)

log_pred = log_model.predict(X_test)

log_accuracy = accuracy_score(y_test, log_pred)

print("Logistic Regression Accuracy :", log_accuracy)


# =====================================================================
# 🌳 DECISION TREE
# =====================================================================

tree_model = DecisionTreeClassifier()

tree_model.fit(X_train, y_train)

tree_pred = tree_model.predict(X_test)

tree_accuracy = accuracy_score(y_test, tree_pred)

print("Decision Tree Accuracy :", tree_accuracy)


# =====================================================================
# 🌲 RANDOM FOREST
# =====================================================================

forest_model = RandomForestClassifier()

forest_model.fit(X_train, y_train)

forest_pred = forest_model.predict(X_test)

forest_accuracy = accuracy_score(y_test, forest_pred)

print("Random Forest Accuracy :", forest_accuracy)


# =====================================================================
# 📈 ACCURACY COMPARISON GRAPH
# =====================================================================

models = ['Logistic Regression', 'Decision Tree', 'Random Forest']

accuracies = [
    log_accuracy * 100,
    tree_accuracy * 100,
    forest_accuracy * 100
]

# Create Bar Chart
plt.figure(figsize=(8,5))

plt.bar(models, accuracies)

plt.title("ML Algorithm Accuracy Comparison")

plt.xlabel("Algorithms")

plt.ylabel("Accuracy Percentage")

plt.show()


# =====================================================================
# 🔍 SAMPLE PREDICTION
# =====================================================================

sample_prediction = forest_model.predict([X.iloc[0]])

if sample_prediction[0] == 1:
    print("Student Performance : PASS")
else:
    print("Student Performance : FAIL")