import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load the dataset
df = pd.read_csv("data/student-mat.csv", sep=";")

# Create results folder if it does not exist
Path("results").mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")

# Chart 1: Distribution of final grades
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="G3", bins=10, kde=True)
plt.title("Distribution of Final Grades")
plt.xlabel("Final Grade (G3)")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig("results/01_grade_distribution.png")
plt.show()

# Chart 2: Study time and final grades
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="studytime", y="G3")
plt.title("Study Time and Final Grade")
plt.xlabel("Study Time Category")
plt.ylabel("Final Grade (G3)")
plt.tight_layout()
plt.savefig("results/02_studytime_grades.png")
plt.show()

# Chart 3: Absences and final grades
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="absences", y="G3", alpha=0.7)
plt.title("Absences and Final Grade")
plt.xlabel("Number of Absences")
plt.ylabel("Final Grade (G3)")
plt.tight_layout()
plt.savefig("results/03_absences_grades.png")
plt.show()

# Chart 4: Previous grades and final grade
plt.figure(figsize=(7, 5))
sns.heatmap(
    df[["G1", "G2", "G3"]].corr(),
    annot=True,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    fmt=".2f"
)
plt.title("Correlation Between Student Grades")
plt.tight_layout()
plt.savefig("results/04_grade_correlation.png")
plt.show()

print("EDA charts saved in the results folder.")


# Chart 5: Mother's education and final grade
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Medu", y="G3")
plt.title("Mother's Education and Final Grade")
plt.xlabel("Mother's Education Level")
plt.ylabel("Final Grade (G3)")
plt.tight_layout()
plt.savefig("results/05_mother_education.png")
plt.show()

# Chart 6: Father's education and final grade
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Fedu", y="G3")
plt.title("Father's Education and Final Grade")
plt.xlabel("Father's Education Level")
plt.ylabel("Final Grade (G3)")
plt.tight_layout()
plt.savefig("results/06_father_education.png")
plt.show()

