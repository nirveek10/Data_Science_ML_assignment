import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression

# Create the models folder
Path("models").mkdir(exist_ok=True)

# Load dataset
df = pd.read_csv("data/student-mat.csv", sep=";")

def build_preprocessor(X):
    categorical_cols = X.select_dtypes(
        include=["object"]
    ).columns.tolist()

    numerical_cols = X.select_dtypes(
        exclude=["object"]
    ).columns.tolist()

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    return ColumnTransformer([
        ("num", numeric_pipeline, numerical_cols),
        ("cat", categorical_pipeline, categorical_cols)
    ])

# -------------------------
# 1. Regression model
# -------------------------
X_reg = df.drop(columns=["G1", "G2", "G3"])
y_reg = df["G3"]

X_train_reg, X_test_reg, y_train_reg, y_test_reg = (
    train_test_split(
        X_reg, y_reg,
        test_size=0.2,
        random_state=42
    )
)

regression_pipeline = Pipeline([
    ("preprocessor", build_preprocessor(X_train_reg)),
    ("model", RandomForestRegressor(
        n_estimators=200,
        min_samples_leaf=2,
        random_state=42
    ))
])

regression_pipeline.fit(X_train_reg, y_train_reg)

joblib.dump(
    regression_pipeline,
    "models/regression_model.joblib"
)

# -------------------------
# 2. Classification model
# -------------------------
X_clf = df.drop(columns=["G1", "G2", "G3"])
y_clf = (df["G3"] < 10).astype(int)

X_train_clf, X_test_clf, y_train_clf, y_test_clf = (
    train_test_split(
        X_clf, y_clf,
        test_size=0.2,
        random_state=42,
        stratify=y_clf
    )
)

classification_pipeline = Pipeline([
    ("preprocessor", build_preprocessor(X_train_clf)),
    ("model", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

classification_pipeline.fit(X_train_clf, y_train_clf)

joblib.dump(
    classification_pipeline,
    "models/classification_model.joblib"
)

# Save feature names and deployment details
metadata = {
    "features": X_reg.columns.tolist(),
    "pass_mark": 10,
    "regression_model": "Random Forest Regressor",
    "classification_model": "Logistic Regression",
    "classification_target": "1 = at risk (G3 < 10), 0 = pass"
}

joblib.dump(metadata, "models/model_metadata.joblib")

print("Models saved successfully!")
print(" - models/regression_model.joblib")
print(" - models/classification_model.joblib")
print(" - models/model_metadata.joblib")
