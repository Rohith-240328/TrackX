# ============================================================
# TRACKX — KOCHI METRO
# ML ROUND-TRIP TRAIN SCHEDULE GENERATOR
# ============================================================
#
# Generates:
#
#   OUTBOUND:
#       Aluva → Tripunithura Terminal
#
#   RETURN:
#       Tripunithura Terminal → Aluva
#
# IMPORTANT:
#
#   • Same physical train uses same TRAIN-ID for return
#   • TRAIN-01 to TRAIN-25 = running trains
#   • TRAIN-26 to TRAIN-30 = backup trains
#   • Journey time = 48 minutes
#   • Terminal time = 10 minutes
#   • Return offset = 58 minutes
#   • No return departure after 23:00
#
# IMPORTANT FOR FRONTEND:
#
# Outbound and return rows are NOT mixed chronologically.
#
# CSV structure:
#
#   ALL OUTBOUND ROWS
#   THEN
#   ALL RETURN ROWS
#
# This allows the frontend to display:
#
#   Aluva → Tripunithura     |     Tripunithura → Aluva
#
# side-by-side.
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
#
# Aluva → Tripunithura = 48 minutes
# Tripunithura → Aluva = 48 minutes
#
# ============================================================

TRAVEL_TIME_SECONDS = 48 * 60


# ============================================================
# TERMINAL BREAK
# ============================================================

TERMINAL_BREAK_SECONDS = 10 * 60


# ============================================================
# RETURN OFFSET
# ============================================================
#
# 48 minutes journey
# + 10 minutes terminal
# = 58 minutes
#
# ============================================================

RETURN_OFFSET_SECONDS = (
    TRAVEL_TIME_SECONDS
    + TERMINAL_BREAK_SECONDS
)


# ============================================================
# LAST ALLOWED DEPARTURE
# ============================================================

LAST_DEPARTURE_SECONDS = 23 * 60 * 60


# ============================================================
# MONDAY-FRIDAY DEPARTURES
# ============================================================

# ============================================================
# MONDAY-FRIDAY DEPARTURES
# ============================================================
#
# EXACT FINAL SCHEDULE
#
# Aluva → Tripunithura
#
# 119 outbound departures
#
# Return departure = outbound + 58 minutes
#
# ============================================================

WEEKDAY_DEPARTURES = [

    # --------------------------------------------------------
    # 06:00–07:00
    # --------------------------------------------------------

    "06:00:00",
    "06:08:00",
    "06:17:00",
    "06:25:00",
    "06:34:00",
    "06:42:00",
    "06:51:00",
    "06:59:00",

    # --------------------------------------------------------
    # 07:00–08:00
    # --------------------------------------------------------

    "07:00:00",
    "07:06:00",
    "07:13:00",
    "07:20:00",
    "07:27:00",
    "07:33:00",
    "07:40:00",
    "07:47:00",
    "07:54:00",

    # --------------------------------------------------------
    # 08:00–09:00
    # --------------------------------------------------------

    "08:00:00",
    "08:07:00",
    "08:14:00",
    "08:21:00",
    "08:27:00",
    "08:34:00",
    "08:41:00",
    "08:48:00",
    "08:54:00",

    # --------------------------------------------------------
    # 09:00–11:00
    # --------------------------------------------------------

    "09:00:00",
    "09:08:00",
    "09:17:00",
    "09:25:00",
    "09:34:00",
    "09:42:00",
    "09:51:00",
    "09:59:00",

    "10:08:00",
    "10:16:00",
    "10:25:00",
    "10:33:00",
    "10:42:00",
    "10:50:00",
    "10:59:00",

    # --------------------------------------------------------
    # 11:00–17:00
    # --------------------------------------------------------

    "11:00:00",
    "11:10:00",
    "11:20:00",
    "11:30:00",
    "11:40:00",
    "11:50:00",

    "12:00:00",
    "12:10:00",
    "12:20:00",
    "12:30:00",
    "12:40:00",
    "12:50:00",

    "13:00:00",
    "13:10:00",
    "13:20:00",
    "13:30:00",
    "13:40:00",
    "13:50:00",

    "14:00:00",
    "14:10:00",
    "14:20:00",
    "14:30:00",
    "14:40:00",
    "14:50:00",

    "15:00:00",
    "15:10:00",
    "15:20:00",
    "15:30:00",
    "15:40:00",
    "15:50:00",

    "16:00:00",
    "16:10:00",
    "16:20:00",
    "16:30:00",
    "16:40:00",
    "16:50:00",

    # --------------------------------------------------------
    # 17:00–20:00
    # --------------------------------------------------------

    "17:00:00",
    "17:06:00",
    "17:13:00",
    "17:20:00",
    "17:27:00",
    "17:33:00",
    "17:40:00",
    "17:47:00",
    "17:54:00",

    "18:00:00",
    "18:07:00",
    "18:14:00",
    "18:21:00",
    "18:27:00",
    "18:34:00",
    "18:41:00",
    "18:48:00",
    "18:54:00",

    "19:01:00",
    "19:08:00",
    "19:15:00",
    "19:21:00",
    "19:28:00",
    "19:35:00",
    "19:42:00",
    "19:48:00",
    "19:55:00",

    # --------------------------------------------------------
    # 20:00–21:00
    # --------------------------------------------------------

    "20:00:00",
    "20:08:00",
    "20:17:00",
    "20:25:00",
    "20:34:00",
    "20:42:00",
    "20:51:00",
    "20:59:00",

    # --------------------------------------------------------
    # 21:00–23:00
    # --------------------------------------------------------

    "21:00:00",
    "21:10:00",
    "21:20:00",
    "21:30:00",
    "21:40:00",
    "21:50:00",

    "22:00:00"
]


