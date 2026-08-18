CREATE DATABASE IF NOT EXISTS protege;

CREATE TABLE IF NOT EXISTS protege.zones
(
    zone_id LowCardinality(String),
    zone_name String,
    activity_code LowCardinality(String),
    productivity_class Enum8(
        'PRODUCTIVE' = 1,
        'NON_PRODUCTIVE_PLANNED' = 2,
        'NON_PRODUCTIVE_INFERRED' = 3,
        'SUPPORT' = 4,
        'UNKNOWN' = 5
    ),
    min_rssi_dbm Int16 DEFAULT -85,
    updated_at DateTime64(3, 'UTC') DEFAULT now64(3)
)
ENGINE = ReplacingMergeTree(updated_at)
ORDER BY zone_id;

CREATE TABLE IF NOT EXISTS protege.gateways
(
    gateway_address String,
    gateway_id String,
    gateway_name String,
    zone_id LowCardinality(String),
    site_id LowCardinality(String),
    latitude Nullable(Float64),
    longitude Nullable(Float64),
    installation_height_m Nullable(Float32),
    active Bool DEFAULT true,
    valid_from DateTime64(3, 'UTC'),
    valid_to Nullable(DateTime64(3, 'UTC')),
    updated_at DateTime64(3, 'UTC') DEFAULT now64(3)
)
ENGINE = ReplacingMergeTree(updated_at)
ORDER BY (gateway_address, valid_from);

CREATE TABLE IF NOT EXISTS protege.workers
(
    tag_address String,
    worker_id String,
    worker_name String,
    contractor String,
    crew String,
    active Bool DEFAULT true,
    valid_from DateTime64(3, 'UTC'),
    valid_to Nullable(DateTime64(3, 'UTC')),
    updated_at DateTime64(3, 'UTC') DEFAULT now64(3)
)
ENGINE = ReplacingMergeTree(updated_at)
ORDER BY (tag_address, valid_from);

CREATE TABLE IF NOT EXISTS protege.ble_scans
(
    event_time DateTime64(3, 'UTC'),
    received_at DateTime64(3, 'UTC') DEFAULT now64(3),
    gateway_address String,
    tag_address String,
    rssi_dbm Int16,
    sequence_no UInt32,
    battery_pct Nullable(UInt8),
    firmware_version LowCardinality(String),
    payload_version UInt8 DEFAULT 1,
    ingestion_id UUID DEFAULT generateUUIDv4()
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(event_time)
ORDER BY (tag_address, event_time, gateway_address)
TTL event_time + INTERVAL 24 MONTH DELETE;

CREATE TABLE IF NOT EXISTS protege.worker_zone_intervals
(
    worker_id String,
    tag_address String,
    shift_date Date,
    interval_start DateTime64(3, 'UTC'),
    interval_end DateTime64(3, 'UTC'),
    zone_id LowCardinality(String),
    activity_code LowCardinality(String),
    productivity_class LowCardinality(String),
    duration_seconds UInt32,
    confidence Float32,
    algorithm_version LowCardinality(String),
    computed_at DateTime64(3, 'UTC') DEFAULT now64(3)
)
ENGINE = ReplacingMergeTree(computed_at)
PARTITION BY toYYYYMM(shift_date)
ORDER BY (shift_date, worker_id, interval_start, zone_id);

