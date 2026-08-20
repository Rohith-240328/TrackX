# =========================================================
# TRACKX - KOCHI METRO CONFIGURATION
# =========================================================
# Realistic operating and scheduling parameters
# =========================================================


# =========================================================
# 1. METRO STATIONS
# =========================================================

STATIONS = [
    "Aluva",
    "Pulinchodu",
    "Companypady",
    "Ambattukavu",
    "Muttom",
    "Kalamassery",
    "Cochin University",
    "Pathadipalam",
    "Edappally",
    "Changampuzha Park",
    "Palarivattom",
    "JLN Stadium",
    "Kaloor",
    "Town Hall",
    "MG Road",
    "Maharaja's College",
    "Ernakulam South",
    "Kadavanthra",
    "Elamkulam",
    "Vyttila",
    "Thaikoodam",
    "Petta",
    "Vadakkekotta",
    "SN Junction",
    "Tripunithura Terminal"
]


# =========================================================
# 2. TRAIN INFORMATION
# =========================================================

NUMBER_OF_TRAINS = 25

TRAIN_CAPACITY = 975

TRAIN_NAMES = [
    f"KMRL-{i:02d}"
    for i in range(1, NUMBER_OF_TRAINS + 1)
]


# =========================================================
# 3. OPERATING HOURS
# =========================================================

OPERATING_HOURS = {

    "Monday": {
        "start": "06:00",
        "end": "23:00"
    },

    "Tuesday": {
        "start": "06:00",
        "end": "23:00"
    },

    "Wednesday": {
        "start": "06:00",
        "end": "23:00"
    },

    "Thursday": {
        "start": "06:00",
        "end": "23:00"
    },

    "Friday": {
        "start": "06:00",
        "end": "23:00"
    },

    "Saturday": {
        "start": "06:00",
        "end": "23:00"
    },

    "Sunday": {
        "start": "07:30",
        "end": "23:00"
    }
}


# =========================================================
# 4. TRAVEL TIME
# =========================================================

# Normal travel time between consecutive stations.
# This is independent of train headway.

INTER_STATION_TRAVEL_TIME = 2 * 60

# Complete journey:
# Aluva -> Tripunithura Terminal = 48 minutes

END_TO_END_TRAVEL_TIME = 48 * 60


# =========================================================
# 5. STATION DWELL TIMES
# =========================================================

# Default intermediate station dwell time

STANDARD_DWELL_TIME = 20


# High-volume stations

HIGH_VOLUME_STATIONS = {

    "Edappally": 45,

    "Cochin University": 45,

    "JLN Stadium": 45,

    "MG Road": 45,

    "Ernakulam South": 45,

    "Vyttila": 45
}


# =========================================================
# 6. TERMINAL TURNAROUND
# =========================================================

# After reaching a terminal, train remains there
# before starting its return journey.

TERMINAL_TURNAROUND_TIME = 10 * 60


# =========================================================
# 7. HEADWAY SCHEDULE
# =========================================================

# Headway = time between two consecutive trains
# leaving the terminal.

HEADWAY_SCHEDULE = [

    {
        "start": "06:00",
        "end": "07:59",
        "headway_seconds": 8 * 60 + 30,
        "headway_minutes": 8.5,
        "multiplier": 1.00
    },

    {
        "start": "08:00",
        "end": "10:00",
        "headway_seconds": 6 * 60 + 45,
        "headway_minutes": 6.75,
        "multiplier": 1.25
    },

    {
        "start": "10:01",
        "end": "15:59",
        "headway_seconds": 8 * 60 + 30,
        "headway_minutes": 8.5,
        "multiplier": 1.00
    },

    {
        "start": "16:00",
        "end": "19:00",
        "headway_seconds": 6 * 60 + 45,
        "headway_minutes": 6.75,
        "multiplier": 1.25
    },

    {
        "start": "19:01",
        "end": "21:59",
        "headway_seconds": 8 * 60 + 30,
        "headway_minutes": 8.5,
        "multiplier": 1.00
    },

    {
        "start": "22:00",
        "end": "23:00",
        "headway_seconds": 10 * 60,
        "headway_minutes": 10.0,
        "multiplier": 0.85
    }
]


# =========================================================
# 8. DEMAND WINDOWS
# =========================================================

DEMAND_WINDOWS = {

    "early_morning": {
        "start": "06:00",
        "end": "08:00"
    },

    "morning_peak": {
        "start": "08:00",
        "end": "10:00"
    },

    "afternoon": {
        "start": "10:00",
        "end": "16:00"
    },

    "evening_peak": {
        "start": "16:00",
        "end": "19:00"
    },

    "night": {
        "start": "19:00",
        "end": "21:00"
    },

    "late_night": {
        "start": "21:00",
        "end": "23:00"
    }
}


# =========================================================
# 9. MONDAY-SATURDAY DEMAND
# =========================================================