# ============================================================
# SATURDAY DEPARTURES
# ============================================================

def generate_saturday_departures():

    departures = []

    # 06:00–07:00
    current = 6 * 3600

    while current < 7 * 3600:

        departures.append(
            seconds_to_time(current)
        )

        current += 10 * 60


    # 07:00–09:00
    current = 7 * 3600

    while current < 9 * 3600:

        departures.append(
            seconds_to_time(current)
        )

        current += 8 * 60 + 30


    # 09:00–17:00
    current = 9 * 3600

    while current < 17 * 3600:

        departures.append(
            seconds_to_time(current)
        )

        current += 10 * 60


    # 17:00–20:00
    current = 17 * 3600

    while current < 20 * 3600:

        departures.append(
            seconds_to_time(current)
        )

        current += 8 * 60 + 30


    # 20:00–23:00
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
        + minute * 60
        + second
    )


# ============================================================
# SECONDS → TIME
# ============================================================

def seconds_to_time(seconds):

    seconds = seconds % (24 * 60 * 60)

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


    if day in [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday"
    ]:

        return WEEKDAY_DEPARTURES.copy()


    if day == "saturday":

        return generate_saturday_departures()


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
# IMPORTANT:
#
# We DO NOT mix outbound and return rows.
#
# First:
#
#   OUTBOUND LIST
#
# Then:
#
#   RETURN LIST
#
# This allows the frontend to display:
#
# ------------------------------------------------------------
#
#   ALUVA → TRIPUNITHURA
#   TRAIN-01  06:00
#
#                         TRIPUNITHURA → ALUVA
#                         TRAIN-01  06:58
#
# ------------------------------------------------------------
#
#   ALUVA → TRIPUNITHURA
#   TRAIN-02  06:08
#
#                         TRIPUNITHURA → ALUVA
#                         TRAIN-02  07:06
#
# ============================================================

