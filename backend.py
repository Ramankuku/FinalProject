import os
import pickle
import numpy as np
from flask import Flask, request, jsonify

model_path = os.path.abspath("model_pickle.pkl")

# Ensure model loads correctly
try:
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None  # Prevents app from breaking if model loading fails

# Initialize Flask app
app = Flask(__name__)

# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Loan Eligibility Prediction API is running!"})

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded. Check the file path."}), 500

    try:
        # Get JSON data from request
        data = request.get_json()

        # Required features
        required_keys = ["experience", "income", "cc_avg", "education", "mortgage", "cd_account", "credit_card"]
        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            return jsonify({"error": f"Missing required fields: {missing_keys}"}), 400

        # Convert data to numpy array
        features = np.array([
            data["experience"], data["income"], data["cc_avg"],
            data["education"], data["mortgage"], data["cd_account"],
            data["credit_card"]
        ]).reshape(1, -1)

        # Make prediction
        prediction = model.predict(features)[0]
        result = "Eligible" if prediction == 1 else "Not Eligible"

        return jsonify({"loan_eligible": int(prediction), "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)
