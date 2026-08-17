from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta


app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# AUTHENTICATION SETTINGS
# =========================================================

SECRET_KEY = "trackx-development-secret-change-later"
ALGORITHM = "HS256"

security = HTTPBearer()


# =========================================================
# DATABASE
# =========================================================

def get_connection():
    return sqlite3.connect("kochi_metro.db")


def create_employee_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# =========================================================
# PASSWORD FUNCTIONS
# =========================================================

def hash_password(password):

    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()

    return salt + ":" + password_hash


def verify_password(password, stored_password):

    salt, stored_hash = stored_password.split(":")

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()

    return secrets.compare_digest(
        password_hash,
        stored_hash
    )


# =========================================================
# CREATE DEFAULT EMPLOYEE
# =========================================================

def create_default_employee():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM employees WHERE username = ?",
        ("admin",)
    )

    employee = cursor.fetchone()

    if employee is None:

        password_hash = hash_password("trackx123")

        cursor.execute(
            """
            INSERT INTO employees
            (username, password_hash)
            VALUES (?, ?)
            """,
            ("admin", password_hash)
        )

        connection.commit()

        print("Default employee created")
        print("Username: admin")
        print("Password: trackx123")

    connection.close()


create_employee_table()
create_default_employee()


# =========================================================
# LOGIN MODEL
# =========================================================

class LoginRequest(BaseModel):

    username: str
    password: str


# =========================================================
# LOGIN
# =========================================================

@app.post("/employee/login")
def employee_login(login: LoginRequest):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username, password_hash
        FROM employees
        WHERE username = ?
        """,
        (login.username,)
    )

    employee = cursor.fetchone()

    connection.close()

    if employee is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    employee_id = employee[0]
    username = employee[1]
    stored_password = employee[2]

    if not verify_password(
        login.password,
        stored_password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token_data = {
        "employee_id": employee_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }

    token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "message": "Login successful",
        "access_token": token
    }


# =========================================================
# VERIFY EMPLOYEE
# =========================================================

def get_current_employee(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Kochi Metro Scheduler Backend is running!"
    }


# =========================================================
# TRAIN AVAILABILITY
# =========================================================

@app.get("/train-availability")
def train_availability():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM trains"
    )

    total_trains = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM trains WHERE available = 1"
    )

    available_trains = cursor.fetchone()[0]

    connection.close()

    return {
        "total_trains": total_trains,
        "available_trains": available_trains
    }


# =========================================================
# STATIONS
# =========================================================

@app.get("/stations")
def get_stations():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, station_name FROM stations"
    )

    stations = cursor.fetchall()

    connection.close()

    return {
        "stations": [
            {
                "id": station[0],
                "name": station[1]
            }
            for station in stations
        ]
    }


# =========================================================
# TRAINS
# =========================================================

@app.get("/trains")
def get_trains():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, train_name, capacity, available FROM trains"
    )

    trains = cursor.fetchall()

    connection.close()

    return {
        "trains": [
            {
                "id": train[0],
                "name": train[1],
                "capacity": train[2],
                "available": train[3]
            }
            for train in trains
        ]
    }
# =========================================================
# FIND TRAINS FOR JOURNEY - BOTH DIRECTIONS
# =========================================================

@app.get("/find-trains")
def find_trains(from_station: int, to_station: int):

    connection = get_connection()
    cursor = connection.cursor()

    # Find the FROM station position for every train
    cursor.execute(
        """
        SELECT train_id, station_id, stop_order
        FROM train_routes
        WHERE station_id = ?
        """,
        (from_station,)
    )

    from_routes = cursor.fetchall()

    matching_trains = []

    for train_id, station_id, from_order in from_routes:

        # Find the TO station on the same train
        cursor.execute(
            """
            SELECT stop_order
            FROM train_routes
            WHERE train_id = ?
            AND station_id = ?
            """,
            (train_id, to_station)
        )

        to_route = cursor.fetchone()

        if to_route is not None:

            to_order = to_route[0]

            # Allow BOTH directions
            if from_order != to_order:

                cursor.execute(
                    """
                    SELECT id, train_name, capacity, available
                    FROM trains
                    WHERE id = ?
                    """,
                    (train_id,)
                )

                train = cursor.fetchone()

                if train is not None and train[3] == 1:

                    matching_trains.append({
                        "id": train[0],
                        "name": train[1],
                        "capacity": train[2],
                        "available": train[3]
                    })

    connection.close()

    return {
        "from_station": from_station,
        "to_station": to_station,
        "trains": matching_trains
    }
# =========================================================
# CHANGE TRAIN STATUS
# =========================================================

class TrainStatusRequest(BaseModel):

    available: bool


@app.put("/employee/trains/{train_id}/status")
def change_train_status(
    train_id: int,
    status: TrainStatusRequest,
    employee=Depends(get_current_employee)
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM trains WHERE id = ?",
        (train_id,)
    )

    train = cursor.fetchone()

    if train is None:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Train not found"
        )

    cursor.execute(
        """
        UPDATE trains
        SET available = ?
        WHERE id = ?
        """,
        (
            int(status.available),
            train_id
        )
    )

    connection.commit()
    connection.close()

    return {
        "message": "Train status updated",
        "train_id": train_id,
        "available": status.available,
        "changed_by": employee["username"]
    }# =========================================================
# ML GENERATED SCHEDULE
# =========================================================

import csv
import os

@app.get("/schedule")
def get_schedule():

    schedule_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "schedule_monday.csv"
    )

    if not os.path.exists(schedule_file):
        raise HTTPException(
            status_code=404,
            detail="Schedule file not found"
        )

    schedule = []

    with open(schedule_file, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            schedule.append({
                "time": row["time"],
                "from_station": row["from_station"],
                "to_station": row["to_station"],
                "predicted_demand": int(row["predicted_demand"]),
                "trains_required": int(row["trains_required"])
            })

    return {
        "day": "Monday",
        "schedule": schedule
    }