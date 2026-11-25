
import json
import os
from datetime import datetime, timezone
from urllib.request import urlopen

import logging




# EXTRACT: Daten abrufen
def extract_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=52.52"
        "&longitude=13.41"
        "&current=temperature_2m,relative_humidity_2m"
    )

    with urlopen(url, timeout=10) as response:
        return json.load(response)


# TRANSFORM: Daten vorbereiten
def transform_weather(data):
    current = data["current"]

    return {
        "city": "Berlin",
        "observed_at": datetime.fromisoformat(
            current["time"]
        ).replace(tzinfo=timezone.utc),
        "temperature_c": current["temperature_2m"],
        "humidity_percent": current["relative_humidity_2m"],
    }


# LOAD: Daten in PostgreSQL speichern
def load_weather(weather):
    import psycopg

    with psycopg.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=5432,
        dbname="weather_db",
        user="weather_user",
        password=os.environ["DB_PASSWORD"],
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
                (
                    weather["city"],
                    weather["observed_at"],
                    weather["temperature_c"],
                    weather["humidity_percent"],
                ),
            )


def main():
    data = extract_weather()
    weather = transform_weather(data)
    load_weather(weather)

    print("Wetterdaten erfolgreich gespeichert!")
    print("Stadt:", weather["city"])
    print("Temperatur:", weather["temperature_c"], "°C")
    print("Luftfeuchtigkeit:", weather["humidity_percent"], "%")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Weather pipeline failed")
        raise SystemExit(1)
