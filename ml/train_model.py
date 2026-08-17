import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load dataset
data = pd.read_csv("dataset.csv")

print("Dataset loaded successfully!")
print(data.head())

# Encode categorical columns
day_encoder = LabelEncoder()
from_encoder = LabelEncoder()
to_encoder = LabelEncoder()

data["day_of_week"] = day_encoder.fit_transform(data["day_of_week"])
data["from_station"] = from_encoder.fit_transform(data["from_station"])
data["to_station"] = to_encoder.fit_transform(data["to_station"])

# Features
X = data[
    [
        "day_of_week",
        "hour",
        "is_weekend",
        "from_station",
        "to_station"
    ]
]

# Target
y = data["demand"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# Create model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

print("Model trained successfully!")

# Predict test data
predictions = model.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Mean Absolute Error:", mae)
print("R2 Score:", r2)

# Save model and encoders
joblib.dump(model, "metro_demand_model.pkl")
joblib.dump(day_encoder, "day_encoder.pkl")
joblib.dump(from_encoder, "from_encoder.pkl")
joblib.dump(to_encoder, "to_encoder.pkl")

print("Model saved successfully!")