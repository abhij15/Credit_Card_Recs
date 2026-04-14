from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


MODEL_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "models" / "spending_model.pkl"
)


@dataclass
class SpendingPredictorArtifacts:
    model: RandomForestRegressor
    feature_columns: List[str]


class SpendingPredictorModel:
    """
    Train and serve a per-category spending prediction model.

    Expected input transactions_df columns:
      - user_id
      - date (datetime or ISO string)
      - amount (numeric)
      - category (string)
    """

    def __init__(self, model_path: Path | None = None) -> None:
        self.model_path = model_path or MODEL_PATH

    # ------------------------------------------------------------------
    # Feature engineering
    # ------------------------------------------------------------------
    def prepare_features(self, transactions_df: pd.DataFrame, user_id: int) -> pd.DataFrame:
        """
        Build a feature matrix for a single user, one row per category.

        Features:
          - avg_last_30_days
          - avg_last_90_days
          - trend (90d avg - 30d avg)
          - transaction_count_30d
          - day_of_week_pattern (0-6 encoded based on reference date)
          - month_seasonal (1-12 encoded based on reference date)
        """
        if transactions_df.empty:
            raise ValueError("transactions_df is empty.")

        df = transactions_df.copy()

        if "user_id" not in df.columns:
            raise ValueError("transactions_df must contain 'user_id' column.")
        if "date" not in df.columns:
            raise ValueError("transactions_df must contain 'date' column.")
        if "amount" not in df.columns:
            raise ValueError("transactions_df must contain 'amount' column.")
        if "category" not in df.columns:
            raise ValueError("transactions_df must contain 'category' column.")

        df = df[df["user_id"] == user_id]
        if df.empty:
            raise ValueError(f"No transactions found for user_id={user_id}.")

        # Ensure datetime
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        reference_date = df["date"].max()
        last_30 = reference_date - pd.Timedelta(days=30)
        last_90 = reference_date - pd.Timedelta(days=90)

        features: List[Dict[str, Any]] = []

        for category, cat_df in df.groupby("category"):
            # Filter windows
            df_30 = cat_df[cat_df["date"] >= last_30]
            df_90 = cat_df[cat_df["date"] >= last_90]

            # Avoid division by zero; use 0 if no txns in window
            avg_30 = df_30["amount"].mean() if not df_30.empty else 0.0
            avg_90 = df_90["amount"].mean() if not df_90.empty else 0.0
            trend = avg_90 - avg_30
            txn_count_30 = float(len(df_30))

            features.append(
                {
                    "user_id": user_id,
                    "category": category,
                    "avg_last_30_days": float(avg_30),
                    "avg_last_90_days": float(avg_90),
                    "trend": float(trend),
                    "transaction_count_30d": txn_count_30,
                    "day_of_week_pattern": float(reference_date.weekday()),
                    "month_seasonal": float(reference_date.month),
                }
            )

        feature_df = pd.DataFrame(features)
        return feature_df

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------
    def train(self, transactions_df: pd.DataFrame) -> Dict[str, float]:
        """
        Train a RandomForestRegressor to predict next 30 days spend by category.

        Strategy:
          - Use last 12 months of data.
          - Use a global cutoff date = max_date - 30 days.
          - For each user & category:
              * Features from data <= cutoff (via prepare-like logic).
              * Target = total amount in (cutoff, cutoff+30] window.
          - Flatten across all users/categories into a single regression problem.

        Saves artifacts (model + feature_columns) to MODEL_PATH.

        Returns metrics dict with RMSE, MAE, R2 on test split.
        """
        if transactions_df.empty:
            raise ValueError("transactions_df is empty; cannot train model.")

        df = transactions_df.copy()
        for col in ["user_id", "date", "amount", "category"]:
            if col not in df.columns:
                raise ValueError(f"transactions_df must contain '{col}' column.")

        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        max_date = df["date"].max()
        cutoff = max_date - pd.Timedelta(days=30)

        # Only consider data from the last year to reduce noise
        one_year_ago = max_date - pd.Timedelta(days=365)
        df = df[df["date"] >= one_year_ago]

        # Build feature/target pairs
        rows: List[Dict[str, Any]] = []

        for user_id, user_df in df.groupby("user_id"):
            # Past data up to cutoff for features
            past_df = user_df[user_df["date"] <= cutoff]
            # Future 30d window for target
            future_df = user_df[
                (user_df["date"] > cutoff)
                & (user_df["date"] <= cutoff + pd.Timedelta(days=30))
            ]

            if past_df.empty or future_df.empty:
                # Not enough data for this user
                continue

            # Build features similar to prepare_features but using cutoff as reference
            for category, cat_past in past_df.groupby("category"):
                cat_future = future_df[future_df["category"] == category]

                last_30 = cutoff - pd.Timedelta(days=30)
                last_90 = cutoff - pd.Timedelta(days=90)

                df_30 = cat_past[cat_past["date"] >= last_30]
                df_90 = cat_past[cat_past["date"] >= last_90]

                avg_30 = df_30["amount"].mean() if not df_30.empty else 0.0
                avg_90 = df_90["amount"].mean() if not df_90.empty else 0.0
                trend = avg_90 - avg_30
                txn_count_30 = float(len(df_30))

                target_next_30 = float(cat_future["amount"].sum())

                rows.append(
                    {
                        "user_id": user_id,
                        "category": category,
                        "avg_last_30_days": float(avg_30),
                        "avg_last_90_days": float(avg_90),
                        "trend": float(trend),
                        "transaction_count_30d": txn_count_30,
                        "day_of_week_pattern": float(cutoff.weekday()),
                        "month_seasonal": float(cutoff.month),
                        "target_next_30": target_next_30,
                    }
                )

        if not rows:
            raise ValueError("Insufficient data to build any training samples.")

        data = pd.DataFrame(rows)

        # One-hot encode category for the model
        data = pd.get_dummies(data, columns=["category"], prefix="cat")

        feature_columns = [
            c
            for c in data.columns
            if c not in ("target_next_30", "user_id")
        ]

        X = data[feature_columns].values
        y = data["target_next_30"].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        if len(np.unique(y_train)) <= 1:
            raise ValueError(
                "Training target has insufficient variability; cannot train model."
            )

        model = RandomForestRegressor(
            n_estimators=200,
            random_state=42,
            n_jobs=-1,
        )
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mae = float(mean_absolute_error(y_test, y_pred))
        r2 = float(r2_score(y_test, y_pred))

        metrics = {"rmse": rmse, "mae": mae, "r2": r2}

        # Persist model + feature columns
        artifacts = SpendingPredictorArtifacts(
            model=model,
            feature_columns=feature_columns,
        )
        self._save_artifacts(artifacts)

        return metrics

    # ------------------------------------------------------------------
    # Prediction
    # ------------------------------------------------------------------
    def predict(self, transactions_df: pd.DataFrame, user_id: int) -> Dict[str, float]:
        """
        Predict next 30 days spending by category for a given user.

        Returns a mapping like:
            {"dining": 450.0, "groceries": 320.0, ...}
        """
        artifacts = self._load_artifacts()

        feature_df = self.prepare_features(transactions_df, user_id)
        if feature_df.empty:
            raise ValueError(f"No feature rows generated for user_id={user_id}.")

        # One-hot encode categories with same schema used in training
        feature_df = pd.get_dummies(feature_df, columns=["category"], prefix="cat")

        # Align columns to training feature set
        for col in artifacts.feature_columns:
            if col not in feature_df.columns:
                feature_df[col] = 0.0
        # Drop any extra columns not in training
        feature_df = feature_df[artifacts.feature_columns]

        X = feature_df.values
        preds = artifacts.model.predict(X)

        # Map predictions back to categories
        # Recover category names from the original (pre-dummies) features:
        # we can re-derive from the dummy columns that were present.
        # Instead, for simplicity, re-build category from any 'cat_*' column == 1.
        # But here, because we created dummy columns from 'feature_df', we
        # lost original 'category' label. So we instead recompute categories
        # directly from columns: this mapping is stable for our use case.
        category_cols = [c for c in artifacts.feature_columns if c.startswith("cat_")]
        if not category_cols:
            raise RuntimeError("No category dummy columns found in feature_columns.")

        categories: List[str] = []
        for _, row in feature_df.iterrows():
            # If row has multiple '1's due to alignment, pick the max value
            values = row[category_cols].values
            idx = int(np.argmax(values))
            cat_col = category_cols[idx]
            categories.append(cat_col.replace("cat_", "", 1))

        results: Dict[str, float] = {}
        for cat, pred in zip(categories, preds):
            results[cat] = float(pred)

        return results

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------
    def _save_artifacts(self, artifacts: SpendingPredictorArtifacts) -> None:
        model_path = self.model_path
        model_path.parent.mkdir(parents=True, exist_ok=True)
        with model_path.open("wb") as f:
            pickle.dump(artifacts, f)

    def _load_artifacts(self) -> SpendingPredictorArtifacts:
        model_path = self.model_path
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {model_path}. Have you trained the model?"
            )
        with model_path.open("rb") as f:
            artifacts = pickle.load(f)
        if not isinstance(artifacts, SpendingPredictorArtifacts):
            # Backward-compatible: allow dict-shaped artifacts
            if isinstance(artifacts, dict) and "model" in artifacts and "feature_columns" in artifacts:
                return SpendingPredictorArtifacts(
                    model=artifacts["model"],
                    feature_columns=list(artifacts["feature_columns"]),
                )
            raise RuntimeError("Unexpected artifact format in model file.")
        return artifacts


if __name__ == "__main__":
    # Example CLI usage for manual testing:
    data_path = (
        Path(__file__).resolve().parents[2] / "data" / "raw" / "transactions.csv"
    )
    if not data_path.exists():
        raise SystemExit(f"Transactions file not found at {data_path}")

    df_tx = pd.read_csv(data_path)
    model = SpendingPredictorModel()
    metrics = model.train(df_tx)
    print("Training metrics:", metrics)

    # Predict for a sample user
    sample_user = int(df_tx["user_id"].iloc[0])
    preds = model.predict(df_tx, sample_user)
    print(f"Next 30-day prediction for user {sample_user}:", preds)

