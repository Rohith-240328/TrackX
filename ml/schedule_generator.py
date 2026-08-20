# ============================================================
# TRACKX — KOCHI METRO
# AI TRAIN SCHEDULE GENERATOR
# ============================================================
#
# FLEET
# ------------------------------------------------------------
# TRAIN-01 → TRAIN-25 = RUNNING TRAINS
# TRAIN-26 → TRAIN-30 = BACKUP TRAINS
#
# The normal AI schedule uses ONLY TRAIN-01 → TRAIN-25.
#
# FREQUENCY
# ------------------------------------------------------------
# MONDAY-FRIDAY
# 06:00-07:00  = 8m 30s
# 07:00-09:00  = 6m 45s
# 09:00-11:00  = 8m 30s
# 11:00-17:00  = 10m
# 17:00-20:00  = 6m 45s
# 20:00-21:00  = 8m 30s
# 21:00-23:00  = 10m
#
# SATURDAY
# 06:00-07:00  = 10m
# 07:00-09:00  = 8m 30s
# 09:00-17:00  = 10m
# 17:00-20:00  = 8m 30s
# 20:00-23:00  = 10m
#
# SUNDAY
# 06:00-23:00  = 10m
#
# OUTPUT
# ------------------------------------------------------------
# schedule_monday.csv
# schedule_tuesday.csv
# schedule_wednesday.csv
# schedule_thursday.csv
# schedule_friday.csv
# schedule_saturday.csv
# schedule_sunday.csv
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
# FREQUENCY RULES
# ============================================================

WEEKDAY_RULES = [
    ("06:00", "07:00", 8 * 60 + 30),
    ("07:00", "09:00", 6 * 60 + 45),
    ("09:00", "11:00", 8 * 60 + 30),
    ("11:00", "17:00", 10 * 60),
    ("17:00", "20:00", 6 * 60 + 45),
    ("20:00", "21:00", 8 * 60 + 30),
    ("21:00", "23:00", 10 * 60),
]


SATURDAY_RULES = [
    ("06:00", "07:00", 10 * 60),
    ("07:00", "09:00", 8 * 60 + 30),
    ("09:00", "17:00", 10 * 60),
    ("17:00", "20:00", 8 * 60 + 30),
    ("20:00", "23:00", 10 * 60),
]


SUNDAY_RULES = [
    ("06:00", "07:00", 10 * 60),
    ("07:00", "09:00", 10 * 60),
    ("09:00", "17:00", 10 * 60),
    ("17:00", "20:00", 10 * 60),
    ("20:00", "23:00", 10 * 60),
]


# ============================================================
# DAY RULE SELECTOR
# ============================================================

def get_rules(day):

    day = day.strip().lower()

    if day in [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday"
    ]:
        return WEEKDAY_RULES

    if day == "saturday":
        return SATURDAY_RULES

    if day == "sunday":
        return SUNDAY_RULES

    raise ValueError(f"Invalid day: {day}")


# ============================================================
# TIME CONVERSION
# ============================================================

def time_to_seconds(time_string):

    hour, minute = map(
        int,
        time_string.split(":")
    )

    return (
        hour * 3600
        +
        minute * 60
    )


def seconds_to_time(seconds):

    hour = seconds // 3600

    minute = (
        seconds % 3600
    ) // 60

    return f"{hour:02d}:{minute:02d}"


# ============================================================
# GENERATE DEPARTURE TIMES
# ============================================================

def generate_departure_times(day):

    rules = get_rules(day)

    departures = []

    for start, end, interval in rules:

        current = time_to_seconds(start)

        end_seconds = time_to_seconds(end)

        while current < end_seconds:

            departures.append(
                seconds_to_time(current)
            )

            current += interval

    return departures


# ============================================================
# ASSIGN 25 RUNNING TRAINS
# ============================================================
#
# Every scheduled departure gets one of the 25 running trains.
#
# Example:
#
# Departure 1  -> TRAIN-01
# Departure 2  -> TRAIN-02
# ...
# Departure 25 -> TRAIN-25
# Departure 26 -> TRAIN-01
#
# Therefore all 25 trains are used.
#
# TRAIN-26 → TRAIN-30 are NOT used normally.
# ============================================================

