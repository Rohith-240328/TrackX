import os
import math
import joblib
import pandas as pd


# =========================================================
# TRACKX V2 - ML PREDICTION ENGINE
# =========================================================


# =========================================================
# FILE LOCATION
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# =========================================================
# LOAD TRAINED MODEL
# =========================================================

model = joblib.load(
    os.path.join(
        BASE_DIR,
        "metro_demand_model_v2.pkl"
    )
)


# =========================================================
# LOAD ENCODERS
# =========================================================

day_encoder = joblib.load(
    os.path.join(
        BASE_DIR,
        "day_encoder_v2.pkl"
    )
)


from_encoder = joblib.load(
    os.path.join(
        BASE_DIR,
        "from_encoder_v2.pkl"
    )
)


to_encoder = joblib.load(
    os.path.join(
        BASE_DIR,
        "to_encoder_v2.pkl"
    )
)


from_zone_encoder = joblib.load(
    os.path.join(
        BASE_DIR,
        "from_zone_encoder_v2.pkl"
    )
)


to_zone_encoder = joblib.load(
    os.path.join(
        BASE_DIR,
        "to_zone_encoder_v2.pkl"
    )
)


demand_window_encoder = joblib.load(
    os.path.join(
        BASE_DIR,
        "demand_window_encoder_v2.pkl"
    )
)


# =========================================================
# TRAIN CONFIGURATION
# =========================================================

TRAIN_CAPACITY = 975


# =========================================================
# STATION → ZONE
# =========================================================

STATION_ZONE_MAP = {

    # -----------------------------------------------------
    # NORTHERN COMMUTER ZONE
    # -----------------------------------------------------

    "Aluva": "Northern Commuter Zone",
    "Pulinchodu": "Northern Commuter Zone",
    "Companypady": "Northern Commuter Zone",
    "Ambattukavu": "Northern Commuter Zone",
    "Muttom": "Northern Commuter Zone",
    "Kalamassery": "Northern Commuter Zone",
    "Cochin University": "Northern Commuter Zone",
    "Pathadipalam": "Northern Commuter Zone",
    "Edappally": "Northern Commuter Zone",

    # -----------------------------------------------------
    # CENTRAL BUSINESS DISTRICT
    # -----------------------------------------------------

    "Changampuzha Park": "Central Business District",
    "Palarivattom": "Central Business District",
    "JLN Stadium": "Central Business District",
    "Kaloor": "Central Business District",
    "Town Hall": "Central Business District",
    "MG Road": "Central Business District",
    "Maharaja's College": "Central Business District",

    # -----------------------------------------------------
    # SOUTHERN RESIDENTIAL ZONE
    # -----------------------------------------------------

    "Ernakulam South": "Southern Residential Zone",
    "Kadavanthra": "Southern Residential Zone",
    "Elamkulam": "Southern Residential Zone",
    "Vyttila": "Southern Residential Zone",
    "Thaikoodam": "Southern Residential Zone",
    "Petta": "Southern Residential Zone",
    "Vadakkekotta": "Southern Residential Zone",
    "SN Junction": "Southern Residential Zone",
    "Tripunithura Terminal": "Southern Residential Zone"
}


# =========================================================
# DEMAND WINDOW
# =========================================================

def get_demand_window(
    day,
    hour
):

    # Sunday metro starts at 07:30
    if day == "Sunday" and hour < 8:

        return "early_morning"


    # Monday - Saturday
    if hour >= 6 and hour < 8:

        return "early_morning"


    if hour >= 8 and hour < 10:

        return "morning_peak"


    if hour >= 10 and hour < 16:

        return "afternoon"


    if hour >= 16 and hour < 19:

        return "evening_peak"


    if hour >= 19 and hour < 21:

        return "night"


    if hour >= 21 and hour <= 23:

        return "late_night"


    return "late_night"


# =========================================================
# FIND EXACT ENCODER VALUE
# =========================================================

def find_encoder_value(
    value,
    encoder,
    field_name
):

    value = value.strip()


    for item in encoder.classes_:

        if item.lower() == value.lower():

            return item


    raise ValueError(
        f"Invalid {field_name}: {value}"
    )


# =========================================================
# PREDICT DEMAND
# =========================================================