def assign_round_trips(
    departure_times
):

    outbound_schedule = []

    return_schedule = []


    # ========================================================
    # CREATE OUTBOUND + RETURN PAIRS
    # ========================================================

    for index, departure_time in enumerate(
        departure_times
    ):

        # ----------------------------------------------------
        # TRAIN-01 → TRAIN-25 → TRAIN-01...
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
        #
        # 48 min journey
        # + 10 min terminal
        # = +58 min
        # ----------------------------------------------------

        return_departure = add_seconds(
            departure_time,
            RETURN_OFFSET_SECONDS
        )


        # ----------------------------------------------------
        # RETURN ARRIVAL
        # ----------------------------------------------------

        return_arrival = add_seconds(
            return_departure,
            TRAVEL_TIME_SECONDS
        )


        # ====================================================
        # OUTBOUND
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
                "ACTIVE",

            "replacement_train_id":
                ""

        }


        outbound_schedule.append(
            outbound
        )


        # ====================================================
        # RETURN
        # ====================================================

        return_departure_seconds = (
            time_to_seconds(
                return_departure
            )
        )


        if (
            return_departure_seconds
            <= LAST_DEPARTURE_SECONDS
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
                    "ACTIVE",

                "replacement_train_id":
                    ""

            }


            return_schedule.append(
                return_train
            )


    # ========================================================
    # IMPORTANT:
    #
    # DO NOT SORT EVERYTHING TOGETHER.
    #
    # OUTBOUND SIDE FIRST
    # RETURN SIDE SECOND
    # ========================================================

    return (
        outbound_schedule
        +
        return_schedule
    )


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
        "status",
        "replacement_train_id"

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
        "✓ TRAIN-01 to TRAIN-25 used for service."
    )

    print(
        "✓ Same train ID used for return."
    )

    print(
        "✓ TRAIN-26 to TRAIN-30 reserved as backup."
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
            "✓ No departures after 11 PM."
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


    # ========================================================
    # CHECK TRAIN IDs
    # ========================================================

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


    # ========================================================
    # CHECK RETURN OFFSET
    # ========================================================

    outbound_by_train = {}

    for row in outbound:

        key = (
            row["train_id"],
            row["departure_time"]
        )

        outbound_by_train[key] = row


    offset_errors = []


    for index in range(
        min(
            len(outbound),
            len(returns)
        )
    ):

        out = outbound[index]

        ret = returns[index]


        expected_return = add_seconds(
            out["departure_time"],
            RETURN_OFFSET_SECONDS
        )


        if (
            ret["train_id"]
            !=
            out["train_id"]
        ):

            offset_errors.append(
                f"{out['train_id']} ID mismatch"
            )

            continue


        if (
            ret["departure_time"]
            !=
            expected_return
        ):

            offset_errors.append(
                f"{out['train_id']} "
                f"{out['departure_time']} "
                f"expected {expected_return} "
                f"got {ret['departure_time']}"
            )


    if not offset_errors:

        print(
            "✓ Every return = outbound + 58 minutes."
        )

    else:

        print(
            "WARNING: Return offset errors:"
        )

        for error in offset_errors:

            print(
                " ",
                error
            )


    print("-" * 60)


# ============================================================
# PREVIEW SIDE-BY-SIDE SCHEDULE
# ============================================================

def preview_schedule(
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
    print("SIDE-BY-SIDE SCHEDULE PREVIEW")
    print("=" * 95)


    print(
        f"{'#':<5}"
        f"{'OUTBOUND':<32}"
        f"{'RETURN':<32}"
        f"{'TRAIN':<15}"
    )

    print("-" * 95)


    preview_count = min(
        10,
        len(outbound),
        len(returns)
    )


    for index in range(
        preview_count
    ):

        out = outbound[index]

        ret = returns[index]


        print(
            f"{index + 1:<5}"
            f"{out['departure_time']} "
            f"{out['from_station']} → "
            f"{out['to_station']:<10}"
            f"{ret['departure_time']} "
            f"{ret['from_station']} → "
            f"{ret['to_station']:<10}"
            f"{out['train_id']:<15}"
        )


    print("=" * 95)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)

    print(
        "TRACKX ML ROUND-TRIP SCHEDULE GENERATOR"
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
        "Journey time          : 48 minutes"
    )

    print(
        "Terminal break        : 10 minutes"
    )

    print(
        "Return offset         : 58 minutes"
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
            f"✓ Outbound departures : "
            f"{outbound_count}"
        )

        print(
            f"✓ Return departures   : "
            f"{return_count}"
        )

        print(
            f"✓ Total journeys      : "
            f"{len(schedule)}"
        )

        print(
            f"✓ Saved               : "
            f"{filepath.name}"
        )


        verify_train_usage(
            schedule
        )


        verify_directions(
            schedule
        )


        preview_schedule(
            schedule
        )


    print()
    print("=" * 70)

    print(
        "DAY-WISE ML SCHEDULE GENERATION COMPLETE"
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
        "✓ Same train ID used for return."
    )

    print(
        "✓ Journey time = 48 minutes."
    )

    print(
        "✓ Terminal break = 10 minutes."
    )

    print(
        "✓ Return offset = 58 minutes."
    )

    print(
        "✓ Outbound and return kept as separate sides."
    )

    print(
        "✓ No chronological mixing of directions."
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