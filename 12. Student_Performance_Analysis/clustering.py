import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# Load the dataset
df = pd.read_csv("data/student-mat.csv", sep=";")

Path("results").mkdir(exist_ok=True)

# Select numerical features for clustering.
# G1, G2 and G3 are retained here to help
# explore overall student performance patterns.
features = [
    "age",
    "studytime",
    "failures",
    "absences",
    "G1",
    "G2",
    "G3"
]

X = df[features].copy()

# Standardize the features so their scales
# do not dominate the clustering.
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Compare several possible numbers of clusters.
print("Silhouette scores:")

for k in [2, 3, 4, 5]:
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )
    labels = model.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    print(f"k={k}: {score:.3f}")

# Use three clusters for the learner-profile analysis.
kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(X_scaled)

# Summarize the characteristics of each cluster.
summary = df.groupby("Cluster")[features].mean().round(2)

print("\nCluster sizes:")
print(df["Cluster"].value_counts().sort_index())

print("\nCluster profiles (mean values):")
print(summary)

summary.to_csv("results/cluster_profiles.csv")

# Visualize clusters in two dimensions using PCA.
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(9, 6))
scatter = plt.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=df["Cluster"],
    cmap="viridis",
    alpha=0.75
)

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("Student Groups Using K-Means Clustering")
plt.colorbar(scatter, label="Cluster")
plt.tight_layout()
plt.savefig("results/student_clusters.png", dpi=150)
plt.show()

print("\nSaved cluster profiles and visualization.")
