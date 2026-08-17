import pandas as pd
import joblib

# Load trained model
model = joblib.load("metro_demand_model.pkl")

# Load encoders
day_encoder = joblib.load("day_encoder.pkl")
from_encoder = joblib.load("from_encoder.pkl")
to_encoder = joblib.load("to_encoder.pkl")


# -----------------------------
# FUNCTION TO FIND STATION
# -----------------------------
def find_station(name, encoder):
    name = name.strip().lower()

    for station in encoder.classes_:
        if station.lower() == name:
            return station

    return None


# -----------------------------
# GET USER INPUT
# -----------------------------
day = input("Enter day: ").strip().capitalize()

hour = int(input("Enter hour (0-23): "))

from_input = input("Enter from station: ")
to_input = input("Enter to station: ")


# -----------------------------
# FIND CORRECT STATION NAMES
# -----------------------------
from_station = find_station(from_input, from_encoder)
to_station = find_station(to_input, to_encoder)


# -----------------------------
# VALIDATE DAY
# -----------------------------
if day not in day_encoder.classes_:

    print()
    print("❌ Invalid day!")
    print("Available days:")

    for d in day_encoder.classes_:
        print("-", d)

    exit()


# -----------------------------
# VALIDATE FROM STATION
# -----------------------------
if from_station is None:

    print()
    print("❌ Invalid FROM station!")
    print("Available stations:")

    for station in from_encoder.classes_:
        print("-", station)

    exit()


# -----------------------------
# VALIDATE TO STATION
# -----------------------------
if to_station is None:

    print()
    print("❌ Invalid TO station!")
    print("Available stations:")

    for station in to_encoder.classes_:
        print("-", station)

    exit()


# -----------------------------
# WEEKEND
# -----------------------------
is_weekend = int(day in ["Saturday", "Sunday"])


# -----------------------------
# ENCODE INPUT
# -----------------------------
day_encoded = day_encoder.transform([day])[0]

from_encoded = from_encoder.transform([from_station])[0]

to_encoded = to_encoder.transform([to_station])[0]


# -----------------------------
# CREATE INPUT DATA
# -----------------------------
input_data = pd.DataFrame([
    {
        "day_of_week": day_encoded,
        "hour": hour,
        "is_weekend": is_weekend,
        "from_station": from_encoded,
        "to_station": to_encoded
    }
])


# -----------------------------
# ML PREDICTION
# -----------------------------
prediction = model.predict(input_data)[0]
# -----------------------------
# TRAIN RECOMMENDATION
# -----------------------------

TRAIN_CAPACITY = 300

recommended_trains = max(
    1,
    int((prediction + TRAIN_CAPACITY - 1) // TRAIN_CAPACITY)
)

# -----------------------------
# DISPLAY RESULT
# -----------------------------
print()
print("===================================")
print("       TRACKX ML PREDICTION")
print("===================================")

print("Day:", day)
print("Time:", f"{hour}:00")

print("From:", from_station)

print("To:", to_station)

print("Predicted passenger demand:", round(prediction))
print("Train capacity:", TRAIN_CAPACITY)
print("Recommended trains:", recommended_trains)
print("===================================")