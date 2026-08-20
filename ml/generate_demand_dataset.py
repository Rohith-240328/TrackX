# =========================================================
# TRACKX - DEMAND DATASET GENERATOR V2
# =========================================================
# Generates realistic training data for the TrackX ML model.
#
# Output:
#     dataset_v2.csv
#
# The dataset considers:
#     - Day of week
#     - Time of day
#     - Station
#     - Direction
#     - Passenger demand
# =========================================================

import random
import pandas as pd

from metro_config import (
    STATIONS,
    DAYS,
    ZONES,
    WEEKDAY_DEMAND,
    SUNDAY_DEMAND,
    ZONE_DEMAND
)


# =========================================================
# SETTINGS
# =========================================================

OUTPUT_FILE = "dataset_v2.csv"

RANDOM_SEED = 42

random.seed(RANDOM_SEED)


# =========================================================
# CREATE STATION → ZONE MAPPING
# =========================================================

STATION_ZONE_MAP = {}

for zone_name, station_list in ZONES.items():

    for station in station_list:

        STATION_ZONE_MAP[station] = zone_name


# =========================================================
# DEMAND WINDOWS
# =========================================================

def get_demand_window(hour, day):
    """
    Returns the demand block for a given hour.
    """

    if day == "Sunday":

        if 7 <= hour < 8:
            return "early_morning"

        elif 8 <= hour < 10:
            return "morning_peak"

        elif 10 <= hour < 16:
            return "afternoon"

        elif 16 <= hour < 19:
            return "evening_peak"

        elif 19 <= hour < 21:
            return "night"

        elif 21 <= hour <= 23:
            return "late_night"

        return None

    else:

        if 6 <= hour < 8:
            return "early_morning"

        elif 8 <= hour < 10:
            return "morning_peak"

        elif 10 <= hour < 16:
            return "afternoon"

        elif 16 <= hour < 19:
            return "evening_peak"

        elif 19 <= hour < 21:
            return "night"

        elif 21 <= hour <= 23:
            return "late_night"

        return None


# =========================================================
# GET BASE DEMAND RANGE
# =========================================================

def get_base_demand_range(day, window):
    """
    Returns the overall passenger demand range
    for the selected day and time window.
    """

    if day == "Sunday":

        demand = SUNDAY_DEMAND[window]

    else:

        demand = WEEKDAY_DEMAND[window]

    return demand["min"], demand["max"]


# =========================================================
# GET ZONE DEMAND RANGE
# =========================================================

def get_zone_demand_range(
    zone,
    day,
    window
):
    """
    Returns demand range for a particular zone.
    """

    if day == "Sunday":

        if window == "evening_peak":

            return ZONE_DEMAND[
                zone
            ]["sunday_peak"]

        if window == "morning_peak":

            # Sunday morning is much lower than weekday peak.
            weekday_min, weekday_max = (
                ZONE_DEMAND[
                    zone
                ]["weekday_peak"]
            )

            return (
                int(weekday_min * 0.35),
                int(weekday_max * 0.50)
            )

        if window == "afternoon":

            weekday_min, weekday_max = (
                ZONE_DEMAND[
                    zone
                ]["weekday_offpeak"]
            )

            return (
                int(weekday_min * 2.5),
                int(weekday_max * 3.5)
            )

        if window == "night":

            weekday_min, weekday_max = (
                ZONE_DEMAND[
                    zone
                ]["weekday_offpeak"]
            )

            return (
                int(weekday_min * 3.0),
                int(weekday_max * 4.0)
            )

        if window == "late_night":

            weekday_min, weekday_max = (
                ZONE_DEMAND[
                    zone
                ]["weekday_offpeak"]
            )

            return (
                int(weekday_min * 1.3),
                int(weekday_max * 1.8)
            )

        return (0, 0)

    else:

        if window in [
            "morning_peak",
            "early_morning"
        ]:

            return ZONE_DEMAND[
                zone
            ]["weekday_peak"]

        if window in [
            "afternoon",
            "night",
            "late_night"
        ]:

            return ZONE_DEMAND[
                zone
            ]["weekday_offpeak"]

        if window == "evening_peak":

            return ZONE_DEMAND[
                zone
            ]["weekday_peak"]

        return (0, 0)


# =========================================================
# DAY-SPECIFIC MULTIPLIERS
# =========================================================

DAY_MULTIPLIERS = {

    "Monday": 1.00,

    "Tuesday": 1.03,

    "Wednesday": 1.05,

    "Thursday": 1.04,

    "Friday": 1.08,

    "Saturday": 0.92,

    "Sunday": 0.88
}


