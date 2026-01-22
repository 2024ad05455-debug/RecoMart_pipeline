import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD
import mlflow
import mlflow.sklearn

# ---------------- CONFIG ----------------
DB_URI = "postgresql://postgres:Dmml123@localhost:5432/RecoMart_DB"
K = 5
N_COMPONENTS = 20

# ---------------- LOAD DATA ----------------
engine = create_engine(DB_URI)

query = """
SELECT user_id, product_id, interaction_count
FROM user_item_features
"""

df = pd.read_sql(query, engine)

# Encode IDs
user_map = {u: i for i, u in enumerate(df.user_id.unique())}
item_map = {i: j for j, i in enumerate(df.product_id.unique())}

df["user_idx"] = df.user_id.map(user_map)
df["item_idx"] = df.product_id.map(item_map)

# Build interaction matrix
matrix = np.zeros((len(user_map), len(item_map)))
for _, row in df.iterrows():
    matrix[row.user_idx, row.item_idx] = row.interaction_count

# Train-test split (by users)
train_matrix = matrix.copy()
test_matrix = np.zeros(matrix.shape)

for u in range(matrix.shape[0]):
    items = np.where(matrix[u] > 0)[0]
    if len(items) > 1:
        test_item = np.random.choice(items)
        train_matrix[u, test_item] = 0
        test_matrix[u, test_item] = 1

# ---------------- MODEL TRAINING ----------------
svd = TruncatedSVD(n_components=N_COMPONENTS, random_state=42)
user_factors = svd.fit_transform(train_matrix)
item_factors = svd.components_.T

# ---------------- EVALUATION ----------------
def precision_at_k(user_factors, item_factors, test_matrix, k=5):
    precisions = []
    for u in range(test_matrix.shape[0]):
        scores = user_factors[u] @ item_factors.T
        top_k = np.argsort(scores)[-k:]
        relevant = np.where(test_matrix[u] > 0)[0]
        if len(relevant) == 0:
            continue
        precision = len(set(top_k) & set(relevant)) / k
        precisions.append(precision)
    return np.mean(precisions)

precision_k = precision_at_k(user_factors, item_factors, test_matrix, K)

# ---------------- MLFLOW TRACKING ----------------
mlflow.set_experiment("RecoMart_CF_Recommender")

with mlflow.start_run():
    mlflow.log_param("model", "MatrixFactorization_SVD")
    mlflow.log_param("n_components", N_COMPONENTS)
    mlflow.log_metric("precision_at_k", precision_k)
    mlflow.sklearn.log_model(svd, "cf_model")

print(f"Precision@{K}: {precision_k:.4f}")
