import sqlite3
import os

# =========================================================
# TRACKX FLEET SETUP
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "kochi_metro.db"
)

print()
print("==============================================")
print(" TRACKX FLEET SETUP")
print("==============================================")
print()

print("Database:")
print(DB_PATH)
print()


# =========================================================
# CONNECT DATABASE
# =========================================================

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()


# =========================================================
# CHECK TRAINS TABLE
# =========================================================

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    AND name='trains'
""")

table = cursor.fetchone()

if table is None:

    print("ERROR: trains table does not exist.")

    connection.close()

    exit()


# =========================================================
# CHECK COLUMNS
# =========================================================

cursor.execute("PRAGMA table_info(trains)")

columns = [
    column[1]
    for column in cursor.fetchall()
]

print("Existing columns:")
print(columns)
print()


# =========================================================
# ADD STATUS COLUMN IF NEEDED
# =========================================================

if "status" not in columns:

    print("Adding status column...")

    cursor.execute("""
        ALTER TABLE trains
        ADD COLUMN status TEXT DEFAULT 'active'
    """)

    connection.commit()

    print("Status column added.")
    print()


# =========================================================
# GET EXISTING TRAINS
# =========================================================

cursor.execute("""
    SELECT id, train_name, capacity, available, status
    FROM trains
    ORDER BY id
""")

existing_trains = cursor.fetchall()

print(
    "Total trains currently in database:",
    len(existing_trains)
)

print()


# =========================================================
# MAKE EXISTING TRAINS ACTIVE
# =========================================================

for train in existing_trains:

    train_id = train[0]

    cursor.execute("""
        UPDATE trains
        SET status = 'active'
        WHERE id = ?
    """, (train_id,))


connection.commit()


# =========================================================
# ADD BACKUP TRAINS
# =========================================================

print("Checking backup fleet...")
print()

backup_count = 0

for number in range(26, 36):

    train_name = f"KMRL-{number:02d}"

    cursor.execute("""
        SELECT id
        FROM trains
        WHERE train_name = ?
    """, (train_name,))

    existing = cursor.fetchone()

    if existing is not None:

        print(
            f"{train_name} already exists."
        )

        continue


    cursor.execute("""
        INSERT INTO trains
        (
            train_name,
            capacity,
            available,
            status
        )
        VALUES (?, ?, ?, ?)
    """, (
        train_name,
        975,
        0,
        "backup"
    ))

    print(
        f"Added backup train: {train_name}"
    )

    backup_count += 1


connection.commit()


# =========================================================
# FINAL FLEET SUMMARY
# =========================================================

cursor.execute("""
    SELECT COUNT(*)
    FROM trains
""")

total_trains = cursor.fetchone()[0]


cursor.execute("""
    SELECT COUNT(*)
    FROM trains
    WHERE status = 'active'
""")

active_trains = cursor.fetchone()[0]


cursor.execute("""
    SELECT COUNT(*)
    FROM trains
    WHERE status = 'backup'
""")

backup_trains = cursor.fetchone()[0]


cursor.execute("""
    SELECT COUNT(*)
    FROM trains
    WHERE status = 'unavailable'
""")

unavailable_trains = cursor.fetchone()[0]


# =========================================================
# CLOSE DATABASE
# =========================================================

connection.close()


# =========================================================
# DISPLAY RESULT
# =========================================================

print()
print("==============================================")
print(" FLEET SETUP COMPLETE")
print("==============================================")

print()
print("Total trains      :", total_trains)
print("Active trains     :", active_trains)
print("Unavailable trains:", unavailable_trains)
print("Backup trains     :", backup_trains)

print()

if total_trains == 35:

    print("SUCCESS!")
    print("TrackX fleet now contains 35 trains.")

else:

    print(
        "WARNING: Expected 35 trains but found",
        total_trains
    )

print()
print("==============================================")