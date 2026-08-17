import csv
import random

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
    "MG Road"
]

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

rows = []

for day in days:

    for hour in range(6, 23):

        for _ in range(5):

            from_station, to_station = random.sample(stations, 2)

            # Base demand
            demand = random.randint(40, 100)

            # Morning peak
            if 7 <= hour <= 10:
                demand += random.randint(60, 120)

            # Evening peak
            if 16 <= hour <= 20:
                demand += random.randint(70, 140)

            # Weekend generally has lower demand
            if day in ["Saturday", "Sunday"]:
                demand -= random.randint(10, 30)

            # Small random variation
            demand += random.randint(-10, 10)

            demand = max(demand, 10)

            rows.append([
                day,
                hour,
                int(day in ["Saturday", "Sunday"]),
                from_station,
                to_station,
                demand
            ])


with open("dataset.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "day_of_week",
        "hour",
        "is_weekend",
        "from_station",
        "to_station",
        "demand"
    ])

    writer.writerows(rows)


print("Dataset created successfully!")
print("Total records:", len(rows))