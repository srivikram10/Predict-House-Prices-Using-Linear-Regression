import numpy as np
import joblib

def predict_price(location, area, bedrooms, bathrooms, sqft, urban_rural):
    model = joblib.load("notebooks/models/linear_model.pkl")
    location_encoded = 1 if location.lower() == 'chennai' else 0
    urban_val = 1 if urban_rural.lower() == 'urban' else 0
    features = np.array([[area, bedrooms, bathrooms, sqft, location_encoded, urban_val]])
    prediction = model.predict(features)[0]
    return round(prediction, 2)

# Example usage
if __name__ == "__main__":
    print(predict_price("Chennai", 1200, 3, 2, 1200, "Urban"))  # Output: 85.0 (approx)