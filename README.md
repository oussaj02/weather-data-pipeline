

\# Automated Weather Data Pipeline



A containerized ETL pipeline built with Python, PostgreSQL, and Docker. The application retrieves weather data from the Open-Meteo API, processes it, and stores it in a PostgreSQL database.



\## Tech Stack



\- Python 3.14

\- PostgreSQL 17

\- Docker \& Docker Compose

\- SQL

\- Git \& GitHub

\- Open-Meteo API

\- Psycopg 3



\## Architecture





```mermaid

flowchart TD

&#x20;   A\["Open-Meteo API"] --> B\["Python ETL"]

&#x20;   D\["Docker Scheduler"] --> B

&#x20;   B --> C\[("PostgreSQL")]

```



\## Features



\- Retrieve real weather data from an external API

\- Extract and transform JSON data

\- Store structured data in PostgreSQL

\- Prevent duplicate records using SQL constraints

\- Run the application in Docker containers

\- Execute the pipeline automatically approximately every hour

\- Inspect pipeline logs



\## Project Structure



```text

weather-data-pipeline/

├── main.py

├── Dockerfile

├── compose.yaml

├── init.sql

├── requirements.txt

├── .dockerignore

├── .gitignore

├── .env.example

└── README.md

```



\## Getting Started



\### 1. Clone the repository



```bash

git clone https://github.com/oussaj02/weather-data-pipeline.git

cd weather-data-pipeline

```



\### 2. Configure environment variables



Copy `.env.example` to `.env` and configure your local database password.



\### 3. Start PostgreSQL



```bash

docker compose up -d --wait db

```



\### 4. Create the database table



```bash

docker compose exec -T db psql -U weather\_user -d weather\_db -v ON\_ERROR\_STOP=1 < init.sql

```



\### 5. Run the ETL pipeline manually



```bash

docker compose build app

docker compose run --rm app

```



\### 6. Start automated execution



```bash

docker compose up -d --build scheduler

```



\### 7. Check pipeline logs



```bash

docker compose logs --tail=30 scheduler

```



\## Database Schema



The `weather\_measurements` table contains:



| Column | Description |

|---|---|

| id | Unique record identifier |

| city | City name |

| observed\_at | Weather observation timestamp |

| temperature\_c | Temperature in Celsius |

| humidity\_percent | Relative humidity percentage |



\## Example SQL Query



```sql

SELECT city, observed\_at, temperature\_c

FROM weather\_measurements

ORDER BY observed\_at DESC

LIMIT 10;

```



\## Future Improvements



\- Add automated tests

\- Improve error handling and logging

\- Support multiple cities

\- Add monitoring and alerts

\- Deploy the pipeline to a cloud environment



\## Learning Outcomes



This project demonstrates foundational skills in ETL development, REST API integration, relational databases, containerization, SQL, and workflow automation.



