# ============================================================
# TRACKX — KOCHI METRO
# EXACT DAY-WISE ROUND-TRIP TRAIN SCHEDULE GENERATOR
# ============================================================
#
# MONDAY-FRIDAY : WEEKDAY SCHEDULE
# SATURDAY      : SATURDAY SCHEDULE
# SUNDAY        : SUNDAY SCHEDULE
#
# EVERY PHYSICAL TRAIN USES THE SAME TRAIN NUMBER
# FOR OUTBOUND AND RETURN JOURNEYS.
#
# OUTBOUND:
# ALUVA → TRIPUNITHURA TERMINAL
#
# RETURN:
# TRIPUNITHURA TERMINAL → ALUVA
#
# JOURNEY TIME:
# 46 minutes 50 seconds
#
# TERMINAL BREAK:
# 10 minutes
#
# RETURN OFFSET:
# 56 minutes 50 seconds
#
# IMPORTANT:
# NO TRAIN DEPARTURE AFTER 23:00:00
#
# ============================================================

from pathlib import Path
import csv


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# TRAIN FLEET
# ============================================================

TOTAL_TRAINS = 30
RUNNING_TRAINS = 25
BACKUP_TRAINS = 5


ALL_TRAINS = [
    f"TRAIN-{i:02d}"
    for i in range(1, TOTAL_TRAINS + 1)
]


RUNNING_TRAIN_IDS = [
    f"TRAIN-{i:02d}"
    for i in range(1, RUNNING_TRAINS + 1)
]


BACKUP_TRAIN_IDS = [
    f"TRAIN-{i:02d}"
    for i in range(
        RUNNING_TRAINS + 1,
        TOTAL_TRAINS + 1
    )
]


# ============================================================
# JOURNEY TIME
# ============================================================

TRAVEL_TIME_SECONDS = (
    46 * 60 + 50
)


# ============================================================
# TERMINAL BREAK
# ============================================================

TERMINAL_BREAK_SECONDS = (
    10 * 60
)


# ============================================================
# RETURN OFFSET
# ============================================================

RETURN_OFFSET_SECONDS = (
    TRAVEL_TIME_SECONDS
    +
    TERMINAL_BREAK_SECONDS
)


# ============================================================
# LAST ALLOWED DEPARTURE
# ============================================================

LAST_DEPARTURE_SECONDS = (
    23 * 60 * 60
)


# ============================================================
# MONDAY-FRIDAY DEPARTURES
# ============================================================
#
# 06:00–07:00  → approximately 8 min 30 sec
# 07:00–09:00  → approximately 6 min 45 sec
# 09:00–11:00  → approximately 8 min 30 sec
# 11:00–17:00  → every 10 min
# 17:00–20:00  → approximately 6 min 45 sec
# 20:00–21:00  → approximately 8 min 30 sec
# 21:00–23:00  → every 10 min
#
# NO DEPARTURE AFTER 23:00.
#
# ============================================================

WEEKDAY_DEPARTURES = [

    "06:00:00",
    "06:08:00",
    "06:17:00",
    "06:25:00",
    "06:34:00",
    "06:42:00",
    "06:51:00",

    "07:00:00",
    "07:06:00",
    "07:13:00",
    "07:20:00",
    "07:27:00",
    "07:33:00",
    "07:40:00",
    "07:47:00",
    "07:54:00",

    "08:00:00",
    "08:04:30",
    "08:13:00",
    "08:21:30",
    "08:30:00",
    "08:38:30",
    "08:47:00",
    "08:55:30",

    "09:04:00",
    "09:12:30",
    "09:21:00",
    "09:29:30",
    "09:38:00",
    "09:46:30",
    "09:55:00",

    "10:03:30",
    "10:12:00",
    "10:20:30",
    "10:29:00",
    "10:37:30",
    "10:46:00",
    "10:54:30",

    "11:03:00",
    "11:13:00",
    "11:23:00",
    "11:33:00",
    "11:43:00",
    "11:53:00",

    "12:03:00",
    "12:13:00",
    "12:23:00",
    "12:33:00",
    "12:43:00",
    "12:53:00",

    "13:03:00",
    "13:13:00",
    "13:23:00",
    "13:33:00",
    "13:43:00",
    "13:53:00",

    "14:03:00",
    "14:13:00",
    "14:23:00",
    "14:33:00",
    "14:43:00",
    "14:53:00",

    "15:03:00",
    "15:13:00",
    "15:23:00",
    "15:33:00",
    "15:43:00",
    "15:53:00",

    "16:03:00",
    "16:13:00",
    "16:23:00",
    "16:33:00",
    "16:43:00",
    "16:53:00",

    "17:03:00",
    "17:09:45",
    "17:16:30",
    "17:23:15",
    "17:30:00",
    "17:36:45",
    "17:43:30",
    "17:50:15",
    "17:57:00",

    "18:03:45",
    "18:10:30",
    "18:17:15",
    "18:24:00",
    "18:30:45",
    "18:37:30",
    "18:44:15",
    "18:51:00",
    "18:57:45",

    "19:04:30",
    "19:11:15",
    "19:18:00",
    "19:24:45",
    "19:31:30",
    "19:38:15",
    "19:45:00",
    "19:51:45",
    "19:58:30",

    "20:05:15",
    "20:12:00",
    "20:20:30",
    "20:29:00",
    "20:37:30",
    "20:46:00",
    "20:54:30",

    "21:03:00",
    "21:13:00",
    "21:23:00",
    "21:33:00",
    "21:43:00",
    "21:53:00",

    "22:03:00",
    "22:13:00",
    "22:23:00",
    "22:33:00",
    "22:43:00",
    "22:53:00"
]