# =========================================================
# TIME-OF-DAY MULTIPLIER
# =========================================================

def get_time_multiplier(hour):

    if 6 <= hour < 8:
        return 0.70

    if 8 <= hour < 10:
        return 1.15

    if 10 <= hour < 16:
        return 0.75

    if 16 <= hour < 19:
        return 1.20

    if 19 <= hour < 21:
        return 0.85

    if 21 <= hour <= 23:
        return 0.45

    return 0.0


# =========================================================
# DIRECTION MULTIPLIER
# =========================================================

def get_direction_multiplier(
    from_station,
    to_station,
    hour,
    day
):
    """
    Models directional passenger flow.

    Morning:
        Aluva → Tripunithura
        stronger flow

    Evening:
        Tripunithura → Aluva
        stronger flow

    Sunday:
        flow is more balanced.
    """

    from_index = STATIONS.index(
        from_station
    )

    to_index = STATIONS.index(
        to_station
    )


    # -----------------------------------------------------
    # Same station
    # -----------------------------------------------------

    if from_station == to_station:

        return 0.0


    # -----------------------------------------------------
    # Morning
    # -----------------------------------------------------

    if 8 <= hour < 10:

        if from_index < to_index:

            return 1.20

        return 0.80


    # -----------------------------------------------------
    # Evening
    # -----------------------------------------------------

    if 16 <= hour < 19:

        if from_index > to_index:

            return 1.20

        return 0.80


    # -----------------------------------------------------
    # Sunday
    # -----------------------------------------------------

    if day == "Sunday":

        return 1.00


    # -----------------------------------------------------
    # Normal periods
    # -----------------------------------------------------

    return 1.00


# =========================================================
# STATION IMPORTANCE
# =========================================================

STATION_IMPORTANCE = {

    "Aluva": 1.15,

    "Pulinchodu": 0.90,

    "Companypady": 0.85,

    "Ambattukavu": 0.80,

    "Muttom": 0.85,

    "Kalamassery": 1.00,

    "Cochin University": 1.20,

    "Pathadipalam": 0.90,

    "Edappally": 1.35,

    "Changampuzha Park": 0.90,

    "Palarivattom": 1.05,

    "JLN Stadium": 1.15,

    "Kaloor": 1.10,

    "Town Hall": 1.00,

    "MG Road": 1.30,

    "Maharaja's College": 1.00,

    "Ernakulam South": 1.25,

    "Kadavanthra": 0.95,

    "Elamkulam": 0.95,

    "Vyttila": 1.35,

    "Thaikoodam": 0.90,

    "Petta": 0.85,

    "Vadakkekotta": 0.90,

    "SN Junction": 0.85,

    "Tripunithura Terminal": 1.10
}


# =========================================================
# GENERATE ONE DEMAND VALUE
# =========================================================

def generate_demand(
    day,
    hour,
    from_station,
    to_station
):

    window = get_demand_window(
        hour,
        day
    )


    if window is None:

        return 0


    # -----------------------------------------------------
    # Base demand
    # -----------------------------------------------------

    base_min, base_max = (
        get_base_demand_range(
            day,
            window
        )
    )


    base_demand = random.uniform(
        base_min,
        base_max
    )


    # -----------------------------------------------------
    # Source zone
    # -----------------------------------------------------

    from_zone = STATION_ZONE_MAP[
        from_station
    ]

    to_zone = STATION_ZONE_MAP[
        to_station
    ]


    from_zone_min, from_zone_max = (
        get_zone_demand_range(
            from_zone,
            day,
            window
        )
    )


    to_zone_min, to_zone_max = (
        get_zone_demand_range(
            to_zone,
            day,
            window
        )
    )


    # -----------------------------------------------------
    # Zone factor
    # -----------------------------------------------------

    from_zone_value = random.uniform(
        from_zone_min,
        from_zone_max
    )

    to_zone_value = random.uniform(
        to_zone_min,
        to_zone_max
    )


    zone_factor = (
        from_zone_value +
        to_zone_value
    ) / 2


    # -----------------------------------------------------
    # Day multiplier
    # -----------------------------------------------------

    day_multiplier = DAY_MULTIPLIERS[
        day
    ]


    # -----------------------------------------------------
    # Time multiplier
    # -----------------------------------------------------

    time_multiplier = get_time_multiplier(
        hour
    )


    # -----------------------------------------------------
    # Direction
    # -----------------------------------------------------

    direction_multiplier = (
        get_direction_multiplier(
            from_station,
            to_station,
            hour,
            day
        )
    )


    # -----------------------------------------------------
    # Station importance
    # -----------------------------------------------------

    from_importance = (
        STATION_IMPORTANCE[
            from_station
        ]
    )

    to_importance = (
        STATION_IMPORTANCE[
            to_station
        ]
    )


    station_factor = (
        from_importance +
        to_importance
    ) / 2


    # -----------------------------------------------------
    # Distance factor
    # -----------------------------------------------------

    from_index = STATIONS.index(
        from_station
    )

    to_index = STATIONS.index(
        to_station
    )

    distance = abs(
        to_index - from_index
    )


    # Longer journeys represent more passenger flow
    # through the corridor.

    distance_factor = (
        0.70 +
        min(distance / 24, 0.50)
    )


    # -----------------------------------------------------
    # Combine factors
    # -----------------------------------------------------

    raw_demand = (

        base_demand

        * 0.35

        + zone_factor * 0.65

    )


    demand = (

        raw_demand

        * day_multiplier

        * time_multiplier

        * direction_multiplier

        * station_factor

        * distance_factor

    )


    # -----------------------------------------------------
    # Random variation
    # -----------------------------------------------------

    variation = random.uniform(
        0.90,
        1.10
    )

    demand *= variation


    # -----------------------------------------------------
    # Prevent impossible values
    # -----------------------------------------------------

    demand = max(
        0,
        int(round(demand))
    )


    return demand


