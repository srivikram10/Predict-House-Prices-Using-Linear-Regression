from flask import Flask, render_template, request, jsonify
import joblib  # Changed from pickle for consistency
import numpy as np
import os

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'notebooks', 'models', 'linear_model.pkl')

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    model = None
    print(f"⚠️ Model not loaded: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        response = {"error": "Model not loaded correctly."}
        return jsonify(response) if request.is_json else render_template('index.html', prediction_text="⚠️ Model not loaded.")

    try:
        data = request.json if request.is_json else request.form
        location = data.get('location', '')
        area = float(data.get('area'))
        bedrooms = int(data.get('bedrooms'))
        bathrooms = int(data.get('bathrooms'))
        sqft = float(data.get('sqft'))
        city_type = data.get('city_type', '')

        if area <= 0 or bedrooms < 1 or bathrooms < 1 or sqft <= 0:
            raise ValueError("Invalid numerical values.")

        location_encoded = 1 if location.lower() == 'chennai' else 0
        city_encoded = 1 if city_type.lower() == 'urban' else 0

        features = np.array([[area, bedrooms, bathrooms, sqft, location_encoded, city_encoded]])
        prediction = model.predict(features)[0]
        prediction = round(prediction, 2)

        result = f"🏠 Predicted Price: ₹{prediction}"
        response = {"prediction": result}

        if request.is_json:
            return jsonify(response)
        else:
            return render_template('index.html', prediction_text=result)
    except Exception as e:
        error = f"⚠️ Error: {str(e)}"
        if request.is_json:
            return jsonify({"error": error})
        else:
            return render_template('index.html', prediction_text=error)

if __name__ == '__main__':
    app.run(debug=True)