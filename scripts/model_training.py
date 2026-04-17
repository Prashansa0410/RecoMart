"""
RecoMart - Hybrid Recommendation Model (SVD + Popularity)

Includes:
- Data preparation
- Hybrid model (SVD + popularity)
- Precision@K, Recall@K, F1@K
- Model + metrics saving
"""

import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
import pickle
import os
import traceback


# -------------------------------
# LOAD DATA
# -------------------------------

def load_data(path):
    df = pd.read_csv(path)

    rating_map = {
        "view": 0.5,
        "cart": 5,
        "purchase": 15
    }

    df["rating"] = df["event_type"].map(rating_map)
    df = df.dropna(subset=["rating"])

    df = df[["user_id", "product_id", "rating"]]

    df = df.groupby(["user_id", "product_id"], as_index=False).mean()

    # Filter users
    user_counts = df["user_id"].value_counts()
    df = df[df["user_id"].isin(user_counts[user_counts >= 3].index)]

    # Filter products
    product_counts = df["product_id"].value_counts()
    df = df[df["product_id"].isin(product_counts[product_counts >= 5].index)]

    return df


# -------------------------------
# TRAIN-TEST SPLIT
# -------------------------------

def train_test_split_user(df, test_ratio=0.2):
    train_list, test_list = [], []

    for user, group in df.groupby("user_id"):
        group = group.sample(frac=1, random_state=42)
        split = int(len(group) * (1 - test_ratio))

        train_list.append(group.iloc[:split])
        test_list.append(group.iloc[split:])

    return pd.concat(train_list), pd.concat(test_list)


# -------------------------------
# POPULARITY
# -------------------------------

def compute_popularity(df):
    popularity = df.groupby("product_id")["rating"].sum()
    popularity = (popularity - popularity.min()) / (popularity.max() - popularity.min())
    return popularity


# -------------------------------
# HYBRID MODEL
# -------------------------------

def train_hybrid(df, k=30, alpha=0.5):

    user_item_matrix = df.pivot_table(
        index='user_id',
        columns='product_id',
        values='rating',
        fill_value=0
    )

    matrix = user_item_matrix.values

    user_mean = np.mean(matrix, axis=1)
    normalized = matrix - user_mean.reshape(-1, 1)

    k = min(k, min(normalized.shape) - 1)

    U, sigma, Vt = svds(normalized, k=k)
    sigma = np.diag(sigma)

    svd_preds = np.dot(np.dot(U, sigma), Vt) + user_mean.reshape(-1, 1)

    svd_df = pd.DataFrame(
        svd_preds,
        index=user_item_matrix.index,
        columns=user_item_matrix.columns
    )

    # Normalize SVD
    svd_df = (svd_df - svd_df.min().min()) / (svd_df.max().max() - svd_df.min().min())

    # Popularity
    popularity = compute_popularity(df)

    pop_df = pd.DataFrame(
        np.tile(popularity.values, (len(svd_df.index), 1)),
        index=svd_df.index,
        columns=svd_df.columns
    )

    # Hybrid score
    hybrid_df = alpha * svd_df + (1 - alpha) * pop_df
    # Re-ranking using popularity (VERY IMPORTANT)
    pop_boost = np.log1p(pop_df)  # log(1 + popularity)
    final_df = hybrid_df * pop_boost
    

    return final_df


# -------------------------------
# METRICS (Precision, Recall, F1)
# -------------------------------

def evaluate_model(preds_df, test_df, train_df, k=10):

    precision_list, recall_list, f1_list = [], [], []

    for user in test_df["user_id"].unique():

        if user not in preds_df.index:
            continue

        actual_items = test_df[test_df["user_id"] == user]["product_id"].tolist()

        user_seen = train_df[train_df["user_id"] == user]["product_id"].tolist()

        predicted_items = [
            item for item in preds_df.loc[user]
            .sort_values(ascending=False)
            .index.tolist()
            if item not in user_seen
        ][:k]

        hits = len(set(predicted_items) & set(actual_items))

        precision = hits / k
        recall = hits / len(actual_items) if actual_items else 0

        if precision + recall == 0:
            f1 = 0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)

        precision_list.append(precision)
        recall_list.append(recall)
        f1_list.append(f1)

    return (
        np.mean(precision_list),
        np.mean(recall_list),
        np.mean(f1_list)
    )


# -------------------------------
# SAVE
# -------------------------------

def save_model(preds_df):
    os.makedirs("models", exist_ok=True)
    with open("models/hybrid_model.pkl", "wb") as f:
        pickle.dump(preds_df, f)


def save_results(precision, recall, f1):
    os.makedirs("reports", exist_ok=True)
    with open("reports/model_results.txt", "w") as f:
        f.write(f"Precision@10: {round(precision, 4)}\n")
        f.write(f"Recall@10: {round(recall, 4)}\n")
        f.write(f"F1@10: {round(f1, 4)}\n")


# -------------------------------
# MAIN
# -------------------------------

def run_model_training():
    try:
        print("Running Hybrid Recommendation Pipeline...")

        df = load_data("data/processed/cleaned_data.csv")

        train_df, test_df = train_test_split_user(df)

        preds_df = train_hybrid(train_df, k=30, alpha=0.7)

        precision, recall, f1 = evaluate_model(preds_df, test_df, train_df)

        print(f"Precision@10: {precision:.4f}")
        print(f"Recall@10: {recall:.4f}")
        print(f"F1@10: {f1:.4f}")

        save_model(preds_df)
        save_results(precision, recall, f1)

        print("Model training completed successfully!")

    except Exception as e:
        traceback.print_exc()
        raise e