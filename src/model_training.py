from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import os
import numpy as np
from src.data_preprocessing import preprocess_data

def train_model():
    X, y, label_encoders = preprocess_data("data/House Price India.csv")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    print(f"R² Score: {r2:.3f}")
    print(f"MSE: {mse:.3f}")
    print(f"RMSE: {rmse:.3f}")
    
    os.makedirs("notebooks/models", exist_ok=True)
    joblib.dump(model, "notebooks/models/linear_model.pkl")
    joblib.dump(label_encoders, "notebooks/models/label_encoders.pkl")
    print("✅ Model trained and saved successfully!")

if __name__ == "__main__":
    train_model()