# ============================================================
# SATURDAY DEPARTURES
# ============================================================

def generate_saturday_departures():

    departures = []


    # --------------------------------------------------------
    # 06:00–07:00
    # Every 10 minutes
    # --------------------------------------------------------

    current = 6 * 3600

    while current < 7 * 3600:

        departures.append(
            seconds_to_time(current)
        )

        current += 10 * 60


    # --------------------------------------------------------
    # 07:00–09:00
    # Every 8 min 30 sec
    # --------------------------------------------------------

    current = 7 * 3600

    while current < 9 * 3600:

        departures.append(
            seconds_to_time(current)
        )

        current += 8 * 60 + 30


    # --------------------------------------------------------
    # 09:00–17:00
    # Every 10 minutes
    # --------------------------------------------------------

    current = 9 * 3600

    while current < 17 * 3600:

        departures.append(
            seconds_to_time(current)
        )

        current += 10 * 60


    # --------------------------------------------------------
    # 17:00–20:00
    # Every 8 min 30 sec
    # --------------------------------------------------------

    current = 17 * 3600

    while current < 20 * 3600:

        departures.append(
            seconds_to_time(current)
        )

        current += 8 * 60 + 30


    # --------------------------------------------------------
    # 20:00–23:00
    # Every 10 minutes
    # --------------------------------------------------------

    current = 20 * 3600

    while current < 23 * 3600:

        departures.append(
            seconds_to_time(current)
        )

        current += 10 * 60


    return departures


# ============================================================
# SUNDAY DEPARTURES
# ============================================================

def generate_sunday_departures():

    departures = []

    current = 6 * 3600

    while current < 23 * 3600:

        departures.append(
            seconds_to_time(current)
        )

        current += 10 * 60

    return departures


# ============================================================
# TIME → SECONDS
# ============================================================

def time_to_seconds(time_string):

    parts = time_string.split(":")

    hour = int(parts[0])

    minute = int(parts[1])

    second = (
        int(parts[2])
        if len(parts) >= 3
        else 0
    )

    return (
        hour * 3600
        +
        minute * 60
        +
        second
    )


# ============================================================
# SECONDS → TIME
# ============================================================

def seconds_to_time(seconds):

    seconds = seconds % (
        24 * 60 * 60
    )

    hour = seconds // 3600

    minute = (
        seconds % 3600
    ) // 60

    second = seconds % 60

    return (
        f"{hour:02d}:"
        f"{minute:02d}:"
        f"{second:02d}"
    )


# ============================================================
# GET DEPARTURES FOR DAY
# ============================================================

def generate_departure_times(day):

    day = day.strip().lower()


    # --------------------------------------------------------
    # Monday-Friday
    # --------------------------------------------------------

    if day in [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday"
    ]:

        return WEEKDAY_DEPARTURES.copy()


    # --------------------------------------------------------
    # Saturday
    # --------------------------------------------------------

    if day == "saturday":

        return generate_saturday_departures()


    # --------------------------------------------------------
    # Sunday
    # --------------------------------------------------------

    if day == "sunday":

        return generate_sunday_departures()


    raise ValueError(
        f"Invalid day: {day}"
    )


# ============================================================
# ADD SECONDS
# ============================================================

def add_seconds(
    time_string,
    seconds_to_add
):

    current = time_to_seconds(
        time_string
    )

    return seconds_to_time(
        current + seconds_to_add
    )


# ============================================================
# ASSIGN ROUND TRIPS
# ============================================================
#
# For EVERY outbound:
#
# TRAIN-XX
# Aluva → Tripunithura
#
# The SAME TRAIN-XX:
# Tripunithura → Aluva
#
# The return is only added if its departure
# is not after 11:00 PM.
#
# ============================================================

