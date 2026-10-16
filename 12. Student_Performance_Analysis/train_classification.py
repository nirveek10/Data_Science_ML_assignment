import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report
)

# Load the dataset
df = pd.read_csv("data/student-mat.csv", sep=";")

Path("results").mkdir(exist_ok=True)
Path("models").mkdir(exist_ok=True)

# 1 = at risk, 0 = pass
y = (df["G3"] < 10).astype(int)

# Early prediction: do not use G1, G2 or G3 as input
X = df.drop(columns=["G1", "G2", "G3"])

print("Class distribution:")
print(y.map({0: "Pass", 1: "At risk"}).value_counts())

# Identify column types
categorical_cols = X.select_dtypes(
    include=["object"]
).columns.tolist()

numerical_cols = X.select_dtypes(
    exclude=["object"]
).columns.tolist()

# Preprocessing
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numerical_cols),
    ("cat", categorical_pipeline, categorical_cols)
])

# Split data while preserving the pass/at-risk proportions
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Compare three classification models
models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ),
    "Decision Tree": DecisionTreeClassifier(
        max_depth=5,
        class_weight="balanced",
        random_state=42
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42
    )
}

results = []
trained_models = {}

for name, model in models.items():
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, predictions),
        "Precision_at_risk": precision_score(
            y_test, predictions, zero_division=0
        ),
        "Recall_at_risk": recall_score(
            y_test, predictions, zero_division=0
        ),
        "F1_at_risk": f1_score(
            y_test, predictions, zero_division=0
        ),
        "ROC_AUC": roc_auc_score(y_test, probabilities)
    })

    trained_models[name] = pipeline

# Compare results
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(
    "F1_at_risk", ascending=False
)

print("\nClassification model comparison:")
print(results_df.round(3).to_string(index=False))

results_df.to_csv(
    "results/classification_comparison.csv",
    index=False
)

# Inspect the leading model's predictions
best_name = results_df.iloc[0]["Model"]
best_model = trained_models[best_name]
predictions = best_model.predict(X_test)

print(f"\nLeading model by at-risk F1: {best_name}")
print("\nClassification report:")
print(
    classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Pass", "At risk"],
        zero_division=0
    )
)

# Plot the confusion matrix
cm = confusion_matrix(y_test, predictions, labels=[0, 1])

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Pass", "At risk"]
)

display.plot(cmap="Blues", values_format="d")
plt.title(f"Confusion Matrix: {best_name}")
plt.tight_layout()
plt.savefig("results/classification_confusion_matrix.png")
plt.show()