def assign_trains(departure_times):

    schedule = []

    for index, departure_time in enumerate(
        departure_times
    ):

        train_id = RUNNING_TRAIN_IDS[
            index % len(RUNNING_TRAIN_IDS)
        ]

        schedule.append({

            "train_id": train_id,

            "train": train_id,

            "departure_time":
                departure_time,

            "status":
                "ACTIVE"

        })

    return schedule


# ============================================================
# CREATE DAY SCHEDULE
# ============================================================

def generate_schedule(day):

    departure_times = (
        generate_departure_times(day)
    )

    schedule = assign_trains(
        departure_times
    )

    final_schedule = []

    for record in schedule:

        final_schedule.append({

            "day":
                day,

            "train_id":
                record["train_id"],

            "train":
                record["train"],

            "departure_time":
                record["departure_time"],

            "status":
                record["status"]

        })

    return final_schedule


# ============================================================
# SAVE CSV
# ============================================================

def save_schedule(day, schedule):

    filename = (
        f"schedule_{day.lower()}.csv"
    )

    filepath = BASE_DIR / filename

    fieldnames = [
        "day",
        "train_id",
        "train",
        "departure_time",
        "status"
    ]

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

def verify_train_usage(schedule):

    used_trains = sorted(
        set(
            row["train_id"]
            for row in schedule
        )
    )

    missing_running = [
        train
        for train in RUNNING_TRAIN_IDS
        if train not in used_trains
    ]

    backup_used = [
        train
        for train in BACKUP_TRAIN_IDS
        if train in used_trains
    ]

    print()
    print("TRAIN USAGE CHECK")
    print("-" * 50)

    print(
        f"Running fleet : {len(RUNNING_TRAIN_IDS)}"
    )

    print(
        f"Used trains   : {len(used_trains)}"
    )

    if missing_running:

        print(
            "Missing running trains:",
            ", ".join(missing_running)
        )

    else:

        print(
            "✓ TRAIN-01 to TRAIN-25 all used"
        )

    if backup_used:

        print(
            "WARNING: Backup trains used:",
            ", ".join(backup_used)
        )

    else:

        print(
            "✓ TRAIN-26 to TRAIN-30 not used"
        )

    print("-" * 50)


# ============================================================
# MAIN GENERATOR
# ============================================================

def main():

    print()
    print("=" * 60)
    print("TRACKX AI SCHEDULE GENERATOR")
    print("=" * 60)

    print()
    print("FLEET CONFIGURATION")
    print("-" * 60)

    print(
        f"Total trains   : {TOTAL_TRAINS}"
    )

    print(
        f"Running trains : {RUNNING_TRAINS}"
    )

    print(
        f"Backup trains  : {BACKUP_TRAINS}"
    )

    print()

    print(
        "Running fleet:"
    )

    print(
        ", ".join(RUNNING_TRAIN_IDS)
    )

    print()

    print(
        "Backup fleet:"
    )

    print(
        ", ".join(BACKUP_TRAIN_IDS)
    )

    print()
    print("=" * 60)

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
            f"Generating AI schedule for {day}..."
        )

        schedule = generate_schedule(day)

        filepath = save_schedule(
            day,
            schedule
        )

        print(
            f"✓ {day}: "
            f"{len(schedule)} departures"
        )

        print(
            f"✓ Saved: {filepath.name}"
        )

        verify_train_usage(
            schedule
        )

    print()
    print("=" * 60)
    print("AI SCHEDULE GENERATION COMPLETE")
    print("=" * 60)

    print()
    print("Generated files:")

    for day in days:

        print(
            f"  ✓ schedule_{day.lower()}.csv"
        )

    print()
    print(
        "25 running trains are assigned to the schedule."
    )

    print(
        "5 backup trains are reserved for employee replacement."
    )

    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()