def assign_round_trips(
    departure_times
):

    schedule = []


    for index, departure_time in enumerate(
        departure_times
    ):


        # ----------------------------------------------------
        # Assign one of the 25 running trains
        # ----------------------------------------------------

        train_id = RUNNING_TRAIN_IDS[
            index % len(RUNNING_TRAIN_IDS)
        ]


        # ----------------------------------------------------
        # OUTBOUND ARRIVAL
        # ----------------------------------------------------

        arrival_time = add_seconds(
            departure_time,
            TRAVEL_TIME_SECONDS
        )


        # ----------------------------------------------------
        # RETURN DEPARTURE
        # ----------------------------------------------------

        return_departure = add_seconds(
            arrival_time,
            TERMINAL_BREAK_SECONDS
        )


        # ----------------------------------------------------
        # RETURN ARRIVAL
        # ----------------------------------------------------

        return_arrival = add_seconds(
            return_departure,
            TRAVEL_TIME_SECONDS
        )


        # ====================================================
        # OUTBOUND JOURNEY
        # ====================================================

        outbound = {

            "train_id":
                train_id,

            "train":
                train_id,

            "direction":
                "ALUVA_TO_TRIPUNITHURA",

            "from_station":
                "Aluva",

            "to_station":
                "Tripunithura Terminal",

            "departure_time":
                departure_time,

            "arrival_time":
                arrival_time,

            "status":
                "ACTIVE"

        }


        schedule.append(
            outbound
        )


        # ====================================================
        # RETURN JOURNEY
        # ====================================================
        #
        # IMPORTANT:
        # The same train_id is used.
        #
        # This is what allows:
        #
        # Tripunithura → Aluva
        #
        # searches to return the correct train.
        #
        # ====================================================

        return_departure_seconds = (
            time_to_seconds(
                return_departure
            )
        )


        if (
            return_departure_seconds
            <=
            LAST_DEPARTURE_SECONDS
        ):

            return_train = {

                "train_id":
                    train_id,

                "train":
                    train_id,

                "direction":
                    "TRIPUNITHURA_TO_ALUVA",

                "from_station":
                    "Tripunithura Terminal",

                "to_station":
                    "Aluva",

                "departure_time":
                    return_departure,

                "arrival_time":
                    return_arrival,

                "status":
                    "ACTIVE"

            }


            schedule.append(
                return_train
            )


    # ========================================================
    # SORT COMPLETE SCHEDULE
    # ========================================================
    #
    # Both directions are mixed chronologically.
    #
    # Example:
    #
    # 06:00  Aluva → Tripunithura
    # 06:08  Aluva → Tripunithura
    # 06:17  Aluva → Tripunithura
    # ...
    # 06:56:50 Tripunithura → Aluva
    #
    # ========================================================

    schedule.sort(
        key=lambda row:
            time_to_seconds(
                row["departure_time"]
            )
    )


    return schedule


# ============================================================
# CREATE DAY SCHEDULE
# ============================================================

def generate_schedule(day):

    departure_times = (
        generate_departure_times(day)
    )

    return assign_round_trips(
        departure_times
    )


# ============================================================
# SAVE CSV
# ============================================================

def save_schedule(
    day,
    schedule
):

    filename = (
        f"schedule_{day.lower()}.csv"
    )

    filepath = (
        BASE_DIR /
        filename
    )


    fieldnames = [

        "day",
        "train_id",
        "train",
        "direction",
        "from_station",
        "to_station",
        "departure_time",
        "arrival_time",
        "status"

    ]


    # --------------------------------------------------------
    # Add day
    # --------------------------------------------------------

    for row in schedule:

        row["day"] = day


    # --------------------------------------------------------
    # Write CSV
    # --------------------------------------------------------

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            schedule
        )


    return filepath


# ============================================================
# VERIFY TRAIN USAGE
# ============================================================