def predict_demand(
    day,
    hour,
    from_station,
    to_station
):

    # -----------------------------------------------------
    # VALIDATE DAY
    # -----------------------------------------------------

    day = day.strip().capitalize()


    if day not in day_encoder.classes_:

        raise ValueError(
            f"Invalid day: {day}"
        )


    # -----------------------------------------------------
    # VALIDATE HOUR
    # -----------------------------------------------------

    hour = int(hour)


    if hour < 0 or hour > 23:

        raise ValueError(
            "Hour must be between 0 and 23"
        )


    # -----------------------------------------------------
    # VALIDATE STATIONS
    # -----------------------------------------------------

    from_station = find_encoder_value(
        from_station,
        from_encoder,
        "FROM station"
    )


    to_station = find_encoder_value(
        to_station,
        to_encoder,
        "TO station"
    )


    if from_station == to_station:

        raise ValueError(
            "FROM and TO stations cannot be the same"
        )


    # -----------------------------------------------------
    # CHECK ZONES
    # -----------------------------------------------------

    if from_station not in STATION_ZONE_MAP:

        raise ValueError(
            f"Zone not found for station: {from_station}"
        )


    if to_station not in STATION_ZONE_MAP:

        raise ValueError(
            f"Zone not found for station: {to_station}"
        )


    from_zone = STATION_ZONE_MAP[
        from_station
    ]


    to_zone = STATION_ZONE_MAP[
        to_station
    ]


    # -----------------------------------------------------
    # SUNDAY
    # -----------------------------------------------------

    is_sunday = int(
        day == "Sunday"
    )


    # -----------------------------------------------------
    # WEEKEND
    # -----------------------------------------------------

    is_weekend = int(
        day in [
            "Saturday",
            "Sunday"
        ]
    )


    # -----------------------------------------------------
    # DEMAND WINDOW
    # -----------------------------------------------------

    demand_window = get_demand_window(
        day,
        hour
    )


    # -----------------------------------------------------
    # ENCODE VALUES
    # -----------------------------------------------------

    day_encoded = day_encoder.transform(
        [day]
    )[0]


    from_station_encoded = from_encoder.transform(
        [from_station]
    )[0]


    to_station_encoded = to_encoder.transform(
        [to_station]
    )[0]


    from_zone_encoded = from_zone_encoder.transform(
        [from_zone]
    )[0]


    to_zone_encoded = to_zone_encoder.transform(
        [to_zone]
    )[0]


    demand_window_encoded = demand_window_encoder.transform(
        [demand_window]
    )[0]


    # -----------------------------------------------------
    # CREATE MODEL INPUT
    # -----------------------------------------------------

    input_data = pd.DataFrame([
        {
            "day_encoded":
                day_encoded,

            "hour":
                hour,

            "from_station_encoded":
                from_station_encoded,

            "to_station_encoded":
                to_station_encoded,

            "from_zone_encoded":
                from_zone_encoded,

            "to_zone_encoded":
                to_zone_encoded,

            "is_weekend":
                is_weekend,

            "is_sunday":
                is_sunday,

            "demand_window_encoded":
                demand_window_encoded
        }
    ])


    # -----------------------------------------------------
    # ML PREDICTION
    # -----------------------------------------------------

    prediction = model.predict(
        input_data
    )[0]


    prediction = max(
        0,
        round(float(prediction))
    )


    # -----------------------------------------------------
    # RECOMMENDED TRAINS
    # -----------------------------------------------------

    recommended_trains = max(
        1,
        math.ceil(
            prediction /
            TRAIN_CAPACITY
        )
    )


    # -----------------------------------------------------
    # RETURN RESULT
    # -----------------------------------------------------

    return {

        "day":
            day,

        "hour":
            hour,

        "demand_window":
            demand_window,

        "from_station":
            from_station,

        "to_station":
            to_station,

        "from_zone":
            from_zone,

        "to_zone":
            to_zone,

        "predicted_passengers":
            prediction,

        "train_capacity":
            TRAIN_CAPACITY,

        "recommended_trains":
            recommended_trains
    }


# =========================================================
# TEST MODE
# =========================================================

if __name__ == "__main__":

    print()
    print("==============================================")
    print(" TRACKX V2 ML PREDICTION ENGINE TEST")
    print("==============================================")


    try:

        result = predict_demand(
            day="Monday",
            hour=8,
            from_station="Aluva",
            to_station="MG Road"
        )


        print()
        print("Prediction successful!")

        print()
        print("Day:",
              result["day"])

        print("Time:",
              f'{result["hour"]}:00')

        print("Demand window:",
              result["demand_window"])

        print("From:",
              result["from_station"])

        print("To:",
              result["to_station"])

        print("From zone:",
              result["from_zone"])

        print("To zone:",
              result["to_zone"])

        print(
            "Predicted passengers:",
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


    except Exception as error:

        print()
        print(
            "Prediction error:",
            error
        )