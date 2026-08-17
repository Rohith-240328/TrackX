import sqlite3

DB_NAME = "kochi_metro.db"

# =========================================================
# OPERATIONAL KOCHI METRO STATIONS
# =========================================================

stations = [
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
# CONNECT DATABASE
# =========================================================

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()


# =========================================================
# STATIONS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS stations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_name TEXT NOT NULL
)
""")


# =========================================================
# RESET STATIONS
# =========================================================

cursor.execute("DELETE FROM stations")

for station in stations:

    cursor.execute(
        """
        INSERT INTO stations (station_name)
        VALUES (?)
        """,
        (station,)
    )


# =========================================================
# TRAINS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS trains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    train_name TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    available INTEGER NOT NULL DEFAULT 1
)
""")


# =========================================================
# RESET TRAINS
# =========================================================

cursor.execute("DELETE FROM trains")

for i in range(1, 26):

    cursor.execute(
        """
        INSERT INTO trains
        (train_name, capacity, available)
        VALUES (?, ?, ?)
        """,
        (
            f"Train {i}",
            300,
            1
        )
    )


# =========================================================
# TRAIN ROUTES TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS train_routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    train_id INTEGER NOT NULL,

    station_id INTEGER NOT NULL,

    stop_order INTEGER NOT NULL,

    FOREIGN KEY (train_id)
        REFERENCES trains(id),

    FOREIGN KEY (station_id)
        REFERENCES stations(id)
)
""")


# =========================================================
# CLEAR OLD ROUTES
# =========================================================

cursor.execute("DELETE FROM train_routes")


# =========================================================
# GET STATION IDs
# =========================================================

cursor.execute("""
SELECT id, station_name
FROM stations
ORDER BY id
""")

station_rows = cursor.fetchall()

station_ids = {
    name: station_id
    for station_id, name in station_rows
}


# =========================================================
# FULL ROUTE
# =========================================================

full_route = stations


# =========================================================
# ROUTE DEFINITIONS
# =========================================================

routes = {

    # Full route
    1: full_route,
    2: full_route,
    3: full_route,
    4: full_route,
    5: full_route,

    # Aluva → Palarivattom
    6: stations[0:11],
    7: stations[0:11],
    8: stations[0:11],
    9: stations[0:11],

    # Palarivattom → Tripunithura
    10: stations[10:25],
    11: stations[10:25],
    12: stations[10:25],
    13: stations[10:25],

    # Full route
    14: full_route,
    15: full_route,
    16: full_route,
    17: full_route,

    # Edappally → MG Road
    18: stations[8:15],
    19: stations[8:15],
    20: stations[8:15],
    21: stations[8:15],

    # Full route
    22: full_route,
    23: full_route,
    24: full_route,
    25: full_route
}


# =========================================================
# INSERT TRAIN ROUTES
# =========================================================

for train_number, route in routes.items():

    for order, station_name in enumerate(route, start=1):

        train_id = train_number

        station_id = station_ids[station_name]

        cursor.execute(
            """
            INSERT INTO train_routes
            (
                train_id,
                station_id,
                stop_order
            )
            VALUES (?, ?, ?)
            """,
            (
                train_id,
                station_id,
                order
            )
        )


# =========================================================
# SAVE
# =========================================================

connection.commit()


# =========================================================
# DISPLAY ROUTES
# =========================================================

print("\n===================================")
print("       TRACKX TRAIN ROUTES")
print("===================================")

for train_number in range(1, 26):

    route = routes[train_number]

    print(
        f"\nTrain {train_number}:"
    )

    print(
        " → ".join(route)
    )


# =========================================================
# DATABASE SUMMARY
# =========================================================

cursor.execute(
    "SELECT COUNT(*) FROM stations"
)

station_count = cursor.fetchone()[0]


cursor.execute(
    "SELECT COUNT(*) FROM trains"
)

train_count = cursor.fetchone()[0]


cursor.execute(
    "SELECT COUNT(*) FROM train_routes"
)

route_count = cursor.fetchone()[0]


print("\n===================================")
print("       DATABASE SUMMARY")
print("===================================")

print(
    f"Stations     : {station_count}"
)

print(
    f"Trains       : {train_count}"
)

print(
    f"Route records: {route_count}"
)

print("\nDatabase route setup complete!")


connection.close()