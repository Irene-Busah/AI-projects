from flask import Flask, request, jsonify
import joblib
import numpy as np
import logging

# initializing the flask app
app = Flask(__name__)

# configuring logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# loading the model
MODEL_PATH = "model.pkl"
try:
    model = joblib.load(MODEL_PATH)
    logging.info(f"✅ Model loaded successfully from {MODEL_PATH}")

except Exception as e:
    logging.error(f"❌ Error loading model: {e}") 
    model = None




@app.route("/", methods=["GET"])
def home():
    """Root Endpoint - API Welcome Message"""

    return jsonify({
        "message": "🚀 Welcome to the ML Prediction API!",
        "endpoints": {
            "Predict": "/predict (POST)"
        }
    })


@app.route("/predict", methods=["POST"])
def predict():
    """Endpoint to make predictions using the trained model."""

    if model is None:
        logging.error("Prediction request failed: Model not loaded.")
        return jsonify({"error": "Model not loaded"}), 500
    try:
        # getting the JSON data from request
        data = request.json.get("input")
        if not data:
            logging.warning("Prediction request failed: Missing 'input' data.")
            return jsonify({"error": "Missing 'input' data"}), 400
        
        # converting input to NumPy array and make prediction
        prediction = model.predict(np.array(data).reshape(-1, 1))
        logging.info(f"Prediction successful: {prediction.tolist()}")
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return jsonify({"error": "Invalid input format"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
