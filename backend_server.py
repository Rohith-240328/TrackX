# ============================================================
# TRACKX — KOCHI METRO SMART TRAIN SCHEDULER
# BACKEND SERVER
#
# USER FRONTEND
#       ↕
#     FastAPI
#       ↕
# AI GENERATED SCHEDULE
#       ↕
# EMPLOYEE FRONTEND
#
# FLEET
# ------------------------------------------------------------
# TRAIN-01 -> TRAIN-25 : Running fleet
# TRAIN-26 -> TRAIN-30 : Backup fleet
#
# Employee can:
#   1. Login
#   2. View available trains
#   3. View unavailable trains
#   4. View backup trains
#   5. Mark train unavailable
#   6. Restore train
#   7. View AI schedule
#   8. View stations
#
# User can:
#   1. Load stations
#   2. Search journey
#   3. View upcoming trains
#   4. View AI schedule
#   5. View train frequency
#
# IMPORTANT:
# ML CSV files remain the schedule source.
# Employee availability is applied LIVE.
# ============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
from pydantic import BaseModel

from pathlib import Path

import sqlite3
import csv
import secrets


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="TrackX Kochi Metro Smart Train Scheduler",
    version="5.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "kochi_metro.db"

ML_DIR = BASE_DIR / "ml"


# ============================================================
# STATIONS
# ============================================================

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


# ============================================================
# FLEET
# ============================================================

TOTAL_TRAINS = 30

RUNNING_TRAINS = 25

BACKUP_TRAINS = 5


# ============================================================
# TRAIN IDS
# ============================================================

TRAIN_IDS = [

    f"TRAIN-{i:02d}"

    for i in range(
        1,
        TOTAL_TRAINS + 1
    )

]


RUNNING_TRAIN_IDS = [

    f"TRAIN-{i:02d}"

    for i in range(
        1,
        RUNNING_TRAINS + 1
    )

]


BACKUP_TRAIN_IDS = [

    f"TRAIN-{i:02d}"

    for i in range(
        RUNNING_TRAINS + 1,
        TOTAL_TRAINS + 1
    )

]


# ============================================================
# TRAIN STATUS
#
# active   = running and available
# inactive = running but unavailable
# backup   = reserve train
# ============================================================

train_status = {}


for train_id in RUNNING_TRAIN_IDS:

    train_status[train_id] = "active"


for train_id in BACKUP_TRAIN_IDS:

    train_status[train_id] = "backup"


# ============================================================
# BACKUP ASSIGNMENTS
# ============================================================

backup_assignments = {}


# ============================================================
# EMPLOYEE TOKENS
# ============================================================

employee_tokens = {}


# ============================================================
# SAFETY CHECKS
# ============================================================

if len(TRAIN_IDS) != 30:

    raise RuntimeError(
        "TrackX fleet error: expected 30 trains."
    )


if len(RUNNING_TRAIN_IDS) != 25:

    raise RuntimeError(
        "TrackX fleet error: expected 25 running trains."
    )


if len(BACKUP_TRAIN_IDS) != 5:

    raise RuntimeError(
        "TrackX fleet error: expected 5 backup trains."
    )


print("=" * 60)
print("TRACKX TRAIN FLEET")
print("=" * 60)

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

print("RUNNING TRAINS:")
print(
    ", ".join(RUNNING_TRAIN_IDS)
)

print()

print("BACKUP TRAINS:")
print(
    ", ".join(BACKUP_TRAIN_IDS)
)

print("=" * 60)


# ============================================================
# AI SCHEDULE FILES
# ============================================================

SCHEDULE_FILES = {

    "Monday":
        ML_DIR / "schedule_monday.csv",

    "Tuesday":
        ML_DIR / "schedule_tuesday.csv",

    "Wednesday":
        ML_DIR / "schedule_wednesday.csv",

    "Thursday":
        ML_DIR / "schedule_thursday.csv",

    "Friday":
        ML_DIR / "schedule_friday.csv",

    "Saturday":
        ML_DIR / "schedule_saturday.csv",

    "Sunday":
        ML_DIR / "schedule_sunday.csv"

}


# ============================================================
# VALID DAYS
# ============================================================

VALID_DAYS = [

    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"

]


# ============================================================
# DAY HELPER
# ============================================================

def normalize_day(day: str):

    if not day:

        return "Monday"


    for valid_day in VALID_DAYS:

        if valid_day.lower() == day.strip().lower():

            return valid_day


    raise HTTPException(
        status_code=400,
        detail="Invalid day."
    )


