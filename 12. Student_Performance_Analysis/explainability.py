import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# Load data
df = pd.read_csv("data/student-mat.csv", sep=";")

Path("results").mkdir(exist_ok=True)

# Predict final grade without using G1 or G2.
# This simulates prediction before earlier grades are available.
y = df["G3"]
X = df.drop(columns=["G1", "G2", "G3"])

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

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numerical_cols),
    ("cat", categorical_pipeline, categorical_cols)
])

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=200,
        min_samples_leaf=2,
        random_state=42
    ))
])

model.fit(X_train, y_train)

# Get names of transformed features
feature_names = (
    model.named_steps["preprocessor"]
    .get_feature_names_out()
)

# Get Random Forest feature importance
importances = (
    model.named_steps["regressor"]
    .feature_importances_
)

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
})

importance_df = importance_df.sort_values(
    "Importance",
    ascending=False
)

print("\nTop 15 important features:")
print(importance_df.head(15).round(4).to_string(index=False))

importance_df.to_csv(
    "results/feature_importance.csv",
    index=False
)

# Plot the top 15 features
top_features = importance_df.head(15).sort_values(
    "Importance"
)

plt.figure(figsize=(10, 7))
plt.barh(
    top_features["Feature"],
    top_features["Importance"]
)

plt.xlabel("Feature Importance")
plt.ylabel("Feature")
plt.title("Top 15 Features for Student Grade Prediction")
plt.tight_layout()

plt.savefig(
    "results/feature_importance.png",
    dpi=150
)

plt.show()

print("\nFeature importance results saved.")
