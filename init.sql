
CREATE TABLE IF NOT EXISTS weather_measurements (
    id BIGSERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    temperature_c DOUBLE PRECISION,
    humidity_percent INTEGER,
    UNIQUE (city, observed_at)
);
