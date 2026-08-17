
import pandas as pd
import joblib
import math


# ============================================================
# LOAD SAVED MODEL AND ENCODERS
# ============================================================

import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "metro_demand_model.pkl"))
day_encoder = joblib.load(os.path.join(BASE_DIR, "day_encoder.pkl"))
from_encoder = joblib.load(os.path.join(BASE_DIR, "from_encoder.pkl"))
to_encoder = joblib.load(os.path.join(BASE_DIR, "to_encoder.pkl"))


# ============================================================
# LOAD DATASET
# ============================================================

data = pd.read_csv(os.path.join(BASE_DIR, "dataset.csv"))

print("Dataset loaded successfully!")


# ============================================================
# TRAIN CAPACITY
# ============================================================

TRAIN_CAPACITY = 200


# ============================================================
# GET STATIONS
# ============================================================

stations = list(from_encoder.classes_)


# ============================================================
# CALCULATE REQUIRED TRAINS
# ============================================================

def calculate_trains(demand):

    if demand <= 0:
        return 0

    return max(
        1,
        math.ceil(demand / TRAIN_CAPACITY)
    )


# ============================================================
# PREDICT DEMAND
# ============================================================

def predict_demand(
    day,
    hour,
    from_station,
    to_station
):

    if day in ["Saturday", "Sunday"]:
        is_weekend = 1
    else:
        is_weekend = 0

    try:

        day_encoded = day_encoder.transform(
            [day]
        )[0]

        from_encoded = from_encoder.transform(
            [from_station]
        )[0]

        to_encoded = to_encoder.transform(
            [to_station]
        )[0]

    except ValueError:

        return 0

    input_data = pd.DataFrame(
        [[
            day_encoded,
            hour,
            is_weekend,
            from_encoded,
            to_encoded
        ]],
        columns=[
            "day_of_week",
            "hour",
            "is_weekend",
            "from_station",
            "to_station"
        ]
    )

    prediction = model.predict(
        input_data
    )[0]

    return max(
        0,
        round(prediction)
    )


# ============================================================
# GENERATE SCHEDULE
# ============================================================

def generate_schedule(day):

    schedule = []

    print()
    print("=" * 80)
    print("TRACKX - KOCHI METRO TRAIN SCHEDULE")
    print("=" * 80)

    print("Day:", day)
    print("Schedule:", "6:00 AM - 11:00 PM")

    print("=" * 80)


    # 6 AM TO 11 PM
    for hour in range(6, 24):

        hourly_entries = []


        # ----------------------------------------------------
        # CHECK EVERY STATION PAIR
        # ----------------------------------------------------

        for from_station in stations:

            for to_station in stations:

                if from_station == to_station:
                    continue


                demand = predict_demand(
                    day,
                    hour,
                    from_station,
                    to_station
                )


                if demand <= 0:
                    continue


                trains_required = calculate_trains(
                    demand
                )


                hourly_entries.append({

                    "time": f"{hour:02d}:00",

                    "from_station":
                        from_station,

                    "to_station":
                        to_station,

                    "predicted_demand":
                        demand,

                    "trains_required":
                        trains_required

                })


        # ----------------------------------------------------
        # SORT BY DEMAND
        # ----------------------------------------------------

        hourly_entries.sort(
            key=lambda x:
                x["predicted_demand"],
            reverse=True
        )


        # Keep top 10 routes
        hourly_entries = hourly_entries[:10]


        schedule.extend(
            hourly_entries
        )


        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

        if hour < 12:

            display_hour = hour
            period = "AM"

        elif hour == 12:

            display_hour = 12
            period = "PM"

        else:

            display_hour = hour - 12
            period = "PM"


        print()
        print(
            f"{display_hour}:00 {period}"
        )

        print("-" * 80)


        if not hourly_entries:

            print(
                "No trains required."
            )

        else:

            for entry in hourly_entries:

                print(
                    f"{entry['from_station']} "
                    f"-> "
                    f"{entry['to_station']} | "
                    f"Demand: "
                    f"{entry['predicted_demand']} | "
                    f"Trains: "
                    f"{entry['trains_required']}"
                )


    return schedule


# ============================================================
# SAVE SCHEDULE
# ============================================================

def save_schedule(
    schedule,
    day
):

    filename = (
        f"schedule_{day.lower()}.csv"
    )


    schedule_df = pd.DataFrame(
        schedule
    )


    schedule_df.to_csv(
        filename,
        index=False
    )


    print()
    print("=" * 80)
    print("SCHEDULE SAVED SUCCESSFULLY")
    print("=" * 80)

    print(
        "File:",
        filename
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("       TRACKX SCHEDULE GENERATOR")
    print("==========================================")

    print()
    print("Select day:")

    print("1. Monday")
    print("2. Tuesday")
    print("3. Wednesday")
    print("4. Thursday")
    print("5. Friday")
    print("6. Saturday")
    print("7. Sunday")


    choice = input(
        "\nEnter choice (1-7): "
    )


    days = {

        "1": "Monday",
        "2": "Tuesday",
        "3": "Wednesday",
        "4": "Thursday",
        "5": "Friday",
        "6": "Saturday",
        "7": "Sunday"

    }


    if choice not in days:

        print(
            "Invalid choice."
        )

    else:

        selected_day = days[
            choice
        ]


        schedule = generate_schedule(
            selected_day
        )


        save_schedule(
            schedule,
            selected_day
        )


        print()
        print(
            "Schedule generation completed!"
        )

