import pandas as pd
import joblib
import os

# =========================================================
# LOAD MODEL FILES
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(
    os.path.join(BASE_DIR, "metro_demand_model.pkl")
)

day_encoder = joblib.load(
    os.path.join(BASE_DIR, "day_encoder.pkl")
)

from_encoder = joblib.load(
    os.path.join(BASE_DIR, "from_encoder.pkl")
)

to_encoder = joblib.load(
    os.path.join(BASE_DIR, "to_encoder.pkl")
)


# =========================================================
# FIND STATION
# =========================================================

def find_station(name, encoder):

    name = name.strip().lower()

    for station in encoder.classes_:

        if station.lower() == name:
            return station

    return None


# =========================================================
# PREDICTION FUNCTION
# =========================================================

def predict_demand(
    day,
    hour,
    from_station,
    to_station
):

    day = day.strip().capitalize()

    from_station = find_station(
        from_station,
        from_encoder
    )

    to_station = find_station(
        to_station,
        to_encoder
    )

    # -----------------------------
    # VALIDATION
    # -----------------------------

    if day not in day_encoder.classes_:
        raise ValueError("Invalid day")

    if from_station is None:
        raise ValueError("Invalid FROM station")

    if to_station is None:
        raise ValueError("Invalid TO station")

    if from_station == to_station:
        raise ValueError(
            "FROM and TO stations cannot be the same"
        )

    # -----------------------------
    # WEEKEND
    # -----------------------------

    is_weekend = int(
        day in ["Saturday", "Sunday"]
    )

    # -----------------------------
    # ENCODE
    # -----------------------------

    day_encoded = day_encoder.transform(
        [day]
    )[0]

    from_encoded = from_encoder.transform(
        [from_station]
    )[0]

    to_encoded = to_encoder.transform(
        [to_station]
    )[0]

    # -----------------------------
    # INPUT DATA
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
    # PREDICT
    # -----------------------------

    prediction = model.predict(
        input_data
    )[0]

    prediction = max(
        0,
        round(float(prediction))
    )

    # -----------------------------
    # TRAIN RECOMMENDATION
    # -----------------------------

    TRAIN_CAPACITY = 300

    recommended_trains = max(
        1,
        (prediction + TRAIN_CAPACITY - 1)
        // TRAIN_CAPACITY
    )

    return {
        "day": day,
        "hour": hour,
        "from_station": from_station,
        "to_station": to_station,
        "predicted_passengers": prediction,
        "train_capacity": TRAIN_CAPACITY,
        "recommended_trains": recommended_trains
    }


# =========================================================
# COMMAND LINE TEST
# =========================================================

if __name__ == "__main__":

    day = input(
        "Enter day: "
    ).strip()

    hour = int(
        input("Enter hour (0-23): ")
    )

    from_input = input(
        "Enter from station: "
    )

    to_input = input(
        "Enter to station: "
    )

    try:

        result = predict_demand(
            day,
            hour,
            from_input,
            to_input
        )

        print()
        print("===================================")
        print("       TRACKX ML PREDICTION")
        print("===================================")

        print(
            "Day:",
            result["day"]
        )

        print(
            "Time:",
            f'{result["hour"]}:00'
        )

        print(
            "From:",
            result["from_station"]
        )

        print(
            "To:",
            result["to_station"]
        )

        print(
            "Predicted passenger demand:",
            result["predicted_passengers"]
        )

        print(
            "Train capacity:",
            result["train_capacity"]
        )

        print(
            "Recommended trains:",
            result["recommended_trains"]
        )

        print("===================================")

    except ValueError as error:

        print()
        print("❌", error)