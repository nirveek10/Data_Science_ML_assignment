# Student Performance Analysis

A beginner-friendly Data Science and Machine Learning project using the UCI Student Performance dataset. The project explores student data, predicts final grades, identifies potentially at-risk students, groups students with similar performance patterns, and provides a Streamlit dashboard.

## Project Features

- **EDA:** Checks the dataset and explores relationships between student characteristics and final grades.
- **Regression:** Compares models to predict the final grade (`G3`).
- **Classification:** Predicts whether a student may be at risk of failing.
- **Clustering:** Uses K-Means to explore student performance groups.
- **Explainability:** Uses Random Forest feature importance to show which features the regression model relies on.
- **Dashboard:** A Streamlit app lets users enter student details and view predictions.

## Dataset

This project uses the Mathematics dataset from the UCI Student Performance dataset.

Download `student-mat.csv` from the [UCI Machine Learning Repository — Student Performance](https://archive.ics.uci.edu/dataset/320/student+performance).

Place the file here:

```text
data/student-mat.csv
```

The dataset is read using a semicolon separator (`sep=";"`).

## Project Structure

```text
12. Student_Performance_Analysis/
├── app.py
├── analysis.py
├── eda.py
├── train_models.py
├── train_classification.py
├── clustering.py
├── explainability.py
├── save_models.py
├── requirements.txt
├── data/
│   └── student-mat.csv
├── models/
│   ├── regression_model.joblib
│   ├── classification_model.joblib
│   └── model_metadata.joblib
└── results/
    ├── regression_comparison.csv
    ├── classification_comparison.csv
    ├── cluster_profiles.csv
    ├── feature_importance.csv
    └── generated charts
```

The files listed under `results/` and `models/` are created by the scripts. Exact output files may vary depending on which scripts have been run.

## Setup

The commands below are for Windows PowerShell, run from the project folder.

### 1. Create and activate a virtual environment

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```bat
env\Scripts\activate.bat
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

If you do not have a `requirements.txt` file yet, create one with:

```text
pandas
numpy
matplotlib
scikit-learn
joblib
streamlit
```

## Run the Project

Run each script from the project root folder so the relative paths to `data/`, `results/`, and `models/` work.

```powershell
python analysis.py
python eda.py
python train_models.py
python train_classification.py
python clustering.py
python explainability.py
python save_models.py
```

The analysis and modeling scripts print results in the terminal and save relevant charts or CSV files in `results/`. The model-saving script saves the trained pipelines in `models/`.

### Launch the Streamlit dashboard

After the dataset and saved model files are in place, run:

```powershell
streamlit run app.py
```

Streamlit will show a local URL in the terminal, usually `http://localhost:8501`.

## Current Results

These are the results from one train/test split and the experiments run for this project. They may vary if the data or settings change.

### Regression

The Random Forest Regressor had the lowest test MAE among the compared models:

- MAE: **3.036**
- RMSE: **3.813**
- R²: **0.291**

The model's predictions have an average absolute error of about 3 grade points on the 0–20 scale in this test split. The R² score indicates that there is still substantial variation the model does not explain.

### Classification

The target was defined as **at risk if `G3 < 10`**, and **pass if `G3 >= 10`**. Grades `G1` and `G2` were excluded to simulate early prediction.

Logistic Regression was selected based on at-risk F1-score:

- Accuracy: **0.696**
- At-risk precision: **0.529**
- At-risk recall: **0.692**
- At-risk F1-score: **0.600**
- ROC-AUC: **0.727**

Recall is useful here because the goal is to identify students who may need support. However, the model misses some at-risk students and also flags some students who pass.

### Clustering

K-Means was used to explore three student groups. Their mean final grades were:

- Cluster 0: **8.77**
- Cluster 1: **14.33**
- Cluster 2: **4.09**

The silhouette score for three clusters was **0.218**. Two clusters scored **0.250**, so the three-cluster solution was retained for more detailed interpretation, not because it had the highest silhouette score.

### Feature Importance

In the Random Forest regression model, the highest feature importance scores were:

1. Absences: **0.2044**
2. Past failures: **0.1575**
3. Health: **0.0525**
4. Going out: **0.0445**
5. Age: **0.0368**

Feature importance describes how much the model relies on features; it does not prove that those features cause a particular grade.

## Limitations

- The dataset is relatively small, so results may not generalize to other schools or student populations.
- The at-risk threshold (`G3 < 10`) is a project definition and may not match every school's grading policy.
- Model results are preliminary and should be evaluated further before real-world use.
- Predictions should support teacher review, not replace teacher judgment or be used as the sole basis for decisions about students.
- The three-cluster solution is useful for interpretation, but the silhouette score indicates that the groups are not strongly separated.

## Learning Summary

This project provided practice in data cleaning, exploratory data analysis, regression, classification, clustering, feature importance, and model deployment with Streamlit. It also showed why several evaluation metrics are needed and why machine learning predictions must be interpreted carefully.

## License and Attribution

The dataset is provided by the UCI Machine Learning Repository. Refer to the [dataset page](https://archive.ics.uci.edu/dataset/320/student+performance) for its source and terms of use.