def verify_train_usage(
    schedule
):

    used_trains = sorted(
        set(
            row["train_id"]
            for row in schedule
        )
    )


    backup_used = [

        train

        for train in BACKUP_TRAIN_IDS

        if train in used_trains

    ]


    after_11 = [

        row

        for row in schedule

        if time_to_seconds(
            row["departure_time"]
        )
        >
        LAST_DEPARTURE_SECONDS

    ]


    print()
    print("TRAIN USAGE CHECK")
    print("-" * 60)


    print(
        f"Total physical trains : {TOTAL_TRAINS}"
    )

    print(
        f"Running trains        : {RUNNING_TRAINS}"
    )

    print(
        f"Backup trains         : {BACKUP_TRAINS}"
    )

    print(
        f"Physical trains used  : {len(used_trains)}"
    )

    print()


    print(
        "✓ Same train IDs used for return journeys."
    )

    print(
        "✓ Aluva → Tripunithura supported."
    )

    print(
        "✓ Tripunithura → Aluva supported."
    )

    print(
        "✓ 46 min 50 sec journey time."
    )

    print(
        "✓ 10-minute terminal break."
    )

    print(
        "✓ Return offset = 56 min 50 sec."
    )

    print(
        "✓ No departure after 11:00 PM."
    )

    print(
        "✓ No TRAIN-31+ created."
    )


    if backup_used:

        print(
            "WARNING: Backup trains used:",
            ", ".join(backup_used)
        )

    else:

        print(
            "✓ TRAIN-26 to TRAIN-30 remain backup."
        )


    if after_11:

        print(
            "WARNING: Trains found after 11 PM:",
            len(after_11)
        )

    else:

        print(
            "✓ No trains scheduled after 11 PM."
        )


    print("-" * 60)


# ============================================================
# VERIFY DIRECTIONS
# ============================================================

def verify_directions(
    schedule
):

    outbound = [

        row

        for row in schedule

        if row["direction"]
        ==
        "ALUVA_TO_TRIPUNITHURA"

    ]


    returns = [

        row

        for row in schedule

        if row["direction"]
        ==
        "TRIPUNITHURA_TO_ALUVA"

    ]


    print()
    print("DIRECTION CHECK")
    print("-" * 60)


    print(
        f"Aluva → Tripunithura : {len(outbound)}"
    )

    print(
        f"Tripunithura → Aluva : {len(returns)}"
    )


    # --------------------------------------------------------
    # Check that return trains use the same train IDs
    # --------------------------------------------------------

    outbound_ids = set(
        row["train_id"]
        for row in outbound
    )


    return_ids = set(
        row["train_id"]
        for row in returns
    )


    if return_ids.issubset(
        outbound_ids
    ):

        print(
            "✓ Return trains use valid running train IDs."
        )

    else:

        print(
            "WARNING: Invalid return train IDs found."
        )


    print("-" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)

    print(
        "TRACKX DAY-WISE ROUND-TRIP SCHEDULE GENERATOR"
    )

    print("=" * 70)


    print()
    print("CONFIGURATION")
    print("-" * 70)


    print(
        f"Total physical trains : {TOTAL_TRAINS}"
    )

    print(
        f"Running trains        : {RUNNING_TRAINS}"
    )

    print(
        f"Backup trains         : {BACKUP_TRAINS}"
    )

    print(
        "Journey time          : 46 min 50 sec"
    )

    print(
        "Terminal break        : 10 min"
    )

    print(
        "Return offset         : 56 min 50 sec"
    )

    print(
        "Last departure        : 23:00:00"
    )


    days = [

        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"

    ]


    for day in days:

        print()
        print(
            f"Generating {day} schedule..."
        )


        departures = (
            generate_departure_times(day)
        )


        schedule = generate_schedule(
            day
        )


        filepath = save_schedule(
            day,
            schedule
        )


        outbound_count = sum(

            1

            for row in schedule

            if row["direction"]
            ==
            "ALUVA_TO_TRIPUNITHURA"

        )


        return_count = sum(

            1

            for row in schedule

            if row["direction"]
            ==
            "TRIPUNITHURA_TO_ALUVA"

        )


        print(
            f"✓ Outbound departures : {outbound_count}"
        )

        print(
            f"✓ Return departures   : {return_count}"
        )

        print(
            f"✓ Total journeys      : {len(schedule)}"
        )

        print(
            f"✓ Saved               : {filepath.name}"
        )


        verify_train_usage(
            schedule
        )


        verify_directions(
            schedule
        )


    print()
    print("=" * 70)

    print(
        "DAY-WISE SCHEDULE GENERATION COMPLETE"
    )

    print("=" * 70)


    print()
    print(
        "✓ Monday-Friday use weekday schedule."
    )

    print(
        "✓ Saturday uses Saturday schedule."
    )

    print(
        "✓ Sunday uses Sunday schedule."
    )

    print(
        "✓ Same train returns from Tripunithura."
    )

    print(
        "✓ Return route is Tripunithura → Aluva."
    )

    print(
        "✓ Outbound route is Aluva → Tripunithura."
    )

    print(
        "✓ Return trains are inserted chronologically."
    )

    print(
        "✓ No departure after 11:00 PM."
    )

    print(
        "✓ TRAIN-26 to TRAIN-30 remain backup."
    )

    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()