# =========================================================
# GENERATE DATASET
# =========================================================

def generate_dataset():

    rows = []


    print()
    print("==============================================")
    print(" TRACKX DEMAND DATASET GENERATOR V2")
    print("==============================================")
    print()


    # -----------------------------------------------------
    # Generate data for every day
    # -----------------------------------------------------

    for day in DAYS:

        print(
            f"Generating data for {day}..."
        )


        # Sunday starts at 07:30.
        # For simplicity, samples are generated every hour.

        if day == "Sunday":

            start_hour = 7

        else:

            start_hour = 6


        for hour in range(
            start_hour,
            24
        ):

            # Metro closes at 23:00.
            if hour > 23:
                continue


            window = get_demand_window(
                hour,
                day
            )


            if window is None:
                continue


            # -------------------------------------------------
            # Every station pair
            # -------------------------------------------------

            for from_station in STATIONS:

                for to_station in STATIONS:

                    if (
                        from_station ==
                        to_station
                    ):
                        continue


                    demand = generate_demand(
                        day,
                        hour,
                        from_station,
                        to_station
                    )


                    rows.append({

                        "day": day,

                        "hour": hour,

                        "from_station":
                            from_station,

                        "to_station":
                            to_station,

                        "from_zone":
                            STATION_ZONE_MAP[
                                from_station
                            ],

                        "to_zone":
                            STATION_ZONE_MAP[
                                to_station
                            ],

                        "is_weekend":
                            int(
                                day in [
                                    "Saturday",
                                    "Sunday"
                                ]
                            ),

                        "is_sunday":
                            int(
                                day ==
                                "Sunday"
                            ),

                        "demand_window":
                            window,

                        "predicted_demand":
                            demand
                    })


    # =====================================================
    # CREATE DATAFRAME
    # =====================================================

    dataframe = pd.DataFrame(
        rows
    )


    # =====================================================
    # SAVE DATASET
    # =====================================================

    dataframe.to_csv(
        OUTPUT_FILE,
        index=False
    )


    # =====================================================
    # DISPLAY INFORMATION
    # =====================================================

    print()
    print("==============================================")
    print(" DATASET GENERATED SUCCESSFULLY")
    print("==============================================")

    print(
        "Output file:",
        OUTPUT_FILE
    )

    print(
        "Total records:",
        len(dataframe)
    )

    print(
        "Columns:",
        len(dataframe.columns)
    )

    print()
    print("Columns:")

    for column in dataframe.columns:

        print(
            "-",
            column
        )


    # =====================================================
    # DAY SUMMARY
    # =====================================================

    print()
    print("==============================================")
    print(" DAY-WISE DEMAND SUMMARY")
    print("==============================================")


    summary = (
        dataframe
        .groupby("day")[
            "predicted_demand"
        ]
        .agg([
            "min",
            "max",
            "mean"
        ])
    )


    print(
        summary.round(0)
    )


    # =====================================================
    # WINDOW SUMMARY
    # =====================================================

    print()
    print("==============================================")
    print(" TIME-WINDOW DEMAND SUMMARY")
    print("==============================================")


    window_summary = (
        dataframe
        .groupby(
            [
                "day",
                "demand_window"
            ]
        )[
            "predicted_demand"
        ]
        .mean()
        .round(0)
    )


    print(
        window_summary
    )


    print()
    print(
        "Dataset generation completed."
    )

    print()


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    generate_dataset()