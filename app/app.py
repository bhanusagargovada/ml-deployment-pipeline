"""
app.py
Flask API serving the churn prediction model.

Endpoints:
    GET  /health   - health check
    POST /predict  - predict churn for a customer

Example request body for /predict:
{
    "tenure_months": 5,
    "monthly_charges": 95.5,
    "total_charges": 480.0,
    "contract_type": 0,
    "support_calls": 4,
    "has_internet_service": 1
}
"""

import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "model.pkl")
_bundle = joblib.load(MODEL_PATH)
model = _bundle["model"]
feature_cols = _bundle["feature_cols"]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    missing = [c for c in feature_cols if c not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        row = pd.DataFrame([{c: data[c] for c in feature_cols}])
        pred = int(model.predict(row)[0])
        proba = float(model.predict_proba(row)[0][1])
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    return jsonify({
        "churn_prediction": pred,
        "churn_probability": round(proba, 4),
        "label": "will churn" if pred == 1 else "will stay",
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
