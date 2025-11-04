import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_data(filepath):
    df = pd.read_csv(filepath)
    label_encoders = {}
    for col in ['Location', 'Area_Type', 'Region_Type']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    X = df.drop(columns=['Price'])
    y = df['Price']
    return X, y, label_encoders