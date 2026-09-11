"""
train.py
Trains a customer churn prediction model and saves it as model.pkl

Usage:
    python train.py
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

def generate_synthetic_churn_data(n_samples=2000):
    """
    Generates a synthetic but realistic customer churn dataset.
    Features: tenure_months, monthly_charges, total_charges,
              contract_type (0=month-to-month, 1=one-year, 2=two-year),
              support_calls, has_internet_service
    Target: churn (0=stayed, 1=churned)
    """
    tenure_months = np.random.randint(1, 72, n_samples)
    monthly_charges = np.round(np.random.uniform(20, 120, n_samples), 2)
    total_charges = np.round(tenure_months * monthly_charges * np.random.uniform(0.9, 1.1, n_samples), 2)
    contract_type = np.random.choice([0, 1, 2], n_samples, p=[0.55, 0.25, 0.20])
    support_calls = np.random.poisson(2, n_samples)
    has_internet_service = np.random.choice([0, 1], n_samples, p=[0.2, 0.8])

    # churn probability logic: short tenure, month-to-month, many support
    # calls, and high monthly charges increase churn risk
    churn_prob = (
        0.35 * (tenure_months < 12).astype(float)
        + 0.30 * (contract_type == 0).astype(float)
        + 0.20 * (support_calls > 3).astype(float)
        + 0.15 * (monthly_charges > 80).astype(float)
    )
    churn_prob = np.clip(churn_prob + np.random.normal(0, 0.1, n_samples), 0, 1)
    churn = (churn_prob > 0.5).astype(int)

    df = pd.DataFrame({
        "tenure_months": tenure_months,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "contract_type": contract_type,
        "support_calls": support_calls,
        "has_internet_service": has_internet_service,
        "churn": churn,
    })
    return df


def main():
    print("Generating synthetic churn dataset...")
    df = generate_synthetic_churn_data()
    print(f"Dataset shape: {df.shape}")
    print(f"Churn rate: {df['churn'].mean():.2%}")

    feature_cols = [
        "tenure_months", "monthly_charges", "total_charges",
        "contract_type", "support_calls", "has_internet_service",
    ]
    X = df[feature_cols]
    y = df["churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    print("Training RandomForestClassifier...")
    model = RandomForestClassifier(
        n_estimators=150, max_depth=8, random_state=RANDOM_STATE
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nTest Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    out_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    joblib.dump({"model": model, "feature_cols": feature_cols}, out_path)
    print(f"\nModel saved to {out_path}")


if __name__ == "__main__":
    main()
