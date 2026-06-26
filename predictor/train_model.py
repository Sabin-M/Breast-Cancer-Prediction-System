import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
import joblib

# Load dataset

df = pd.read_csv("data.csv")

# Features

X = df[[
    "radius_mean",
    "texture_mean",
    "perimeter_mean",
    "area_mean",
    "smoothness_mean",
    "compactness_mean",
    "concavity_mean",
    "concave points_mean",
    "symmetry_mean",
    "fractal_dimension_mean"
]]

# Target

y = df["diagnosis"]

# Label encoding

le = LabelEncoder()
y = le.fit_transform(y)

# Scaling

scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split data

x_train, x_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model

model = LogisticRegression(max_iter=1000)
model.fit(x_train, y_train)

# Save model

joblib.dump(model, 'model.pkl')
joblib.dump(le, 'label_encoder.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Model Saved Successfully")