# ============================================================
# TIME HELPER
# ============================================================

def time_to_minutes(value: str):

    if not value:

        return 0


    value = str(value).strip()


    try:

        parts = value.split(":")

        hour = int(parts[0])

        minute = int(parts[1])

        second = 0


        if len(parts) >= 3:

            second = int(parts[2])


        return (
            hour * 60
            +
            minute
            +
            second / 60
        )


    except Exception:

        return 0


# ============================================================
# NORMALIZE TIME
# ============================================================

def normalize_time(value):

    if value is None:

        return ""


    value = str(value).strip()


    if not value:

        return ""


    try:

        parts = value.split(":")

        hour = int(parts[0])

        minute = int(parts[1])

        second = 0


        if len(parts) >= 3:

            second = int(parts[2])


        return (
            f"{hour:02d}:"
            f"{minute:02d}:"
            f"{second:02d}"
        )


    except Exception:

        return value


# ============================================================
# DATABASE
# ============================================================

def get_db_connection():

    connection = sqlite3.connect(
        str(DB_PATH)
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# STATIONS
# ============================================================

@app.get("/stations")
def get_stations():

    try:

        connection = get_db_connection()


        rows = connection.execute(

            """
            SELECT id, station_name
            FROM stations
            ORDER BY id
            """

        ).fetchall()


        connection.close()


        if rows:

            return [

                {
                    "id": row["id"],
                    "station_name":
                        row["station_name"]
                }

                for row in rows

            ]


    except Exception as error:

        print(
            "Database station loading failed:",
            error
        )


    return [

        {
            "id": index + 1,
            "station_name": station
        }

        for index, station
        in enumerate(STATIONS)

    ]


# ============================================================
# LOAD AI SCHEDULE
# ============================================================

def load_ai_schedule(day: str):

    day = normalize_day(day)

    file_path = SCHEDULE_FILES[day]


    if not file_path.exists():

        print(
            f"WARNING: AI schedule file missing: "
            f"{file_path}"
        )

        return []


    schedules = []


    try:

        with open(

            file_path,

            "r",

            encoding="utf-8-sig",

            newline=""

        ) as file:


            reader = csv.DictReader(file)


            print()
            print(
                f"Loading AI schedule: "
                f"{file_path.name}"
            )

            print(
                "CSV columns:",
                reader.fieldnames
            )


            for row in reader:


                departure_time = (

                    row.get("departure_time")

                    or

                    row.get("time")

                    or

                    row.get("departure")

                    or

                    ""

                ).strip()


                departure_time = normalize_time(
                    departure_time
                )


                if not departure_time:

                    continue


                from_station = (

                    row.get("from_station")

                    or

                    row.get("from")

                    or

                    STATIONS[0]

                ).strip()


                to_station = (

                    row.get("to_station")

                    or

                    row.get("to")

                    or

                    STATIONS[-1]

                ).strip()


                demand = (

                    row.get("predicted_demand")

                    or

                    row.get("demand")

                    or

                    ""

                )


                trains_required = (

                    row.get("trains_required")

                    or

                    row.get("required_trains")

                    or

                    ""

                )


                existing_train_id = (

                    row.get("train_id")

                    or

                    row.get("train")

                    or

                    ""

                ).strip()


                schedules.append({

                    "train":
                        existing_train_id,

                    "train_id":
                        existing_train_id,

                    "departure_time":
                        departure_time,

                    "day":
                        day,

                    "from_station":
                        from_station,

                    "to_station":
                        to_station,

                    "predicted_demand":
                        demand,

                    "trains_required":
                        trains_required,

                    "status":
                        "ACTIVE"

                })


        schedules.sort(

            key=lambda item:

                time_to_minutes(
                    item["departure_time"]
                )

        )


        # ====================================================
        # ASSIGN TRAIN IDS IF CSV DOES NOT HAVE THEM
        # ====================================================

        departure_train_map = {}

        next_train_index = 0


        for item in schedules:

            departure_time = item[
                "departure_time"
            ]


            if item["train_id"]:

                departure_train_map[
                    departure_time
                ] = item["train_id"]

                continue


            if departure_time in departure_train_map:

                assigned_train = (
                    departure_train_map[
                        departure_time
                    ]
                )

                item["train_id"] = assigned_train

                item["train"] = assigned_train

                continue


            assigned_train = RUNNING_TRAIN_IDS[
                next_train_index
                %
                len(RUNNING_TRAIN_IDS)
            ]


            departure_train_map[
                departure_time
            ] = assigned_train


            item["train_id"] = assigned_train

            item["train"] = assigned_train


            next_train_index += 1


        print(
            f"✓ {day}: "
            f"{len(schedules)} CSV records loaded"
        )


        print(
            f"✓ {day}: "
            f"{len(departure_train_map)} unique "
            f"departure timings"
        )


        return schedules


    except Exception as error:

        print(
            f"ERROR loading {day} schedule:",
            error
        )

        return []


# ============================================================
# CALCULATE BACKUP ASSIGNMENTS
# ============================================================

def calculate_backup_assignments():

    global backup_assignments

    backup_assignments = {}


    unavailable_running = [

        train_id

        for train_id in RUNNING_TRAIN_IDS

        if train_status.get(train_id)
        == "inactive"

    ]


    available_backups = [

        train_id

        for train_id in BACKUP_TRAIN_IDS

        if train_status.get(train_id)
        == "backup"

    ]


    for index, unavailable_train in enumerate(

        unavailable_running

    ):

        if index >= len(available_backups):

            break


        backup_train = available_backups[index]


        backup_assignments[
            unavailable_train
        ] = backup_train


    return backup_assignments


# ============================================================
# GET REPLACEMENT TRAIN
# ============================================================

def get_replacement_train(original_train):

    assignments = calculate_backup_assignments()


    if train_status.get(
        original_train
    ) == "active":

        return original_train


    if original_train in assignments:

        return assignments[
            original_train
        ]


    return None


# ============================================================
# APPLY LIVE TRAIN STATUS
# ============================================================

def apply_train_status(schedule):

    final_schedule = []


    assignments = calculate_backup_assignments()


    for item in schedule:

        new_item = dict(item)


        original_train = (

            item.get("train_id")

            or

            RUNNING_TRAIN_IDS[
                len(final_schedule)
                %
                len(RUNNING_TRAIN_IDS)
            ]

        )


        assigned_train = get_replacement_train(
            original_train
        )


        # ----------------------------------------------------
        # NO TRAIN AVAILABLE
        # ----------------------------------------------------

        if assigned_train is None:

            new_item["train"] = None

            new_item["train_id"] = None

            new_item["original_train"] = (
                original_train
            )

            new_item["fleet_type"] = (
                "NO_TRAIN_AVAILABLE"
            )

            new_item["status"] = (
                "UNAVAILABLE"
            )

            final_schedule.append(new_item)

            continue


        # ----------------------------------------------------
        # ASSIGNED TRAIN
        # ----------------------------------------------------

        new_item["train"] = assigned_train

        new_item["train_id"] = assigned_train

        new_item["original_train"] = (
            original_train
        )


        if assigned_train in BACKUP_TRAIN_IDS:

            new_item["fleet_type"] = "BACKUP"

            new_item["replacement_for"] = (
                original_train
            )

        else:

            new_item["fleet_type"] = "RUNNING"

            new_item["replacement_for"] = None


        new_item["status"] = "ACTIVE"


        final_schedule.append(new_item)


    return final_schedule


# ============================================================
# FINAL SCHEDULE
# ============================================================

def get_final_schedule(day: str):

    day = normalize_day(day)


    ai_schedule = load_ai_schedule(day)


    if not ai_schedule:

        return []


    return apply_train_status(ai_schedule)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {

        "message":
            "TrackX Kochi Metro Scheduler backend is running.",

        "status":
            "online",

        "ai_schedule":
            "enabled",

        "schedule_source":
            "ML generated CSV files",

        "total_trains":
            TOTAL_TRAINS,

        "running_trains":
            RUNNING_TRAINS,

        "backup_trains":
            BACKUP_TRAINS

    }


# ============================================================
# TRAIN AVAILABILITY
# ============================================================

@app.get("/train-availability")
def train_availability():

    active = sum(

        1

        for train_id in RUNNING_TRAIN_IDS

        if train_status.get(train_id)
        == "active"

    )


    inactive = sum(

        1

        for train_id in RUNNING_TRAIN_IDS

        if train_status.get(train_id)
        == "inactive"

    )


    return {

        "total_trains":
            TOTAL_TRAINS,

        "running_trains":
            RUNNING_TRAINS,

        "available_trains":
            active,

        "unavailable_trains":
            inactive,

        "backup_trains":
            BACKUP_TRAINS,

        "active_backup_assignments":
            calculate_backup_assignments()

    }


# ============================================================
# EMPLOYEE LOGIN
# ============================================================

class EmployeeLoginRequest(BaseModel):

    employee_id: str

    password: str


EMPLOYEE_ID = "EMP001"

EMPLOYEE_PASSWORD = "TrackX@123"


@app.post("/employee/login")
def employee_login(
    request: EmployeeLoginRequest
):

    employee_id = request.employee_id.strip()

    password = request.password


    if (

        employee_id != EMPLOYEE_ID

        or

        password != EMPLOYEE_PASSWORD

    ):

        raise HTTPException(

            status_code=401,

            detail=
                "Invalid Employee ID or password."

        )


    token = secrets.token_urlsafe(32)


    employee_tokens[token] = employee_id


    return {

        "success":
            True,

        "message":
            "Employee login successful.",

        "employee_id":
            employee_id,

        "role":
            "employee",

        "token":
            token

    }


# ============================================================
# EMPLOYEE TRAIN REQUEST
# ============================================================

class TrainRequest(BaseModel):

    train_id: str


# ============================================================
# EMPLOYEE TRAIN AVAILABILITY REQUEST
# ============================================================

class TrainAvailabilityUpdate(BaseModel):

    available: bool


# ============================================================
# EMPLOYEE — ALL TRAINS
# ============================================================

@app.get("/employee/trains")
def employee_trains():

    available_trains = []

    unavailable_trains = []

    backup_trains = []


    assignments = calculate_backup_assignments()


    # --------------------------------------------------------
    # RUNNING TRAINS
    # --------------------------------------------------------

    for train_id in RUNNING_TRAIN_IDS:

        status = train_status.get(
            train_id,
            "inactive"
        )


        replacement = assignments.get(
            train_id
        )


        train = {

            "train_id":
                train_id,

            "status":
                status,

            "capacity":
                1000,

            "available":
                status == "active",

            "fleet_type":
                "RUNNING",

            "replacement_train":
                replacement

        }


        if status == "active":

            available_trains.append(train)

        else:

            unavailable_trains.append(train)


    # --------------------------------------------------------
    # BACKUP TRAINS
    # --------------------------------------------------------

    assigned_backup_ids = set(
        assignments.values()
    )


    for train_id in BACKUP_TRAIN_IDS:

        assigned_to = None


        for (
            original_train,
            backup_train
        ) in assignments.items():

            if backup_train == train_id:

                assigned_to = original_train

                break


        backup_trains.append({

            "train_id":
                train_id,

            "status":
                "backup",

            "capacity":
                1000,

            "available":
                True,

            "fleet_type":
                "BACKUP",

            "in_service":
                train_id in assigned_backup_ids,

            "assigned_to":
                assigned_to

        })


    return {

        "success":
            True,

        "total_trains":
            TOTAL_TRAINS,

        "available_count":
            len(available_trains),

        "unavailable_count":
            len(unavailable_trains),

        "backup_count":
            len(backup_trains),

        "available_trains":
            available_trains,

        "unavailable_trains":
            unavailable_trains,

        "backup_trains":
            backup_trains,

        "backup_assignments":
            assignments,

        "trains":
            (
                available_trains
                +
                unavailable_trains
                +
                backup_trains
            )

    }


# ============================================================
# EMPLOYEE TRAIN AVAILABILITY UPDATE
#
# THIS IS THE IMPORTANT FIX.
#
# The old code used:
#
# AVAILABLE_TRAINS
# UNAVAILABLE_TRAINS
# save_train_availability()
#
# Those variables/functions did not exist.
#
# This version directly updates train_status.
# ============================================================

@app.post("/employee/trains/{train_id}/availability")
def update_train_availability(
    train_id: str,
    update: TrainAvailabilityUpdate
):

    train_id = train_id.upper().strip()


    # --------------------------------------------------------
    # VALIDATE TRAIN
    # --------------------------------------------------------

    if train_id not in TRAIN_IDS:

        raise HTTPException(

            status_code=404,

            detail=
                f"{train_id} does not exist."

        )


    # --------------------------------------------------------
    # BACKUP TRAINS
    #
    # Backup trains are not moved into the normal
    # available/unavailable running lists.
    # --------------------------------------------------------

    if train_id in BACKUP_TRAIN_IDS:

        raise HTTPException(

            status_code=400,

            detail=
                "Backup trains are managed separately."

        )


    # --------------------------------------------------------
    # UPDATE LIVE STATUS
    # --------------------------------------------------------

    if update.available:

        train_status[train_id] = "active"

        status = "available"

        message = (
            f"{train_id} is now available."
        )

    else:

        train_status[train_id] = "inactive"

        status = "unavailable"

        message = (
            f"{train_id} is now unavailable."
        )


    # --------------------------------------------------------
    # RECALCULATE BACKUPS
    # --------------------------------------------------------

    assignments = calculate_backup_assignments()


    backup_train = assignments.get(
        train_id
    )


    if not update.available:

        if backup_train:

            message = (

                f"{train_id} marked unavailable. "

                f"{backup_train} is assigned as "
                f"replacement."

            )

        else:

            message = (

                f"{train_id} marked unavailable. "

                f"No backup train is currently available."

            )


    else:

        message = (

            f"{train_id} restored successfully."

        )


    # --------------------------------------------------------
    # SERVER LOG
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("EMPLOYEE TRAIN CONTROL")
    print("=" * 60)

    print(
        f"Train       : {train_id}"
    )

    print(
        f"Availability: {status}"
    )

    print(
        f"Backup      : {backup_train}"
    )

    print(
        "Assignments :",
        assignments
    )

    print("=" * 60)
    print()


    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    active_count = sum(

        1

        for train in RUNNING_TRAIN_IDS

        if train_status.get(train)
        == "active"

    )


    inactive_count = sum(

        1

        for train in RUNNING_TRAIN_IDS

        if train_status.get(train)
        == "inactive"

    )


    return {

        "success":
            True,

        "train_id":
            train_id,

        "available":
            update.available,

        "status":
            status,

        "message":
            message,

        "backup_train":
            backup_train,

        "backup_assignments":
            assignments,

        "total_trains":
            TOTAL_TRAINS,

        "available_trains":
            active_count,

        "unavailable_trains":
            inactive_count

    }


# ============================================================
# MARK TRAIN UNAVAILABLE
# ============================================================

@app.post("/employee/train/unavailable")
def mark_train_unavailable(
    request: TrainRequest
):

    train_id = request.train_id.upper().strip()


    if train_id not in train_status:

        raise HTTPException(

            status_code=404,

            detail="Train not found."

        )


    if train_id in BACKUP_TRAIN_IDS:

        raise HTTPException(

            status_code=400,

            detail=
                "Backup trains are managed separately."

        )


    if train_status.get(
        train_id
    ) == "inactive":

        return {

            "success":
                True,

            "train_id":
                train_id,

            "status":
                "inactive",

            "message":
                f"{train_id} is already unavailable.",

            "backup_assignments":
                calculate_backup_assignments()

        }


    train_status[
        train_id
    ] = "inactive"


    assignments = calculate_backup_assignments()


    assigned_backup = assignments.get(
        train_id
    )


    if assigned_backup:

        message = (

            f"{train_id} marked unavailable. "

            f"{assigned_backup} is now replacing "
            f"{train_id}."

        )

    else:

        message = (

            f"{train_id} marked unavailable. "

            f"No backup train is currently available."

        )


    print()
    print("EMPLOYEE CONTROL")
    print(message)
    print()


    return {

        "success":
            True,

        "train_id":
            train_id,

        "status":
            "inactive",

        "backup_train":
            assigned_backup,

        "backup_assignments":
            assignments,

        "message":
            message

    }


# ============================================================
# RESTORE TRAIN
# ============================================================

@app.post("/employee/train/restore")
def restore_train(
    request: TrainRequest
):

    train_id = request.train_id.upper().strip()


    if train_id not in train_status:

        raise HTTPException(

            status_code=404,

            detail="Train not found."

        )


    if train_id in BACKUP_TRAIN_IDS:

        raise HTTPException(

            status_code=400,

            detail=
                "Backup trains remain in the backup fleet."

        )


    train_status[
        train_id
    ] = "active"


    assignments = calculate_backup_assignments()


    print()
    print(
        f"EMPLOYEE CONTROL: "
        f"{train_id} restored."
    )

    print(
        "Updated backup assignments:",
        assignments
    )

    print()


    return {

        "success":
            True,

        "train_id":
            train_id,

        "status":
            "active",

        "backup_assignments":
            assignments,

        "message":
            f"{train_id} restored successfully. "

    }

# ============================================================
# USER — TRAINS RUNNING
#
# IMPORTANT:
# Shows ALL scheduled departures from the AI CSV.
# It does NOT limit the result to 25 unique train IDs.
#
# Example:
# 06:00
# 06:08
# 06:17
# 06:25
# ...
#
# Every departure is displayed.
# Employee availability is still applied live.
# ============================================================

@app.get("/train-running")
def train_running(
    day: str = "Monday"
):

    matching_day = normalize_day(day)

    # --------------------------------------------------------
    # LOAD FINAL AI SCHEDULE
    # --------------------------------------------------------

    schedule = get_final_schedule(
        matching_day
    )

    running_trains = []

    # --------------------------------------------------------
    # EVERY SCHEDULED DEPARTURE
    #
    # Do NOT group by train_id.
    # A physical train can have multiple scheduled
    # departures during the day.
    # --------------------------------------------------------

    for index, item in enumerate(schedule):

        train_id = item.get(
            "train_id"
        )

        departure_time = item.get(
            "departure_time"
        )

        # ----------------------------------------------------
        # Ignore records with no assigned train
        # ----------------------------------------------------

        if not train_id:

            continue

        if not departure_time:

            continue

        # ----------------------------------------------------
        # Add every schedule departure
        # ----------------------------------------------------

        running_trains.append({

            "schedule_number":
                index + 1,

            "train_id":
                train_id,

            "train":
                train_id,

            "status":
                item.get(
                    "status",
                    "ACTIVE"
                ),

            "fleet_type":
                item.get(
                    "fleet_type",
                    "RUNNING"
                ),

            "original_train":
                item.get(
                    "original_train",
                    train_id
                ),

            "replacement_for":
                item.get(
                    "replacement_for"
                ),

            "from_station":
                item.get(
                    "from_station",
                    STATIONS[0]
                ),

            "to_station":
                item.get(
                    "to_station",
                    STATIONS[-1]
                ),

            "next_departure":
                departure_time,

            "departure_time":
                departure_time,

            "predicted_demand":
                item.get(
                    "predicted_demand"
                ),

            "trains_required":
                item.get(
                    "trains_required"
                )

        })

    # --------------------------------------------------------
    # RETURN ALL DEPARTURES
    # --------------------------------------------------------

    return {

        "success":
            True,

        "day":
            matching_day,

        "total_running":
            len(running_trains),

        "total_departures":
            len(running_trains),

        "trains":
            running_trains

    }

# ============================================================
# AI SCHEDULE
# ============================================================

@app.get("/schedule")
def get_schedule(
    day: str = "Monday"
):

    matching_day = normalize_day(day)


    schedule = get_final_schedule(
        matching_day
    )


    return {

        "success":
            True,

        "day":
            matching_day,

        "total_trains":
            len(schedule),

        "backup_assignments":
            calculate_backup_assignments(),

        "schedule":
            schedule

    }


# ============================================================
# FIND UPCOMING TRAINS
# ============================================================

@app.get("/find-trains")
def find_trains(

    from_station: str,

    to_station: str,

    day: str = "Monday",

    time: str = "06:00"

):

    from_station = from_station.strip()

    to_station = to_station.strip()


    station_lookup = {

        station.lower():
            station

        for station in STATIONS

    }


    if from_station.lower() not in station_lookup:

        raise HTTPException(

            status_code=400,

            detail=
                "Invalid starting station."

        )


    if to_station.lower() not in station_lookup:

        raise HTTPException(

            status_code=400,

            detail=
                "Invalid destination station."

        )


    if from_station.lower() == to_station.lower():

        raise HTTPException(

            status_code=400,

            detail=
                "Starting and destination stations "
                "cannot be the same."

        )


    from_station = station_lookup[
        from_station.lower()
    ]


    to_station = station_lookup[
        to_station.lower()
    ]


    matching_day = normalize_day(day)


    requested_minutes = time_to_minutes(
        time
    )


    schedule = get_final_schedule(
        matching_day
    )


    results = []

    seen = set()


    for train in schedule:

        train_id = train.get(
            "train_id"
        )


        departure_time = train.get(
            "departure_time"
        )


        if not train_id:

            continue


        if not departure_time:

            continue


        departure_minutes = time_to_minutes(
            departure_time
        )


        if departure_minutes < requested_minutes:

            continue


        unique_key = (

            train_id,

            departure_time

        )


        if unique_key in seen:

            continue


        seen.add(unique_key)


        results.append({

            "train_id":
                train_id,

            "train":
                train_id,

            "departure_time":
                departure_time,

            "from_station":
                from_station,

            "to_station":
                to_station,

            "status":
                train.get(
                    "status",
                    "ACTIVE"
                ),

            "fleet_type":
                train.get(
                    "fleet_type",
                    "RUNNING"
                ),

            "original_train":
                train.get(
                    "original_train",
                    train_id
                ),

            "replacement_for":
                train.get(
                    "replacement_for"
                ),

            "predicted_demand":
                train.get(
                    "predicted_demand"
                ),

            "trains_required":
                train.get(
                    "trains_required"
                )

        })


        if len(results) >= 5:

            break


    return {

        "success":
            True,

        "from_station":
            from_station,

        "to_station":
            to_station,

        "day":
            matching_day,

        "requested_time":
            time,

        "count":
            len(results),

        "results":
            results

    }


# ============================================================
# FREQUENCY
# ============================================================

@app.get("/frequency")
def get_frequency(

    day: str = "Monday",

    station: str = "",

    start_time: str = "06:00",

    end_time: str = "23:00"

):

    matching_day = normalize_day(day)


    schedule = get_final_schedule(
        matching_day
    )


    start_minutes = time_to_minutes(
        start_time
    )


    end_minutes = time_to_minutes(
        end_time
    )


    filtered = []

    seen = set()


    for train in schedule:

        train_id = train.get(
            "train_id"
        )


        departure_time = train.get(
            "departure_time"
        )


        if not train_id:

            continue


        if not departure_time:

            continue


        departure_minutes = time_to_minutes(
            departure_time
        )


        if (

            departure_minutes
            >=
            start_minutes

            and

            departure_minutes
            <=
            end_minutes

        ):

            key = (

                train_id,

                departure_time

            )


            if key in seen:

                continue


            seen.add(key)


            filtered.append(train)


    return {

        "success":
            True,

        "day":
            matching_day,

        "station":
            station,

        "start_time":
            start_time,

        "end_time":
            end_time,

        "count":
            len(filtered),

        "trains":
            filtered

    }


# ============================================================
# EMPLOYEE AI SCHEDULE
# ============================================================

@app.get("/employee/schedule")
def employee_schedule(
    day: str = "Monday"
):

    matching_day = normalize_day(day)


    schedule = get_final_schedule(
        matching_day
    )


    return {

        "success":
            True,

        "day":
            matching_day,

        "total_trains":
            len(schedule),

        "backup_assignments":
            calculate_backup_assignments(),

        "schedule":
            schedule

    }


# ============================================================
# EMPLOYEE STATUS
# ============================================================

@app.get("/employee/status")
def employee_status():

    available = [

        train_id

        for train_id in RUNNING_TRAIN_IDS

        if train_status.get(train_id)
        == "active"

    ]


    unavailable = [

        train_id

        for train_id in RUNNING_TRAIN_IDS

        if train_status.get(train_id)
        == "inactive"

    ]


    backups = [

        train_id

        for train_id in BACKUP_TRAIN_IDS

    ]


    assignments = calculate_backup_assignments()


    return {

        "success":
            True,

        "total_trains":
            TOTAL_TRAINS,

        "available_running":
            available,

        "unavailable_running":
            unavailable,

        "backup_trains":
            backups,

        "backup_assignments":
            assignments

    }


# ============================================================
# SCHEDULE SUMMARY
# ============================================================

@app.get("/schedule-summary")
def schedule_summary():

    summary = {}


    for day in VALID_DAYS:

        schedule = get_final_schedule(
            day
        )


        valid_schedule = [

            item

            for item in schedule

            if item.get("train_id")

        ]


        summary[day] = {

            "departures":
                len(valid_schedule),

            "first_train":

                (

                    valid_schedule[0]
                    ["departure_time"]

                    if valid_schedule

                    else None

                ),

            "last_train":

                (

                    valid_schedule[-1]
                    ["departure_time"]

                    if valid_schedule

                    else None

                )

        }


    return {

        "success":
            True,

        "summary":
            summary

    }


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "backend_server:app",

        host="127.0.0.1",

        port=8000,

        reload=True

    )