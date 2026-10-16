import pandas as pd

# Load the student mathematics dataset
df = pd.read_csv("data/student-mat.csv", sep=";")

# Display the first five rows
print(df.head())

# Check the number of rows and columns
print("\nDataset shape:")
print(df.shape)

# Display column names and data types
print("\nDataset information:")
df.info()

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Display summary statistics
print("\nSummary statistics:")
print(df.describe())

# 1. Check missing values
print("\nMissing values:")
print(df.isnull().sum().sum())

# 2. Check duplicate rows
print("\nDuplicate rows:")
print(df.duplicated().sum())

# 3. Check data types
print("\nData types:")
print(df.dtypes.value_counts())

# 4. Check final grade statistics
print("\nFinal grade statistics:")
print(df["G3"].describe())

# 5. Check final grade frequencies
print("\nFinal grade counts:")
print(df["G3"].value_counts().sort_index())

