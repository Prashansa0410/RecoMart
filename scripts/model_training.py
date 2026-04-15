"""
RecoMart Model Training & Evaluation Pipeline
Person: Flavia
Input: /data/features/feature_data.csv
Output: /models/ + evaluation metrics

MODEL APPROACH:
- Collaborative Filtering (simple but effective)
- Build user-product interaction matrix
- Calculate similarity & recommendations

EVALUATION METRICS:
- Precision@K
- Recall@K
"""

import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from sklearn.model_selection import train_test_split
import pickle
import os
import traceback

# -------------------------------
# LOAD & PREPARE DATA
# -------------------------------

def load_data(path):
    df = pd.read_csv(path)

    # Convert event_type → rating
    rating_map = {
        "view": 1,
        "cart": 3,
        "purchase": 5
    }

    df["rating"] = df["event_type"].map(rating_map)
    df = df.dropna(subset=["rating"])

    df = df[["user_id", "product_id", "rating"]]

    # Aggregate duplicates
    df = df.groupby(["user_id", "product_id"], as_index=False).mean()

    return df


# -------------------------------
# TRAIN MODEL
# -------------------------------

def train_svd(df, k=50):

    user_item_matrix = df.pivot_table(
        index='user_id',
        columns='product_id',
        values='rating',
        fill_value=0
    )

    matrix = user_item_matrix.values
    user_mean = np.mean(matrix, axis=1)
    normalized = matrix - user_mean.reshape(-1, 1)

    # Ensure k is less than min(matrix.shape)
    k = min(k, min(normalized.shape) - 1)

    U, sigma, Vt = svds(normalized, k=k)
    sigma = np.diag(sigma)

    preds = np.dot(np.dot(U, sigma), Vt) + user_mean.reshape(-1, 1)

    preds_df = pd.DataFrame(preds,
                            index=user_item_matrix.index,
                            columns=user_item_matrix.columns)

    return preds_df


# -------------------------------
# PRECISION@K & RECALL@K
# -------------------------------

def precision_recall_at_k(preds_df, test_df, k=10):
    precision_list = []
    recall_list = []

    for user in test_df["user_id"].unique():

        if user not in preds_df.index:
            continue

        actual_items = test_df[test_df["user_id"] == user]["product_id"].tolist()

        predicted_items = (
            preds_df.loc[user]
            .sort_values(ascending=False)
            .head(k)
            .index.tolist()
        )

        hits = len(set(predicted_items) & set(actual_items))

        precision = hits / k
        recall = hits / len(actual_items) if actual_items else 0

        precision_list.append(precision)
        recall_list.append(recall)

    return np.mean(precision_list), np.mean(recall_list)


# -------------------------------
# SAVE MODEL
# -------------------------------

def save_model(preds_df):
    os.makedirs("models", exist_ok=True)

    with open("models/svd_model.pkl", "wb") as f:
        pickle.dump(preds_df, f)


# -------------------------------
# SAVE RESULTS
# -------------------------------

def save_results(precision, recall):
    os.makedirs("reports", exist_ok=True)

    with open("reports/model_results.txt", "w") as f:
        f.write(f"Precision@K: {precision}\n")
        f.write(f"Recall@K: {recall}\n")


# -------------------------------
# MAIN PIPELINE
# -------------------------------

# if __name__ == "__main__":

#     print("Running Recommendation Pipeline...")

#     df = load_data("data/processed/cleaned_data.csv")

#     train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

#     preds_df = train_svd(train_df)

#     precision, recall = precision_recall_at_k(preds_df, test_df, k=10)

#     print(f"Precision@10: {precision}")
#     print(f"Recall@10: {recall}")

#     save_model(preds_df)
#     save_results(precision, recall)

#     print("✅ Pipeline completed successfully!")

def run_model_training():
    try:
        print("Running Recommendation Pipeline...")

        df = load_data("data/processed/cleaned_data.csv")

        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

        preds_df = train_svd(train_df)

        precision, recall = precision_recall_at_k(preds_df, test_df, k=10)

        print(f"Precision@10: {precision}")
        print(f"Recall@10: {recall}")

        save_model(preds_df)
        save_results(precision, recall)

        print("✅ Pipeline completed successfully!")

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        line_number = tb[-1].lineno
        print(f"❌ Error at line {line_number}: {str(e)}")
        traceback.print_exc()