WEEKDAY_DEMAND = {

    "early_morning": {
        "min": 5000,
        "max": 8000
    },

    "morning_peak": {
        "min": 28000,
        "max": 35000
    },

    "afternoon": {
        "min": 10000,
        "max": 14000
    },

    "evening_peak": {
        "min": 32000,
        "max": 38000
    },

    "night": {
        "min": 12000,
        "max": 16000
    },

    "late_night": {
        "min": 3000,
        "max": 6000
    }
}


# =========================================================
# 10. SUNDAY DEMAND
# =========================================================

SUNDAY_DEMAND = {

    "early_morning": {
        "min": 0,
        "max": 0
    },

    "morning_peak": {
        "min": 4000,
        "max": 7000
    },

    "afternoon": {
        "min": 15000,
        "max": 22000
    },

    "evening_peak": {
        "min": 25000,
        "max": 30000
    },

    "night": {
        "min": 14000,
        "max": 18000
    },

    "late_night": {
        "min": 4000,
        "max": 7000
    }
}


# =========================================================
# 11. SPATIAL DEMAND ZONES
# =========================================================

ZONES = {

    "Northern Commuter Zone": [

        "Aluva",
        "Pulinchodu",
        "Companypady",
        "Ambattukavu",
        "Muttom",
        "Kalamassery",
        "Cochin University",
        "Pathadipalam",
        "Edappally"

    ],

    "Central Business District": [

        "Changampuzha Park",
        "Palarivattom",
        "JLN Stadium",
        "Kaloor",
        "Town Hall",
        "MG Road",
        "Maharaja's College"

    ],

    "Southern Residential Zone": [

        "Ernakulam South",
        "Kadavanthra",
        "Elamkulam",
        "Vyttila",
        "Thaikoodam",
        "Petta",
        "Vadakkekotta",
        "SN Junction",
        "Tripunithura Terminal"

    ]
}


# =========================================================
# 12. ZONE DEMAND RANGES
# =========================================================

ZONE_DEMAND = {

    "Northern Commuter Zone": {

        "weekday_peak": (12000, 15000),

        "weekday_offpeak": (4000, 6000),

        "sunday_peak": (9000, 11000)

    },


    "Central Business District": {

        "weekday_peak": (10000, 13000),

        "weekday_offpeak": (3500, 5000),

        "sunday_peak": (6000, 8000)

    },


    "Southern Residential Zone": {

        "weekday_peak": (6000, 9000),

        "weekday_offpeak": (2500, 4000),

        "sunday_peak": (7000, 9000)

    }

}


# =========================================================
# 13. DAYS
# =========================================================

DAYS = [

    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"

]


# =========================================================
# 14. DIRECTIONS
# =========================================================

DIRECTION_ALUVA_TO_TRIPUNITHURA = (
    "Aluva",
    "Tripunithura Terminal"
)

DIRECTION_TRIPUNITHURA_TO_ALUVA = (
    "Tripunithura Terminal",
    "Aluva"
)


# =========================================================
# 15. HELPER FUNCTIONS
# =========================================================

def get_station_index(station):

    if station not in STATIONS:
        raise ValueError(
            f"Unknown station: {station}"
        )

    return STATIONS.index(station)


def get_travel_time(from_station, to_station):

    from_index = get_station_index(from_station)

    to_index = get_station_index(to_station)

    station_difference = abs(
        to_index - from_index
    )

    return station_difference * INTER_STATION_TRAVEL_TIME


def get_headway(hour, minute):

    current_minutes = (
        hour * 60 + minute
    )

    for block in HEADWAY_SCHEDULE:

        start_hour, start_minute = map(
            int,
            block["start"].split(":")
        )

        end_hour, end_minute = map(
            int,
            block["end"].split(":")
        )

        start_minutes = (
            start_hour * 60 +
            start_minute
        )

        end_minutes = (
            end_hour * 60 +
            end_minute
        )

        if (
            start_minutes
            <= current_minutes
            <= end_minutes
        ):

            return block["headway_seconds"]

    return None


def get_dwell_time(station):

    if station in HIGH_VOLUME_STATIONS:

        return (
            HIGH_VOLUME_STATIONS[station]
        )

    return STANDARD_DWELL_TIME


# =========================================================
# 16. PRINT CONFIGURATION
# =========================================================

if __name__ == "__main__":

    print("======================================")
    print("       TRACKX METRO CONFIGURATION")
    print("======================================")

    print(
        "Number of stations:",
        len(STATIONS)
    )

    print(
        "Number of trains:",
        NUMBER_OF_TRAINS
    )

    print(
        "Train capacity:",
        TRAIN_CAPACITY
    )

    print(
        "Aluva → Tripunithura:",
        END_TO_END_TRAVEL_TIME // 60,
        "minutes"
    )

    print(
        "Terminal turnaround:",
        TERMINAL_TURNAROUND_TIME // 60,
        "minutes"
    )

    print()
    print("Train fleet:")

    for train in TRAIN_NAMES:
        print("-", train)

    print()
    print("Configuration loaded successfully.")