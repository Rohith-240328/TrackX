import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# =========================================================
# TRACKX - DEMAND PREDICTION MODEL V2
# =========================================================

print()
print("==============================================")
print(" TRACKX DEMAND PREDICTION MODEL V2")
print("==============================================")


# =========================================================
# LOAD DATASET
# =========================================================

DATASET_FILE = "dataset_v2.csv"

print()
print("Loading dataset...")

data = pd.read_csv(DATASET_FILE)

print("Dataset loaded successfully.")
print("Total records:", len(data))


# =========================================================
# DISPLAY DATASET INFORMATION
# =========================================================

print()
print("Dataset columns:")

for column in data.columns:
    print("-", column)


# =========================================================
# CLEAN DATA
# =========================================================

data = data.dropna()

print()
print("Records after cleaning:", len(data))


# =========================================================
# ENCODERS
# =========================================================

day_encoder = LabelEncoder()
from_encoder = LabelEncoder()
to_encoder = LabelEncoder()
from_zone_encoder = LabelEncoder()
to_zone_encoder = LabelEncoder()
demand_window_encoder = LabelEncoder()


# =========================================================
# ENCODE CATEGORICAL DATA
# =========================================================

data["day_encoded"] = day_encoder.fit_transform(
    data["day"]
)

data["from_station_encoded"] = from_encoder.fit_transform(
    data["from_station"]
)

data["to_station_encoded"] = to_encoder.fit_transform(
    data["to_station"]
)

data["from_zone_encoded"] = from_zone_encoder.fit_transform(
    data["from_zone"]
)

data["to_zone_encoded"] = to_zone_encoder.fit_transform(
    data["to_zone"]
)

data["demand_window_encoded"] = demand_window_encoder.fit_transform(
    data["demand_window"]
)


# =========================================================
# FEATURES
# =========================================================

FEATURE_COLUMNS = [
    "day_encoded",
    "hour",
    "from_station_encoded",
    "to_station_encoded",
    "from_zone_encoded",
    "to_zone_encoded",
    "is_weekend",
    "is_sunday",
    "demand_window_encoded"
]


X = data[FEATURE_COLUMNS]

y = data["predicted_demand"]


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


print()
print("Training records:", len(X_train))
print("Testing records:", len(X_test))


# =========================================================
# RANDOM FOREST MODEL
# =========================================================

print()
print("Training Random Forest model...")

model = RandomForestRegressor(
    n_estimators=150,
    max_depth=20,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)


print("Model trained successfully.")


# =========================================================
# MODEL EVALUATION
# =========================================================

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


print()
print("==============================================")
print(" MODEL EVALUATION")
print("==============================================")

print(
    "Mean Absolute Error:",
    round(mae, 2)
)

print(
    "R2 Score:",
    round(r2, 4)
)


# =========================================================
# SAVE MODEL
# =========================================================

joblib.dump(
    model,
    "metro_demand_model_v2.pkl"
)

print()
print("Model saved:")
print("metro_demand_model_v2.pkl")


# =========================================================
# SAVE ENCODERS
# =========================================================

joblib.dump(
    day_encoder,
    "day_encoder_v2.pkl"
)

joblib.dump(
    from_encoder,
    "from_encoder_v2.pkl"
)

joblib.dump(
    to_encoder,
    "to_encoder_v2.pkl"
)

joblib.dump(
    from_zone_encoder,
    "from_zone_encoder_v2.pkl"
)

joblib.dump(
    to_zone_encoder,
    "to_zone_encoder_v2.pkl"
)

joblib.dump(
    demand_window_encoder,
    "demand_window_encoder_v2.pkl"
)


# =========================================================
# DISPLAY ENCODER INFORMATION
# =========================================================

print()
print("Encoders saved successfully.")

print()
print("Days:")
print(list(day_encoder.classes_))

print()
print("Stations:")
print(list(from_encoder.classes_))

print()
print("Zones:")
print(list(from_zone_encoder.classes_))

print()
print("Demand windows:")
print(list(demand_window_encoder.classes_))


# =========================================================
# FEATURE IMPORTANCE
# =========================================================

print()
print("==============================================")
print(" FEATURE IMPORTANCE")
print("==============================================")


importance = pd.DataFrame({
    "feature": FEATURE_COLUMNS,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)


for _, row in importance.iterrows():

    print(
        f"{row['feature']}: "
        f"{row['importance']:.4f}"
    )


# =========================================================
# COMPLETED
# =========================================================

print()
print("==============================================")
print(" TRAINING COMPLETED SUCCESSFULLY")
print("==============================================")

print()
print("Files created:")

print("1. metro_demand_model_v2.pkl")
print("2. day_encoder_v2.pkl")
print("3. from_encoder_v2.pkl")
print("4. to_encoder_v2.pkl")
print("5. from_zone_encoder_v2.pkl")
print("6. to_zone_encoder_v2.pkl")
print("7. demand_window_encoder_v2.pkl")

print()
print("TrackX V2 ML model is ready.")