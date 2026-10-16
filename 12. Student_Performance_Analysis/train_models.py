import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor

# Load data
df = pd.read_csv("data/student-mat.csv", sep=";")

# Create output folder
Path("results").mkdir(exist_ok=True)
Path("models").mkdir(exist_ok=True)

# Target: final grade
y = df["G3"]

# Early prediction: exclude G1 and G2 to avoid using past grades
X = df.drop(columns=["G3", "G1", "G2"])

# Identify categorical and numerical columns
categorical_cols = X.select_dtypes(
    include=["object"]
).columns.tolist()

numerical_cols = X.select_dtypes(
    exclude=["object"]
).columns.tolist()

# Prepare preprocessing separately for each column type
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

# Split before fitting preprocessing to avoid data leakage
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Models to compare
models = {
    "Baseline": DummyRegressor(strategy="mean"),
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        min_samples_leaf=2
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

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    results.append({
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    })

    trained_models[name] = pipeline

# Compare model results
results_df = pd.DataFrame(results).sort_values("MAE")
print("\nRegression model comparison:")
print(results_df.round(3).to_string(index=False))

results_df.to_csv("results/regression_comparison.csv", index=False)

# Select the best model by test MAE
best_name = results_df.iloc[0]["Model"]
best_model = trained_models[best_name]

print(f"\nBest model by test MAE: {best_name}")

# Plot actual vs predicted scores
predictions = best_model.predict(X_test)

plt.figure(figsize=(7, 5))
plt.scatter(y_test, predictions, alpha=0.7)
plt.plot([0, 20], [0, 20], linestyle="--")
plt.xlabel("Actual Final Grade")
plt.ylabel("Predicted Final Grade")
plt.title(f"Actual vs Predicted Grades: {best_name}")
plt.tight_layout()
plt.savefig("results/regression_predictions.png")
plt.show()
