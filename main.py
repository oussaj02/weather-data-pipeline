

import json
import os
from datetime import datetime, timezone
from urllib.request import urlopen

import psycopg

# 1. EXTRACT: Wetterdaten abrufen
url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=52.52"
    "&longitude=13.41"
    "&current=temperature_2m,relative_humidity_2m"
)

with urlopen(url, timeout=10) as response:
    data = json.load(response)

# 2. TRANSFORM: Daten vorbereiten
weather = data["current"]
city = "Berlin"

# Open-Meteo liefert hier standardmäßig GMT/UTC
observed_at = datetime.fromisoformat(
    weather["time"]
).replace(tzinfo=timezone.utc)

temperature = weather["temperature_2m"]
humidity = weather["relative_humidity_2m"]

# 3. LOAD: In PostgreSQL speichern
password = os.environ["DB_PASSWORD"]

with psycopg.connect(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=5432,
    dbname="weather_db",
    user="weather_user",
    password=password
) as conn:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO weather_measurements
                (city, observed_at, temperature_c, humidity_percent)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (city, observed_at)
            DO UPDATE SET
                temperature_c = EXCLUDED.temperature_c,
                humidity_percent = EXCLUDED.humidity_percent
            """,
            (city, observed_at, temperature, humidity)
        )

print("Wetterdaten erfolgreich gespeichert!")
print("Stadt:", city)
print("Temperatur:", temperature, "°C")
print("Luftfeuchtigkeit:", humidity, "%")

